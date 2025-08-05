# Task 2: Books to Scrape - Multiprocessing Web Scraper

## Overview

This project implements a multiprocessing web scraper for [books.toscrape.com](https://books.toscrape.com/) using Playwright. It is designed to scrape book details from specified categories and store them in a PostgreSQL database. The architecture ensures fault tolerance through a custom process manager that restarts failed scraper processes.

## Features

* **Playwright-based scraping** (no external parsers like BeautifulSoup or lxml)
* **Multiprocessing architecture** with isolated browser instances per process
* **ProcessManager** for monitoring and restarting crashed scraper processes
* **Configurable number of scraper processes** via `.env`
* **PostgreSQL integration** using `psycopg2`
* **Graceful WriterProcess shutdown** using a `STOP_SIGNAL`
* **Duplicate link filtering** in `CategoryParser`
* **Data validation** before database insertion

## Data Collected

For each book:

* Title
* Category
* Price
* Rating
* Stock availability
* Image URL
* Description
* Product information (UPC, product type, tax, prices, reviews)

## Project Structure

```
task2/
├── browser/
│   ├── book_parser.py         # Parses book detail pages
│   └── category_parser.py     # Collects unique book links from category pages
├── data_models/
│   └── book.py                # Book dataclass definition
├── storage/
│   └── writer.py              # WriterProcess for inserting books into PostgreSQL
├── debug/
│   └── debug_book_scrape.py   # Debug utilities for testing parsers
├── config.py                  # Loads configuration from environment variables
├── docker-compose.yml         # PostgreSQL service for local development
├── main.py                    # Entry point; starts and monitors processes
├── process_manager.py         # Starts, monitors, and restarts scraper processes
├── scraper_process.py         # ScraperProcess class
├── requirements.txt           # Python dependencies
├── schema.sql                 # Database schema for books table
└── .env.example               # Example environment configuration
```

## Requirements

* Python 3.10+
* Playwright
* psycopg2
* PostgreSQL (local or Dockerized)

## Setup

1. **Clone repository and switch to `task2` branch**

```bash
git checkout task2
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
playwright install
```

3. **Set up PostgreSQL**

```bash
docker-compose up -d
psql -h localhost -p 5434 -U postgres -d books -f schema.sql
```

4. **Configure environment variables**

```bash
cp .env.example .env
# Edit .env with your settings
```

## Running the Scraper

```bash
python main.py
```

Default categories are defined in `config.py` under `DEFAULT_CATEGORIES`.

To run with a custom number of processes:

```bash
NUM_PROCESSES=5 python main.py
```

## Testing Fault Tolerance

Enable crash simulation in `.env`:

```
SIMULATE_CRASH=true
```

Run the scraper and observe `ProcessManager` restarting the crashed process.

## Logs

Logging is configured in `main.py` and provides detailed output:

* Process starts/stops
* Pages being scraped
* Books inserted into DB
* Process restarts after crash

## Database Schema

The `books` table contains the following columns:

* title, price, rating, availability, image\_url
* description, category, upc, product\_type
* price\_excl\_tax, price\_incl\_tax, tax, num\_reviews

Primary key is `upc` to prevent duplicate inserts.

## Stopping the Scraper

The scraper stops automatically when:

* All tasks are completed
* All scraper processes have finished
* `STOP_SIGNAL` is sent to WriterProcess

## Example Command Sequence

```bash
git checkout task2
pip install -r requirements.txt
playwright install
docker-compose up -d
psql -h localhost -p 5434 -U postgres -d books -f schema.sql
cp .env.example .env
python main.py
```
