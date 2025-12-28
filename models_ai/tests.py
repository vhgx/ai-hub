import pytest
from models_ai.services import extract_expense_details

@pytest.mark.parametrize("text, expected_amount, expected_category", [
    ("Uber 25", 25.0, "Transporte"),
    ("Almoço de R$ 50,50", 50.5, "Alimentação"),
    ("Gastei 100 no mercado", 100.0, "Mercado"),
    ("Netflix mensal", 0.0, "Lazer"), # Logic might extract 0 if no number
    ("Compra genérica 10", 10.0, "Outros"),
    ("Paguei a luz", 0.0, "Contas"),
    ("Curso de Python 1000", 1000.0, "Educação"),
    ("Farmacia 50.99", 50.99, "Saúde"),
])
def test_extract_expense_details(text, expected_amount, expected_category):
    result = extract_expense_details(text)
    assert result["amount"] == expected_amount
    assert result["category"] == expected_category

def test_extract_expense_no_amount():
    result = extract_expense_details("Só texto sem valor")
    assert result["amount"] == 0.0
    assert result["category"] == "Outros"

def test_extract_expense_complex_currency():
    result = extract_expense_details("R$1.200,50 em Eletrônicos") # "compras" category keywords: eletrônico
    assert result["amount"] == 1200.50
    assert result["category"] == "Compras"
