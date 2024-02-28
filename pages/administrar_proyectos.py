import streamlit as st
from st_xatadb_connection  import XataConnection,XataClient
from st_tiny_editor import tiny_editor
import asyncio
import requests
import time


client = XataClient(st.secrets['XATA_API_KEY'],db_url=st.secrets['XATA_DB_URL'])
st.set_page_config(layout='wide')
xata = st.connection('xata',type=XataConnection)

if 'login' not in st.session_state or not st.session_state.login:
    st.switch_page(page='Login.py')

#--------------------------------------------------------------------------
#Funciones
async def get_random_image(query='random'):
    try:
        result = await asyncio.to_thread(requests.get, f'https://source.unsplash.com/random/600x400?{query}',timeout=1)
        return result.content
    except Exception as e:
        print(e)
        return f"https://source.unsplash.com/random/600x400?{query}"

def get_projects():
    try:
        response = xata.query("Proyecto")
        return response
    except Exception as e:
        st.error(f'Error: {e}')
        return None

def update_projects():
    st.session_state.projects = get_projects()['records']

def delete_project(project_id):
    try:
        response = xata.delete("Proyecto",project_id)
        st.write(response)
        st.toast('Proyecto eliminado correctamente',icon='🎉')
        time.sleep(1)
        update_projects()
    except Exception as e:
        st.error(f'Error: {e}')

def render_project(project):
    with st.container(border=True):
        st.write(f'## {project["titulo"]}')
        st.write(f'### URL: {project["url"]}')
        st.checkbox('Embed',value=project['embed'],disabled=True)

        c1 , c2 = st.columns(2)
        if c1.button('Editar',key=f'edit_{project["id"]}',on_click=set_editor,args=(project,),use_container_width=True):
            st.rerun()

        if c2.button(':red[Eliminar]',key=f'delete_{project["id"]}',on_click=delete_project,args=(project["id"],),use_container_width=True):
            st.toast('Proyecto eliminado correctamente',icon='🎉')
            st.rerun()


def set_editor(project):
    st.session_state.project = project


def render_editor():
    cc,cb = st.columns([0.9,0.1])
    cc.header('Editar Proyecto')
    if cb.button('Cerrar',key='close_editor',use_container_width=True):
        st.session_state.project = None
        st.rerun()
    titulo = st.text_input('Titulo',value=st.session_state.project['titulo'])
    url = st.text_input('URL',value=st.session_state.project['url'])
    embed = st.toggle('Embed',value=st.session_state.project['embed'])
    with st.form(key='editor_formpr'):
        contenido = tiny_editor(st.secrets['TINY_API_KEY'],
                            initialValue=st.session_state.project['descripcion'],
                            height=600,
                            key='welcomeeditor',
                            toolbar = 'undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | link image media table | align lineheight | numlist bullist indent outdent | emoticons charmap | removeformat',
                            plugins = [
                              "advlist", "anchor", "autolink", "charmap", "code",
                              "help", "image", "insertdatetime", "link", "lists", "media",
                              "preview", "searchreplace", "table", "visualblocks", "accordion",'emoticons',
                              ]
                            )
        if st.form_submit_button('Vista previa',use_container_width=True):
            st.write(contenido,unsafe_allow_html=True)
            with st.expander('Ver HTML'):
                st.text(contenido)

    payload = {}

    if titulo != st.session_state.project['titulo']:
        payload['titulo'] = titulo
    if url != st.session_state.project['url']:
        payload['url'] = url

    if embed != st.session_state.project['embed']:
        payload['embed'] = embed

    if contenido is not None and contenido != st.session_state.project['descripcion']:
        payload['descripcion'] = contenido

    if len(payload) > 0:
        if st.button('Guardar cambios',use_container_width=True):
            try:
                response = xata.update("Proyecto",st.session_state.project['id'],payload)
                st.write(response)
                st.success('Proyecto actualizado correctamente',icon='🎉')
                time.sleep(1)
                update_projects()
                st.session_state.project = None
                st.rerun()
            except Exception as e:
                st.error(f'Error: {e}')

if 'projects' not in st.session_state:
    st.session_state.projects = get_projects()['records']

if 'project' not in st.session_state:
    st.session_state.project = None

st.title('Administrar Proyectos',help='Administra tus proyectos')

st.divider()


cols = st.columns(3)
k = 0
if st.session_state.project is not None:
    render_editor()
else:
    for project in st.session_state.projects:
        with cols[k]:
            render_project(project)
        k += 1
        if k == 3:
            k = 0
