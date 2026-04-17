import sqlite3

DB = "database.db"

def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS clients")
    cursor.execute("DROP TABLE IF EXISTS produits")

    cursor.execute("""
        CREATE TABLE clients (
            id TEXT PRIMARY KEY,
            nom TEXT,
            email TEXT,
            ville TEXT,
            solde REAL,
            type_compte TEXT,
            date_inscription TEXT,
            achats_total REAL
        )
    """)

    cursor.execute("""
        CREATE TABLE produits (
            id TEXT PRIMARY KEY,
            nom TEXT,
            prix_ht REAL,
            stock INTEGER
        )
    """)

    clients = [
        ("C001", "Marie Dupont", "marie.dupont@email.fr", "Paris", 15420.50, "Premium", "2021-03-15", 8750.00),
        ("C002", "Jean Martin", None, None, 3200.00, "Standard", None, None),
        ("C003", "Sophie Bernard", None, None, 28900.00, "VIP", None, None),
        ("C004", "Lucas Petit", None, None, 750.00, "Standard", None, None),
    ]

    cursor.executemany("""
        INSERT INTO clients VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, clients)

    produits = [
        ("P001", "Ordinateur portable Pro", 899.00, 45),
        ("P002", "Souris ergonomique", 49.90, 120),
        ("P003", "Bureau réglable", 350.00, 18),
        ("P004", "Casque audio sans fil", 129.00, 67),
        ("P005", "Écran 27 pouces 4K", 549.00, 30),
    ]

    cursor.executemany("""
        INSERT INTO produits VALUES (?, ?, ?, ?)
    """, produits)

    conn.commit()
    conn.close()
    print("Database initialized.")

if __name__ == "__main__":
    init_db()