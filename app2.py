import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
from google.oauth2 import service_account
from gspread_pandas import Spread, Client
from gspread_dataframe import set_with_dataframe

# Definir escopos para Google Sheets e Google Drive
scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

# Carregar as credenciais de acesso do arquivo JSON
creds = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes= scope)
# Autenticar com o Google Sheets (conectar as credencias)
client = Client(scope=scope, creds=creds)
spreadsheetname = "controlador"
spread = Spread(spreadsheetname, client = client)
#link com a planilha do google sheets
sheet = client.open(spreadsheetname).sheet1

val = sheet.get_all_values()
# fr é a variavel da planilha do google sheets
fr = pd.DataFrame(val)
#separa a primeira linha da planilha google sheets
cab = fr.iloc[0]
#fazendo com que a planilha seja lida a partir da primeira linha
fr = fr[1:]
#seta as colunas
fr.columns = cab
st.set_page_config(layout='wide')

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}<style>", unsafe_allow_html=True)

st.header('Consultar Entregas')
with st.form('proc', clear_on_submit=True, border=True):
    st.subheader('Procurar entregas')
    crit = st.selectbox('Selecione um critério:',
                        ['Data', 'Status', 'Documento', 'Observação'])

    
    dat= st.text_input('Escreva o valor correspondente')
    # fr é a varaivel que contem a planilha do google sheets
    if st.form_submit_button('Procurar'):

        if crit == 'Data':
            df = fr[fr['data'] == dat]
        if crit == 'Status':
            df = fr[fr['status'] == dat]
        if crit == 'Documento':
            df = fr[fr['documento'] == dat]
        if crit == 'Observação':
            df = fr[fr['observações'] == dat]
            

        st.dataframe(df, use_container_width=True)

st.subheader('Pesquisar por período')
data_inicial = st.date_input('Data de início', datetime.now().date(), format='DD/MM/YYYY')
data_final = st.date_input('Data de fim', datetime.now().date(), format='DD/MM/YYYY')
if data_inicial > data_final:
    st.error("A data inicial deve ser anterior ou igual à data final!")
else:
    lista_datas = []
    data_atual = data_inicial
    while data_atual <= data_final:
        a = str(data_atual)
        dataformat = f'{a[-2:]}/{a[5:7]}/{a[:4]}'
        lista_datas.append(dataformat)
        data_atual += timedelta(days=1)

df = fr[fr['data'] == lista_datas]
if st.button('Pesquisar'):
    st.dataframe(dff, use_container_width=True)

st.subheader('Lista de Status')
st.dataframe(fr, use_container_width=True, height=800)
