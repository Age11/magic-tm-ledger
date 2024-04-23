import requests

from config import URL


class Assets:

    def __init__(self, selected_project):
        self.selected_project_id = selected_project
        self.url_path = f"{URL}/{self.selected_project_id}"

    def fetch_all_assets(self):
        print(f"retrieving assets from {self.url_path}/assets")
        assets = requests.get(f"{self.url_path}/assets").json()
        print(f"Retrieved {assets}")
        return assets

    def create_asset(self, asset_data):
        print(f"Creating asset with the following data: {asset_data}")
        return requests.post(f"{self.url_path}/assets", json=asset_data)
