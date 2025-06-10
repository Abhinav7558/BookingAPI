from fastapi import status


def test_get_classes_success(client):
    response = client.get("/classes?time_zone=Asia/Kolkata")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

def test_get_classes_default_timezone(client):
    response = client.get("/classes")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)

def test_get_classes_invalid_timezone(client):
    response = client.get("/classes?time_zone=Invalid/Timezone")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid timezone" in response.json()["detail"]
