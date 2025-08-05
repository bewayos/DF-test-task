# Dataforest Test Tasks

This repository contains two separate test tasks implemented for the Dataforest technical assessment. Each task is located on its own branch.

## Branches

* **`main`**: General repository information and instructions.
* **`task1`**: Implementation of Task 1 - Vendr scraper with multithreading and PostgreSQL integration.
* **`task2`**: Implementation of Task 2 - Books to Scrape scraper with multiprocessing, Playwright, and PostgreSQL integration.

## Task Overview

### Task 1: Vendr Scraper

* **Objective**: Scrape products from three specified categories on vendr.com.
* **Technologies**: `requests`, `lxml`, `psycopg2`.
* **Architecture**:

  * Multithreaded design: multiple worker threads scrape products, a dedicated writer thread inserts data into PostgreSQL.
  * Task queue for coordinating work between threads.
* **Collected Data**: Product name, category, price range, description.

### Task 2: Books to Scrape Scraper

* **Objective**: Scrape book details from books.toscrape.com.
* **Technologies**: Playwright, multiprocessing, PostgreSQL.
* **Architecture**:

  * Multiple scraper processes, each with its own Playwright browser instance.
  * Process manager to monitor and restart crashed processes.
  * Writer process for inserting results into PostgreSQL.
* **Collected Data**: Title, category, price, rating, availability, image URL, description, product information.

## How to Access Code

Switch to the respective branch to view the implementation of each task:

```bash
git checkout task1
# or
git checkout task2
```

## Environment Configuration

Both tasks use environment variables stored in a `.env` file. An `.env.example` file is provided in each branch as a template.

## Requirements

* Python 3.10+
* PostgreSQL
* Additional dependencies listed in `requirements.txt` of each task branch.

## Running the Tasks

Each task branch contains its own `README.md` file with detailed setup and execution instructions.

## License

This repository is provided for technical assessment purposes only.