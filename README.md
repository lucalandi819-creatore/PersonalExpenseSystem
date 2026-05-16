# Sistema di Gestione delle Spese Personali e del Budget

Progetto finale di programmazione: applicazione a riga di comando per la
gestione delle spese personali, sviluppata in Python con database
relazionale SQLite.

## Funzionalita'

L'applicazione consente all'utente di:
- Registrare le spese giornaliere
- Organizzare le spese per categoria
- Definire limiti di spesa mensili (budget) per categoria
- Visualizzare report riepilogativi:
  - Totale delle spese per categoria
  - Confronto tra spese mensili e budget
  - Elenco completo delle spese ordinate per data

## Requisiti per l'esecuzione

- Python 3.10 o superiore (per il supporto di match-case)
- SQLite3 (incluso nella libreria standard di Python)
- Sistema operativo: macOS, Linux o Windows

Non sono richieste librerie esterne: il programma utilizza solo moduli
della libreria standard di Python (sqlite3).

## Struttura del progetto

PersonalExpenseSystem/
- src/main.py            : codice sorgente principale
- sql/database.sql       : script di creazione e popolamento DB
- sql/spese.db           : database SQLite
- demo/demo_video.mp4    : video dimostrativo
- README.md

## Istruzioni per l'esecuzione

### 1. Creazione del database

Da terminale, posizionarsi nella cartella sql ed eseguire:

    cd sql
    sqlite3 spese.db < database.sql

Questo comando crea il database spese.db con tutte le tabelle
(categorie, spese, budget) e inserisce i dati di esempio.

### 2. Avvio del programma

Posizionarsi nella cartella src ed eseguire:

    cd ../src
    python3 main.py

In alternativa si puo' aprire main.py con IDLE e premere F5.

## Utilizzo del programma

Dopo l'avvio appare il Menu Principale con cinque opzioni:

1. Gestione Categorie: aggiunta di una nuova categoria di spesa
2. Inserisci Spesa: registrazione di una nuova spesa
3. Definisci Budget Mensile: limite di spesa mensile per categoria
4. Visualizza Report: accesso al sotto-menu dei report
5. Esci: chiusura del programma

## Vincoli del database

Lo schema implementa i seguenti vincoli di integrita':
- PRIMARY KEY su tutte le tabelle
- FOREIGN KEY da spese e budget verso categorie
- CHECK (importo > 0) su spese e budget
- UNIQUE sul nome della categoria e sulla coppia (mese, categoria) del budget
- NOT NULL sui campi obbligatori

## Autore

Luca Landi

