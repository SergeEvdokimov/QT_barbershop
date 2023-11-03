import sys
import sqlite3
from PyQt5.QtCore import Qt
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QTabWidget, QPushButton, QMainWindow, QLabel, \
    QComboBox, QTableWidgetItem, QMessageBox, QTableWidget, QSpinBox, QLineEdit


class EditScheduleWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(300, 300, 300, 100)
        self.setWindowTitle('Изменение данных')

        self.time_lbl = QLabel('Время (с точностью до часов)', self)
        self.time_lbl.resize(200, 30)
        self.time_lbl.move(10, 10)

        self.time = QSpinBox(self)
        self.time.setRange(0, 24)
        self.time.move(200, 10)
        self.time.resize(60, 30)

        self.con = sqlite3.connect("barbershop.db")
        self.cur = self.con.cursor()

        self.saveButton = QPushButton('Сохранить', self)
        self.saveButton.clicked.connect(self.try_to_edit)
        self.saveButton.move(165, 50)
        self.saveButton.resize(120, 30)

        self.closeButton = QPushButton('Закрыть', self)
        self.closeButton.clicked.connect(self.close)
        self.closeButton.move(15, 50)
        self.closeButton.resize(120, 30)

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


class AddServiceWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Изменение данных')

        self.name_lbl = QLabel('Название', self)
        self.name_lbl.resize(100, 30)
        self.name_lbl.move(10, 10)

        self.name = QLineEdit(self)
        self.name.resize(180, 30)
        self.name.move(100, 10)

        self.price_lbl = QLabel('Цена', self)
        self.price_lbl.resize(100, 30)
        self.price_lbl.move(10, 50)

        self.price = QLineEdit(self)
        self.price.resize(180, 30)
        self.price.move(100, 50)

        self.time_lbl = QLabel('Время на стрижку\n(с точностью до часов)', self)
        self.time_lbl.resize(200, 30)
        self.time_lbl.move(10, 90)

        self.time = QSpinBox(self)
        self.time.setRange(0, 24)
        self.time.move(200, 90)
        self.time.resize(60, 30)

        self.con = sqlite3.connect("barbershop.db")
        self.cur = self.con.cursor()

        self.Button = QPushButton('Сохранить', self)
        self.Button.move(165, 140)
        self.Button.resize(120, 30)

        self.closeButton = QPushButton('Закрыть', self)
        self.closeButton.clicked.connect(self.close)
        self.closeButton.move(15, 140)
        self.closeButton.resize(120, 30)

        self.statusbar = self.statusBar()

    def try_to_add(self):
        if self.get_adding_verdict():
            self.con.commit()
            self.parent().update_services()
            self.close()

    def get_adding_verdict(self):
        try:
            name = self.name.text()
            price = int(self.price.text())
            time = int(self.time.value())

            if not name or price < 0:
                raise NameError

            self.cur.execute(f'''INSERT INTO services(Name, Price, RequiredTime)
             VALUES("{name}", {price}, {time})''')
            self.con.commit()
            return True

        except Exception:
            self.statusbar.showMessage('Неверно заполнена форма')
            return False

    def try_to_edit(self):
        if self.get_editing_verdict():
            self.con.commit()
            self.parent().update_services()
            self.close()

    def get_editing_verdict(self):
        try:
            name = self.name.text()
            price = int(self.price.text())
            time = int(self.time.value())
            row = self.parent().servicesTable.currentRow()
            ID = int(self.parent().servicesTable.item(row, 0).text())

            if not name or price < 0:
                raise NameError

            self.cur.execute(f'''update services
             set Name = "{name}", Price = {price}, RequiredTime = {time} where id = {ID}''')
            self.con.commit()
            return True

        except Exception:
            self.statusbar.showMessage('Неверно заполнена форма')
            return False


