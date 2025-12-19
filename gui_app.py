import customtkinter as ctk
import json
import os
import budget_tracker

# ----------------------------------------------
# ----------------------------------------------
# ----------------------------------------------
# ------------------ DEFAULTS ------------------
ctk.set_default_color_theme("blue")

# ----------------------------------------------
# ----------------------------------------------
# ----------------------------------------------
# ------------------ SETTINGS ------------------
def load_settings():
    if not os.path.exists("settings.json"):
        return {"appearance_mode": "System"}
    with open("settings.json", "r") as f:
        return json.load(f)

def save_settings(key, value):
    data = load_settings()
    data[key] = value
    with open("settings.json", "w") as f:
        json.dump(data, f, indent=4)
        
# ----------------------------------------------
# ----------------------------------------------
# ----------------------------------------------
# ------------------ APP ------------------
root = ctk.CTk()
root.geometry("1000x700")
root.title("Talabat SUT")

settings = load_settings()
ctk.set_appearance_mode(settings.get("appearance_mode", "System"))

# ----------------------------------------------
# ----------------------------------------------
# ----------------------------------------------
# ------------------ TABS ------------------
def on_tab_change():
    if tabs.get() == "Menu":
        show_restaurant("All")  # Show all restaurants by default
    elif tabs.get() == "Cart":
        refresh_cart()

tabs = ctk.CTkTabview(root, width=950, height=650, command=on_tab_change)
tabs.pack(padx=20, pady=20)

tab_menu = tabs.add("Menu")
tab_cart = tabs.add("Cart")
tab_settings = tabs.add("Settings")

# ----------------------------------------------
# ----------------------------------------------
# ----------------------------------------------
# ------------------ MENU TAB ------------------
# Create main container for menu tab
menu_main_frame = ctk.CTkFrame(tab_menu)
menu_main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Create sidebar frame for restaurant buttons
sidebar_frame = ctk.CTkFrame(menu_main_frame, width=220)  # Slightly wider for restaurant names
sidebar_frame.pack(side="left", fill="y", padx=(0, 10), pady=5)
sidebar_frame.pack_propagate(False)

# Create scrollable frame for menu items
menu_frame = ctk.CTkScrollableFrame(menu_main_frame)
menu_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)

# Restaurant data and buttons
restaurant_buttons = {}
restaurant_data = {}  # Store restaurant data for display

menu_loaded = False

def build_menu():
    global menu_loaded, restaurant_data
    if menu_loaded:
        return

    # Load menu data directly from JSON to get restaurant information
    with open("menu.json", "r", encoding="utf-8") as f:
        restaurants = json.load(f)
    
    # Store restaurant data for display
    restaurant_data = {restaurant["restaurant"]: restaurant for restaurant in restaurants}
    
    # Create "All" button to show all restaurants
    all_button = ctk.CTkButton(
        sidebar_frame,
        text="All Restaurants",
        font=("Arial", 14, "bold"),
        height=40,
        command=lambda: show_restaurant("All")
    )
    all_button.pack(fill="x", padx=10, pady=(10, 5))
    restaurant_buttons["All"] = all_button
    
    # Add separator
    ctk.CTkLabel(sidebar_frame, text="RESTAURANTS", font=("Arial", 12, "bold")).pack(pady=(15, 5))
    
    # Create restaurant buttons
    for restaurant_name in sorted(restaurant_data.keys()):
        btn = ctk.CTkButton(
            sidebar_frame,
            text=restaurant_name,
            font=("Arial", 12),
            height=35,
            anchor="w",
            command=lambda r=restaurant_name: show_restaurant(r)
        )
        btn.pack(fill="x", padx=10, pady=2)
        restaurant_buttons[restaurant_name] = btn
    
    menu_loaded = True

