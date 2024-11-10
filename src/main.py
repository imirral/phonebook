from db_service import DbService


def main():
    print("Добро пожаловать в телефонную книгу!")

    # Экземпляр DbService с параметрами для подключения
    db_service = DbService(
        dbname="phonebook",
        host="localhost",
        user="postgres",
        password="postgres",
        port="5432"
    )

    table = 'phonebook'

    while True:
        try:
            print("Используйте команды: add, delete, update, search_by_name, search_by_number, exit")
            command = input("Введите команду: ").strip().lower()

            if command == "add":
                name = input("Введите имя: ")
                phone = input("Введите номер: ")
                comment = input("Введите комментарий: ")
                db_service.add_record(table, name, phone, comment)

            elif command == "delete":
                name = input("Введите имя для удаления: ")
                db_service.delete_record(table, name)

            elif command == "update":
                name = input("Введите имя для обновления: ")
                new_phone = input("Введите новый номер: ")
                db_service.update_number(table, name, new_phone)

            elif command == "search_by_name":
                name = input("Введите имя для поиска: ")
                db_service.search_by_name(table, name)

            elif command == "search_by_number":
                partial_number = input("Введите часть номера для поиска: ")
                db_service.search_by_number(table, partial_number)

            elif command == "exit":
                print("Выход из программы.")
                break

            else:
                print("Неизвестная команда. Попробуйте снова.")

        except Exception as e:
            print(f"Произошла ошибка: {e}")
            break


if __name__ == "__main__":
    main()
