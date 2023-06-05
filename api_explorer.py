import streamlit as st
import requests
import json
from asset import Asset
from event import Event, EventTable

class OpenSeaAPIExplorer:
    def __init__(self, endpoint):
        self.endpoint = endpoint

    def run_events(self):
        try:
            params = {
                "collection_slug": st.sidebar.text_input("Collection"),
                "asset_contract_address": st.sidebar.text_input("Contract Address"),
                "token_id": st.sidebar.text_input("Token ID"),
                "event_type": st.sidebar.selectbox("Event Type", ["offer_entered", "cancelled", "bid_withdrawn", "transfer", "approve"]),
            }

            events = requests.get("https://api.opensea.io/api/v1/events", params=params).json().get("asset_events", [])

            EventTable(events).create_table()

        except requests.exceptions.RequestException as e:
            st.error(f"Error occurred during API request: {e}")

        except json.JSONDecodeError as e:
            st.error(f"Error occurred while decoding JSON response: {e}")

    def run_assets(self):
        try:
            params = {
                "owner": st.sidebar.text_input("Owner"),
                "collection": st.sidebar.text_input("Collection")
            }

            assets = requests.get("https://api.opensea.io/api/v1/assets", params=params).json().get("assets", [])

            for asset in assets:
                Asset(**asset).render()

            st.subheader("Raw JSON Data")
            st.write(assets)

        except requests.exceptions.RequestException as e:
            st.error(f"Error occurred during API request: {e}")

        except json.JSONDecodeError as e:
            st.error(f"Error occurred while decoding JSON response: {e}")

    def run_rarity(self):
        st.write("Rarity Endpoint")

    def run(self):
        st.sidebar.header("Endpoints")
        st.title(f"OpenSea API Explorer - {self.endpoint}")
        if self.endpoint == "Events":
            self.run_events()
        elif self.endpoint == "Assets":
            self.run_assets()
        elif self.endpoint == "Rarity":
            self.run_rarity()
