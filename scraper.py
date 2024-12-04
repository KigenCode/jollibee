import requests
from bs4 import BeautifulSoup
import sqlite3

def scrape_menu():
    url = "https://www.jollibeedelivery.com/menu/best-sellers"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    menu_items = []

    for item in soup.select(".menu-item-selector"):  # Update selectors as needed
        name = item.select_one(".item-name").text.strip()
        price = int(item.select_one(".item-price").text.strip().replace('PHP', '').replace(',', ''))
        rice_count = 1 if "rice" in name.lower() else 0
        drink_count = 1 if "drink" in name.lower() or "combo" in name.lower() else 0
        value_score = (rice_count + drink_count) / price
        menu_items.append((name, price, "combo" if rice_count + drink_count > 1 else "single", rice_count, drink_count, value_score))

    return menu_items

def update_menu_data():
    menu_items = scrape_menu()
    conn = sqlite3.connect("menu.db")
    c = conn.cursor()
    c.execute("DELETE FROM menu_items")
    c.executemany('''
        INSERT INTO menu_items (name, price, type, rice_count, drink_count, value_score) 
        VALUES (?, ?, ?, ?, ?, ?)
    ''', menu_items)
    conn.commit()
    conn.close()
