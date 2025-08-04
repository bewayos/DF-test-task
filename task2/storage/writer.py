import psycopg2
import multiprocessing
from data_models.book import Book
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


class WriterProcess(multiprocessing.Process):
    """
    WriterProcess reads Book objects from results_queue and inserts them into PostgreSQL.
    """

    def __init__(self, results_queue: multiprocessing.Queue):
        super().__init__()
        self.results_queue = results_queue

    def run(self):
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        conn.autocommit = False
        cursor = conn.cursor()

        while True:
            try:
                book = self.results_queue.get(timeout=10)
                print(f"[WriterProcess] Writing to DB: {book.title}")
                self.insert_book(cursor, book)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print(f"[WriterProcess] Error inserting book: {e}")


    def insert_book(self, cursor, book: Book):
        cursor.execute("""
            INSERT INTO books (
                title, price, rating, availability, image_url,
                description, category, upc, product_type,
                price_excl_tax, price_incl_tax, tax, num_reviews
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (upc) DO NOTHING;
        """, (
            book.title,
            book.price,
            book.rating,
            book.availability,
            book.image_url,
            book.description,
            book.category,
            book.upc,
            book.product_type,
            book.price_excl_tax,
            book.price_incl_tax,
            book.tax,
            book.num_reviews,
        ))
