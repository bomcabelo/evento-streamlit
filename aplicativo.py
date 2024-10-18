# Streamlit
import streamlit as st
from streamlit_option_menu import option_menu              # menu para sidebar do streamlit

# Analise de Dados
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objs as go

### ### ### ### ### ###
# GRUPO DE FUNÇÕES
### ### ### ### ### ###

def gerar_grafico_serie( dados_serie ):
    '''
    Função renderizar o gráfico de série temporal
    Parametro: uma base de dados no formato especifico
    '''

    # Criar figura
    Figura = go.Figure()

    # Adicionar série temporal diária
    Figura.add_trace(
        go.Scatter(
            x=dados_serie.index,
            y=dados_serie['media_preco'],
            mode='lines',
            name='Diário',
            line=dict(color='#157806')
        )
    )

    # Adicionar média móvel de 7 dias
    Figura.add_trace(
        go.Scatter(
            x=dados_serie.index,
            y=dados_serie['mm7d'],
            mode='lines',
            name='mm7d',
            line=dict(color='#1af0ac', width=2)
        )
    )

    # Adicionar média móvel de 30 dias com janela rolante de 20 dias
    Figura.add_trace(
        go.Scatter(
            x=dados_serie.index,
            y=dados_serie['mm30d'].rolling(window=20).mean(),
            mode='lines',
            name='mm30d',
            line=dict(color='#adf03a', width=2)
        )
    )

    # Títulos e labels
    Figura.update_layout(
        title='Série Temporal | Preço megawatt-hora (MWh) €',
        xaxis_title='Data',
        yaxis_title='Preço em EURO €',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5,
        ),
        height=500,
        width=1200
    )

    return Figura

def gerar_grafico_outliers( dados_serie ):
    
    # Filtrar dados para remover outliers
    dados_filtrados = dados_serie.loc[dados_serie['euros_per_mwh'] < 4000]

    # Criar figura
    Figura2 = go.Figure()

    # Adicionar um boxplot para cada mês (assumindo que 'data_boxplot' contém a categoria mensal)
    for categoria in dados_filtrados['data_boxplot'].unique():

        Figura2.add_trace(go.Box(
            y=dados_filtrados[dados_filtrados['data_boxplot'] == categoria]['euros_per_mwh'],
            name=categoria,
            boxmean='sd',  # Para mostrar a média e desvio padrão no boxplot
            width=0.5,
            marker_color='#db4061'
        ))

    # Títulos e labels
    Figura2.update_layout(
        title='Distribuição de Preço megawatt-hora (MWh) € | Mensal',
        xaxis_title='Mês',
        yaxis_title='Preço em EURO €',
        xaxis={'type': 'category'},  # Para garantir que os meses sejam categóricos
        height=500,
        width=1200,
        showlegend=False
    )

    # Rotacionar os rótulos do eixo x
    Figura2.update_xaxes(tickangle=90)

    return Figura2

def gerar_grafico_estudo( dados, ano, mes ):

    # ANO , MES -> Interação do usuário no Front-end

    # Filtrar o ano e mes que o usuário está setando no FRONT-END
    Filtro = dados.loc[ (dados.ano == ano) & (dados.mes == mes) ]
    
    # Analise
    anl_estudo = Filtro.groupby( by=['dia', 'hora'] ).agg(
        media_preco = ('euros_per_mwh', 'mean')
    ).reset_index()

    # Pivotar a tabela
    anl_estudo = anl_estudo.pivot_table( index='hora', columns='dia', values='media_preco')

    # Ordenacao
    anl_estudo = anl_estudo.sort_index()

    # Ajuste no index
    anl_estudo.index = anl_estudo.index.astype(str)

    # Criar heatmap
    Figura3 = go.Figure(
        data=go.Heatmap(
            z=anl_estudo.values,
            x=anl_estudo.columns,
            y=anl_estudo.index,
            colorscale='Reds',
            showscale=True,
            colorbar=dict(thickness=10, len=0.5)
        )
    )

    # Títulos e labels
    Figura3.update_layout(
        title=f'Comportamento entre horário e dia',
        xaxis_title='Dias',
        yaxis_title='Horário',
        height=700,
        width=1200
    )

    return Figura3


### ### ### ### ### ###
# CARREGAR OS ARQUIVOS
### ### ### ### ### ###

