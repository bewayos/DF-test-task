CREATE TABLE IF NOT EXISTS products (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    median_price TEXT,
    price_range TEXT,
    description TEXT,
    url TEXT UNIQUE NOT NULL
);
