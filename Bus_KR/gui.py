import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.park = None
        self.title("Автобусный парк")
        self.geometry("1200x600")
        self.sort_mode = tk.StringVar(value="number")
        self._bild_ui()

    def _bild_ui(self):
        menuBar = tk.Menu(self)
        filemenu = tk.Menu(menuBar, tearoff=0)
        filemenu.add_command(label="Загрузка", command=self.load_file)
        filemenu.add_command(label="Сохранение", command=self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label="Выход", command=self.destroy)
        menuBar.add_cascade(label="Файл", menu=filemenu)
        self.config(menu=menuBar)

        top = ttk.Frame(self, padding=10)
        top.pack(fill="x")
        ttk.Button(top, text="Добавить автобус", command=self.add_bus).pack(side="left")
        ttk.Button(top, text="Выезд на маршрут", command=self.depart).pack(side="left", padx=5)
        ttk.Button(top, text="Въезд в парк", command=self.arrive).pack(side="left", padx=5)

        ttk.Label(top, text="Сортировка:").pack(side="left", padx=(20, 5))
        ttk.Radiobutton(top, text="По номеру", variable=self.sort_mode,
                        value="number", command=self._refresh).pack(side="left")
        ttk.Radiobutton(top, text="По маршруту", variable=self.sort_mode,
                        value="route", command=self._refresh).pack(side="left")

        tables = ttk.Frame(self, padding=10)
        tables.pack(fill="both", expand=True)

        self.tree_park = self._make_tree(tables, "В парке")
        self.tree_route = self._make_tree(tables, "На маршруте")
        self.tree_park.master.pack(side="left", fill="both", expand=True, padx=5)
        self.tree_route.master.pack(side="left", fill="both", expand=True, padx=5)

    def _make_tree(self, parent, title):
        frame = ttk.LabelFrame(parent, text=title, padding=5)
        tree = ttk.Treeview(frame, columns=("num", "driver", "route"),
                            show="headings", height=15)
        for col, txt, w in (("num", "Номер", 70),
                            ("driver", "Водитель", 200),
                            ("route", "Маршрут", 80)):
            tree.heading(col, text=txt)
            tree.column(col, width=w)
        tree.pack(fill="both", expand=True)
        return tree

    def _refresh(self):
        for tree in (self.tree_park, self.tree_route):
            tree.delete(*tree.get_children())

        if self.sort_mode.get() == "number":
            in_park, on_route = self.park.sorted_by_number()
        else:
            in_park, on_route = self.park.sorted_by_route()

        for bus in in_park:
            self.tree_park.insert("", "end", values=(bus.number, bus.driver, bus.route))
        for bus in on_route:
            self.tree_route.insert("", "end", values=(bus.number, bus.driver, bus.route))
    def add_bus(self):
        num = simpledialog.askinteger("Новый автобус", "Номер автобуса:")
        if num is None:
            driver = simpledialog.askinteger("Новый автобус", "ФИО водителя:")
        if driver is None:
            route = simpledialog.askinteger("Новый автобус", "Номер маршрута:")
        if route is None:
            return
        try:
            self.park.add_bus(Bus(num, driver, route))
            self._refresh()
        except Exception as e:
            messagebox.showerror(e)

    def depart(self):
        pass
    def arrive(self):
        pass

    def load_file(self):
        file = filedialog.askopenfilename(filetypes=[("Text", "*.txt"), ("All", "*.")])
        if not file:
            return
        try:
            self.park.load_from_file(file)
            self._refresh()
        except Exception as ex:
            messagebox.showerror("Ошибка", str(ex))



    def save_file(self):
        pass

