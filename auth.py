import streamlit as st

class AuthManager:
    def __init__(self):
        self.username = st.secrets["auth"]["username"]
        self.password = st.secrets["auth"]["password"]

    def validate(self, user, pwd):
        return user == self.username and pwd == self.password

    def login(self):
        st.session_state.logged_in = True

    def logout(self):
        st.session_state.logged_in = False
