import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .routers import bookings, classes
from .initial_data_loading import initial_data_load_fitness_classes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    logger.info("Starting up Fitness Studio Booking API")
    initial_data_load_fitness_classes()
    yield
    # Shutdown
    logger.info("Shutting down Fitness Studio Booking API")


# Create FastAPI instance
app = FastAPI(
    title="Fitness Studio Booking API",
    description="A comprehensive booking system for fitness studio classes",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(bookings.router)
app.include_router(classes.router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors"""
    logger.error(f"Validation error: {exc.errors()}")
    
    # Get the first error
    error = exc.errors()[0]
    
    # Get field name (skip 'body' prefix)
    field_parts = [str(loc) for loc in error["loc"] if str(loc) != "body"]
    field = ".".join(field_parts) if field_parts else "field"
    
    # Clean up the message
    message = error["msg"]
    message = message.replace("value is not a valid", "Invalid")
    message = message.replace("String should", f"{field.capitalize()} should")
    message = message.replace("value", field)
    
    # Extract specific error after colon if exists
    if ":" in message and "Invalid" in message:
        message = message.split(":", 1)[-1].strip()
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": message}
    )


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Fitness Studio Booking API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}
