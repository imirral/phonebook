import unittest
import psycopg2
from src.db_service import DbService


class TestPhonebookIntegration(unittest.TestCase):

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

    # Проверка добавления записи
    def test_add_record(self):
        self.db_service.add_record("Иван", "89999999999", "Друг")
        self.cur.execute("SELECT name, phone FROM phonebook WHERE name = %s", ("Иван",))
        result = self.cur.fetchone()
        self.assertIsNotNone(result)
        self.assertEqual(result[1], "89999999999")

    # Проверка обновления записи
    def test_update_number(self):
        self.db_service.add_record("Мария", "92222222222", "Знакомая")
        self.db_service.update_number("Мария", "93333333333")
        self.cur.execute("SELECT phone FROM phonebook WHERE name = %s", ("Мария",))
        result = self.cur.fetchone()
        self.assertEqual(result[0], "93333333333")

    # Проверка удаления записи
    def test_delete_record(self):
        self.db_service.add_record("Василий", "91111111111", "Коллега")
        self.db_service.delete_record("Василий")
        self.cur.execute("SELECT name FROM phonebook WHERE name = %s", ("Василий",))
        result = self.cur.fetchone()
        self.assertIsNone(result)

