class BusTicketSystem:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def show_routes(self):
        """
        Отображение всех доступных рейсов.
        """
        routes = self.db_manager.get_all_routes()
        if not routes:
            print("Нет доступных рейсов.")
        else:
            for route in routes:
                print(f"Рейс {route[0]}: {route[1]} | Водитель: {route[2]} | "
                      f"Автобус: {route[3]} | Время отправления: {route[4]} | "
                      f"Цена: {route[5]} | Свободные места: {route[6]}")

    def search_route(self, max_price=None, seats_required=1, departure_time=None):
        """
        Поиск подходящих рейсов по критериям.
        """
        found_routes = self.db_manager.search_routes(max_price, seats_required, departure_time)

        if not found_routes:
            print("Нет подходящих рейсов по заданным критериям.")
        else:
            print("Найденные рейсы:")
            for route in found_routes:
                print(f"Рейс {route[0]}: {route[1]} | Водитель: {route[2]} | "
                      f"Автобус: {route[3]} | Время отправления: {route[4]} | "
                      f"Цена: {route[5]} | Свободные места: {route[6]}")

    def book_ticket(self, route_number, seats_requested):
        """Бронирование билетов на указанный рейс."""
        if self.db_manager.book_ticket(route_number, seats_requested):
            print(f"Успешное бронирование {seats_requested} мест на рейс {route_number}.")
        else:
            print("Недостаточно мест или рейс не найден.")
            
   