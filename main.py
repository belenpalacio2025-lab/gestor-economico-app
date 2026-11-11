from datetime import datetime, date
from pathlib import Path
import sqlite3

from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.label import Label

DB_PATH = Path(__file__).parent / "gestor.db"

KV = r"""
#:import dp kivy.metrics.dp

<MainButton@Button>:
    size_hint_y: None
    height: dp(54)
    font_size: '17sp'
    background_normal: ''
    background_color: (0.10, 0.40, 0.82, 1)
    color: (1, 1, 1, 1)

<SecondaryButton@Button>:
    size_hint_y: None
    height: dp(48)
    font_size: '16sp'
    background_normal: ''
    background_color: (0.90, 0.93, 0.97, 1)
    color: (0.10, 0.18, 0.28, 1)

<MainScreen>:
    name: 'home'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(18)
        spacing: dp(12)
        canvas.before:
            Color:
                rgba: (0.95, 0.96, 0.98, 1)
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            text: 'GESTOR ECONÓMICO'
            size_hint_y: None
            height: dp(35)
            color: (0.08, 0.22, 0.40, 1)
            bold: True
            font_size: '20sp'
        Label:
            text: 'Resumen de hoy'
            size_hint_y: None
            height: dp(28)
            color: (0.25, 0.30, 0.38, 1)
            font_size: '16sp'
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(112)
            padding: dp(14)
            canvas.before:
                Color:
                    rgba: (0.10, 0.40, 0.82, 1)
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(14)]
            Label:
                text: 'GANANCIA DEL DÍA'
                color: (0.85, 0.91, 1, 1)
                font_size: '13sp'
            Label:
                id: profit
                text: '$U 0,00'
                color: (1, 1, 1, 1)
                bold: True
                font_size: '29sp'
        GridLayout:
            cols: 2
            spacing: dp(10)
            size_hint_y: None
            height: dp(112)
            BoxLayout:
                orientation: 'vertical'
                padding: dp(10)
                canvas.before:
                    Color:
                        rgba: (1, 1, 1, 1)
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [dp(12)]
                Label:
                    text: 'VENTAS'
                    color: (0.35, 0.40, 0.48, 1)
                Label:
                    id: sales_total
                    text: '$U 0,00'
                    color: (0.05, 0.48, 0.25, 1)
                    bold: True
                    font_size: '21sp'
            BoxLayout:
                orientation: 'vertical'
                padding: dp(10)
                canvas.before:
                    Color:
                        rgba: (1, 1, 1, 1)
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [dp(12)]
                Label:
                    text: 'GASTOS'
                    color: (0.35, 0.40, 0.48, 1)
                Label:
                    id: expenses_total
                    text: '$U 0,00'
                    color: (0.75, 0.22, 0.18, 1)
                    bold: True
                    font_size: '21sp'
        MainButton:
            text: '+ Registrar venta'
            on_release: app.root.current = 'sale'
        MainButton:
            text: '+ Registrar gasto'
            background_color: (0.12, 0.55, 0.36, 1)
            on_release: app.root.current = 'expense'
        SecondaryButton:
            text: 'Ver historial'
            on_release: app.root.current = 'history'
        Widget:
        Label:
            text: 'Tus datos quedan guardados en este celular.'
            size_hint_y: None
            height: dp(24)
            color: (0.45, 0.49, 0.55, 1)
            font_size: '12sp'

<FormScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: dp(18)
        spacing: dp(12)
        canvas.before:
            Color:
                rgba: (0.95, 0.96, 0.98, 1)
            Rectangle:
                pos: self.pos
                size: self.size
        Label:
            id: form_title
            text: 'Registrar'
            size_hint_y: None
            height: dp(42)
            color: (0.08, 0.22, 0.40, 1)
            bold: True
            font_size: '21sp'
        Label:
            id: first_label
            text: 'Producto'
            size_hint_y: None
            height: dp(25)
            color: (0.18, 0.23, 0.30, 1)
            halign: 'left'
            text_size: self.size
        TextInput:
            id: description
            hint_text: 'Ej.: Hamburguesa'
            multiline: False
            size_hint_y: None
            height: dp(52)
            font_size: '17sp'
        Label:
            text: 'Cantidad' if root.name == 'sale' else 'Importe ($U)'
            size_hint_y: None
            height: dp(25)
            color: (0.18, 0.23, 0.30, 1)
            halign: 'left'
            text_size: self.size
        TextInput:
            id: quantity
            hint_text: 'Ej.: 2'
            multiline: False
            input_filter: 'int' if root.name == 'sale' else 'float'
            size_hint_y: None
            height: dp(52)
            font_size: '17sp'
        Label:
            id: price_label
            text: 'Precio unitario ($U)'
            size_hint_y: None
            height: dp(25)
            color: (0.18, 0.23, 0.30, 1)
            halign: 'left'
            text_size: self.size
        TextInput:
            id: price
            hint_text: 'Ej.: 250'
            multiline: False
            input_filter: 'float'
            size_hint_y: None
            height: dp(52)
            font_size: '17sp'
        MainButton:
            text: 'Guardar'
            on_release: root.save_record()
        SecondaryButton:
            text: 'Volver al inicio'
            on_release: app.root.current = 'home'
        Widget:

<HistoryScreen>:
    name: 'history'
    BoxLayout:
        orientation: 'vertical'
        padding: dp(16)
        spacing: dp(8)
        Label:
            text: 'Historial de movimientos'
            size_hint_y: None
            height: dp(42)
            color: (0.08, 0.22, 0.40, 1)
            bold: True
            font_size: '20sp'
        ScrollView:
            do_scroll_x: False
            GridLayout:
                id: history_list
                cols: 1
                spacing: dp(7)
                size_hint_y: None
                height: self.minimum_height
        SecondaryButton:
            text: 'Volver al inicio'
            on_release: app.root.current = 'home'
"""

