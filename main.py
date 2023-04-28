
from datetime import datetime


class Person(object):
    def __init__(self, first_name, second_name):
        self._first_name = first_name
        self._second_name = second_name

    def buy_ticket(self, amount):
        pass

    def __str__(self):
        return f"First name: {self._first_name}, Second name: {self._second_name}"


class Employee(Person):
    def __init__(self, first_name, second_name):
        super().__init__(first_name=first_name, second_name=second_name)


class Passenger(Person):
    def __init__(self,  first_name, second_name):
        super().__init__(first_name=first_name, second_name=second_name)


class Ticket:
    def __init__(self, ticket_id, flight_id, seat_id):
        self.ticket_id = ticket_id
        self.flight_id = flight_id
        self.seat_id = seat_id


class Purchase:
    def __init__(self, customer, flight, date):
        self.customer = customer
        self.flight = flight
        self.date = date


class Flight:
    pass


class Plane:
    pass


class Lotnisko:
    pass


if __name__ == "__main__":
    jan = Employee("Jan", "Kowalski")
    jozef = Passenger("Jozef", "Mackowiak")
    print(jan)
    print(jozef)