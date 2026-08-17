import streamlit as st
import yfinance as yf
import pandas as pd
import sqlite3

# --- 1. CONFIGURAÇÃO DA TELA ---
st.set_page_config(page_title="Meu Portfólio Financeiro", layout="wide")
st.title("📊 Painel de Análise de Ativos")
st.subheader("Primeiro Projeto de Portfólio: Python + SQL")

# --- 2. COLETA DE DADOS (PYTHON) ---
tickers = ["PETR4.SA", "VALE3.SA", "WEGE3.SA", "ITUB4.SA", "^BVSP"]

@st.cache_data
def carregar_e_salvar_dados():
    dados = yf.download(tickers, period="1y")['Close']
    dados = dados.reset_index()
    dados_longos = dados.melt(id_vars=['Date'], value_vars=tickers, 
                              var_name='ticker', value_name='preco_fechamento')
    dados_longos.columns = ['data', 'ticker', 'preco_fechamento']
    
    # --- 3. ARMAZENAMENTO (SQL) ---
    conn = sqlite3.connect("banco_financeiro.db")
    dados_longos.to_sql("historico_precos", conn, if_exists="replace", index=False)
    conn.close()

carregar_e_salvar_dados()

# --- 4. ANÁLISE DE DADOS (SQL) ---
conn = sqlite3.connect("banco_financeiro.db")
ativos_disponiveis = pd.read_sql("SELECT DISTINCT ticker FROM historico_precos", conn)
filtro_ativo = st.sidebar.selectbox("Escolha um ativo para analisar:", ativos_disponiveis['ticker'])

query_analise = f"""
SELECT 
    data,
    ticker,
    preco_fechamento,
    AVG(preco_fechamento) OVER(ORDER BY data ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) as media_movel_20d
FROM historico_precos
WHERE ticker = '{filtro_ativo}'
ORDER BY data
"""
df_filtrado = pd.read_sql(query_analise, conn)
conn.close()

# --- 5. VISUALIZAÇÃO (STREAMLIT) ---
preco_atual = df_filtrado['preco_fechamento'].iloc[-1]
preco_inicial = df_filtrado['preco_fechamento'].iloc[0]
retorno_total = ((preco_atual - preco_inicial) / preco_inicial) * 100

col1, col2 = st.columns(2)
col1.metric(label=f"Preço Atual de {filtro_ativo}", value=f"R$ {preco_atual:.2f}")
col2.metric(label="Retorno no Período (1 Ano)", value=f"{retorno_total:.2f}%")

st.markdown("### Evolução do Preço vs Média Móvel (20 dias)")
st.line_chart(df_filtrado.set_index('data')[['preco_fechamento', 'media_movel_20d']])

if st.checkbox("Mostrar dados brutos retornados pelo SQL"):
    st.dataframe(df_filtrado)