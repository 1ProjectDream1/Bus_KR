class Bus:
    def __init__(self, number, driver, route):
        self.number = number
        self.driver = driver
        self.route = route
    def __str__(self):
        return f"№{self.number} | ФИО {self.driver} | маршрут {self.route}"
