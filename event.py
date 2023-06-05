from typing import Optional, List
from dataclasses import dataclass
from web3 import Web3
import pandas as pd

@dataclass
class Event:
    created_date: str
    from_account: dict
    bid_amount: int
    asset: dict

class EventTable:
    def __init__(self, events: List[Event]):
        self.events = events

    def create_table(self):
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

        pd.DataFrame(event_list, columns=["time", "bidder", "bid_amount", "collection", "token_id"]).write()
        st.write(self.events)
