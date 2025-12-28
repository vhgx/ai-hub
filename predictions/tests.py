import pytest
import json
from django.contrib.auth.models import User
from predictions.models import Prediction
from django.urls import reverse

@pytest.mark.django_db
class TestPredictionModel:
    def test_str_method(self):
        user = User.objects.create_user(username='testuser', password='password')
        prediction = Prediction.objects.create(
            user=user,
            input_data="Teste",
            output_data='{"amount": 10}'
        )
        assert str(prediction) == f"Prediction #{prediction.id} - testuser"

@pytest.mark.django_db
class TestPredictView:
    def test_view_unauthenticated_redirects(self, client):
        url = reverse('predict')
        response = client.get(url)
        assert response.status_code == 302
        assert "/accounts/login/" in response.url

    def test_view_get_authenticated(self, client):
        user = User.objects.create_user(username='testuser', password='password')
        client.force_login(user)
        url = reverse('predict')
        response = client.get(url)
        assert response.status_code == 200
        assert "predictions/predict.html" in [t.name for t in response.templates]

    def test_view_post_creates_prediction(self, client):
        user = User.objects.create_user(username='testuser', password='password')
        client.force_login(user)
        
        # Ensure no predictions initially
        assert Prediction.objects.count() == 0
        
        url = reverse('predict')
        data = {"input_value": "Almoço R$ 50,00"}
        response = client.post(url, data)
        
        assert response.status_code == 200
        assert Prediction.objects.count() == 1
        
        prediction = Prediction.objects.first()
        assert prediction.user == user
        assert prediction.input_data == "Almoço R$ 50,00"
        
        # Verify context output
        assert response.context['result']['amount'] == 50.0
        assert response.context['result']['category'] == 'Alimentação'
