import json
import os
import datetime

MENU_FILE = "menu.json"
STATE_FILE = "tracker_state.json"

# -------- GLOBAL STATE --------
menu_data = {}
purchased_items = []
daily_total = 0.0


# -------- MENU --------
def load_menu_data(path=MENU_FILE):
    with open(path, "r", encoding="utf-8") as f:
        restaurants = json.load(f)

    menu = {}

    for restaurant in restaurants:
        for category in restaurant["categories"]:
            cat_name = category["category"]
            items = category.get("items", [])

            if cat_name not in menu:
                menu[cat_name] = []

            for item in items:
                menu[cat_name].append({
                    "name": item["name"],
                    "price": float(item["price"])
                })

    return menu



def init_menu():
    global menu_data
    menu_data = load_menu_data()


def get_menu():
    return menu_data


# -------- STATE --------
def _state_file():
    return os.path.join(os.path.dirname(__file__), STATE_FILE)


def save_state():
    data = {
        "date": datetime.date.today().isoformat(),
        "items": purchased_items,
        "total": daily_total
    }
    with open(_state_file(), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_state_if_today():
    global purchased_items, daily_total

    if not os.path.exists(_state_file()):
        return

    with open(_state_file(), "r", encoding="utf-8") as f:
        data = json.load(f)

    if data.get("date") == datetime.date.today().isoformat():
        purchased_items = data.get("items", [])
        daily_total = data.get("total", 0.0)


# -------- CART --------
def add_to_cart(name, price, category):
    global daily_total

    for item in purchased_items:
        if item["name"] == name and item["category"] == category:
            item["qty"] += 1
            daily_total += price
            save_state()
            return

    purchased_items.append({
        "name": name,
        "price": price,
        "category": category,
        "qty": 1
    })

    daily_total += price
    save_state()


def delete_from_cart(name, category):
    global daily_total

    for item in purchased_items[:]:
        if item["name"] == name and item["category"] == category:
            daily_total -= item["price"] * item["qty"]
            purchased_items.remove(item)
            save_state()
            return


def get_cart_items():
    return purchased_items


def get_total():
    return daily_total





def increase_qty(name, category):
    global daily_total

    for item in purchased_items:
        if item["name"] == name and item["category"] == category:
            item["qty"] += 1
            daily_total += item["price"]
            save_state()
            return


# decrease item quantity
def decrease_qty(name, category):
    for item in purchased_items:
        if item["name"] == name and item["category"] == category:
            global daily_total
            if item["qty"] > 1:
                item["qty"] -= 1
                daily_total -= item["price"]
            else:
                daily_total -= item["price"]
                purchased_items.remove(item)
            save_state()
            break


def clear_cart():
    global purchased_items, daily_total
    purchased_items.clear()
    daily_total = 0
    save_state()


