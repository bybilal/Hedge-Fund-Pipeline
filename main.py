import streamlit as st
from api_explorer import OpenSeaAPIExplorer

if __name__ == "__main__":
    endpoint = st.sidebar.selectbox("Choose an Endpoint", ["Assets", "Events", "Rarity"])
    api_explorer = OpenSeaAPIExplorer(endpoint)
    api_explorer.run()
