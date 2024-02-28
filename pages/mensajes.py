import streamlit as st
from st_xatadb_connection  import XataConnection,XataClient
import bcrypt


client = XataClient(st.secrets['XATA_API_KEY'],db_url=st.secrets['XATA_DB_URL'])
st.set_page_config(layout='centered')
xata = st.connection('xata',type=XataConnection)


def update_messages():
    st.session_state.messages = xata.query("Mensaje",{"columns": [
        "emisor",
        "correo",
        "motivo",
        "contenido",
        "leido"
    ],
    'filter':{
        'leido':{"$is": False}
    }})
def mark_as_read(message_id):
    try:
        response = xata.update("Mensaje",message_id,{"leido":True})
        #st.write(response)
        st.toast('Mensaje marcado como leido',icon='📩')
    except Exception as e:
        st.error(f'Error: {e}')


def render_message(message):
    st.write(f"De: {message['emisor']}")
    st.write(f"Correo: {message['correo']}")
    st.write(f"Motivo: {message['motivo']}")
    st.write(f"Mensaje: {message['contenido']}")
    if not message['leido']:
        st.button('Marcar como leido',on_click=mark_as_read,args=(message['id'],))



if 'messages' not in st.session_state:
    st.session_state.messages = xata.query("Mensaje",{"columns": [
        "emisor",
        "correo",
        "motivo",
        "contenido",
        "leido"
    ],
    'filter':{
        'leido':{"$is": False}
    }
    })



