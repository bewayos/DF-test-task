CREATE TABLE IF NOT EXISTS books (
    id SERIAL PRIMARY KEY,
    title TEXT,
    price TEXT,
    rating TEXT,
    availability TEXT,
    image_url TEXT,
    description TEXT,
    category TEXT,
    upc TEXT UNIQUE,
    product_type TEXT,
    price_excl_tax TEXT,
    price_incl_tax TEXT,
    tax TEXT,
    num_reviews TEXT
);
