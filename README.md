# AI Hub | Finanças Inteligentes 🚀

O **AI Hub** é uma plataforma web baseada em Django que utiliza Inteligência Artificial para simplificar a gestão financeira pessoal. O sistema permite que usuários descrevam seus gastos em linguagem natural e recebam automaticamente a classificação e extração do valor monetário.

---

## 🌟 Funcionalidades Principais

- **Processamento de Linguagem Natural (NLP)**: Extração automática de valores e categorias a partir de frases comuns (ex: "Gastei 50 reais no almoço").
- **Classificação Automática**: Categorização inteligente baseada em palavras-chave (Alimentação, Transporte, Lazer, Contas).
- **Histórico Persistente**: Armazenamento seguro de todas as predições vinculadas ao perfil de cada usuário.
- **Interface Premium**: Design moderno com suporte a Dark Mode, Glassmorphism e animações fluidas.

---

## 🛠️ Tecnologias Utilizadas

- **Backend**: [Django 4.2](https://www.djangoproject.com/) (Python por trás de tudo).
- **Frontend**: HTML5, CSS3 (Vanilla com Variáveis Modernas), JavaScript (Lucide Icons).
- **IA/Lógica**: Módulo customizado de processamento de texto em `models_ai`.
- **Banco de Dados**: SQLite (padrão de desenvolvimento).

---

## 📂 Estrutura do Projeto

```text
ai_hub/
├── core/             # Configurações centrais do Django e URLs globais.
├── predictions/      # App principal: Gerencia a lógica de negócio e banco de dados de gastos.
├── models_ai/        # App de inteligência: Contém os serviços de processamento de dados.
├── users/            # App de autenticação: Gestão de login e perfis.
├── static/           # Arquivos de estilo (CSS) e assets visuais.
└── templates/        # Arquivos HTML estruturados.
```

---

## 🚀 Como Executar o Projeto

1.  **Clone o repositório**:
    ```bash
    git clone [url-do-repositorio]
    cd ai_hub
    ```

2.  **Crie e ative um ambiente virtual**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # No macOS/Linux
    ```

3.  **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute as migrações**:
    ```bash
    python manage.py migrate
    ```

5.  **Inicie o servidor**:
    ```bash
    python manage.py runserver
    ```

Acesse em: `http://127.0.0.1:8000/`

---

## 🧠 Lógica da "IA"

Atualmente, o sistema utiliza um modelo baseado em heurísticas e expressões regulares para garantir alta velocidade e precisão em gastos comuns. 

**Exemplo de Processamento:**
- **Input**: "Uber para casa R$ 25,50"
- **Processamento**:
    - `Valor`: Detecta `25.50`.
    - `Categoria`: Mapeia "Uber" para `Transporte`.
- **Output (JSON)**: `{"amount": 25.5, "category": "Transporte"}`

---

## 🔮 Próximos Passos

- [ ] Integração com APIs reais de Open Banking.
- [ ] Dashboards com gráficos de pizza por categoria.
- [ ] Upload de fotos de recibos com OCR (Visão Computacional).
- [ ] Exportação de relatórios para CSV/Excel.

---
