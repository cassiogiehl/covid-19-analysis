import streamlit as st
import pandas as pd
import requests
import json
import matplotlib.pyplot as plt
import plotly.express as px

st.title('Coronavírus no RS')

DATA_URL = 'https://brasil.io/dataset/covid19/caso?format=csv'
NULL = '---'


# @st.cache
def load_data():
    data = pd.read_csv(DATA_URL)
    data = data.loc[data.place_type == 'city']
    return data

# Cria um elemento na tela
data_load_state = st.text('Carregando dados...')

# Carrega 10k linhas no df
data = load_data()

# Muda o texto criado anteriormente
data_load_state.text('Carregando dados... Pronto!')


st.subheader('Dados Utilizados na análise')
st.write(data)


# Select de ESTADOS

de_para_silga_estado = {
	'AC': 'Acre',
	'AL': 'Alagoas',
	'AP': 'Amapá',
	'AM': 'Amazonas',
	'BA': 'Bahia',
	'CE': 'Ceará',
	'DF': 'Distrito Federal',
	'ES': 'Espírito Santo ',
	'GO': 'Goiás',
	'MA': 'Maranhão',
	'MT': 'Mato Grosso',
	'MS': 'Mato Grosso do Sul',
	'MG': 'Minas Gerais',
	'PA': 'Pará',
	'PB': 'Paraíba',
	'PR': 'Paraná',
	'PE': 'Pernambuco',
	'PI': 'Piauí',
	'RJ': 'Rio de Janeiro',
	'RN': 'Rio Grande do Norte',
	'RS': 'Rio Grande do Sul',
	'RO': 'Rondônia',
	'RR': 'Roraima',
	'SC': 'Santa Catarina',
	'SP': 'São Paulo',
	'SE': 'Sergipe',
	'TO': 'Tocantins'
	}


de_para_estado_silga = {
	'Acre': 'AC',
	'Alagoas': 'AL',
	'Amapá': 'AP',
	'Amazonas': 'AM',
	'Bahia': 'BA',
	'Ceará': 'CE',
	'Distrito Federal': 'DF',
	'Espírito Santo ': 'ES',
	'Goiás': 'GO',
	'Maranhão': 'MA',
	'Mato Grosso': 'MT',
	'Mato Grosso do Sul': 'MS',
	'Minas Gerais': 'MG',
	'Pará': 'PA',
	'Paraíba': 'PB',
	'Paraná': 'PR',
	'Pernambuco': 'PE',
	'Piauí': 'PI',
	'Rio de Janeiro': 'RJ',
	'Rio Grande do Norte': 'RN',
	'Rio Grande do Sul': 'RS',
	'Rondônia': 'RO',
	'Roraima': 'RR',
	'Santa Catarina': 'SC',
	'São Paulo': 'SP',
	'Sergipe': 'SE',
	'Tocantins': 'TO'
	}

estados = []
estados.append(NULL)
for estado in data['state'].sort_values().unique():
	estados.append(de_para_silga_estado[estado])

estado_selecionado = st.selectbox(
    'Escolha o estado',
	estados
)

'Estado selecionado: ', estado_selecionado





# Select de CIDADES do ESTADO selecionado
if estado_selecionado is not NULL:
	cidades_estado_selecionado = data['city'].loc[data.state == de_para_estado_silga[estado_selecionado]].sort_values().unique()
	cidades = []

	cidades.append(NULL)
	for cidade in cidades_estado_selecionado:
		cidades.append(cidade)

	cidade_selecionada = st.selectbox(
		'Escolha a cidade',
		cidades
	)

	'Cidade selecionada: ', cidade_selecionada


	# Filtrando a cidade selecionada na base de dados
	df_cidade = data.loc[data['city'] == cidade_selecionada]
	df_cidade.sort_values(by='date', ascending=True)

	# dataframe de casos confirmados na cidade filtrada
	df_cidade_confirmados = df_cidade[['date', 'confirmed']]
	df_cidade_confirmados.columns = ['Data', cidade_selecionada]

	# dataframe de casos de óbitos na cidade filtrada
	df_cidade_obitos = df_cidade[['date', 'deaths']]

	
#def line_plot(self, col_y,col_x,hue=None, group=None):
#        return px.line(self.df, x=col_x, y=col_y,color=hue, line_group=group)


	# plot dos gráficos de quantidade de confirmados e óbitos por dia 
	# na cidade filtrada
	if cidade_selecionada is not NULL:
	    #st.line_chart(df_cidade_confirmados[cidade_selecionada])
            
            fig = px.line(df_cidade_confirmados, x='Data', y=cidade_selecionada)
            fig
