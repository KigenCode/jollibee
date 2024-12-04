import sqlite3

conn = sqlite3.connect("menu.db")
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS menu_items (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        type TEXT NOT NULL,
        rice_count INTEGER DEFAULT 0,
        drink_count INTEGER DEFAULT 0,
        value_score REAL
    )
''')
conn.commit()
conn.close()