import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from busPark import BusPark
from models import Bus
from readFile import readFile


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Автобусный парк")
        self.geometry("500x500")

        self.park = BusPark()
        self._bild_ui()

    def _bild_ui(self):
        tables = ttk.Frame(self)
        tables.pack(fill="both", expand=True)
        self.tree_park = self._make_tree(tables, "В парке")
        self.tree_route = self._make_tree(tables, "На маршруте")
        self.tree_park.master.pack(side="left", fill="both", expand=True, padx=5)
        self.tree_route.master.pack(side="left", fill="both", expand=True, padx=5)

    def _make_tree(self, parent, title):
        frame = ttk.LabelFrame(parent, text=title, padding=5)

        tree = ttk.Treeview(frame, columns=("number", "driver", "route"), show="headings", height=15)
        tree.heading("number", text="Номер автобуса")
        tree.heading("driver", text="ФИО водителя")
        tree.heading("route", text="Маршрут")
        file = readFile()
        for item in file:
            number = int(item["number"])
            driver = item["driver"]
            route = item["route"]
            tree.insert("", "end", values=(number, driver, route))
        tree.pack(fill="both", expand=True)
        return tree
