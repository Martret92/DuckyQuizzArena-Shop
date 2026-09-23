"""
Temporary catalog data source.

This module exists to allow independent development of the shop
catalog while the duckies/shop persistence layer is being integrated.

Expected future flow:

    ShopItem -> duckies.Item -> InventoryItem -> Ducky

This data source is temporary and must not be treated as persistent
application data.
"""

SHOP_CATALOG = [
    {
        "id": 1,
        "name": "Ducky Sword",
        "description": "A powerful sword for your Ducky.",
        "price": 100,
        "rarity": "rare",
        "item_type": "weapon",
        "available": True,
    },
    {
        "id": 2,
        "name": "Golden Shield",
        "description": "A defensive shield with a golden finish.",
        "price": 150,
        "rarity": "epic",
        "item_type": "armor",
        "available": True,
    },
    {
        "id": 3,
        "name": "Ducky Potion",
        "description": "A useful potion for your Ducky.",
        "price": 50,
        "rarity": "common",
        "item_type": "consumable",
        "available": True,
    },
    {
        "id": 4,
        "name": "Legendary Crown",
        "description": "A legendary crown reserved for exceptional Duckies.",
        "price": 500,
        "rarity": "legendary",
        "item_type": "accessory",
        "available": False,
    },
]
