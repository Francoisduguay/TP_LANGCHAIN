import yfinance as yf
 
def obtenir_cours_action(symbole: str) -> str:
    """Retourne le cours simulé d'une action avec sa variation (+/-3%)."""
    symbole = symbole.strip().upper()

    try:
        ticker = yf.Ticker(symbole)
        histo = ticker.history(period="2d")

        if histo.empty or len(histo) < 2:
            return f"Action '{symbole}' non trouvée ou données indisponibles."

        # Derniers jours
        last = histo.iloc[-1]
        prev = histo.iloc[-2]

        current_price = last["Close"]
        previous_price = prev["Close"]

        variation_pct = ((current_price - previous_price) / previous_price) * 100
        volume = int(last["Volume"])

        tendance = '↑' if variation_pct >= 0 else '↓'

        return (f"{symbole} {tendance} : {current_price:.2f} $ ({variation_pct:+.2f}%) | Volume : {volume:,}\n")
    
    except Exception as e:
        return f" {e}: Erreur lors de la récupération de {symbole}."

    
def obtenir_cours_crypto(symbole: str) -> str:
    """Retourne le cours réel d'une crypto avec variation."""
    symbole = symbole.strip().upper()
    yf_symbol = f"{symbole}-USD"

    try:
        ticker = yf.Ticker(yf_symbol)
        hist = ticker.history(period="2d")

        if hist.empty or len(hist) < 2:
            return f"Crypto '{symbole}' non trouvée ou données indisponibles."

        last = hist.iloc[-1]
        prev = hist.iloc[-2]

        current_price = last["Close"]
        previous_price = prev["Close"]

        variation_pct = ((current_price - previous_price) / previous_price) * 100

        tendance = '↑' if variation_pct >= 0 else '↓'

        return f"{symbole} {tendance} : {current_price:.2f} $ ({variation_pct:+.2f}%)\n"

    except Exception:
        return f"Erreur lors de la récupération de {symbole}."
    
    
if __name__ == "__main__":
    print("=== Test obtenir_cours_action ===")
    for symbole in ["AAPL", "MSFT", "TSLA", "INCONNU"]:
        print(obtenir_cours_action(symbole))

    print("\n=== Test obtenir_cours_crypto ===")
    for symbole in ["BTC", "ETH", "SOL", "DOGE"]:
        print(obtenir_cours_crypto(symbole))