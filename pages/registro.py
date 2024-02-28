import streamlit as st
from st_xatadb_connection  import XataConnection,XataClient
import bcrypt


client = XataClient(st.secrets['XATA_API_KEY'],db_url=st.secrets['XATA_DB_URL'])
st.set_page_config(layout='centered')
xata = st.connection('xata',type=XataConnection)


def register_user(username,password):
    try:
        response = xata.insert("Usuario",{"username":username,"password":bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')})
        st.write(response)
        st.toast('Usuario registrado correctamente',icon='🎉')
        st.balloons()
    except Exception as e:
        st.error(f'Error: {e}')

st.title('Registro')

with st.form(key='registro'):
    username = st.text_input('Usuario')
    pass1 = st.text_input('Contraseña',type='password')
    pass2 = st.text_input('Repetir Contraseña',type='password')

    if st.form_submit_button('Registrar',use_container_width=True):
        if pass1 == pass2:
            if username != '' and pass1 != '':
                register_user(username,pass1)
            else:
                st.error('El usuario y la contraseña no pueden estar vacios')
        else:
            st.error('Las contraseñas no coinciden')
