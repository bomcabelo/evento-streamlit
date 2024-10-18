import streamlit as st

# Definir um titulo
st.title('Evento | Dashboard com Python')

# Cabeçalho
st.header('Conhecendo os elementos do Streamlit')

# Subtitulo
st.subheader('Aula 2 [2/5]')

# Texto simples
st.text('Nesta aula vamos entender os elementos do Streamlit')

# Texto formatado
st.markdown('# Stremlit')

# Texto
st.write('Streamlit é um framework de alto nível do Python!')

# Botão com validação | Combinando o Streamlit
if st.button('Clique aqui'):
    for Loop in range(5):
        st.write(f'Botão selecionado!{Loop}')

# Radio - selecionar
Escolha = st.radio( 'Qual linguagem de programação você mais utiliza', ('Python', 'R', 'Java', 'Outro') )

# Seleção de caixa
Lista_Frameworks = ['Matplotlib', 'Seaborn', 'Plotly']
Opcao = st.selectbox('Escolha seu framework favorito de Data Visualization:', Lista_Frameworks)

# Seleção de multiplas caixa
Lista_Estudo = ['Pandas', 'Numpy', 'Matplotlib', 'Seaborn', 'Plotly', 'Scipy', 'TensorFlow']
Selecoes = st.multiselect('Escolha múltiplas opções:', Lista_Estudo)

# Selecao
Valor = st.slider('Quantos anos trabalha com Data Science:', 0, 30, 1)
# começa no zero
# vai até o 30
# Pula de 1 em 1 

# Uploads
Arquivo = st.file_uploader('Escolha um arquivo', type=['csv', 'txt'])

# Imagem
st.image('logo_python.png', caption='Descrivo da imagem', use_column_width=False)

import pandas as pd
import numpy as np

# Criando um DataFrame base
df = pd.DataFrame(
    { 
        'Dias': [loop for loop in range(31)]
    }
)

# Adicionando novas colunas com dados fictícios
df['Valor de Venda'] = np.random.randint(100, 1000, size=31)
df['Custo'] = df['Valor de Venda'] * 0.8  
df['Lucro'] = df['Valor de Venda'] - df['Custo']
df['Quantidade Vendida'] = np.random.randint(10, 50, size=31)
df['Cliente'] = ['Cliente ' + str(i) for i in range(1, 32)]

# Incluir essa tabela
st.dataframe( df )

import altair as alt

# Criando um gráfico de linha com Altair
chart = alt.Chart(df).mark_line().encode(
    x='Dias',
    y='Valor de Venda'
)

# Exibindo o gráfico no Streamlit
st.altair_chart(chart)





