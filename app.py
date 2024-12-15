import streamlit as st
from DatabaseManager import DatabaseManager
from BusTicketSystem import BusTicketSystem
import datetime

# Инициализация базы данных и системы
db_manager = DatabaseManager()
system = BusTicketSystem(db_manager)

def show_available_routes():
    """
    Отображение всех доступных маршрутов в Streamlit.
    """
    routes = db_manager.get_all_routes()
    if routes:
        for route in routes:
            st.write(f"**Рейс {route[0]}**: {route[1]} | Водитель: {route[2]} | Автобус: {route[3]} | "
                     f"Время отправления: {route[4]} | Цена: {route[5]} | Свободные места: {route[6]}")
    else:
        st.write("Нет доступных рейсов.")

def search_routes():
    """
    Поиск рейсов по введенным данным.
    """
    st.title("Поиск рейсов")
    max_price = st.number_input("Максимальная цена билета:", min_value=0, step=100, value=2000)
    seats_required = st.number_input("Минимальное количество мест:", min_value=1, step=1, value=1)
    departure_time = st.date_input("Дата отправления (по умолчанию все):", value=datetime.date.today())

    if st.button("Поиск рейсов"):
        found_routes = db_manager.search_routes(max_price=max_price, seats_required=seats_required, departure_time=str(departure_time))
        if found_routes:
            for route in found_routes:
                st.write(f"**Рейс {route[0]}**: {route[1]} | Водитель: {route[2]} | Автобус: {route[3]} | "
                         f"Время отправления: {route[4]} | Цена: {route[5]} | Свободные места: {route[6]}")
        else:
            st.write("Нет подходящих рейсов.")

def book_ticket_interface():
    """
    Интерфейс для бронирования билетов.
    """
    st.title("Бронирование билетов")
    route_number = st.number_input("Номер рейса:", min_value=1, step=1)
    seats_requested = st.number_input("Количество мест:", min_value=1, step=1)

    if st.button("Забронировать"):
        system.book_ticket(route_number, seats_requested)
        st.write(f"Вы забронировали {seats_requested} мест(а) на рейс {route_number}.")

def add_route_interface():
    """
    Интерфейс для добавления новых рейсов.
    """
    st.title("Добавление нового рейса")
    route_number = st.number_input("Номер рейса:", min_value=1, step=1)
    route_name = st.text_input("Название маршрута:")
    driver = st.text_input("Водитель:")
    bus_type = st.selectbox("Тип автобуса:", ["Люкс", "Комфорт", "Эконом"])
    departure_time = st.text_input("Дата и время отправления (формат: ГГГГ-ММ-ДД ЧЧ:ММ):", value="2024-12-20 08:00")
    price = st.number_input("Цена билета:", min_value=1, step=100)
    seats_available = st.number_input("Количество мест:", min_value=1, step=1)

    if st.button("Добавить маршрут"):
        system.db_manager.add_route(route_number, route_name, driver, bus_type, departure_time, price, seats_available)
        st.write(f"Маршрут {route_number} успешно добавлен.")

def main():
    st.sidebar.title("Меню")
    options = st.sidebar.selectbox("Выберите действие", ["Просмотр всех рейсов", "Поиск рейсов", "Бронирование билетов", "Добавить рейс"])

    if options == "Просмотр всех рейсов":
        show_available_routes()
    elif options == "Поиск рейсов":
        search_routes()
    elif options == "Бронирование билетов":
        book_ticket_interface()
    elif options == "Добавить рейс":
        add_route_interface()

if __name__ == "__main__":
    main()
    
 # Нужно объеденить поиск и бронь в одну опцию
    # Не рабоатет бронь 
    # Корочь поменять базу 
    # И можно лучше сделать просмотр всех рейсов 