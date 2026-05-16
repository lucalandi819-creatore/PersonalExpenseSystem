# main.py
# Sistema di Gestione delle Spese Personali e del Budget

import sqlite3

# Apertura della connessione al database
conn = sqlite3.connect("../sql/spese.db")
conn.execute("PRAGMA foreign_keys = ON")
cur = conn.cursor()


# ===== FUNZIONI DEI MODULI =====

def gestisci_categorie():
    """Modulo 1: Inserimento di una nuova categoria di spesa."""
    print()
    print("--- Gestione Categorie ---")
    nome = input("Inserisci il nome della nuova categoria: ").strip()
    
    if nome == "":
        print("Errore: il nome della categoria non puo' essere vuoto.")
        return
    
    cur.execute("SELECT id FROM categorie WHERE nome = ?", (nome,))
    if cur.fetchone() is not None:
        print("La categoria esiste gia'.")
    else:
        cur.execute("INSERT INTO categorie (nome) VALUES (?)", (nome,))
        conn.commit()
        print("Categoria inserita correttamente.")


def inserisci_spesa():
    """Modulo 2: Registrazione di una nuova spesa."""
    print()
    print("--- Inserisci Spesa ---")
    data = input("Inserisci la data (YYYY-MM-DD): ").strip()
    
    try:
        importo = float(input("Inserisci l'importo: "))
    except ValueError:
        print("Errore: l'importo deve essere un numero.")
        return
    
    if importo <= 0:
        print("Errore: l'importo deve essere maggiore di zero.")
        return
    
    nome_categoria = input("Inserisci il nome della categoria: ").strip()
    descrizione = input("Inserisci una descrizione (facoltativa): ").strip()
    
    # Verifica esistenza categoria
    cur.execute("SELECT id FROM categorie WHERE nome = ?", (nome_categoria,))
    risultato = cur.fetchone()
    if risultato is None:
        print("Errore: la categoria non esiste.")
        return
    id_categoria = risultato[0]
    
    cur.execute(
        "INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES (?, ?, ?, ?)",
        (data, importo, id_categoria, descrizione)
    )
    conn.commit()
    print("Spesa inserita correttamente.")


def definisci_budget():
    """Modulo 3: Definizione di un budget mensile per una categoria."""
    print()
    print("--- Definisci Budget Mensile ---")
    mese = input("Inserisci il mese (YYYY-MM): ").strip()
    nome_categoria = input("Inserisci il nome della categoria: ").strip()
    
    try:
        importo = float(input("Inserisci l'importo del budget: "))
    except ValueError:
        print("Errore: l'importo deve essere un numero.")
        return
    
    if importo <= 0:
        print("Errore: il budget deve essere maggiore di zero.")
        return
    
    cur.execute("SELECT id FROM categorie WHERE nome = ?", (nome_categoria,))
    risultato = cur.fetchone()
    if risultato is None:
        print("Errore: la categoria non esiste.")
        return
    id_categoria = risultato[0]
    
    # Inserimento o aggiornamento (UPSERT)
    cur.execute("SELECT id FROM budget WHERE mese = ? AND id_categoria = ?", (mese, id_categoria))
    esistente = cur.fetchone()
    if esistente is not None:
        cur.execute("UPDATE budget SET importo = ? WHERE id = ?", (importo, esistente[0]))
    else:
        cur.execute(
            "INSERT INTO budget (mese, id_categoria, importo) VALUES (?, ?, ?)",
            (mese, id_categoria, importo)
        )
    conn.commit()
    print("Budget mensile salvato correttamente.")


def report_totale_per_categoria():
    """Report 1: Totale delle spese per categoria."""
    print()
    print("--- Totale Spese per Categoria ---")
    cur.execute("""
        SELECT c.nome, SUM(s.importo)
        FROM spese s
        JOIN categorie c ON s.id_categoria = c.id
        GROUP BY c.nome
        ORDER BY c.nome
    """)
    righe = cur.fetchall()
    if not righe:
        print("Nessuna spesa registrata.")
        return
    print(f"{'Categoria':<20}{'Totale Speso':>15}")
    print("-" * 35)
    for nome, totale in righe:
        print(f"{nome:<20}{totale:>15.2f}")


def report_spese_vs_budget():
    """Report 2: Confronto spese mensili e budget."""
    print()
    print("--- Spese Mensili vs Budget ---")
    cur.execute("""
        SELECT b.mese, c.nome, b.importo,
               COALESCE((SELECT SUM(s.importo)
                         FROM spese s
                         WHERE s.id_categoria = b.id_categoria
                           AND substr(s.data, 1, 7) = b.mese), 0)
        FROM budget b
        JOIN categorie c ON b.id_categoria = c.id
        ORDER BY b.mese, c.nome
    """)
    righe = cur.fetchall()
    if not righe:
        print("Nessun budget definito.")
        return
    for mese, categoria, budget, speso in righe:
        print()
        print(f"Mese: {mese}")
        print(f"Categoria: {categoria}")
        print(f"Budget: {budget:.2f}")
        print(f"Speso: {speso:.2f}")
        if speso > budget:
            print("Stato: SUPERAMENTO BUDGET")
        else:
            print("Stato: nei limiti")


def report_elenco_spese():
    """Report 3: Elenco di tutte le spese ordinate per data."""
    print()
    print("--- Elenco Completo delle Spese ---")
    cur.execute("""
        SELECT s.data, c.nome, s.importo, s.descrizione
        FROM spese s
        JOIN categorie c ON s.id_categoria = c.id
        ORDER BY s.data
    """)
    righe = cur.fetchall()
    if not righe:
        print("Nessuna spesa registrata.")
        return
    print(f"{'Data':<12}{'Categoria':<15}{'Importo':>10}  Descrizione")
    print("-" * 60)
    for data, categoria, importo, descrizione in righe:
        desc = descrizione if descrizione else ""
        print(f"{data:<12}{categoria:<15}{importo:>10.2f}  {desc}")


def visualizza_report():
    """Modulo 4: Sotto-menu per la visualizzazione dei report."""
    while True:
        print()
        print("--- Menu Report ---")
        print("1. Totale spese per categoria")
        print("2. Spese mensili vs budget")
        print("3. Elenco completo delle spese")
        print("4. Ritorna al menu principale")
        scelta = input("Inserisci la tua scelta: ")
        
        match scelta:
            case "1":
                report_totale_per_categoria()
            case "2":
                report_spese_vs_budget()
            case "3":
                report_elenco_spese()
            case "4":
                return
            case _:
                print("Scelta non valida. Riprovare.")


# ===== MENU PRINCIPALE =====
while True:
    print()
    print("-------------------------")
    print("SISTEMA SPESE PERSONALI")
    print("-------------------------")
    print("1. Gestione Categorie")
    print("2. Inserisci Spesa")
    print("3. Definisci Budget Mensile")
    print("4. Visualizza Report")
    print("5. Esci")
    print("-------------------------")
    
    scelta = input("Inserisci la tua scelta: ")
    
    match scelta:
        case "1":
            gestisci_categorie()
        case "2":
            inserisci_spesa()
        case "3":
            definisci_budget()
        case "4":
            visualizza_report()
        case "5":
            print("Arrivederci!")
            break
        case _:
            print("Scelta non valida. Riprovare.")

# Chiusura della connessione
conn.close()
