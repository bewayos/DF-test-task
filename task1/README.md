# Task 1: Vendr Scraper

## Overview

This project is a multithreaded web scraper designed to extract product data from specific categories on [vendr.com](https://www.vendr.com/) and store the results in a PostgreSQL database.

### Categories scraped:

* DevOps
* IT Infrastructure
* Data Analytics and Management

### Data collected per product:

* Name
* Category
* Price range
* Description
* Product URL

---

## Tech Stack

* Python 3.10+
* `requests` + `lxml` for scraping
* `psycopg2` for PostgreSQL interaction
* `threading` + `queue` for concurrency
* `dotenv` for environment configuration
* Docker (for PostgreSQL instance)

---

## Project Structure

```
task1/
├── config.py
├── main.py
├── .env
├── .env.example
├── requirements.txt
├── docker-compose.yml
├── database/
│   ├── database.py
│   └── schema.sql
├── scraper/
│   ├── http_client.py
│   ├── link_extractor.py
│   ├── models.py
│   ├── product_parser.py
│   └── scraper.py
├── threads/
│   ├── queue.py
│   ├── worker.py
│   └── writer.py
└── tests/
    ├── test_link_extractor.py
    └── test_product_parser.py
```

---

## Setup Instructions

### 1. Clone the repository and navigate to the project

```
git clone https://github.com/bewayos/DF-test-task.git
cd dataforest-test-task/task1
```

### 2. Setup the environment

Install the requirements:

```
pip install -r requirements.txt
```

Create and configure `.env` file:

```
cp .env.example .env
# Edit if needed
```

### 3. Start PostgreSQL (Docker)

```
docker-compose up -d db
```

Create the database schema:

```
docker exec -it task1-db-1 psql -U postgres -d vendr -f /schema.sql
```

---

## Run Scraper

```
python main.py
```

This will:

* Extract product links
* Spawn multiple worker threads to scrape data
* Use a writer thread to insert data into PostgreSQL

Logs will indicate progress and completion.

---

## Environment Variables

See `.env.example`:

```env
DB_HOST=localhost
DB_PORT=5433
DB_NAME=vendr
DB_USER=postgres
DB_PASSWORD=secret
NUM_WORKERS=15
BASE_URL=https://www.vendr.com
```

---

## Testing

To run tests:

```
python -m task1.tests.test_product_parser -v
python -m task1.tests.test_link_extractor -v
```

---

## Notes

* Make sure the site structure of vendr.com hasn't changed since the scraper relies on static HTML structure.
* All exceptions are logged. Network failures are handled gracefully.
* Thread joining is performed to ensure clean exit.

---

## Author

Test task completed for Dataforest recruitment.
Contact: [artyashchenko.wrk@gmail.com](mailto:artyashchenko.wrk@gmail.com)
