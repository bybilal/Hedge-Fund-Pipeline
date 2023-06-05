import streamlit as st

class CustomRenderer:
    def __init__(self, image_url, content_type):
        self.image_url = image_url
        self.content_type = content_type

    def render(self):
        st.write(f"Custom render for {self.content_type}: {self.image_url}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

class FallbackRenderer:
    def __init__(self, image_url):
        self.image_url = image_url

    def render(self):
        st.write(f"Fallback render: {self.image_url}")
