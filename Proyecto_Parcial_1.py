import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px



st.title('Resultados de futbol entre 1872 y 2017')
data_load_state = st.text('JAIME IVAN AVILA MUNOZ - ZS20006783')


DATA_URL=('results.csv')

st.sidebar.image("logo.png")

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    return data
def load_data_city(city):
    data = pd.read_csv(DATA_URL)
    filtered_data_city = data[data['city'].str.upper().str.contains(city)]
    city.isupper()
    return filtered_data_city
def load_data_tournament(tournament):
    data = pd.read_csv(DATA_URL)
    filtered_data_tournament = data[data['tournament'].str.contains(tournament)]
    city.isupper()
    return filtered_data_tournament

data_load_state = st.text('Loading results data...')
data = load_data(10000)
data_load_state.text("Done! (using st.cache)")

sidebar = st.sidebar
agree = sidebar.checkbox("Mostrar todos los datos de los partidos")


if agree:
  st.dataframe(data)

city = sidebar.text_input('Cuidad :')
btnRange = sidebar.button('Buscar cuidad')

if (city):
    if (btnRange):
        st.markdown("Numero de partidos que se jugo en la cuidad")
        filtercity = load_data_city(city.upper())
        count_row = filtercity.shape[0]
        city = city.lower()
        st.write(f"Buscar Cuidad : {count_row}")
        st.dataframe(filtercity)


selected_tournament= sidebar.selectbox("Seleccionar Tipo de Torneo: ", data ['tournament'].unique())
btnFilterbytournament = sidebar.button('Filtrar Tipo de Torneo')

if (btnFilterbytournament):
    filterbytournament = load_data_tournament(selected_tournament)
    count_row = filterbytournament.shape[0]
    st.write(f"Total  : {count_row}")
    st.dataframe(filterbytournament)



goles_local = data['home_score']
if st.sidebar.checkbox('Goles locales'):
    st.markdown("Grafica que muestra la frecuencia del total de goles de local en  cada partido siendo 0 el numero mas bajo y siendo la frecuencia el numero de partidos")
    fig, ax = plt.subplots()
    ax.hist(goles_local, bins=35, range=(0, 35))
    ax.set_xlabel('Goles de local')
    ax.set_ylabel('Frecuencia')
    ax.set_title('Histograma del número de goles de local')
    st.pyplot(fig)

goles_visitante = data['away_score']
if st.sidebar.checkbox('Goles Visitante'):
    st.markdown("Grafica que muestra la frecuencia del total de goles de visitante en cada partido siendo 0 el numero mas bajo y siendo la frecuencia el numero de partidos")
    fig, ax = plt.subplots()
    ax.hist(goles_local, bins=35, range=(0, 35))
    ax.set_xlabel('Goles de local')
    ax.set_ylabel('Frecuencia')
    ax.set_title('Histograma del número de goles de local')
    st.pyplot(fig)


away = st.sidebar.multiselect("Goles visitante", sorted(data["home_score"].unique()))
home = st.sidebar.multiselect("Goles de local", sorted(data["away_score"].unique()))

if st.sidebar.button("Filtrar goles"):
    st.markdown("Se selecciona el numero de goles de visitante y local y muesta los resultados de  partidos con ese numero de goles")
    mask = (data["home_score"].isin(home)) & (data["away_score"].isin(away))
    partidos_seleccionados = data[mask]
    st.write("Goles Seleccionados:")
    st.write(partidos_seleccionados)


columnas = ['Local', 'Visita']
columna_seleccionada = st.sidebar.multiselect('Selecciona el tipo de goles', columnas)
local_goles = data['home_score'].sum()
visitante_goles = data['away_score'].sum()

if columna_seleccionada:
    st.markdown("Muestra el total de goles de Local y Visitante de todos los partidos")
    df = pd.DataFrame({
    'Goles': ['Local', 'Visitante'],
    'Total': [local_goles, visitante_goles]
    })
    fig = px.bar(df, x='Goles', y='Total')
    st.plotly_chart(fig, use_container_width=True)




torneo = data['tournament']
ciudad = data['city']
home_score = data["home_score"]
away_score = data["away_score"]
home_team = data['home_team']
away_team = data['away_team']
fecha = data["date"]


if st.sidebar.checkbox('Partidos'):
   fig_perf_work=px.scatter(data,
                         x=torneo,
                         y=ciudad,
                         color=home_team,
                         title="Muestra los partidos que se jugaron en diferentes cuidades y el tipo de torneo",
                         template="plotly_white")
   fig_perf_work.update_layout(plot_bgcolor="rgba(0,0,0,0)")
   st.plotly_chart(fig_perf_work)


