CREATE TABLE IF NOT EXISTS company_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL,
    category TEXT NOT NULL,
    sub_category TEXT NOT NULL,
    amount TEXT NOT NULL,
    date TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS simulation_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    config_name TEXT NOT NULL,
    rules TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS simulation_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    config_id INTEGER REFERENCES simulation_config(id),
    result TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO company_data (company_name, category, sub_category, amount, date) VALUES
('Company A', 'Category 1', 'Sub Category 1', 1000.0, '2023-01-01'),
('Company B', 'Category 2', 'Sub Category 2', 1500.0, '2023-02-01'),
('Company C', 'Category 3', 'Sub Category 3', 2000.0, '2023-03-01');

CREATE TABLE IF NOT EXISTS devises (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        shortcut TEXT NOT NULL,
        name TEXT NOT NULL
        )

CREATE TABLE IF NOT EXISTS langues (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        shortcut TEXT NOT NULL,
        name TEXT NOT NULL
        )

INSERT INTO devises (shortcut, name) VALUES
('EUR', 'Euro'),
('USD', 'Dollar Américain'),
('GBP', 'Livre Sterling'),
('CAD', 'Dollar Canadien'),
('CHF', 'Franc Suisse');

INSERT INTO langues (shortcut, name) VALUES
('FR', 'Français'),
('EN', 'Anglais'),
('ES', 'Espagnol');