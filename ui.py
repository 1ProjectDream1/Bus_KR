import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from busPark import BusPark
from models import Bus
from readFile import readFile


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Автобусный парк")
        self.geometry("900x500")

        buttonGrip = ttk.Frame(self)
        buttonGrip.pack(side="top", fill="x", padx=5, pady=10)
        addBus = ttk.Button(buttonGrip, text="Добавить автобус", command=self.open_add_dialog)
        addBus.grid(column=0, row=0, padx=5, pady=5)

        departBus = ttk.Button(buttonGrip, text="Отправить на маршрут", command=self.open_depart_dialog)
        departBus.grid(column=1, row=0, padx=5, pady=5)

        arriveBus = ttk.Button(buttonGrip, text="Вернуть в парк", command=self.open_arrive_dialog)
        arriveBus.grid(column=2, row=0, padx=5, pady=5)

        self.sort_value = tk.IntVar(value=0)
        sortBoxDesc = ttk.Checkbutton(buttonGrip, text="Сортировка по убыванию", offvalue=0, variable=self.sort_value, onvalue= 1, command=self.handle_sorting)
        sortBoxDesc.grid(column=9, row= 0, padx=5, pady=5)
        sortBoxASC = ttk.Checkbutton(buttonGrip, text="Сортировка по возрастанию", offvalue=0, variable=self.sort_value, onvalue=2, command=self.handle_sorting)
        sortBoxASC.grid(column=10, row=0, padx=5, pady=5)

        self.park = BusPark()
        self._bild_ui()

    def open_add_dialog(self):
        number = simpledialog.askinteger("Новый автобус", "Введите номер")
        if number is None:
            return
        driver = simpledialog.askstring("Новый автобус", "Введите ФИО")
        if driver is None:
            return
        route = simpledialog.askstring("Новый автобус", "Введите маршрут")
        if route is None:
            return
        new_bus = Bus(number, driver, route)

        try:
            self.add_bus_list(new_bus)
            self.tree_park.insert("", "end", values=(new_bus.number, new_bus.driver, new_bus.route))
            messagebox.showinfo(f"Автобус добавлен с номером {new_bus.number}")
        except ValueError as e:
            messagebox.showerror(str(e))

    def open_depart_dialog(self):
        number = simpledialog.askinteger("Отправить на маршрут", "Номер маршрута")
        if number is None:
            return

        self.park.depart(int(number))
        depart_bus = self.park.out_park[int(number)]
        self.tree_route.insert("", "end", values=(depart_bus.number, depart_bus.driver, depart_bus.route))
        for i in self.tree_park.get_children():
            if (int(self.tree_park.item(i, "values")[0])) == int(number):
                self.tree_park.delete(i)
                break

    def add_bus_list(self, bus):
        self.park.add_bus(bus)

    def open_arrive_dialog(self):
        number = simpledialog.askinteger("Вернуть в парк", "Номер машрута")
        if number is None:
            return

        self.park.arrive(int(number))
        arrive_bus = self.park.in_park[int(number)]
        self.tree_park.insert("", "end", values=(arrive_bus.number, arrive_bus.driver, arrive_bus.route))
        for i in self.tree_route.get_children():
            if (int(self.tree_route.item(i, "values")[0])) == int(number):
                self.tree_route.delete(i)
                break


    def _bild_ui(self):
        tables = ttk.Frame(self)
        tables.pack(fill="both", expand=True)

        self.tree_park = self.on_park(tables, "В парке")
        self.tree_route = self.on_route(tables, "На маршруте")
        self.tree_park.master.pack(side="left", fill="both", expand=True, padx=5)
        self.tree_route.master.pack(side="left", fill="both", expand=True, padx=5)

    def on_park(self, parent, title):
        frame = ttk.LabelFrame(parent, text=title, padding=5)

        tree = ttk.Treeview(frame, columns=("number", "driver", "route"), show="headings", height=15)
        tree.heading("number", text="Номер автобуса")
        tree.heading("driver", text="ФИО водителя")
        tree.heading("route", text="Маршрут")
        file = readFile("inPark.json")
        for item in file:
            number = int(item["number"])
            driver = item["driver"]
            route = item["route"]
            tree.insert("", "end", values=(number, driver, route))
        tree.pack(fill="both", expand=True)
        return tree

    def on_route(self, parent, title):
        frame = ttk.LabelFrame(parent, text=title, padding=5)

        tree = ttk.Treeview(frame, columns=("number", "driver", "route"), show="headings", height=15)
        tree.heading("number", text="Номер автобуса")
        tree.heading("driver", text="ФИО водителя")
        tree.heading("route", text="Маршрут")

        file = readFile("inRoute.json")
        for item in file:
            number = int(item["number"])
            driver = item["driver"]
            route = item["route"]
            tree.insert("", "end", values=(number, driver, route))
            tree.pack(fill="both", expand=True)
        return tree

    def handle_sorting(self):
        state = self.sort_value.get()
        if state == 1:
            self.sort_asc()
        elif state == 2:
            self.sort_desc()

    def _resort_tree(self, tree, reverse):
        items = []
        for row_id in tree.get_children(""):
            values = tree.item(row_id, "values")
            bus_number = int(values[0])
            items.append((bus_number, row_id))

        items.sort(reverse=reverse)

        for index, (val, row_id) in enumerate(items):
            tree.move(row_id, "", index)

    def sort_asc(self):
        self._resort_tree(self.tree_park, reverse=False)
        self._resort_tree(self.tree_route, reverse=False)

    def sort_desc(self):
        self._resort_tree(self.tree_park, reverse=True)
        self._resort_tree(self.tree_route, reverse=True)