def show_restaurant(restaurant_name):
    """Show menu for a specific restaurant or all restaurants"""
    # Clear previous widgets in menu frame
    for widget in menu_frame.winfo_children():
        widget.destroy()
    
    # Update button styles to show active restaurant
    for r_name, btn in restaurant_buttons.items():
        if r_name == restaurant_name:
            btn.configure(fg_color="#2FA572", hover_color="#27AE60")  # Green for active
        else:
            btn.configure(fg_color=("#3A7EBF", "#1F538D"), hover_color=("#325882", "#14375E"))
    
    if restaurant_name == "All":
        # Show all restaurants
        title = ctk.CTkLabel(
            menu_frame,
            text="All Restaurants",
            font=("Arial", 28, "bold")
        )
        title.pack(pady=(10, 20))
        
        for rest_name, restaurant in sorted(restaurant_data.items()):
            # Restaurant header
            rest_header = ctk.CTkFrame(menu_frame)
            rest_header.pack(fill="x", pady=(25, 15), padx=10)
            
            ctk.CTkLabel(
                rest_header,
                text=rest_name,
                font=("Arial", 24, "bold"),
                text_color="#2FA572"
            ).pack(side="left", padx=10)
            
            # Restaurant categories
            for category in restaurant["categories"]:
                # Category header
                cat_header = ctk.CTkFrame(menu_frame)
                cat_header.pack(fill="x", pady=(15, 10), padx=20)
                
                ctk.CTkLabel(
                    cat_header,
                    text=category["category"],
                    font=("Arial", 20, "bold"),
                    anchor="w"
                ).pack(side="left", padx=10)
                
                # Category items
                for item in category.get("items", []):
                    create_menu_item_row(item, category["category"], rest_name)
    else:
        # Show specific restaurant
        restaurant = restaurant_data[restaurant_name]
        
        # Restaurant title
        title = ctk.CTkLabel(
            menu_frame,
            text=restaurant_name,
            font=("Arial", 28, "bold"),
            text_color="#2FA572"
        )
        title.pack(pady=(10, 20))
        
        # Restaurant categories
        for category in restaurant["categories"]:
            # Category header
            cat_header = ctk.CTkFrame(menu_frame)
            cat_header.pack(fill="x", pady=(15, 10), padx=10)
            
            ctk.CTkLabel(
                cat_header,
                text=category["category"],
                font=("Arial", 22, "bold"),
                anchor="w"
            ).pack(side="left", padx=10)
            
            # Category items
            for item in category.get("items", []):
                create_menu_item_row(item, category["category"], restaurant_name)

def create_menu_item_row(item, category, restaurant_name):
    """Create a row for a menu item"""
    row = ctk.CTkFrame(menu_frame)
    row.pack(fill="x", pady=4, padx=20)
    
    # Item name with optional styling
    name_label = ctk.CTkLabel(row, text=item["name"], font=("Arial", 14))
    name_label.pack(side="left", padx=20, fill="x", expand=True)
    
    # Price
    price_label = ctk.CTkLabel(row, text=f'{item["price"]} E£', font=("Arial", 14, "bold"))
    price_label.pack(side="right", padx=20)
    
    # Add button
    add_btn = ctk.CTkButton(
        row,
        text="Add to Cart",
        width=100,
        font=("Arial", 12),
        fg_color="#27AE60",
        hover_color="#1E8449",
        command=lambda n=item["name"], p=item["price"], c=category: 
            (budget_tracker.add_to_cart(n, p, c), refresh_cart())
    )
    add_btn.pack(side="right", padx=10)
    
    # Optional: Add small restaurant indicator (for "All" view)
    if restaurant_name != "All":
        rest_label = ctk.CTkLabel(row, text=f"({restaurant_name})", font=("Arial", 10), text_color="gray")
        rest_label.pack(side="right", padx=5)

# ----------------------------------------------
# ----------------------------------------------
# ----------------------------------------------
# ------------------ CART TAB ------------------
cart_frame = ctk.CTkScrollableFrame(tab_cart)
cart_frame.pack(fill="both", expand=True, padx=15, pady=15)

