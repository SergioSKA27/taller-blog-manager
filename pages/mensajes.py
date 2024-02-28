import streamlit as st
from st_xatadb_connection  import XataConnection
import time

st.set_page_config(layout='wide')
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

def update_read_messages():
    st.session_state.read_messages = xata.query("Mensaje",{"columns": [
        "emisor",
        "correo",
        "motivo",
        "contenido",
        "leido"
    ],
    'filter':{
        'leido':{"$is": True}
    }})

def mark_as_read(message_id):
    try:
        response = xata.update("Mensaje",message_id,{"leido":True})
        #st.write(response)
        st.toast('Mensaje marcado como leido',icon='📩')
        update_read_messages()
    except Exception as e:
        st.error(f'Error: {e}')

def delete_message(message_id):
    try:
        xata.delete("Mensaje",message_id)
        st.toast('Mensaje eliminado',icon='🗑️')
        time.sleep(1)
        update_read_messages()
    except Exception as e:
        st.error(f'Error: {e}')

def render_message(message):
    st.write(f"De: {message['emisor']}")
    st.write(f"Correo: {message['correo']}")
    st.write(f"Motivo: {message['motivo']}")
    st.write(f"Mensaje: {message['contenido']}")
    if not message['leido']:
        if st.button('Marcar como leido',on_click=mark_as_read,args=(message['id'],),key=message['id']):
            update_messages()
            st.rerun()
    else:
        if st.button(':red[Eliminar]',on_click=delete_message,args=(message['id'],),key=message['id']):
            st.rerun()





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

if 'read_messages' not in st.session_state:
    st.session_state.read_messages = xata.query("Mensaje",{"columns": [
        "emisor",
        "correo",
        "motivo",
        "contenido",
        "leido"
    ],
    'filter':{
        'leido':{"$is": True}
    }
    })



st.title('Mensajes')
if st.button('Actualizar mensajes',on_click=update_messages,use_container_width=True):
    update_read_messages()
    st.rerun()
cols = st.columns(4)
k=0


for i in st.session_state.messages['records']:
    with cols[k]:
        render_message(i)
        k+=1
        if k==4:
            k=0


st.header('Mensajes Leidos')
cols2 = st.columns(4)
t = 0

for i in st.session_state.read_messages['records']:
    with cols2[t]:
        render_message(i)
    t+=1
    if t==4:
        t=0
