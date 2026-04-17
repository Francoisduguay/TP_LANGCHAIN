from langchain_classic.tools import Tool
from langchain_experimental.tools import PythonREPLTool
from dotenv import load_dotenv
load_dotenv()

from langchain_community.tools import TavilySearchResults
from tools.database import rechercher_client, rechercher_produit
from tools.finance import obtenir_cours_action, obtenir_cours_crypto
from tools.calculs import calculer_interets_composes, calculer_marge, calculer_mensualite_pret, calculer_tva
from tools.api_publique import convertir_devise
from tools.texte import  extraire_mots_cles, formater_rapport, resumer_texte
from tools.recommandation import recommander_produits
from tools.portefeuille import calculer_portefeuille

from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from langchain_classic.memory import ConversationBufferMemory
from langchain_classic import hub


# A3
tavily_tool = TavilySearchResults(max_results=1)
tavily_tool.name = "recherche_web"
tavily_tool.description = (
    "Effectue une recherche web en temps réel pour obtenir des informations récentes "
    "ou externes non disponibles dans les outils internes. "
    "Utiliser pour : actualités, entreprises, finance, événements récents ou questions générales. "
    "Entrée : une question en langage naturel."
)

# B2
python_repl = PythonREPLTool()
python_repl.description = (
    "Exécute du code Python pour effectuer des calculs complexes, "
    "analyses de données ou traitements non couverts par les autres outils. "
    "Entrée : code Python valide sous forme de chaîne."
)
# ATTENTION SECURITE : cet outil exécute du code arbitraire.
# Ne jamais utiliser en production sans sandbox.


tools =[
    # ── Outil 1 : Base de données ─────────────────────────────────────
    Tool(name='rechercher_client', func=rechercher_client,
         description='Recherche un client par nom ou ID (ex: C001). '
                     'Retourne solde, type de compte, historique achats.'),
    Tool(name='rechercher_produit', func=rechercher_produit,
         description='Recherche un produit par nom ou ID. '
                     'Retourne prix HT, TVA, prix TTC, stock.'),
    # ── Outil 2 : Données financières ─────────────────────────────────
    Tool(name='cours_action', func=obtenir_cours_action,
         description='Cours boursier d\'une action. '
                     'Entrée : symbole majuscule ex AAPL, MSFT, TSLA, LVMH, AIR.'),
    Tool(name='cours_crypto', func=obtenir_cours_crypto,
         description='Cours d\'une crypto. '
                     'Entrée : symbole ex BTC, ETH, SOL, BNB, DOGE.'),
    # ── Outil 3 : Calculs financiers ──────────────────────────────────
    Tool(name='calculer_tva', func=calculer_tva,
         description='Calcule TVA et prix TTC. Entrée : prix_ht,taux ex 100,20.'),
    Tool(name='calculer_interets', func=calculer_interets_composes,
         description='Intérêts composés. Entrée : capital,taux_annuel,années ex 10000,5,3.'),
    Tool(name='calculer_marge', func=calculer_marge,
         description='Marge commerciale. Entrée : prix_vente,cout_achat ex 150,80.'),
    Tool(name='calculer_mensualite', func=calculer_mensualite_pret,
         description='Mensualité prêt. Entrée : capital,taux_annuel,mois ex 200000,3.5,240.'),
    # ── Outil 4 : API publique ────────────────────────────────────────
    Tool(name='convertir_devise', func=convertir_devise,
         description='Conversion de devises en temps réel (API Frankfurter). '
                     'Entrée : montant,DEV_SOURCE,DEV_CIBLE ex 100,USD,EUR.'),
    # ── Outil 5 : Transformation de texte ────────────────────────────
    Tool(name='resumer_texte', func=resumer_texte,
         description='Résume un texte et donne des statistiques. Entrée : texte complet.'),
    Tool(name='formater_rapport', func=formater_rapport,
         description='Formate en rapport. Entrée : Cle1:Val1|Cle2:Val2.'),
    Tool(name='extraire_mots_cles', func=extraire_mots_cles,
         description='Extrait les mots-clés d\'un texte. Entrée : texte complet.'),
    # ── Outil 6 : Recommandation ─────────────────────────────────────
    Tool(name='recommander_produits', func=recommander_produits,
         description='Recommandations produits. '
                     'Entrée : budget,categorie,type_compte ex 300,Informatique,Premium. '
                     'Catégories : Informatique, Mobilier, Audio, Toutes. '
                     'Types : Standard, Premium, VIP.'),
     Tool(name="calculer_portefeuille", func=calculer_portefeuille,
          description="Calcule la valeur d'un portefeuille d'actions et cryptos. "
                       "Entrée format: SYMBOLE:QUANTITE|SYMBOLE:QUANTITE "
                       "Exemple: AAPL:5|MSFT:2|BTC:1"),
     tavily_tool,
     python_repl
]

def creer_agent():
    """Crée et retourne un agent LangChain configuré."""
    from langchain_openai import ChatOpenAI
    from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
    from langchain_classic import hub
    from langchain_classic.memory import ConversationBufferMemory
    import os

    # Initialisation du LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    # Prompt compatible tools + memory
    prompt = hub.pull("hwchase17/openai-tools-agent")

    # Mémoire conversationnelle
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )

    # Création de l'agent (tools + memory aware)
    agent = create_openai_tools_agent(
        llm=llm,
        tools=tools,
        prompt=prompt
    )

    # Agent executor avec mémoire
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,
        max_iterations=10,
        handle_parsing_errors=True
    )

    return agent_executor


def interroger_agent(agent, question: str):
    """Envoie une question à l'agent et affiche la réponse finale."""
    print(f"\n{'='*60}")
    print(f"Question : {question}")
    print('='*60)
    result = agent.invoke({"input": question})
    print(f"\nRéponse finale : {result['output']}")
    return result