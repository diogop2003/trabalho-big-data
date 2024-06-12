import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt

# Para instalar as bibliotecas necessárias, execute os seguintes comandos:
# pip install streamlit pandas plotly openpyxl matplotlib numpy

# Configurar para usar a página toda
st.set_page_config(layout="wide")

# Carregar o arquivo
file_path = "clientes.xlsx"
df = pd.read_excel(file_path, engine='openpyxl')

# Transformar colunas de data para datetime
df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y %H:%M:%S')
df['data_pagamento'] = pd.to_datetime(df['data_pagamento'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
df['data_cancelamento'] = pd.to_datetime(df['data_cancelamento'], format='%d/%m/%Y %H:%M:%S', errors='coerce')

# Adicionar uma coluna fictícia de custo (50% do total para simplicidade)
df['custo'] = df['total'] * 0.5

# Calcular lucro
df['lucro'] = df['total'] - df['custo']

# Faturamento e lucro por mês
df['mes_ano'] = df['data'].dt.to_period('M')
faturamento_lucro_mensal = df.groupby('mes_ano').agg({'total': 'sum', 'lucro': 'sum'}).reset_index()

# Modelos mais vendidos
produtos_mais_vendidos = df.groupby('produto').agg({'quantidade': 'sum'}).reset_index().sort_values(by='quantidade', ascending=False).head(10)

# Tipos de pagamento mais utilizados
tipos_pagamento = df['pagamento'].value_counts().reset_index()
tipos_pagamento.columns = ['pagamento', 'frequencia']

# Definindo a divisão de tela
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# Convert mes_ano to string
faturamento_lucro_mensal['mes_ano'] = faturamento_lucro_mensal['mes_ano'].astype(str)

# Faturamento e lucro mensal
fig_faturamento_lucro_mensal = px.bar(faturamento_lucro_mensal, x='mes_ano', y=['total', 'lucro'], title='Faturamento e Lucro Mensal')
col1.plotly_chart(fig_faturamento_lucro_mensal, use_container_width=True)

# Produtos mais vendidos
fig_produtos_mais_vendidos = px.bar(produtos_mais_vendidos, x='quantidade', y='produto', orientation='h', title='Produtos Mais Vendidos')
col2.plotly_chart(fig_produtos_mais_vendidos, use_container_width=True)

# Tipos de pagamento
fig_tipos_pagamento = px.pie(tipos_pagamento, names='pagamento', values='frequencia', title='Tipos de Pagamento Mais Utilizados')
col3.plotly_chart(fig_tipos_pagamento, use_container_width=True)

# Análise de cancelamentos
cancelamentos = df[df['data_cancelamento'].notna()].shape[0]
col4.metric("Número de Cancelamentos", cancelamentos)

# Agrupando por produto e calculando o lucro total por produto
lucro_por_produto = df.groupby('produto')['lucro'].sum()

# Gráfico de barras mostrando a rentabilidade por produto
st.write("### Rentabilidade por Produto")
fig, ax = plt.subplots(figsize=(12, 12))

# Ordenar os valores e plotar o gráfico de barras horizontais com maior espaçamento
lucro_por_produto.sort_values().plot(kind='barh', ax=ax, edgecolor='black')

# Ajustar os rótulos para que não se sobreponham
ax.set_title('Rentabilidade por Produto')
ax.set_xlabel('Lucro Total')
ax.set_ylabel('Produto')
ax.grid(axis='x')

# Aumentar o espaçamento entre as barras
for patch in ax.patches:
    patch.set_height(0.8)  # Aumentar o espaçamento entre as barras

# Ajustar a margem do eixo y
fig.subplots_adjust(left=0.35, right=0.9, top=0.9, bottom=0.1)

# Melhorar a legibilidade dos rótulos
ax.yaxis.set_tick_params(labelsize=10, labelrotation=0)

st.pyplot(fig)

# Calculando o número de clientes recorrentes
clientes_recorrentes = df['cliente_id'].value_counts()

# Filtrando clientes recorrentes (clientes com mais de 1 compra)
clientes_recorrentes = clientes_recorrentes[clientes_recorrentes > 1]

# Gráfico de barras mostrando a retenção de clientes (número de compras por cliente)
st.write("### Retenção de Clientes")
fig, ax = plt.subplots(figsize=(12, 6))
clientes_recorrentes.plot(kind='bar', ax=ax)
ax.set_title('Retenção de Clientes')
ax.set_xlabel('Cliente ID')
ax.set_ylabel('Número de Compras')
ax.grid(axis='y')
st.pyplot(fig)
