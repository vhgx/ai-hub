import re

def extract_expense_details(text: str):
    """
    Simula um modelo de IA que extrai informações de uma frase de gastos.
    """
    # Regex melhorado para capturar valores com R$, $ e vírgulas
    clean_text = text.replace('R$', '').replace('$', '').strip()
    amount_match = re.search(r'(\d+(?:[.,]\d+)?)', clean_text)
    
    if amount_match:
        val_str = amount_match.group(1).replace(',', '.')
        try:
            amount = float(val_str)
        except ValueError:
            amount = 0.0
    else:
        amount = 0.0

    # Categorias simples baseadas em palavras-chave
    categories = {
        'alimentação': ['café', 'restaurante', 'almoço', 'jantar', 'comida', 'ifood', 'burger', 'starbucks'],
        'transporte': ['uber', '99', 'gasolina', 'combustível', 'ônibus', 'metrô'],
        'lazer': ['cinema', 'show', 'teatro', 'viagem', 'netflix', 'spotify', 'jogo'],
        'contas': ['aluguel', 'luz', 'água', 'internet', 'celular', 'energia'],
    }

    category = "Outros"
    text_lower = text.lower()
    for cat, keywords in categories.items():
        if any(keyword in text_lower for keyword in keywords):
            category = cat.capitalize()
            break

    return {
        "amount": amount,
        "category": category,
        "original_text": text
    }