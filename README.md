# 📊 Dashboard de Análise Financeira Interativo

Este projeto demonstra a construção de um pipeline de dados ponta a ponta: desde a captura automática de cotações do mercado financeiro, passando pelo armazenamento estruturado em banco de dados relacional (SQL), até a análise avançada e visualização em um painel interativo.

O objetivo principal é calcular e monitorar a evolução dos preços de grandes ativos brasileiros vs. sua Média Móvel de 20 dias para suporte a decisões de investimentos.

---

## 🚀 O Projeto em Ação
![Visualização do Dashboard](dashboard.png)

---

## 🛠️ Tecnologias e Habilidades Demonstradas

*   *Python*: Automação na extração de dados brutos da API de finanças (yfinance) e manipulação estruturada com Pandas.
*   *SQL (SQLite): Criação de banco de dados relacional local, persistência de dados históricos e consultas analíticas utilizando **Window Functions* (AVG() OVER) para cálculo de médias móveis de mercado.
*   *Streamlit*: Construção rápida de interface de usuário (UI/UX) focada em dados, com filtros dinâmicos e componentes visuais nativos.

---

## 📈 Arquitetura de Dados Simplificada
1. *Extração*: Python busca dados reais de 1 ano de histórico de ativos (PETR4, VALE3, WEGE3, ITUB4, ^BVSP).
2. *Carga*: Os dados são limpos, transformados do formato largo para o longo e salvos em uma tabela SQL (historico_precos).
3. *Análise*: Queries SQL realizam cálculos estatísticos diretamente no banco de dados.
4. *Consumo*: O Streamlit plota os resultados de forma gráfica e interativa para o usuário final.

---

## 💻 Como Executar este Projeto Localmente

1. Instale as dependências executando o comando no terminal:
   bash
   python -m pip install -r requirements.txt
   
2. Inicialize o servidor do dashboard com o comando:
   bash
   python -m streamlit run app.py