import json
from typing import List, Optional
import mimetypes
import requests

import pandas as pd
import streamlit as st
from dataclasses import dataclass
from web3 import Web3



@dataclass
class Asset:
    name: str
    collection: dict
    token_id: str
    description: Optional[str]
    image_url: Optional[str]


class AssetRenderer:
    """
    Renders individual assets with their name, description, and image.

    Methods:
        render(): Renders the asset with its associated information.
    """

    def __init__(self, asset: Asset):
        self.asset = asset

    def render(self) -> None:
        asset_name = self.asset.name if self.asset.name else f"{self.asset.collection['name']} #{self.asset.token_id}"
        st.subheader(asset_name)
        st.write(self.asset.description if self.asset.description else self.asset.collection['description'])

        if self.asset.image_url:
            content_type = mimetypes.guess_type(self.asset.image_url)[0]

            render_functions = {
                'image': lambda url: st.image(url),
                'video': lambda url: st.video(url),
                'svg': lambda url: st.image(requests.get(url).content.decode())
            }

            if content_type:
                for file_type, render_func in render_functions.items():
                    if content_type.startswith(file_type):
                        render_func(self.asset.image_url)
                        break
                else:
                    CustomRenderer(self.asset.image_url, content_type).render()
            else:
                FallbackRenderer(self.asset.image_url).render()


@dataclass
class Event:
    created_date: str
    from_account: dict
    bid_amount: int
    asset: dict


class EventTable:
    """
    Creates a table for events with their relevant information.

    Methods:
        create_table(): Generates the table with event details.
    """

    def __init__(self, events: List[Event]):
        self.events = events

    def create_table(self) -> None:
        event_list = [
            [
                event.created_date,
                (event.from_account['user'] or {}).get('username', event.from_account['address']),
                float(Web3.fromWei(int(event.bid_amount), 'ether')),
                event.asset['collection']['name'],
                event.asset['token_id']
            ]
            for event in self.events
            if event.bid_amount
        ]

        st.write(pd.DataFrame(event_list, columns=["time", "bidder", "bid_amount", "collection", "token_id"]))
        st.write(self.events)


class OpenSeaAPIExplorer:
    """
    Main class for the OpenSea API Explorer.

    Methods:
        run_events(): Handles the 'Events' endpoint and fetches events data.
        run_assets(): Handles the 'Assets' endpoint and fetches asset data.
        run_rarity(): Handles the 'Rarity' endpoint.
        run(): Executes the appropriate endpoint based on user selection.
    """

    def __init__(self, endpoint: str):
        self.endpoint = endpoint

    def run_events(self) -> None:
        try:
            params = {
                "collection_slug": st.sidebar.text_input("Collection"),
                "asset_contract_address": st.sidebar.text_input("Contract Address"),
                "token_id": st.sidebar.text_input("Token ID"),
                "event_type": st.sidebar.selectbox("Event Type", ["offer_entered", "cancelled", "bid_withdrawn", "transfer", "approve"]),
            }

            events = requests.get("https://api.opensea.io/api/v1/events", params=params).json().get("asset_events", [])

            EventTable(events).create_table()

        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            st.error(f"Error occurred: {e}")



    def run_assets(self) -> None:
        try:
            params = {
                "owner": st.sidebar.text_input("Owner"),
                "collection": st.sidebar.text_input("Collection")
            }

            assets = requests.get("https://api.opensea.io/api/v1/assets", params=params).json().get("assets", [])

            for asset in assets:
                AssetRenderer(Asset(**asset)).render()

            st.subheader("Raw JSON Data")
            st.write(assets)

        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            st.error(f"Error occurred: {e}")


    def run_rarity(self) -> None:
        st.write("Rarity Endpoint")


    def run(self) -> None:
        st.sidebar.header("Endpoints")
        st.title(f"OpenSea API Explorer - {self.endpoint}")
        if self.endpoint == "Events":
            self.run_events()
        elif self.endpoint == "Assets":
            self.run_assets()
        elif self.endpoint == "Rarity":
            self.run_rarity()


class CustomRenderer:
    """
    Handles custom rendering for specific content types.

    Methods:
        render(): Renders the content in a custom way.
    """

    def __init__(self, image_url: str, content_type: str):
        self.image_url = image_url
        self.content_type = content_type

    def render(self) -> None:
        st.write(f"Custom render for {self.content_type}: {self.image_url}")


class FallbackRenderer:
    """
    Handles fallback rendering for assets.

    Methods:
        render(): Performs a fallback render for assets.
    """

    def __init__(self, image_url: str):
        self.image_url = image_url

    def render(self) -> None:
        st.write(f"Fallback render: {self.image_url}")


if __name__ == "__main__":
    endpoint = st.sidebar.selectbox("Choose an Endpoint", ["Assets", "Events", "Rarity"])
    api_explorer = OpenSeaAPIExplorer(endpoint)
    api_explorer.run()
