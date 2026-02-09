import bcrypt
import streamlit as st
from supabase import create_client

class AuthManager:
    def __init__(self):
        self.supabase = create_client(
            st.secrets["SUPABASE_URL"],
            st.secrets["SUPABASE_KEY"]
        )

    def login(self, username, password):
        res = (
            self.supabase
            .table("users")
            .select("password_hash")
            .eq("username", username)
            .execute()
        )

        if not res.data:
            return False

        hashed = res.data[0]["password_hash"].encode()
        return bcrypt.checkpw(password.encode(), hashed)

    def reset_password(self, username, new_password):
        new_hash = bcrypt.hashpw(
            new_password.encode(),
            bcrypt.gensalt()
        ).decode()

        res = (
            self.supabase
            .table("users")
            .update({"password_hash": new_hash})
            .eq("username", username)
            .execute()
        )

        return bool(res.data)
