import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QTabWidget, QPushButton, QMainWindow, QLabel, \
    QPlainTextEdit, QComboBox, QTableWidgetItem, QMessageBox, QTableWidget, QSpinBox


class EditScheduleWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(300, 300, 400, 400)

        self.time_lbl = QLabel('Время (с точностью до часов)', self)
        self.time_lbl.resize(200, 30)
        self.time_lbl.move(10, 10)

        self.time = QSpinBox(self)
        self.time.setRange(0, 24)
        self.time.move(200, 10)
        self.time.resize(200, 30)

        self.con = sqlite3.connect("barbershop.db")
        self.cur = self.con.cursor()

        self.saveButton = QPushButton('Сохранить', self)
        self.saveButton.clicked.connect(self.try_to_edit)
        self.saveButton.move(150, 200)
        self.saveButton.resize(150, 30)

        self.statusbar = self.statusBar()

    def try_to_edit(self):
        if self.get_editing_verdict():
            self.con.commit()
            self.parent().update_schedule()
            self.close()

    def get_editing_verdict(self):
        try:
            set_time = int(self.time.text())
            row = self.parent().scheduleTable.currentRow()
            col = self.parent().scheduleTable.currentColumn()
            weekDay = self.parent().scheduleTable.item(row, 0).text()
            if col == 1:
                if set_time >= int(self.parent().scheduleTable.item(row, 2).text().split(':')[0]):
                    raise ValueError
                self.cur.execute(f'update WorkSсhedule set StartTime = {set_time} where weekDay = "{weekDay}"')
            else:
                if set_time <= int(self.parent().scheduleTable.item(row, 1).text().split(':')[0]):
                    print(2)
                    raise ValueError
                self.cur.execute(f'update WorkSсhedule set EndTime = {set_time} where weekDay = "{weekDay}"')
            return True
        except Exception:
            self.statusbar.showMessage('Введено недопустимое значение')
            return False


class BarberShop(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 650, 600)
        self.status = self.statusBar()

        # создание страниц
        self.scheduleTab = QWidget(self)
        first_layout = QGridLayout()
        self.scheduleTab.setLayout(first_layout)

        # интерфейс первой страницы
        self.changeScheduleButton = QPushButton('Изменить расписание', self)
        self.changeScheduleButton.clicked.connect(self.edit_schedule)
        first_layout.addWidget(self.changeScheduleButton, 0, 0, 1, 1)

        self.scheduleTable = QTableWidget(self)
        first_layout.addWidget(self.scheduleTable, 1, 0, 8, 8)

        self.tabWidget = QTabWidget(self)
        self.tabWidget.addTab(self.scheduleTab, 'Расписание')

        # отбражение страниц
        main_layout = QGridLayout(self)
        self.setLayout(main_layout)
        main_layout.addWidget(self.tabWidget, 0, 0, 2, 1)
        self.container = QWidget(self)
        self.container.setLayout(main_layout)
        self.setCentralWidget(self.container)

        # работа с БД
        self.con = sqlite3.connect("barbershop.db")
        self.cur = self.con.cursor()

        # отображение данных
        self.update_schedule()

    def update_schedule(self):
        self.schedule_query = self.cur.execute("SELECT * from WorkSсhedule").fetchall()

        self.scheduleTable.setRowCount(len(self.schedule_query))
        self.scheduleTable.setColumnCount(len(self.schedule_query[0]))

        title = ['День недели', 'Время начала работы', 'Время окончания работы']
        self.scheduleTable.setHorizontalHeaderLabels(title)

        for i, elem in enumerate(self.schedule_query):
            for j, val in enumerate(elem):
                if j == 0:
                    self.scheduleTable.setItem(i, j, QTableWidgetItem(str(val)))
                else:
                    self.scheduleTable.setItem(i, j, QTableWidgetItem(f'{str(val)}:00'))

    def edit_schedule(self):
        self.status.showMessage('')
        self.edit_work_schedule_widget = EditScheduleWidget(self)
        if self.scheduleTable.currentRow() == -1:
            self.status.showMessage('Необходимо выбрать ячейку со временем')
        else:
            self.edit_work_schedule_widget.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BarberShop()
    window.show()
    sys.exit(app.exec())