import sqlite3

DB = "database.db"

def rechercher_client(query: str) -> str:
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    query = query.strip()

    cursor.execute("SELECT nom, solde, type_compte FROM clients WHERE id = ?", (query.upper(),))
    result = cursor.fetchone()

    if not result:
        cursor.execute("SELECT nom, solde, type_compte FROM clients WHERE nom LIKE ?", (f"%{query}%",))
        result = cursor.fetchone()

    conn.close()

    if result:
        nom, solde, type_compte = result
        return f"Client : {nom} | Solde : {solde:.2f} € | Type de compte : {type_compte}"
    
    return f"Aucun client trouvé pour : '{query}'"

def rechercher_produit(query: str) -> str:
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    query = query.strip()

    cursor.execute("SELECT nom, prix_ht, stock FROM produits WHERE id = ?", (query.upper(),))
    result = cursor.fetchone()

    if not result:
        cursor.execute("SELECT nom, prix_ht, stock FROM produits WHERE nom LIKE ?", (f"%{query}%",))
        result = cursor.fetchone()

    conn.close()

    if result:
        nom, prix_ht, stock = result
        tva = prix_ht * 0.20
        prix_ttc = prix_ht + tva

        return (
            f"Produit : {nom} | Prix HT : {prix_ht:.2f} € "
            f"| TVA : {tva:.2f} € | Prix TTC : {prix_ttc:.2f} € | Stock : {stock}"
        )

    return f"Aucun produit trouvé pour : '{query}'"


def lister_tous_les_clients(query: str = "") -> str:
    """Retourne la liste complète de tous les clients."""
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()

    cursor.execute("SELECT id, nom, type_compte, solde FROM clients")
    rows = cursor.fetchall()

    conn.close()

    if not rows:
        return "Aucun client trouvé."

    result = "Liste des clients :\n"
    for cid, nom, type_compte, solde in rows:
        result += f"  {cid} : {nom} | {type_compte} | Solde : {solde:.2f} €\n"

    return result


if __name__ == "__main__":
    print("=== Test rechercher_client ===")
    print(rechercher_client("Marie Dupont"))
    print(rechercher_client("C002"))
    print(rechercher_client("inconnu"))

    print("\n=== Test rechercher_produit ===")
    print(rechercher_produit("P001"))
    print(rechercher_produit("Souris"))
    print(rechercher_produit("inconnu"))

    print("\n=== Test lister_tous_les_clients ===")
    print(lister_tous_les_clients())