class BarberShop(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 650, 600)
        self.setWindowTitle('Барбершоп')

        self.status = self.statusBar()
        self.tabWidget = QTabWidget(self)

        # создание страниц
        self.scheduleTab = QWidget(self)
        schedule_layout = QGridLayout()
        self.scheduleTab.setLayout(schedule_layout)

        self.registrationsTab = QWidget(self)
        registrations_layout = QGridLayout()
        self.registrationsTab.setLayout(registrations_layout)

        self.workersTab = QWidget(self)
        workers_layout = QGridLayout()
        self.workersTab.setLayout(workers_layout)

        self.servicesTab = QWidget(self)
        services_layout = QGridLayout()
        self.servicesTab.setLayout(services_layout)

        # интерфейс первой страницы
        self.changeScheduleButton = QPushButton('Изменить время', self)
        self.changeScheduleButton.clicked.connect(self.edit_schedule)
        schedule_layout.addWidget(self.changeScheduleButton, 0, 0, 1, 1)

        self.scheduleTable = QTableWidget(self)
        schedule_layout.addWidget(self.scheduleTable, 1, 0, 8, 8)

        self.tabWidget.addTab(self.scheduleTab, 'Режим работы')
        self.scheduleTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)

        # интерфейс второй страницы
        self.curWeekButton = QPushButton('Текущая неделя', self)
        self.curWeekButton.clicked.connect(self.cur_week_only)
        registrations_layout.addWidget(self.curWeekButton, 0, 0, 1, 1)

        self.nextWeekButton = QPushButton('Следующая неделя', self)
        self.nextWeekButton.clicked.connect(self.next_week_only)
        registrations_layout.addWidget(self.nextWeekButton, 0, 1, 1, 1)

        self.selectPeriodButton = QPushButton('Выбрать период', self)
        self.selectPeriodButton.clicked.connect(self.select_period)
        registrations_layout.addWidget(self.selectPeriodButton, 0, 2, 1, 1)

        self.discardButton = QPushButton('Сбросить', self)
        self.discardButton.clicked.connect(self.show_registrations)
        registrations_layout.addWidget(self.discardButton, 0, 3, 1, 1)

        self.registrationsTable = QTableWidget(self)
        registrations_layout.addWidget(self.registrationsTable, 1, 0, 8, 8)

        self.tabWidget.addTab(self.registrationsTab, 'Записи')

        # интерфейс третьей страницы
        self.workersTable = QTableWidget(self)
        workers_layout.addWidget(self.workersTable, 1, 0, 8, 8)

        self.tabWidget.addTab(self.workersTab, 'Мастера')

        # интерфейс четвертой страницы
        self.editServiceButton = QPushButton('Изменить услугу', self)
        self.editServiceButton.clicked.connect(self.edit_service)
        services_layout.addWidget(self.editServiceButton, 0, 0, 1, 1)

        self.addServiceButton = QPushButton('Добавить услугу', self)
        self.addServiceButton.clicked.connect(self.add_service)
        services_layout.addWidget(self.addServiceButton, 0, 1, 1, 1)

        self.servicesTable = QTableWidget(self)
        services_layout.addWidget(self.servicesTable, 1, 0, 8, 8)

        self.tabWidget.addTab(self.servicesTab, 'Услуги')
        self.servicesTable.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)

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
        self.show_registrations()
        self.show_workers()
        self.update_services()

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
                    self.scheduleTable.item(i, j).setFlags(Qt.ItemIsDropEnabled)
                else:
                    self.scheduleTable.setItem(i, j, QTableWidgetItem(f'{str(val)}:00'))
                    self.scheduleTable.item(i, j).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

        self.scheduleTable.resizeColumnsToContents()

    def edit_schedule(self):
        self.status.showMessage('')
        self.edit_work_schedule_widget = EditScheduleWidget(self)
        row = self.scheduleTable.currentRow()
        col = self.scheduleTable.currentColumn()
        if row == -1 or col == 0:
            self.status.showMessage('Необходимо выбрать ячейку со временем')
        else:
            self.edit_work_schedule_widget.show()
            self.edit_work_schedule_widget.time.setValue(int(self.scheduleTable.item(row, col).text().split(':')[0]))

    def cur_week_only(self):
        pass

    def next_week_only(self):
        pass

    def select_period(self):
        pass

    def show_registrations(self):
        pass

    def show_workers(self):
        self.workers_query = self.cur.execute("SELECT * from Workers").fetchall()

        self.workersTable.setRowCount(len(self.workers_query))
        self.workersTable.setColumnCount(len(self.workers_query[0]))

        title = ['ID', 'Имя', 'Комментарий']
        self.workersTable.setHorizontalHeaderLabels(title)

        for i, elem in enumerate(self.workers_query):
            for j, val in enumerate(elem):
                self.workersTable.setItem(i, j, QTableWidgetItem(str(val)))
                self.workersTable.item(i, j).setFlags(Qt.ItemIsDropEnabled)

    def update_services(self):
        self.services_query = self.cur.execute("SELECT * from services").fetchall()

        self.servicesTable.setRowCount(len(self.services_query))
        self.servicesTable.setColumnCount(len(self.services_query[0]))

        title = ['ID', 'Название', 'Цена, руб', 'Необходимое время, ч']
        self.servicesTable.setHorizontalHeaderLabels(title)

        for i, elem in enumerate(self.services_query):
            for j, val in enumerate(elem):
                self.servicesTable.setItem(i, j, QTableWidgetItem(str(val)))
                if not j:
                    self.servicesTable.item(i, j).setFlags(Qt.ItemIsDropEnabled)
                else:
                    self.servicesTable.item(i, j).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

        self.servicesTable.resizeColumnsToContents()

    def edit_service(self):
        self.status.showMessage('')
        self.edit_service_widget = AddServiceWidget(self)
        self.edit_service_widget.Button.clicked.connect(self.edit_service_widget.try_to_edit)
        row = self.servicesTable.currentRow()
        col = self.servicesTable.currentColumn()
        if row == -1:
            self.status.showMessage('Необходимо выбрать ячейку')
        else:
            self.edit_service_widget.show()
            self.edit_service_widget.name.setText(self.servicesTable.item(row, 1).text())
            self.edit_service_widget.price.setText(self.servicesTable.item(row, 2).text())
            self.edit_service_widget.time.setValue(int(self.servicesTable.item(row, 3).text()))

    def add_service(self):
        self.status.showMessage('')
        self.add_service_widget = AddServiceWidget(self)
        self.add_service_widget.Button.clicked.connect(self.add_service_widget.try_to_add)
        self.add_service_widget.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BarberShop()
    window.show()
    sys.exit(app.exec())
