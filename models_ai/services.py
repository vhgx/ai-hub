import re
import unicodedata

def normalize_text(text: str) -> str:
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII').lower()

def extract_expense_details(text: str):
    """
    Simula um modelo de IA que extrai informações de uma frase de gastos.
    """
    # Remove R$ and $ first
    clean_text = text.replace('R$', '').replace('$', '').strip()
    
    # Improved regex to capture numbers like 1.200,50 or 1200.50 or 25,00
    # Matches groups of digits separated by dots or commas
    # We look for the pattern that looks most like a price
    
    # Strategy: Find all things that look like numbers
    # Pattern: digits, optionally separated by . or , followed by digits
    matches = re.findall(r'\b\d+(?:[.,]\d+)*\b', clean_text)
    
    amount = 0.0
    val_str = ""
    
    if matches:
        # Pega o último match numérico, geralmente é o valor se houver outros números (ex: data)
        # Ou pegar o que tem separador decimal? Vamos pegar o maior comprimento para tentar capturar "1.200,50" inteiro
        val_str = max(matches, key=len)
        
        # Heurística de conversão PT-BR vs US
        if ',' in val_str and '.' in val_str:
            # Assumir 1.200,50 -> tira ponto, troca vírgula
            val_str_clean = val_str.replace('.', '').replace(',', '.')
        elif ',' in val_str:
            # 25,50 -> 25.50
            val_str_clean = val_str.replace(',', '.')
        else:
            # 1200 or 1200.50
            val_str_clean = val_str
            
        try:
            amount = float(val_str_clean)
        except ValueError:
            amount = 0.0

    # Categorias
    categories = {
        'alimentação': ['cafe', 'restaurante', 'almoco', 'jantar', 'comida', 'ifood', 'burger', 'starbucks', 'padaria', 'lanche', 'pizza'],
        'transporte': ['uber', '99', 'gasolina', 'combustivel', 'onibus', 'metro', 'estacionamento', 'pedagio', 'ipva', 'oficina'],
        'lazer': ['cinema', 'show', 'teatro', 'viagem', 'netflix', 'spotify', 'jogo', 'festa', 'bar', 'cerveja', 'clube'],
        'contas': ['aluguel', 'luz', 'agua', 'internet', 'celular', 'energia', 'condominio', 'gas', 'iptu', 'seguro'],
        'saúde': ['farmacia', 'medico', 'hospital', 'dentista', 'remedio', 'exame', 'plano de saude'],
        'mercado': ['supermercado', 'mercado', 'extra', 'carrefour', 'pao de acucar', 'atacadao', 'feira'],
        'compras': ['amazon', 'shopping', 'roupa', 'sapato', 'eletronico', 'presente', 'magalu', 'mercadolivre'],
        'educação': ['curso', 'faculdade', 'escola', 'livro', 'mensalidade', 'material escolar'],
    }

    category = "Outros"
    
    # Remove o valor do texto para não dar match errado (ex: "99" centavos match com 99 taxi)
    text_without_amount = text.replace(val_str, "") if val_str else text
    norm_text = normalize_text(text_without_amount)

    for cat, keywords in categories.items():
        # Clean keywords too (removed accents from dictionary above for simplicity)
        # Use word boundaries to avoid matching "gas" in "gastei"
        for keyword in keywords:
            # Allow optional 's' at the end for plural forms
            if re.search(r'\b' + re.escape(keyword) + r's?\b', norm_text):
                category = cat.capitalize()
                break
        if category != "Outros":
            break

    return {
        "amount": amount,
        "category": category,
        "original_text": text
    }