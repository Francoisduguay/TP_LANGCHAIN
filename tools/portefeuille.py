import yfinance as yf

def calculer_portefeuille(input_str: str) -> str:
    """
    Calcule la valeur d'un portefeuille.
    Entrée SYMBOLE:QUANTITE: "AAPL:5|MSFT:2|BTC:1"
    """

    try:
        lignes = input_str.strip().split("|")

        details = []
        total_value = 0.0
        total_prev_value = 0.0

        for ligne in lignes:
            symbole, quantite = ligne.split(":")
            symbole = symbole.strip().upper()
            quantite = float(quantite)

            yf_symbol = symbole
            if symbole in ["BTC", "ETH", "SOL"]:
                yf_symbol = f"{symbole}-USD"

            ticker = yf.Ticker(yf_symbol)
            hist = ticker.history(period="2d")

            if hist.empty or len(hist) < 2:
                return f"Données indisponibles: {symbole}"

            last = hist.iloc[-1]
            prev = hist.iloc[-2]

            price = last["Close"]
            prev_price = prev["Close"]

            value = price * quantite
            prev_value = prev_price * quantite

            total_value += value
            total_prev_value += prev_value

            variation = ((price - prev_price) / prev_price) * 100

            details.append(
                f"{symbole} x{quantite} → {value:.2f}$ ({variation:+.2f}%)"
            )

        global_variation = ((total_value - total_prev_value) / total_prev_value) * 100

        result = "PORTFOLIO\n"
        result += "\n".join(details)
        result += f"\n\nTotal: {total_value:.2f}$"
        result += f"\nVariation globale: {global_variation:+.2f}%"

        return result

    except Exception as e:
        return f"Erreur portefeuille: {str(e)}"