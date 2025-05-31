
# Mangue Metrics Dashboard v0.5

![Logo do Projeto](images/logo-dark.png)

> **MVP do Dashboard interativo para análise técnica de criptomoedas e ativos financeiros, auxiliando investidores em decisões mais seguras e informadas.**  
> Projeto acadêmico – Cesar School

---

## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Como Rodar o Projeto](#como-rodar-o-projeto)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Futuras Implementações](#futuras-implementações)
- [Contato](#contato)

---

## Sobre o Projeto

O **Mangue Metrics Dashboard** é uma aplicação web desenvolvida em Python, focada na análise técnica de criptomoedas e outros ativos financeiros (como Bitcoin, Solana, Ripple, SPY, EWZ). O objetivo é facilitar a visualização de métricas técnicas e tendências, promovendo decisões de investimento mais seguras para usuários de diferentes níveis de experiência.

---

## Funcionalidades

- Consulta e comparação de ativos financeiros
- Visualização de preços, retornos, amplitude diária, médias móveis, RSI e outros indicadores
- Interface intuitiva e responsiva
- Simulação de carteiras e acompanhamento de desempenho
- Dados atualizados automaticamente via [yfinance](https://github.com/ranaroussi/yfinance)
- Chatbot voltado para investimentos

---

## Tecnologias Utilizadas

- **Linguagem:** Python 3.12.9
- **Web Framework:** [Streamlit](https://streamlit.io/)
- **Visualização de Dados:** Plotly, Matplotlib, Seaborn
- **Coleta de Dados:** yfinance, pandas
- **Estilização:** CSS customizado
- **Outros:** NumPy

---

## Como Rodar o Projeto

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/mangue-metrics.git
   cd mangue-metrics
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado):**

   ```bash
   python -m venv .venv
   # Para Linux/Mac:
   source .venv/bin/activate
   # Para Windows:
   .venv\Scripts\activate
   ```

3. **Instale as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o aplicativo:**

   ```bash
   streamlit run app.py
   ```

5. **Acesse no navegador:**  
   Normalmente em [http://localhost:8501](http://localhost:8501)

---

## Estrutura do Projeto

```

mangue-metrics/
│
├── app.py
├── requirements.txt
├── README.md
├── styles.html
|
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── dados.py
│   ├── indicadores.py
│   ├── visualizacao.py
│   ├── ui.py
│   ├── utils.py
│   └── widgets.py
│
├── images/
│   ├── logo-dark.png
│   └── logo-light.png
│
└── pages/
    ├── capa.py
    ├── chatbot.py
    ├── analise-ativo.py
    └── comparativo.py


```

---
## Futuras Implementações

- Expandir a lista de ativos
- Inclusão de novos indicadores técnicos (ex: MACD, Bollinger Bands)
- Implementação de ferramenta de backtest de estratégias
- Integração com novas fontes de dados além do yfinance
- Exportação de análises em PDF
- Área para customização de carteiras pelo usuário
- Autenticação de usuários e histórico de análises

---
## Contato

Desenvolvido por Marcelo Queiroz  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue?logo=linkedin)](https://www.linkedin.com/in/marceloqueirozjr/)  
Email: marcelomulder@gmail.com

---

> *Este projeto foi desenvolvido como parte do curso de graduação em Gestão de Tecnologia da Informação (GTI) da Cesar School. Sinta-se à vontade para sugerir melhorias!*
