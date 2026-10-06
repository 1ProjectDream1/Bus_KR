from models import Bus
from readFile import readFile

class BusPark:
    def __init__(self):
        self.in_park = {}
        self.out_park = {}

    def add_bus(self, bus):
        all_bus = []
        for inP in self.in_park.keys():
            all_bus.append(inP)
        for inR in self.out_park.keys():
            all_bus.append(inR)

        if bus.number in all_bus:
            raise ValueError(f"Автобус с номером {bus.number} уже находится в парке!")
        else:
            self.in_park[bus.number] = bus

    def add_route(self, bus):
        if bus.number in self.in_park:
            busNumber = self.in_park.pop(bus.number)
            self.out_park[bus.number] = busNumber
        elif bus.number in self.out_park:
            raise ValueError(f"Автобус с таким номером {bus.number} уже на маршруте!")
        else:
            self.out_park[bus.number] = bus

if __name__ == "__main__":
    busPark = BusPark()

    file = readFile()
    for key in file:
        numder = key["number"]
        driver = key["driver"]
        route = key["route"]
        bus = Bus(numder, driver, route)
        busPark.add_bus(bus)



