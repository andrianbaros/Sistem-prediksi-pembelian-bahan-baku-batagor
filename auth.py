import streamlit as st

class AuthManager:
    def __init__(self):
        if "auth" not in st.secrets:
            st.error("Secrets auth belum diset")
            st.stop()

        self.username = st.secrets["auth"]["username"]
        self.password = st.secrets["auth"]["password"]
        self.owner_code = st.secrets["auth"]["owner_code"]

        # password runtime (kalau direset)
        if "runtime_password" not in st.session_state:
            st.session_state.runtime_password = self.password

    def validate(self, user, pwd):
        return (
            user == self.username
            and pwd == st.session_state.runtime_password
        )

    def reset_password(self, code, new_password):
        if code == self.owner_code:
            st.session_state.runtime_password = new_password
            return True
        return False

    def login(self):
        st.session_state.logged_in = True

    def logout(self):
        st.session_state.logged_in = False
