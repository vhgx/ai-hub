import pytest
from django.contrib.auth.models import User
from predictions.models import Prediction
from django.urls import reverse
from django.db.models import Sum

@pytest.mark.django_db
class TestDashboardView:
    def test_dashboard_aggregation(self, client):
        user = User.objects.create_user(username='testuser', password='password')
        client.force_login(user)
        
        # Create dummy data
        Prediction.objects.create(user=user, input_data="A", output_data="{}", amount=50.00, category="Alimentação")
        Prediction.objects.create(user=user, input_data="B", output_data="{}", amount=30.00, category="Alimentação")
        Prediction.objects.create(user=user, input_data="C", output_data="{}", amount=100.00, category="Transporte")
        
        response = client.get(reverse('dashboard'))
        assert response.status_code == 200
        
        # Verify Context Data
        expenses = response.context['expenses']
        # Should have 2 categories
        assert len(expenses) == 2
        
        # Check Alimentação Total (80.00)
        food_stats = next(item for item in expenses if item['category'] == "Alimentação")
        assert food_stats['total'] == 80.00
        
        # Check Transporte Total (100.00)
        transport_stats = next(item for item in expenses if item['category'] == "Transporte")
        assert transport_stats['total'] == 100.00

    def test_dashboard_no_data(self, client):
        user = User.objects.create_user(username='testuser', password='password')
        client.force_login(user)
        response = client.get(reverse('dashboard'))
        assert response.status_code == 200
        assert len(response.context['expenses']) == 0