dados_bignumbers = pd.read_parquet('./dados_bignumber.parquet')
dados_serietemporal = pd.read_parquet('./dados_serietemporal.parquet')
dados_boxplot = pd.read_parquet('./dados_boxplot.parquet')
dados_estudo = pd.read_parquet('./dados_estudo.parquet')

### ### ### ###
### FRONT-END ###
### ### ### ###

# Titulo - subtitulo
st.set_page_config( 
    page_title='Data Viking',
    page_icon='📊',
    layout='wide'
)

### Sidebar Superior ###
st.sidebar.image('./logo_enefit.png')
st.sidebar.title('Analytics')

# customizar a sidebar
with st.sidebar:

    # menu de seleção
    selected = option_menu(

        # titulo
        'Menu',

        # opções de navegação
        ['Dashboard', 'Tatico', 'Operacional'],

        # Icones para o menu das opções
        icons=['bar-chart-fill', 'bar-chart-fill', 'bar-chart-fill'],

        # icone do menu principal
        menu_icon='cast',

        # Seleção padrão
        default_index=0,

        # Estilos
        styles={
            'menu-title' : {'font-size' : '18px'}, # Diminui o tamanho da fonte do título
            'menu-icon': {'display': 'none'},  # Remove o ícone do título
            'icon': {'font-size': '12px'},  # Estilo dos ícones
            'nav-link': {
                'font-size': '15px',  # Tamanho da fonte dos itens do menu
                '--hover-color': '#6052d9',  # Cor de fundo ao passar o mouse
            },
            'nav-link-selected': {'background-color': '#157806'},  # Cor de fundo do item selecionado
        }
    )

# Navegação das paginas
if selected == 'Dashboard':
    
    # Titulo da pagina
    st.title('Análise Indicadores de Energia')

    # Big Numbers | Superiores
    st.subheader('Estatísticas dos preços')

    # Futuramento tem que conectar na base de dados
    big_2021 = dados_bignumbers[ dados_bignumbers.ano == 2021 ]['media'].round(1)
    big_2022 = dados_bignumbers[ dados_bignumbers.ano == 2022 ]['media'].round(1)
    big_2023 = dados_bignumbers[ dados_bignumbers.ano == 2023 ]['media'].round(1)
    big_media = dados_bignumbers[ dados_bignumbers.ano == 2024 ]['media'].round(1)

    # Frame para incluir os big numerbs
    # 4 colunas
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric('Preço médio 2021 €', big_2021)

    with col2:
        st.metric('Preço médio 2022 €', big_2022)

    with col3:
        st.metric('Preço médio 2023 €', big_2023)

    with col4:
        st.metric('Preço médio Geral €', big_media)

    # Gráfico de Série temporal
    #st.text('Gráfico de Série temporal')

    # Chamando a função para renderizar o gráfico
    chamar_grafico = gerar_grafico_serie( dados_serietemporal )
    st.plotly_chart( chamar_grafico )

    # Gráfico de Boxplot
    #st.text('Gráfico de Boxplot')
    chamar_grafico_2 = gerar_grafico_outliers( dados_boxplot )
    st.plotly_chart( chamar_grafico_2 )

    # Indicador Dinâmico 
    st.subheader('Estudo do preço comparando Dia vs Horário do comsumo')

    # Filtros
    lista_ano = [2023, 2022, 2021]
    lista_meses = [ mes for mes in range(1, 13) ]

    # Tabela
    col1, col2, col3 = st.columns(3)

    with col1:
        selecione_ano = st.selectbox('Selecione o ano', lista_ano)
    
    with col2:
        selecione_mes = st.selectbox('Selecione o mes', lista_meses)

    # Gráfico de Calor
    #st.text('Gráfico de Calor')
    chamar_grafico_3 = gerar_grafico_estudo( dados_estudo, selecione_ano, selecione_mes )
    st.plotly_chart( chamar_grafico_3 )

    # rodapé 
    st.markdown(
        '''
            <hr style='border: 1px solid #d3d3d3;'/>
            <p style='text-align: center; color: gray;'>
                Dashboard de Custo de Energia | Dados fornecidos por Enefit | Desenvolvido por Odemir Depieri Jr | © 2024
            </p>
        ''',
        unsafe_allow_html=True
    )


elif selected == 'Tatico':
    pass

elif selected == 'Operacional':
    pass

else:
    pass