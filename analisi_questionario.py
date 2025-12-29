# ======================================================
# Tesi di laurea – Capitolo 4 - Analisi del questionario
# Riccardo Ravelli
# ======================================================

import logging, warnings
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

warnings.filterwarnings(
    "ignore",
    message="pkg_resources is deprecated as an API.*",
    category=UserWarning
)

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] - [%(levelname)s] - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(f"./resources/script.log", mode='a')
    ]
)

plt.rcParams.update({
    "font.family": "Arial",
    "font.size": 12
})

FILE_CSV = "./resources/risposte_29_12_2025.csv"
OUTPUT_DIR = Path("output_plots")
OUTPUT_DIR.mkdir(exist_ok=True)

df = pd.read_csv(FILE_CSV)

def grafico_bar(series, titolo, nome_file, xlabel="", ylabel="Numero rispondenti"):
    counts = series.value_counts()

    if pd.api.types.is_numeric_dtype(counts.index):
        counts = counts.sort_index()
    else:
        counts.index = (
            counts.index
            .astype(str)
            .str.replace("&lt;", "<", regex=False)
            .str.replace("&gt;", ">", regex=False)
        )

        ordine_reddito = [
            "< 1000€",
            "1000 - 1500€",
            "1500 - 2000€",
            "> 2000€"
        ]

        if set(ordine_reddito).issuperset(set(counts.index)):
            counts = counts.reindex(ordine_reddito)

    counts.plot(kind="bar")
    plt.title(titolo)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / nome_file, dpi=300)
    plt.close()

def grafico_bar_checkbox(colonne, titolo, nome_file):
    counts = {col: df[col].notna().sum() for col in colonne}
    pd.Series(counts).sort_values(ascending=False).plot(kind="bar")
    plt.title(titolo)
    plt.ylabel("Numero rispondenti")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / nome_file, dpi=300)
    plt.close()

try:
    logging.info("Inizio analisi del questionario.")
    
    #Segmentazione e customer journey (4.2)
    grafico_bar(
        df["Età"],
        "Distribuzione del campione per fascia d'età",
        "01_eta.png"
    )

    grafico_bar(
        df["Occupazione"],
        "Distribuzione del campione per occupazione",
        "02_occupazione.png"
    )

    grafico_bar(
        df["Reddito Mensile Personale"],
        "Distribuzione del campione per fascia di reddito mensile",
        "03_reddito.png"
    )

    grafico_bar(
        df["Quanto ritieni importante proteggersi da rischi?"],
        "Importanza attribuita alla protezione dai rischi",
        "04_importanza_protezione.png",
        xlabel="Livello (1 = basso, 5 = alto)"
    )

    grafico_bar(
        df["Attualmente hai una polizza?"],
        "Possesso di una polizza assicurativa",
        "05_possesso_polizza.png"
    )

    motivazioni = [
        "Sentirmi più sicuro/a",
        "Proteggere me stesso/a da imprevisti",
        "Proteggere la mia famiglia / partner",
        "Avere copertura sanitaria",
        "Essere obbligato (es. auto)",
        "Gestire meglio situazioni di rischio"
    ]

    grafico_bar_checkbox(
        motivazioni,
        "Motivazioni alla sottoscrizione di una polizza",
        "06_motivazioni.png"
    )

    canali = [
        "Internet / Google",
        "Social media",
        "Siti comparatori (es. Facile.it)",
        "Agenzia assicurativa / consulente",
        "Amici o familiari",
        "Video informativi (YouTube, TikTok…)"
    ]

    grafico_bar_checkbox(
        canali,
        "Canali utilizzati per informarsi sui prodotti assicurativi",
        "07_canali.png"
    )

    #Evidenze e criticità (4.3)
    grafico_bar(
        df["Quanto ti senti informato sui prodotti assicurativi?"],
        "Livello di informazione percepito sui prodotti assicurativi",
        "08_livello_informazione.png",
        xlabel="Livello (1 = basso, 5 = alto)"
    )

    ostacoli = [
        "Costi troppo alti",
        "Linguaggio complicato",
        "Poca trasparenza / chiarezza",
        "Non mi fido delle compagnie",
        "Non mi interessa / non è una priorità",
        "Esperienze negative passate"
    ]

    grafico_bar_checkbox(
        ostacoli,
        "Principali ostacoli alla sottoscrizione di una polizza",
        "09_ostacoli.png"
    )

    logging.info("Analisi completata.")
    logging.info(f"Grafici salvati in: {OUTPUT_DIR.resolve()}")

except Exception as e:
    logging.error(f"Errore durante l'analisi: {e}")