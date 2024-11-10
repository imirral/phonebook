import unittest
import psycopg2
from src.db_service import DbService


class TestPhonebookIntegration(unittest.TestCase):

    table = 'phonebook_test'

    def setUp(self):
        self.db_service = DbService(
            dbname="phonebook",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        self.conn = psycopg2.connect(
            dbname="phonebook",
            user="postgres",
            password="postgres",
            host="localhost",
            port="5432"
        )
        self.cur = self.conn.cursor()
        self.cur.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.table} (
                id SERIAL PRIMARY KEY,
                name VARCHAR(30),
                phone VARCHAR(11),
                comment TEXT
            );
            """
        )
        self.conn.commit()

    def tearDown(self):
        self.cur.execute(f"DROP TABLE {self.table};")
        self.conn.commit()
        self.cur.close()
        self.conn.close()

    # Проверка добавления записи
    def test_add_record(self):
        self.db_service.add_record(self.table, "Иван", "89999999999", "Друг")
        self.cur.execute(f"SELECT name, phone FROM {self.table} WHERE name = %s", ("Иван",))
        result = self.cur.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "89999999999")

    # Проверка обновления записи
    def test_update_number(self):
        self.db_service.add_record(self.table, "Мария", "92222222222", "Знакомая")
        self.db_service.update_number(self.table, "Мария", "93333333333")
        self.cur.execute(f"SELECT phone FROM {self.table} WHERE name = %s", ("Мария",))
        result = self.cur.fetchone()
        self.assertEqual(result[0], "93333333333")

    # Проверка удаления записи
    def test_delete_record(self):
        self.db_service.add_record(self.table, "Василий", "91111111111", "Коллега")
        self.db_service.delete_record(self.table, "Василий")
        self.cur.execute(f"SELECT name FROM {self.table} WHERE name = %s", ("Василий",))
        result = self.cur.fetchone()
        self.assertIsNone(result)

