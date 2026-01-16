import streamlit as st
import time

class Auth:

    @staticmethod
    def check_login():
        if "authenticated" not in st.session_state:
            st.session_state.authenticated = False
        return st.session_state.authenticated

    @staticmethod
    def login(username, password):
        time.sleep(1)
        
        if username and password:
            st.session_state.authenticated = True
            st.session_state.username = username
            return True
        return False

    @staticmethod
    def logout():
        st.session_state.clear()
        st.rerun()
