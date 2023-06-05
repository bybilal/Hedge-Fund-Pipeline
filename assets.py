from typing import Optional
from dataclasses import dataclass
import mimetypes
import streamlit as st
import requests
from renderer import CustomRenderer, FallbackRenderer

@dataclass
class Asset:
    name: str
    collection: dict
    token_id: str
    description: Optional[str]
    image_url: Optional[str]

    def render(self):
        asset_name = self.name if self.name else f"{self.collection['name']} #{self.token_id}"
        st.subheader(asset_name)
        st.write(self.description if self.description else self.collection['description'])

        if self.image_url:
            content_type = mimetypes.guess_type(self.image_url)[0]

            render_functions = {
                'image': st.image,
                'video': st.video,
                'svg': lambda url: st.image(requests.get(url).content.decode())
            }

            render_func = next((render_functions[file_type] for file_type in render_functions if content_type and content_type.startswith(file_type)), None)
            if render_func:
                render_func(self.image_url)
            else:
                with CustomRenderer(self.image_url, content_type) as renderer:
                    renderer.render()
