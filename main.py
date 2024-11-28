import sys
import sqlite3
from PyQt5 import QtWidgets, uic


class AddEditCoffeeForm(QtWidgets.QWidget):
    def __init__(self, parent, coffee_id=None):
        super().__init__()
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.parent = parent
        self.coffee_id = coffee_id

        if self.coffee_id:
            self.load_coffee_data()

        self.button_save.clicked.connect(self.save_coffee)
        self.button_cancel.clicked.connect(self.close)

    def load_coffee_data(self):
        conn = sqlite3.connect("coffee.sqlite")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coffee WHERE id = ?", (self.coffee_id,))
        coffee = cursor.fetchone()
        conn.close()

        if coffee:
            self.lineEdit_name.setText(coffee[1])
            self.lineEdit_roast.setText(coffee[2])

    def save_coffee(self):
        name = self.lineEdit_name.text()
        roast = self.lineEdit_roast.text()

        conn = sqlite3.connect("coffee.sqlite")
        cursor = conn.cursor()

        if self.coffee_id:
            cursor.execute("""
                UPDATE coffee
                SET name = ?, roast_level = ?
                WHERE id = ?
            """, (name, roast, self.coffee_id))
        else:
            cursor.execute("""
                INSERT INTO coffee (name, roast_level)
                VALUES (?, ?)
            """, (name, roast))

        conn.commit()
        conn.close()
        self.parent.load_data()
        self.close()


class CoffeeApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)

        self.refreshButton.clicked.connect(self.load_data)
        self.addButton.clicked.connect(self.add_coffee)
        self.editButton.clicked.connect(self.edit_coffee)

        self.load_data()

    def load_data(self):
        conn = sqlite3.connect("coffee.sqlite")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coffee")
        rows = cursor.fetchall()

        self.tableWidget.setRowCount(len(rows))
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setHorizontalHeaderLabels(["ID", "Сорт", "Обжарка", "Форма", "Описание", "Цена", "Объем"])

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))

        conn.close()

    def add_coffee(self):
        self.form = AddEditCoffeeForm(self)
        self.form.show()

    def edit_coffee(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row != -1:
            coffee_id = int(self.tableWidget.item(selected_row, 0).text())
            self.form = AddEditCoffeeForm(self, coffee_id)
            self.form.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec_())
