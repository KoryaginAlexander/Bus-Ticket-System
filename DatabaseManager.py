import sqlite3

class DatabaseManager:
    def __init__(self):
        self.connection = sqlite3.connect('bus_tickets.db')
        self.cursor = self.connection.cursor()
        self.create_routes_table()

    def create_routes_table(self):
        """
        Создание таблицы routes, если она не существует.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS routes (
                route_number INTEGER PRIMARY KEY,
                route_name TEXT,
                driver TEXT,
                bus_type TEXT,
                departure_time TEXT,
                price INTEGER,
                seats_available INTEGER
            )
        ''')
        self.connection.commit()

    def add_route(self, route_number, route_name, driver, bus_type, departure_time, price, seats_available):
        """
        Добавление нового маршрута в базу данных.
        """
        # Проверка на наличие маршрута с таким номером
        self.cursor.execute("SELECT COUNT(*) FROM routes WHERE route_number = ?", (route_number,))
        if self.cursor.fetchone()[0] > 0:
            print(f"Маршрут с номером {route_number} уже существует!")
            return

        # Добавление нового маршрута
        self.cursor.execute('''INSERT INTO routes (route_number, route_name, driver, bus_type, departure_time, price, seats_available)
                               VALUES (?, ?, ?, ?, ?, ?, ?)''', 
                            (route_number, route_name, driver, bus_type, departure_time, price, seats_available))
        self.connection.commit()
        print(f"Маршрут с номером {route_number} успешно добавлен.")

    def get_all_routes(self):
        """
        Получение всех маршрутов из базы данных.
        """
        self.cursor.execute("SELECT * FROM routes")
        routes = self.cursor.fetchall()
        return routes

    def search_routes(self, max_price=None, seats_required=1, departure_time=None):
        """
        Поиск рейсов по заданным критериям (максимальная цена, минимальное количество мест, время отправления).
        """
        query = "SELECT * FROM routes WHERE 1=1"
        params = []

        if max_price is not None:
            query += " AND price <= ?"
            params.append(max_price)
        
        if seats_required > 0:
            query += " AND seats_available >= ?"
            params.append(seats_required)
        
        if departure_time is not None:
            query += " AND departure_time >= ?"
            params.append(departure_time)

        self.cursor.execute(query, tuple(params))
        found_routes = self.cursor.fetchall()
        return found_routes

    def book_ticket(self, route_number, seats_requested):
        """
        Бронирование билетов на указанный рейс.
        """
        # Проверяем, существует ли маршрут с указанным номером
        self.cursor.execute("SELECT seats_available FROM routes WHERE route_number = ?", (route_number,))
        route = self.cursor.fetchone()

        if route:
            seats_available = route[0]
            if seats_available >= seats_requested:
                # Обновляем количество свободных мест
                new_seats = seats_available - seats_requested
                self.cursor.execute("UPDATE routes SET seats_available = ? WHERE route_number = ?", 
                                    (new_seats, route_number))
                self.connection.commit()
                print(f"Успешное бронирование {seats_requested} мест на рейс {route_number}.")
            else:
                print(f"Недостаточно мест на рейс {route_number}. Доступно всего {seats_available} мест.")
        else:
            print(f"Рейс с номером {route_number} не найден.")

    def __del__(self):
        """
        Закрытие соединения с базой данных при удалении объекта.
        """
        if hasattr(self, 'connection'):
            self.connection.close()
            print("Соединение с базой данных закрыто.")