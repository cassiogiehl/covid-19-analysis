import streamlit as st
import pandas as pd
import requests
import json
import matplotlib.pyplot as plt
import plotly.express as px

st.title('Coronavírus no Brasil')

DATA_URL = 'https://brasil.io/dataset/covid19/caso?format=csv'
NULL = '---'


data = pd.read_csv(DATA_URL)
data = data.loc[data.place_type == 'city']


st.subheader('Dados Utilizados na análise')
st.write(data)

def mostra_grafico(df, x_label, y_label, titulo):
	fig = px.line(df, x=x_label, y=y_label, title=titulo)
	fig


# de para sigla -> estado
de_para_sigla_estado = {
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

# de para estado sigla
de_para_estado_sigla = {
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

# buscando e convertendo sigla para estado
estados = []
estados.append(NULL)
for estado in data['state'].sort_values().unique():
	estados.append(de_para_sigla_estado[estado])

# select de estado
estado_selecionado = st.selectbox(
    'Escolha o estado',
	estados
)

# mostra o estado selecionado
if estado_selecionado is not NULL:
	'Estado selecionado: ', estado_selecionado

	# utilizando somente dados do estado selecionado
	data = data.loc[data.state == de_para_estado_sigla[estado_selecionado]]


	st.subheader('Análise do estado selecionado')

    # dataframe de estado agregados pela data
	df_estado = data.sort_values(by='date', ascending=True)

    # dataframe de casos confirmados no estado selecionado
	df_estado_confirmados = df_estado.groupby('date')[['confirmed']].sum().reset_index()
	df_estado_confirmados.columns = ['data', f'qtd casos confirmados {estado_selecionado}']

    # dataframe de casos de óbitos na cidade filtrada
	df_estado_obitos = df_estado.groupby('date')['deaths'].sum().reset_index()
	df_estado_obitos.columns = ['data', f'qtd de óbitos {estado_selecionado}']

	mostra_grafico(df_estado_confirmados, 'data', f'qtd casos confirmados {estado_selecionado}', f'Casos confirmados em {estado_selecionado}')
	
	mostra_grafico(df_estado_obitos, 'data', f'qtd de óbitos {estado_selecionado}', f'Casos de óbitos em {estado_selecionado}')

   
    # Select de CIDADES do ESTADO selecionado
	cidades_estado_selecionado = data['city'].sort_values().unique()
	cidades = []

	cidades.append(NULL)
	for cidade in cidades_estado_selecionado:
		cidades.append(cidade)

	cidade_selecionada = st.selectbox(
		'Escolha a cidade',
		cidades
	)

	if cidade_selecionada is not NULL:
		'Cidade selecionada: ', cidade_selecionada

		st.subheader('Análise da cidade selecionada')
	
		# Filtrando a cidade selecionada no dataframe do estado
		df_cidade = data.loc[data['city'] == cidade_selecionada]
		df_cidade.sort_values(by='date', ascending=True)

		# dataframe de casos confirmados na cidade filtrada
		df_cidade_confirmados = df_cidade.groupby('date')['confirmed'].sum().reset_index()
		df_cidade_confirmados.columns = ['data', f'qtd casos confirmados {cidade_selecionada}']

		# dataframe de casos de óbitos na cidade filtrada
		df_cidade_obitos = df_cidade.groupby('date')['deaths'].sum().reset_index()
		df_cidade_obitos.columns = ['data', f'qtd de óbitos {cidade_selecionada}']


		# plot dos gráficos de quantidade de confirmados e óbitos por dia 
		# na cidade filtrada
		if cidade_selecionada is not NULL:
			
			mostra_grafico(df_cidade_confirmados, 'data', f'qtd casos confirmados {cidade_selecionada}', f'Casos confirmados em {cidade_selecionada}')

			mostra_grafico(df_cidade_obitos, 'data', f'qtd de óbitos {cidade_selecionada}', f'Casos de óbitos em {cidade_selecionada}')
			
