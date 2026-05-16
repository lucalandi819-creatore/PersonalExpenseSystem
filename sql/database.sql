-- =============================================
-- DATABASE: Sistema Gestione Spese Personali
-- =============================================

-- Tabella Categorie 
CREATE TABLE categorie (
id INTEGER PRIMARY KEY AUTOINCREMENT,
nome TEXT NOT NULL UNIQUE
);

--Tabella Spese 
CREATE TABLE spese (
id INTEGER PRIMARY KEY AUTOINCREMENT,
data TEXT NOT NULL,
importo REAL NOT NULL CHECK (importo>0),
id_categoria INTEGER NOT NULL,
descrizione TEXT,
FOREIGN KEY (id_categoria) REFERENCES categorie (id)
);

--Tabella Budget
CREATE TABLE budget (
id INTEGER PRIMARY KEY AUTOINCREMENT,
mese TEXT NOT NULL,
id_categoria INTEGER NOT NULL,
importo REAL NOT NULL CHECK (importo>0),
UNIQUE (mese, id_categoria),
FOREIGN KEY (id_categoria) REFERENCES categorie(id)
);
-- ==============================================
-- DATI DI ESEMPIO
-- ==============================================

-- Categorie di esempio
INSERT INTO categorie (nome) VALUES ('Alimentari');
INSERT INTO categorie (nome) VALUES ('Trasporto');
INSERT INTO categorie (nome) VALUES ('Svago');
INSERT INTO categorie (nome) VALUES ('Utenze');
INSERT INTO categorie (nome) VALUES ('Abbonamenti');

-- Spese di esempio
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES ('2026-05-02', 45.30, 1, 'Spesa supermercato');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES ('2026-05-05', 18.50, 2, 'Benzina');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES ('2026-05-08', 25.00, 3, 'Cinema');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES ('2026-05-10', 62.00, 4, 'Bolletta luce');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES ('2026-05-12', 9.99, 5, 'Abbonamento Netflix');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES ('2026-05-14', 30.00, 1, 'Spesa frutta e verdura');

-- Budget mensili di esempio
INSERT INTO budget (mese, id_categoria, importo) VALUES ('2026-05', 1, 200.00);
INSERT INTO budget (mese, id_categoria, importo) VALUES ('2026-05', 2, 80.00);
INSERT INTO budget (mese, id_categoria, importo) VALUES ('2026-05', 3, 50.00);


