import psycopg2
import logging
from psycopg2 import OperationalError, IntegrityError
from task1.scraper.models import Product
from task1.config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD


class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None
        try:
            self.conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
            )
            self.conn.autocommit = False
            self.cursor = self.conn.cursor()
            logging.info("[Database] Connected successfully.")
        except OperationalError as e:
            logging.error(f"[Database] Connection failed: {e}")
            raise
        except Exception as e:
            logging.error(f"[Database] Unexpected error during connection: {e}")
            raise

    def insert_product(self, product: Product):
        if not self.conn or not self.cursor:
            logging.error("[Database] No active connection")
            return
            
        try:
            query = """
                INSERT INTO products (name, category, median_price, price_range, description, url)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (url) DO NOTHING;
            """
            self.cursor.execute(query, (
                product.name,
                product.category,
                product.median_price,
                product.price_range,
                product.description,
                product.url
            ))
            self.conn.commit()
            logging.debug(f"[Database] Successfully inserted product: {product.name}")
        except IntegrityError as e:
            self.conn.rollback()
            logging.warning(f"[Database] Integrity error for product {product.name}: {e}")
        except Exception as e:
            self.conn.rollback()
            logging.error(f"[Database] Insert failed for product {product.name}: {e}")
            raise

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
            logging.info("[Database] Connection closed successfully.")
        except Exception as e:
            logging.error(f"[Database] Error closing connection: {e}")
