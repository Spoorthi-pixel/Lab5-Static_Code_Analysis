"""
A simple inventory management system to track stock data.

This script allows for adding, removing, and querying item quantities,
as well as saving and loading inventory data to/from a JSON file.
It uses the logging module for clear, informative output.
"""

import json
import logging

# --- Module-level Configurations ---
logging.basicConfig(
    level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s'
)


def add_item(data: dict, item: str, qty: int) -> None:
    """
    Adds a specified quantity of an item to the inventory.

    Validates that the item is a string and qty is an integer
    before proceeding.

    Args:
        data (dict): The inventory data dictionary.
        item (str): The name of the item to add.
        qty (int): The quantity to add. Must be an integer.
    """
    if not isinstance(item, str) or not isinstance(qty, int):
        logging.error("Invalid types: item str, quantity int required.")
        return

    if not item:
        logging.warning("Cannot add an item with an empty name.")
        return

    data[item] = data.get(item, 0) + qty
    logging.info("Added %s of %s", qty, item)


def remove_item(data: dict, item: str, qty: int) -> None:
    """
    Removes a specified quantity of an item from the inventory.

    If the quantity to remove is greater than or equal to the current stock,
    the item is deleted entirely. Handles cases where the item does not exist.

    Args:
        data (dict): The inventory data dictionary.
        item (str): The name of the item to remove.
        qty (int): The quantity to remove.
    """
    try:
        if data[item] > qty:
            data[item] -= qty
            logging.info(
                "Removed %s of %s. New stock: %s", qty, item, data[item]
            )
        else:
            del data[item]
            logging.info("Removed all stock of %s.", item)
    except KeyError:
        logging.warning(
            "Attempted to remove '%s' but it does not exist in stock.", item
        )


def get_qty(data: dict, item: str) -> int:
    """
    Retrieves the current quantity of a specific item.

    Args:
        data (dict): The inventory data dictionary.
        item (str): The name of the item to query.

    Returns:
        int: The current quantity of the item, or 0 if not found.
    """
    return data.get(item, 0)


def load_data(file: str = "inventory.json") -> dict:
    """
    Loads inventory data from a JSON file.

    Handles FileNotFoundError and JSONDecodeError gracefully by returning
    an empty inventory if the file is missing or corrupt.

    Args:
        file (str, optional): The file to load from.
                              Defaults to "inventory.json".

    Returns:
        dict: The loaded inventory data.
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            loaded_data = json.load(f)
            logging.info("Data loaded successfully from %s.", file)
            return loaded_data
    except FileNotFoundError:
        logging.warning(
            "File '%s' not found. Starting with empty inventory.", file
        )
        return {}
    except json.JSONDecodeError:
        logging.error("Could not decode JSON from %s. Starting fresh.", file)
        return {}


def save_data(data: dict, file: str = "inventory.json") -> None:
    """
    Saves the current inventory data to a JSON file.

    Uses 'with open' for safe file handling and pretty-prints the JSON.

    Args:
        data (dict): The inventory data dictionary.
        file (str, optional): The file to save to.
                              Defaults to "inventory.json".
    """
    with open(file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
        logging.info("Data saved successfully to %s.", file)


def print_data(data: dict) -> None:
    """
    Prints a formatted report of all items currently in stock.

    Args:
        data (dict): The inventory data dictionary.
    """
    print("\n--- Items Report ---")
    if not data:
        print("Inventory is empty.")
    else:
        for item, qty in data.items():
            print(f"{item} -> {qty}")
    print("--------------------\n")


def check_low_items(data: dict, threshold: int = 5) -> list[str]:
    """
    Finds all items with a quantity below a certain threshold.

    Args:
        data (dict): The inventory data dictionary.
        threshold (int, optional): The stock level to check against.
                                 Defaults to 5.

    Returns:
        list[str]: A list of item names that are below the threshold.
    """
    return [item for item, qty in data.items() if qty < threshold]


def main() -> None:
    """Main function to demonstrate inventory system functionality."""
    stock_data = load_data()

    add_item(stock_data, "apple", 10)
    add_item(stock_data, "banana", 20)
    add_item(stock_data, 123, "ten")  # Safely ignored due to validation
    remove_item(stock_data, "apple", 3)
    remove_item(stock_data, "orange", 1)  # Safely ignored

    print(f"Apple stock: {get_qty(stock_data, 'apple')}")
    print(f"Low items (below 5): {check_low_items(stock_data)}")
    print_data(stock_data)
    save_data(stock_data)
    print("Script finished safely.")


if __name__ == "__main__":
    main()
