import streamlit as st
from st_xatadb_connection  import XataConnection,XataClient
import bcrypt
import time


client = XataClient(st.secrets['XATA_API_KEY'],db_url=st.secrets['XATA_DB_URL'])
st.set_page_config(layout='centered')
xata = st.connection('xata',type=XataConnection)


def validate_user(username,password):
    try:
        response = xata.query("Usuario",{"filter":{ "username": {"$is": username}}})
        if response['records'] != []:
            if bcrypt.checkpw(password.encode('utf-8'),response['records'][0]['password'].encode('utf-8')):
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        st.error(f'Error: {e}')
        return False



if 'login' not in st.session_state:
    st.session_state.login = False
else:
    if st.session_state.login:
        st.switch_page(page='pages/administrar_proyectos.py')

st.title('Iniciar Sesión')
with st.form(key='loginform'):
    username = st.text_input('Usuario')
    password = st.text_input('Contraseña',type='password')

    if st.form_submit_button('Iniciar Sesión',use_container_width=True):
        if username != '' and password != '':
            if validate_user(username,password):
                st.success('Iniciando sesión...')
                st.session_state.login = True
                st.balloons()
                time.sleep(2)
                st.switch_page(page='pages/administrar_proyectos.py')
            else:
                st.error('Usuario o contraseña incorrectos')
        else:
            st.error('El usuario y la contraseña no pueden estar vacios')
