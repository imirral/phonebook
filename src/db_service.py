import psycopg2


def format_phone(phone):
    return f"+7({phone[1:4]})-{phone[4:7]}-{phone[7:9]}-{phone[9:11]}"


class DbService:

    def __init__(self, dbname, host, user, password, port):
        self.db_params = {
            'dbname': dbname,
            'host': host,
            'user': user,
            'password': password,
            'port': port
        }

    def connect_db(self):
        return psycopg2.connect(**self.db_params)

    # Добавление записи
    def add_record(self, name, phone, comment):
        if not phone.isdigit() or len(phone) != 11:
            print("Неверный формат номера телефона.")
            return
        if not (2 <= len(name) <= 30):
            print("Имя должно содержать от 2 до 30 символов.")
            return

        try:
            conn = self.connect_db()
            cur = conn.cursor()
            cur.execute("INSERT INTO phonebook (name, phone, comment) VALUES (%s, %s, %s)", (name, phone, comment))
            conn.commit()
            print("Запись добавлена!")
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            cur.close()
            conn.close()

    # Удаление записи (по имени)
    def delete_record(self, name):
        try:
            conn = self.connect_db()
            cur = conn.cursor()
            cur.execute("DELETE FROM phonebook WHERE name = %s", (name,))
            conn.commit()
            print("Запись удалена!")
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            cur.close()
            conn.close()

    # Обновление записи (номера телефона по имени)
    def update_number(self, name, new_phone):
        if not new_phone.isdigit() or len(new_phone) != 11:
            print("Неверный формат номера телефона.")
            return

        try:
            conn = self.connect_db()
            cur = conn.cursor()
            cur.execute("UPDATE phonebook SET phone = %s WHERE name = %s", (new_phone, name))
            conn.commit()
            print("Номер обновлён!")
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            cur.close()
            conn.close()

    # Поиск записи (по имени)
    def search_by_name(self, name):
        try:
            conn = self.connect_db()
            cur = conn.cursor()
            cur.execute("SELECT * FROM phonebook WHERE name = %s", (name,))
            records = cur.fetchall()
            for record in records:
                print(record[1], format_phone(record[2]), record[3])
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            cur.close()
            conn.close()

    # Поиск записи (по номеру телефона / части номера телефона)
    def search_by_number(self, partial_number):
        try:
            conn = self.connect_db()
            cur = conn.cursor()
            cur.execute("SELECT * FROM phonebook WHERE phone LIKE %s", ('%' + partial_number + '%',))
            records = cur.fetchall()
            for record in records:
                print(record[1], format_phone(record[2]), record[3])
        except Exception as e:
            print(f"Ошибка: {e}")
        finally:
            cur.close()
            conn.close()