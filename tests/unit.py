import unittest
from unittest.mock import patch, MagicMock
from src.db_service import *


class TestPhonebook(unittest.TestCase):

    def setUp(self):
        self.db_service = DbService(
            dbname="phonebook",
            user="user",
            password="password",
            host="localhost",
            port="5432"
        )

    # Проверка форматирования номера телефона
    def test_format_phone(self):
        phone = "89999999999"
        formatted_phone = format_phone(phone)
        self.assertEqual(formatted_phone, "+7(999)-999-99-99")

    # Проверка валидности генерируемого SQL на добавление записи
    @patch('src.db_service.psycopg2.connect')
    def test_add_record(self, mock_connect):
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur

        self.db_service.add_record("Тест", "89999999999", "Тест")

        mock_cur.execute.assert_called_with(
            "INSERT INTO phonebook (name, phone, comment) VALUES (%s, %s, %s)",
            ("Тест", "89999999999", "Тест")
        )

    # Проверка обработчика входных данных (имени) при добавлении записи
    def test_add_record_invalid_name_length(self):
        with patch('src.db_service.psycopg2.connect') as mock_connect:
            mock_conn = MagicMock()
            mock_cur = MagicMock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cur

            # Имя меньше 2 символов
            self.db_service.add_record("И", "89999999999", "Тест")
            mock_cur.execute.assert_not_called()

            # Имя больше 30 символов
            long_name = "ИванИванИванИванИванИванИванИванИванИван"
            self.db_service.add_record(long_name, "89999999999", "Тест")
            mock_cur.execute.assert_not_called()

    # Проверка обработчика входных данных (телефона) при добавлении записи
    def test_add_record_invalid_phone_length(self):
        with patch('src.db_service.psycopg2.connect') as mock_connect:
            mock_conn = MagicMock()
            mock_cur = MagicMock()
            mock_connect.return_value = mock_conn
            mock_conn.cursor.return_value = mock_cur

            # Номер с 10 символами
            self.db_service.add_record("Тест", "8999999999", "Тест")
            mock_cur.execute.assert_not_called()

            # Номер с 12 символами
            self.db_service.add_record("Тест", "899999999999", "Тест")
            mock_cur.execute.assert_not_called()

    # Проверка валидности генерируемого SQL на обновление записи
    @patch('src.db_service.psycopg2.connect')
    def test_update_number(self, mock_connect):
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur

        self.db_service.update_number("Тест", "81111111111")
        mock_cur.execute.assert_called_with(
            "UPDATE phonebook SET phone = %s WHERE name = %s", ("81111111111", "Тест")
        )

    # Проверка валидности генерируемого SQL на поиск записи (по имени)
    @patch('src.db_service.psycopg2.connect')
    def test_search_by_name(self, mock_connect):
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur

        mock_cur.fetchall.return_value = [("Тест", "89999999999", "Тест")]

        self.db_service.search_by_name("Тест")
        mock_cur.execute.assert_called_with("SELECT * FROM phonebook WHERE name = %s", ("Тест",))

    # Проверка валидности генерируемого SQL на поиск записи (по номеру телефона)
    @patch('src.db_service.psycopg2.connect')
    def test_search_by_number(self, mock_connect):
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur

        mock_cur.fetchall.return_value = [("Тест", "89999999999", "Тест")]

        self.db_service.search_by_number("999")
        mock_cur.execute.assert_called_with("SELECT * FROM phonebook WHERE phone LIKE %s", ('%999%',))

    # Проверка валидности генерируемого SQL на удаление записи
    @patch('src.db_service.psycopg2.connect')
    def test_delete_record(self, mock_connect):
        mock_conn = MagicMock()
        mock_cur = MagicMock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cur

        self.db_service.delete_record("Тест")

        mock_cur.execute.assert_called_with(
            "DELETE FROM phonebook WHERE name = %s", ("Тест",)
        )