class Database:
    def __init__(self, path):
        self.conn = sqlite3.connect(str(path))
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                kind TEXT NOT NULL,
                description TEXT NOT NULL,
                quantity REAL NOT NULL,
                unit_price REAL NOT NULL,
                total REAL NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        self.conn.commit()

    def add(self, kind, description, quantity, unit_price):
        total = quantity * unit_price
        self.conn.execute(
            "INSERT INTO movements(kind, description, quantity, unit_price, total, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (kind, description, quantity, unit_price, total, datetime.now().isoformat(timespec="minutes"))
        )
        self.conn.commit()

    def totals_today(self):
        today = date.today().isoformat()
        row = self.conn.execute("""
            SELECT
                COALESCE(SUM(CASE WHEN kind='venta' THEN total ELSE 0 END), 0),
                COALESCE(SUM(CASE WHEN kind='gasto' THEN total ELSE 0 END), 0)
            FROM movements WHERE substr(created_at, 1, 10)=?
        """, (today,)).fetchone()
        return row[0], row[1]

    def history(self):
        return self.conn.execute(
            "SELECT kind, description, quantity, unit_price, total, created_at FROM movements ORDER BY id DESC LIMIT 200"
        ).fetchall()


def money(value):
    return "$U " + f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


class MainScreen(Screen):
    pass

class FormScreen(Screen):
    def on_pre_enter(self):
        is_sale = self.name == "sale"
        self.ids.form_title.text = "Registrar venta" if is_sale else "Registrar gasto"
        self.ids.first_label.text = "Producto vendido" if is_sale else "Descripción del gasto"
        self.ids.description.hint_text = "Ej.: Hamburguesa" if is_sale else "Ej.: Compra de verduras"
        self.ids.quantity.hint_text = "Ej.: 2 unidades" if is_sale else "Dejar en 1"
        self.ids.price_label.text = "Precio por unidad ($U)" if is_sale else "Importe ($U)"
        self.ids.price.hint_text = "Ej.: 250"
        self.ids.quantity.text = "1" if not is_sale else ""
        self.ids.description.text = ""
        self.ids.price.text = ""

    def save_record(self):
        desc = self.ids.description.text.strip()
        q_text = self.ids.quantity.text.strip()
        p_text = self.ids.price.text.strip().replace(",", ".")
        if not desc or not q_text or not p_text:
            show_message("Completá todos los campos.")
            return
        try:
            quantity = float(q_text)
            price = float(p_text)
            if quantity <= 0 or price <= 0:
                raise ValueError
        except ValueError:
            show_message("Ingresá una cantidad y un importe mayores que cero.")
            return

        kind = "venta" if self.name == "sale" else "gasto"
        App.get_running_app().db.add(kind, desc, quantity, price)
        show_message("Movimiento guardado correctamente.")
        self.manager.current = "home"


class HistoryScreen(Screen):
    def on_pre_enter(self):
        layout = self.ids.history_list
        layout.clear_widgets()
        rows = App.get_running_app().db.history()
        if not rows:
            layout.add_widget(Label(text="Todavía no hay movimientos.", size_hint_y=None, height=dp(50), color=(0.25,0.3,0.38,1)))
            return
        for kind, desc, qty, unit, total, created in rows:
            sign = "+" if kind == "venta" else "-"
            color = (0.05, 0.48, 0.25, 1) if kind == "venta" else (0.75, 0.22, 0.18, 1)
            item = Label(
                text=f"[b]{'VENTA' if kind == 'venta' else 'GASTO'}[/b] · {desc}\n{qty:g} x {money(unit)}   [b]{sign}{money(total)}[/b]\n{created.replace('T', ' ')}",
                markup=True, size_hint_y=None, height=dp(82), halign="left", valign="middle",
                color=color
            )
            item.text_size = (None, None)
            layout.add_widget(item)


def show_message(message):
    Popup(title="Gestor Económico", content=Label(text=message), size_hint=(0.82, 0.28)).open()


class GestorApp(App):
    def build(self):
        self.title = "Gestor Económico Digital"
        self.db = Database(DB_PATH)
        Builder.load_string(KV)
        manager = ScreenManager()
        manager.add_widget(MainScreen(name="home"))
        manager.add_widget(FormScreen(name="sale"))
        manager.add_widget(FormScreen(name="expense"))
        manager.add_widget(HistoryScreen(name="history"))
        manager.bind(current=self.refresh_dashboard)
        self.manager = manager
        self.refresh_dashboard()
        return manager

    def refresh_dashboard(self, *args):
        if not hasattr(self, "manager"):
            return
        sales, expenses = self.db.totals_today()
        home = self.manager.get_screen("home")
        home.ids.sales_total.text = money(sales)
        home.ids.expenses_total.text = money(expenses)
        home.ids.profit.text = money(sales - expenses)

    def on_start(self):
        self.refresh_dashboard()


if __name__ == "__main__":
    GestorApp().run()