# Clear cart function
def clear_cart():
    budget_tracker.clear_cart()
    refresh_cart()

# Refresh cart display
def refresh_cart():
    # Clear previous widgets
    for widget in cart_frame.winfo_children():
        widget.destroy()

    # Display each cart item
    for item in budget_tracker.get_cart_items():
        row = ctk.CTkFrame(cart_frame)
        row.pack(fill="x", pady=5, padx=5)

        # Item name
        name_label = ctk.CTkLabel(row, text=item["name"], width=200, anchor="w")
        name_label.grid(row=0, column=0, sticky="w", padx=5)

        # Minus button
        minus_btn = ctk.CTkButton(
            row,
            text="-",
            width=30,
            fg_color="#E74C3C",
            hover_color="#C0392B",
            command=lambda n=item["name"], c=item["category"]: [budget_tracker.decrease_qty(n, c), refresh_cart()]
        )
        minus_btn.grid(row=0, column=1, padx=2)

        # Quantity
        qty_label = ctk.CTkLabel(row, text=str(item["qty"]), width=30)
        qty_label.grid(row=0, column=2, padx=2)

        # Plus button
        plus_btn = ctk.CTkButton(
            row,
            text="+",
            width=30,
            fg_color="#27AE60",
            hover_color="#1E8449",
            command=lambda n=item["name"], p=item["price"], c=item["category"]: [budget_tracker.add_to_cart(n, p, c), refresh_cart()]
        )
        plus_btn.grid(row=0, column=3, padx=2)

        # Item total price
        price_label = ctk.CTkLabel(row, text=f"{item['price']*item['qty']} E£", width=100, anchor="e")
        price_label.grid(row=0, column=4, sticky="e", padx=5)

        # Configure grid to align properly
        row.grid_columnconfigure(0, weight=3)
        row.grid_columnconfigure(1, weight=1)
        row.grid_columnconfigure(2, weight=1)
        row.grid_columnconfigure(3, weight=1)
        row.grid_columnconfigure(4, weight=2)

    # Bottom row: total + clear button
    bottom_frame = ctk.CTkFrame(cart_frame)
    bottom_frame.pack(fill="x", pady=10, padx=5)

    total_lbl = ctk.CTkLabel(bottom_frame, text=f"Total: {budget_tracker.get_total()} E£", font=("Arial", 20, "bold"))
    total_lbl.pack(side="left", padx=5)

    clear_btn = ctk.CTkButton(bottom_frame, text="Clear Cart", fg_color="#E74C3C", hover_color="#C0392B",
                              command=clear_cart)
    clear_btn.pack(side="right", padx=5)
    
# ----------------------------------------------
# ----------------------------------------------
# ----------------------------------------------
# ------------------ SETTINGS TAB ------------------
loaded_settings = load_settings()
start_mode = loaded_settings.get("appearance_mode", "System")
ctk.set_appearance_mode(start_mode)
switch_var = ctk.StringVar(value="on" if start_mode == "dark" else "off")
def change_theme():
    
    if switch_var.get() =="on":
        ctk.set_appearance_mode("Dark")
        save_settings("appearance_mode", "Dark")
    else:
        ctk.set_appearance_mode("Light")
        save_settings("appearance_mode", "Light")

theme_switch = ctk.CTkSwitch(tab_settings,
                             text="Dark Mode",
                             command=change_theme,
                             variable=switch_var,
                             onvalue="on",
                             offvalue="off")
theme_switch.pack(pady=10, padx=0)

# ----------------------------------------------
# ----------------------------------------------
# ----------------------------------------------
# ------------------ STARTUP ------------------
budget_tracker.init_menu()
budget_tracker.load_state_if_today()

tabs.set("Menu")
build_menu()
show_restaurant("All")  # Show all restaurants by default
refresh_cart()

# ----------------------------------------------
# ----------------------------------------------
# ----------------------------------------------
# ------------------ RUN ------------------
root.mainloop()