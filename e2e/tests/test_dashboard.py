import pytest
from playwright.sync_api import Page, expect

@pytest.mark.django_db
def test_dashboard_flow(page: Page, live_server, create_user):
    user = create_user(username='testuser', password='password')
    
    # 1. Login
    page.goto(live_server.url + "/accounts/login/")
    page.fill("input[name='username']", "testuser")
    page.fill("input[name='password']", "password")
    page.click("button[type='submit']")
    
    # 2. Add some data via Predict (to ensure chart has data)
    page.goto(live_server.url + "/predict/")
    page.fill("input[name='input_value']", "Almoço R$ 50")
    page.click("button[type='submit']")
    page.wait_for_selector("text=IA Identificou")
    
    # 3. Go to Dashboard
    page.goto(live_server.url + "/dashboard/")
    expect(page).to_have_title("Dashboard Financeiro | AI Hub")
    
    # 4. Verify Elements
    expect(page.locator("h1")).to_contain_text("Dashboard")
    
    # Verify Chart Canvas exists
    expect(page.locator("#expensesChart")).to_be_visible()
    
    # Verify List contains category
    expect(page.locator(".history-card")).to_contain_text("Alimentação")
    expect(page.locator(".history-card")).to_contain_text("R$ 50,00")
