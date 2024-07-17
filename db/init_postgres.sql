CREATE TABLE IF NOT EXISTS company_data (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    sub_category VARCHAR(255) NOT NULL,
    amount DECIMAL(15, 2) NOT NULL,
    date DATE NOT NULL
);

CREATE TABLE IF NOT EXISTS simulation_config (
    id SERIAL PRIMARY KEY,
    config_name VARCHAR(255) NOT NULL,
    rules JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS simulation_results (
    id SERIAL PRIMARY KEY,
    config_id INT REFERENCES simulation_config(id),
    result JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
