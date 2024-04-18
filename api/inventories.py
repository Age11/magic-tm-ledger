import requests

from config import (
    URL,
    INVENTORY_PATH,
    ITEMS_PATH,
)


class Inventories:
    def __init__(self, selected_project):
        self.selected_project_id = selected_project
        self.url_path = f"{URL}/{self.selected_project_id}"

    def fetch(self):
        print(f"retrieving inventory from {self.url_path}{INVENTORY_PATH}")
        inventories = requests.get(f"{self.url_path}{INVENTORY_PATH}").json()
        print(f"Retrieved {inventories}")
        return inventories

    def create_inventory(self, inventory_data):
        print(f"Creating inventory with the following data: {inventory_data}")
        return requests.post(f"{self.url_path}{INVENTORY_PATH}", json=inventory_data)

    def fetch_inventory_items(self, inventory_id):
        print(
            f"retrieving inventory items from {self.url_path}{INVENTORY_PATH}/{inventory_id}{ITEMS_PATH}"
        )
        items = requests.get(
            f"{self.url_path}{INVENTORY_PATH}/{inventory_id}/{ITEMS_PATH}"
        ).json()
        print(f"Retrieved {items}")
        return items

    def create_inventory_item(self, inventory_id, item_data):
        print(f"Creating inventory item with the following data: {item_data}")
        requests.post(
            f"{self.url_path}{INVENTORY_PATH}/{inventory_id}{ITEMS_PATH}",
            json=item_data,
        )

    def decrease_stock(self, item_id, inventory_id, quantity, invoice_id):
        print(
            f"Decreasing stock for item {item_id} in inventory {inventory_id} by {quantity}"
        )
        print(
            f"Put at {self.url_path}{INVENTORY_PATH}/{inventory_id}{ITEMS_PATH}/{item_id}/decrease-stock/"
        )

        requests.put(
            f"{self.url_path}{INVENTORY_PATH}/{inventory_id}{ITEMS_PATH}/{item_id}/decrease-stock/",
            json={"quantity": quantity, "invoice_id": invoice_id},
        )

    def update_inventory_item(project_id, inventory_id, item_data):
        print(f"Updating inventory item with the following data: {item_data}")
        # requests.post(
        #     f"{self.url_path}{INVENTORY_PATH}/{inventory_id}{ITEMS_PATH}/{item_data['id']}",
        #     json=item_data,
        # )
