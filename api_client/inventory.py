import requests

from config import URL, INVENTORY_PATH, ITEMS_PATH


def fetch_inventories(project_id):
    print(f"retrieving inventory from {URL}/{project_id}{INVENTORY_PATH}")
    inventories = requests.get(f"{URL}/{project_id}{INVENTORY_PATH}").json()
    print(f"Retrieved {inventories}")
    return inventories


def create_inventory(project_id, inventory_data):
    print(f"Creating inventory with the following data: {inventory_data}")
    return requests.post(f"{URL}/{project_id}{INVENTORY_PATH}", json=inventory_data)


def fetch_inventory_items(project_id, inventory_id):
    print(
        f"retrieving inventory items from {URL}/{project_id}{INVENTORY_PATH}/{inventory_id}{ITEMS_PATH}"
    )
    items = requests.get(
        f"{URL}/{project_id}{INVENTORY_PATH}/{inventory_id}/{ITEMS_PATH}"
    ).json()
    print(f"Retrieved {items}")
    return items


def create_inventory_item(project_id, invenory_id, item_data):
    print(f"Creating inventory item with the following data: {item_data}")
    requests.post(
        f"{URL}/{project_id}{INVENTORY_PATH}/{invenory_id}{ITEMS_PATH}", json=item_data
    )


def update_inventory_item(project_id, inventory_id, item_data):
    print(f"Updating inventory item with the following data: {item_data}")
    # requests.put(
    #     f"{URL}/{project_id}{INVENTORY_PATH}/{inventory_id}{ITEMS_PATH}/{item_data['id']}",
    #     json=item_data,
    # )
