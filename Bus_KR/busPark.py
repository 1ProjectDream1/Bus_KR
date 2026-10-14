from models import Bus
from readFile import readFile, wrete_json

class BusPark:
    def __init__(self):
        self.in_park = {}
        self.out_park = {}
        self.load_data()

    def load_data(self):
        data = readFile("inPark.json")
        try:
            for item in data:
                number = int(item["number"])
                if number not in self.in_park:
                    self.in_park[number] = Bus(number, item['driver'], item['route'])
        except Exception:
            pass

        data = readFile("inRoute.json")
        try:
            if data:
                for item in data:
                    number = int(item["number"])
                    if number not in self.out_park:
                        self.out_park[number] = Bus(number, item["driver"], item["route"])
        except Exception:
            pass


    def add_bus(self, bus):
        if bus.number in self.in_park or bus.number in self.out_park:
            raise ValueError(f"Автобус с номером {bus.number} уже находится в парке!")
        else:
            if len(self.in_park) == 0:
                self.load_data()
            self.in_park[bus.number] = bus
            read_in_park_json = [item.__dict__ for item in self.in_park.values()]
            #read_in_park_json.sort(key=lambda x: x[bus.number])
            self.save_state(read_in_park_json, True)

    def depart(self, number):
        if number not in self.in_park:
            raise ValueError(f"Автобус с номером {number} находится не в парке!")
        else:
            bus_object = self.in_park.pop(number)
            self.out_park[number] = bus_object

            read_in_park_json = [item.__dict__ for item in self.in_park.values()]
            read_in_park_json.sort(key=lambda x: x["number"])
            self.save_state(read_in_park_json, True)

            read_in_route_json = [item.__dict__ for item in self.out_park.values()]
            read_in_route_json.sort(key=lambda x: x["number"])
            self.save_state(read_in_route_json, False)

    def arrive(self, number):
        if number not in self.out_park:
            raise ValueError(f"Автобус с номером {number} находится не на маршруте!")
        else:
            bus_object = self.out_park.pop(number)
            self.in_park[number] = bus_object

            read_in_park_json = [item.__dict__ for item in self.in_park.values()]
            read_in_park_json.sort(key=lambda x: x["number"])
            self.save_state(read_in_park_json, True)

            read_in_route_json = [item.__dict__ for item in self.out_park.values()]
            read_in_route_json.sort(key = lambda x: x["number"])
            self.save_state(read_in_route_json, False)

    def save_state(self, data, flag):
        if flag:
            wrete_json("inPark.json", data)
        else:
            wrete_json("inRoute.json", data)


if __name__ == "__main__":
    busPark = BusPark()




