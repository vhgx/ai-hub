import pytest
from playwright.sync_api import Page, expect

@pytest.mark.django_db
def test_full_prediction_flow(page: Page, live_server, create_user):
    # 1. Setup User
    user = create_user(username='testuser', password='password123')
    
    # 2. Go to Home
    page.goto(live_server.url)
    expect(page).to_have_title("Bem-vindo ao AI Hub | Seu Assistente Financeiro IA")
    
    # 3. Click "Começar Agora"
    page.click("text=Começar Agora")
    
    # 4. Should be redirected to Login
    # Wait for navigation/load
    page.wait_for_url("**/accounts/login/?next=/predict/")
    
    # 5. Fill Login
    # Assuming form fields are typical Django defaults (id_username, id_password)
    # If not sure, I'll use selectors based on name attribute or guesses.
    # Standard: name="username", name="password"
    page.fill("input[name='username']", "testuser")
    page.fill("input[name='password']", "password123")
    page.click("button[type='submit']")
    
    # 6. Should be on Predict Page
    page.wait_for_url("**/predict/")
    expect(page.locator("h1")).to_contain_text("AI Hub Finanças")
    
    # 7. Create Prediction
    page.fill("input[name='input_value']", "Jantar no restaurante R$ 80,00")
    page.click("button[type='submit']")
    
    # 8. Check Result
    # Wait for result area to appear
    expect(page.locator(".stat-value.amount")).to_contain_text("R$ 80.0")
    # Target specific container to avoid ambiguity with history
    expect(page.locator(".stat-card >> text=Alimentação")).to_be_visible()
    
    # 9. Check History
    # Should see the item in history
    history_card = page.locator(".history-card").first
    expect(history_card).to_contain_text("Jantar no restaurante R$ 80,00")
    expect(history_card.locator("text=Alimentação")).to_be_visible()
