import io
import sys
import sqlite3
import datetime
import PyQt5.uic as uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QTabWidget, QPushButton, QMainWindow, QLabel, \
    QTableWidgetItem, QTableWidget, QMessageBox, QLineEdit, QAbstractScrollArea

weekdays = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
months = {1: 'январь', 2: 'февраль', 3: 'март', 4: 'апрель', 5: 'май', 6: 'июнь', 7: 'июль', 8: 'август',
          9: 'сентябрь', 10: 'октябрь', 11: 'ноябрь', 12: 'декабрь'}

choose_date_ui = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>440</width>
    <height>440</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>MainWindow</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QWidget" name="verticalLayoutWidget">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>10</y>
      <width>411</width>
      <height>381</height>
     </rect>
    </property>
    <layout class="QVBoxLayout" name="verticalLayout">
     <item>
      <widget class="QCalendarWidget" name="calendarWidget"/>
     </item>
     <item>
      <layout class="QHBoxLayout" name="service_layout">
       <item>
        <widget class="QLabel" name="service_lbl">
         <property name="text">
          <string>Услуга</string>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QComboBox" name="service_comboBox"/>
       </item>
      </layout>
     </item>
     <item>
      <layout class="QHBoxLayout" name="buttons_layout">
       <item>
        <widget class="QPushButton" name="cancelButton">
         <property name="text">
          <string>Отмена</string>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QPushButton" name="continueButton">
         <property name="text">
          <string>Продолжить</string>
         </property>
        </widget>
       </item>
      </layout>
     </item>
    </layout>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>440</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
'''
filters_ui = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>290</width>
    <height>180</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>Добавление фильтров</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QWidget" name="verticalLayoutWidget">
    <property name="geometry">
     <rect>
      <x>9</x>
      <y>9</y>
      <width>271</width>
      <height>141</height>
     </rect>
    </property>
    <layout class="QVBoxLayout" name="vertical_layout">
     <item>
      <layout class="QHBoxLayout" name="master_layout">
       <item>
        <widget class="QLabel" name="master_label">
         <property name="text">
          <string>Выберите мастера</string>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QComboBox" name="masters_comboBox"/>
       </item>
      </layout>
     </item>
     <item>
      <layout class="QHBoxLayout" name="start_date_layout">
       <item>
        <widget class="QLabel" name="start_date_label">
         <property name="text">
          <string>С</string>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QLineEdit" name="start_day"/>
       </item>
       <item>
        <widget class="QComboBox" name="start_month"/>
       </item>
       <item>
        <widget class="QLineEdit" name="start_year"/>
       </item>
      </layout>
     </item>
     <item>
      <layout class="QHBoxLayout" name="end_date_layout">
       <item>
        <widget class="QLabel" name="end_date_label">
         <property name="text">
          <string>По</string>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QLineEdit" name="end_day"/>
       </item>
       <item>
        <widget class="QComboBox" name="end_month"/>
       </item>
       <item>
        <widget class="QLineEdit" name="end_year"/>
       </item>
      </layout>
     </item>
     <item>
      <layout class="QHBoxLayout" name="buttons_layout">
       <item>
        <widget class="QPushButton" name="closeButton">
         <property name="text">
          <string>Отмена</string>
         </property>
        </widget>
       </item>
       <item>
        <widget class="QPushButton" name="saveButton">
         <property name="text">
          <string>Сохранить</string>
         </property>
        </widget>
       </item>
      </layout>
     </item>
    </layout>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>290</width>
     <height>21</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
</ui>
'''

con = sqlite3.connect("barbershop.db")
cur = con.cursor()


class AddServiceWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(300, 200)
        self.setWindowTitle('Новые данные')
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)

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

        self.Button = QPushButton('Сохранить', self)
        self.Button.move(165, 140)
        self.Button.resize(120, 30)

        self.closeButton = QPushButton('Отмена', self)
        self.closeButton.clicked.connect(self.close)
        self.closeButton.move(15, 140)
        self.closeButton.resize(120, 30)

        self.statusbar = self.statusBar()

    def try_to_add(self):
        if self.get_adding_verdict():
            con.commit()
            self.parent().update_services()
            self.close()

    def get_adding_verdict(self):
        try:
            name = self.name.text()
            price = int(self.price.text())

            if not name or price < 0:
                raise NameError

            cur.execute(f'''INSERT INTO services(Name, Price)
             VALUES("{name}", {price})''')
            con.commit()
            return True

        except Exception:
            self.statusbar.showMessage('Неверно заполнена форма')
            return False

    def try_to_edit(self):
        if self.get_editing_verdict():
            con.commit()
            self.parent().update_services()
            self.close()

    def get_editing_verdict(self):
        try:
            name = self.name.text()
            price = int(self.price.text())
            row = self.parent().servicesTable.currentRow()
            unic = int(self.parent().servicesTable.item(row, 0).text())

            if not name or price < 0:
                raise NameError

            cur.execute(f'''update services
             set Name = "{name}", Price = {price} where id = {unic}''')
            con.commit()
            return True

        except Exception:
            self.statusbar.showMessage('Неверно заполнена форма')
            return False


class AddRegistrationWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setGeometry(900, 300, 1000, 400)
        self.setFixedSize(1000, 400)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.date = self.parent().date
        self.status = self.statusBar()

        self.closeButton = QPushButton('Отмена', self)
        self.closeButton.clicked.connect(self.close)
        self.closeButton.move(80, 350)

        self.saveButton = QPushButton('Сохранить', self)
        self.saveButton.clicked.connect(self.try_to_add)
        self.saveButton.move(820, 350)

        self.addingTable = QTableWidget(self)
        self.addingTable.resize(950, 300)
        self.addingTable.move(10, 10)
        self.timetable_query = cur.execute(f'''SELECT * from WorkSсhedule 
        where weekDay == {self.date.weekday()}''').fetchall()[0]
        self.workers_query = cur.execute(f'''select * from workers''').fetchall()
        self.addingTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        workers = {}
        for line in self.workers_query:
            workers[line[0]] = line[1]

        self.addingTable.setRowCount(len(self.workers_query))
        self.addingTable.setColumnCount(self.timetable_query[2] - self.timetable_query[1])
        title = list(map(lambda x: str(x) + ':00', range(self.timetable_query[2])[self.timetable_query[1]:]))
        f_column = list(map(lambda x: f'{x[1]} (id: {x[0]})', self.workers_query))
        self.addingTable.setHorizontalHeaderLabels(title)
        self.addingTable.setVerticalHeaderLabels(f_column)

        self.query = cur.execute(f'''select r.startTime, r.MasterID from Registrations as R, workers as W
        inner join Registrations on R.MasterID = W.id where r.date == "{self.date}"''').fetchall()

        for i, elem in enumerate(self.workers_query):
            for j, val in enumerate(range(self.timetable_query[2])[self.timetable_query[1]:]):
                if (val, elem[0]) in self.query:
                    self.addingTable.setItem(i, j, QTableWidgetItem('Занято'))
                    self.addingTable.item(i, j).setFlags(Qt.ItemIsDropEnabled)
                    self.addingTable.item(i, j).setBackground(QColor(255, 218, 185))
                else:
                    self.addingTable.setItem(i, j, QTableWidgetItem('Свободно'))
                    self.addingTable.item(i, j).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
                    self.addingTable.item(i, j).setBackground(QColor(152, 251, 152))

        self.addingTable.resizeColumnsToContents()

    def try_to_add(self):
        if self.get_adding_verdict():
            con.commit()
            self.parent().parent().update_registrations()
            self.parent().close()
            self.close()

    def get_adding_verdict(self):
        try:
            date = self.parent().date
            row = self.addingTable.currentRow()
            col = self.addingTable.currentColumn()
            service = self.parent().service
            time = self.addingTable.horizontalHeaderItem(col).text().split(':')[0]
            master_id = self.addingTable.verticalHeaderItem(row).text().split()[-1][:-1]
            cur.execute(f'''insert into Registrations (date, masterID, Service, StartTime)
             values ("{date}", {master_id}, "{service}", {time})''')
            return True
        except Exception:
            self.statusbar.showMessage('Выберите время и мастера')
            return False

    def close(self):
        self.parent().calendarWidget.setEnabled(True)
        self.parent().continueButton.setEnabled(True)
        super().close()


class ChooseDateWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui = io.StringIO(choose_date_ui)
        uic.loadUi(ui, self)
        self.setFixedSize(440, 440)
        self.setWindowTitle('Новые данные')
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.statusbar = self.statusBar()

        self.cancelButton.clicked.connect(self.close)
        self.continueButton.clicked.connect(self.choose_time)

        self.service_comboBox.addItems(list(map(lambda x: f'{x[1]} ({x[2]}руб.)',
                                                self.parent().get_services())))

    def choose_time(self):
        self.continueButton.setEnabled(False)
        self.calendarWidget.setEnabled(False)
        self.date = self.calendarWidget.selectedDate().toPyDate()
        self.service = self.service_comboBox.currentText().split(' (')[0]
        self.add_registration_widget = AddRegistrationWidget(self)
        self.add_registration_widget.show()


class AddFiltersWidget(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        ui = io.StringIO(filters_ui)
        uic.loadUi(ui, self)
        self.setGeometry(300, 300, 290, 180)
        self.setFixedSize(290, 180)
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)
        self.status = self.statusBar()

        self.closeButton.clicked.connect(self.close)
        self.saveButton.clicked.connect(self.try_to_save)

        workers_query = cur.execute(f'''select * from workers''').fetchall()
        workers = ['Не важно'] + list(map(lambda x: f'{x[1]} (id: {x[0]})', workers_query))
        self.masters_comboBox.addItems(workers)

        for i in workers[1:]:
            if self.parent().master_id == int(i.split(': ')[1][:-1]):
                self.masters_comboBox.setCurrentText(i)

        self.start_month.addItems(months.values())
        self.end_month.addItems(months.values())

        if self.parent().start_date is not None:
            first_date = self.parent().start_date
            second_date = self.parent().end_date
        else:
            first_date = datetime.date.today()
            second_date = datetime.date.today()

        self.start_day.setText(str(str(first_date).split('-')[-1]))
        self.start_year.setText(str(str(first_date).split('-')[0]))
        self.start_month.setCurrentText(months[int(str(first_date).split('-')[1])])

        self.end_day.setText(str(str(second_date).split('-')[-1]))
        self.end_year.setText(str(str(second_date).split('-')[0]))
        self.end_month.setCurrentText(months[int(str(second_date).split('-')[1])])

    def try_to_save(self):
        if self.get_saving_verdict():
            con.commit()
            self.parent().update_registrations()
            self.close()

    def get_saving_verdict(self):
        try:
            start_month = 0
            end_month = 0
            for key in months:
                if months[key] == self.start_month.currentText():
                    start_month = key
                if months[key] == self.end_month.currentText():
                    end_month = key

            start_day = self.start_day.text()
            start_year = self.start_year.text()
            start_date = datetime.date(int(start_year), int(start_month), int(start_day))

            end_day = self.end_day.text()
            end_year = self.end_year.text()
            end_date = datetime.date(int(end_year), int(end_month), int(end_day))

            if self.masters_comboBox.currentText() != 'Не важно':
                self.parent().master_id = int(self.masters_comboBox.currentText().split(': ')[1][:-1])
            self.parent().start_date = start_date
            self.parent().end_date = end_date

            assert start_date <= end_date
            return True

        except Exception:
            self.statusbar.showMessage('Неверно заполнена форма')
            return False


class BarberShop(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(200, 200, 1000, 600)
        self.setWindowTitle('Барбершоп')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

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
        self.scheduleTable = QTableWidget(self)
        schedule_layout.addWidget(self.scheduleTable, 0, 0, 8, 8)

        self.tabWidget.addTab(self.scheduleTab, 'Режим работы')
        self.scheduleTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        # интерфейс второй страницы
        self.newRegistrationButton = QPushButton('Добавить запись', self)
        self.newRegistrationButton.clicked.connect(self.new_registration)
        registrations_layout.addWidget(self.newRegistrationButton, 0, 0, 1, 1)

        self.addFiltersButton = QPushButton('Фильтр', self)
        self.addFiltersButton.clicked.connect(self.add_filters)
        registrations_layout.addWidget(self.addFiltersButton, 0, 1, 1, 1)

        self.delFiltersButton = QPushButton('Удалить фильтры', self)
        self.delFiltersButton.clicked.connect(self.del_filters)
        registrations_layout.addWidget(self.delFiltersButton, 0, 2, 1, 1)

        self.delRegistrationButton = QPushButton('Удалить запись', self)
        self.delRegistrationButton.clicked.connect(self.del_registration)
        registrations_layout.addWidget(self.delRegistrationButton, 0, 7, 1, 1)

        self.registrationsTable = QTableWidget(self)
        registrations_layout.addWidget(self.registrationsTable, 1, 0, 8, 8)

        self.tabWidget.addTab(self.registrationsTab, 'Записи')
        self.registrationsTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        # интерфейс третьей страницы
        self.workersTable = QTableWidget(self)
        workers_layout.addWidget(self.workersTable, 1, 0, 8, 8)

        self.tabWidget.addTab(self.workersTab, 'Мастера')

        # интерфейс четвертой страницы
        self.editServiceButton = QPushButton('Изменить услугу', self)
        self.editServiceButton.clicked.connect(self.edit_service)
        services_layout.addWidget(self.editServiceButton, 0, 0, 1, 1)

        self.addServiceButton = QPushButton('Добавить', self)
        self.addServiceButton.clicked.connect(self.add_service)
        services_layout.addWidget(self.addServiceButton, 0, 1, 1, 1)

        self.servicesTable = QTableWidget(self)
        services_layout.addWidget(self.servicesTable, 1, 0, 8, 8)

        self.tabWidget.addTab(self.servicesTab, 'Услуги')
        self.servicesTable.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)

        # отбражение страниц
        main_layout = QGridLayout(self)
        self.setLayout(main_layout)
        main_layout.addWidget(self.tabWidget, 0, 0, 2, 1)
        self.container = QWidget(self)
        self.container.setLayout(main_layout)
        self.setCentralWidget(self.container)

        self.master_id = None
        self.start_date = None
        self.end_date = None

        # отображение данных
        self.show_schedule()
        self.show_workers()
        self.update_services()
        self.update_registrations()

    def show_schedule(self):
        schedule_query = cur.execute("SELECT * from WorkSсhedule").fetchall()

        self.scheduleTable.setRowCount(len(schedule_query))
        self.scheduleTable.setColumnCount(len(schedule_query[0]))

        title = ['День недели', 'Время начала работы', 'Время окончания работы']
        self.scheduleTable.setHorizontalHeaderLabels(title)

        for i, elem in enumerate(schedule_query):
            for j, val in enumerate(elem):
                if j == 0:
                    self.scheduleTable.setItem(i, j, QTableWidgetItem(weekdays[val]))
                    self.scheduleTable.item(i, j).setFlags(Qt.ItemIsDropEnabled)
                else:
                    self.scheduleTable.setItem(i, j, QTableWidgetItem(f'{str(val)}:00'))
                    self.scheduleTable.item(i, j).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

        self.scheduleTable.resizeColumnsToContents()

    def show_workers(self):
        workers_query = cur.execute("SELECT * from Workers").fetchall()

        self.workersTable.setRowCount(len(workers_query))
        self.workersTable.setColumnCount(len(workers_query[0]))

        title = ['ID', 'Имя', 'Комментарий']
        self.workersTable.setHorizontalHeaderLabels(title)

        for i, elem in enumerate(workers_query):
            for j, val in enumerate(elem):
                self.workersTable.setItem(i, j, QTableWidgetItem(str(val)))
                self.workersTable.item(i, j).setFlags(Qt.ItemIsDropEnabled)

    def update_services(self):
        services_query = cur.execute("SELECT * from services").fetchall()

        self.servicesTable.setRowCount(len(services_query))
        self.servicesTable.setColumnCount(len(services_query[0]))

        title = ['ID', 'Название', 'Цена, руб', 'Необходимое время, ч']
        self.servicesTable.setHorizontalHeaderLabels(title)

        for i, elem in enumerate(services_query):
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
        if row == -1:
            self.status.showMessage('Необходимо выбрать ячейку')
        else:
            self.edit_service_widget.show()
            self.edit_service_widget.name.setText(self.servicesTable.item(row, 1).text())
            self.edit_service_widget.price.setText(self.servicesTable.item(row, 2).text())

    def add_service(self):
        self.status.showMessage('')
        self.add_service_widget = AddServiceWidget(self)
        self.add_service_widget.Button.clicked.connect(self.add_service_widget.try_to_add)
        self.add_service_widget.show()

    def update_registrations(self):
        addition_to_query = ''
        if self.master_id is not None:
            addition_to_query = f'where r.MasterID = {self.master_id}'
        registrations_query = cur.execute(f'''select distinct r.id, r.date, r.startTime, r.Service,
        w.Name as Master from Registrations as R, workers as W
        inner join Registrations on R.MasterID = W.id {addition_to_query}
        order by r.date, r.startTime''').fetchall()

        if self.start_date is not None:
            def is_row_ok(line):
                if self.start_date <= datetime.datetime.strptime(line[1], '%Y-%m-%d').date() <= self.end_date:
                    return True
            useful_registrations_query = list(filter(is_row_ok, registrations_query))
        else:
            useful_registrations_query = registrations_query

        self.registrationsTable.setRowCount(len(useful_registrations_query))
        self.registrationsTable.setColumnCount(9)

        title = ['ID', 'Число', 'Месяц', 'Год', 'День недели', 'Время\nначала',
                 'Время\nокончания', 'Услуга', 'Мастер']
        self.registrationsTable.setHorizontalHeaderLabels(title)

        for i, elem in enumerate(useful_registrations_query):
            row_date_time = datetime.datetime.strptime(elem[1], '%Y-%m-%d')
            row_date = row_date_time.date()
            year, month, day, start_time = str(row_date).split('-') + [str(elem[2])]
            row = [elem[0], day, month, year, weekdays[row_date.weekday()], start_time + ':00',
                   str(1 + int(start_time)) + ':00', *elem[3:]]
            for j, val in enumerate(row):
                self.registrationsTable.setItem(i, j, QTableWidgetItem(str(val)))
                self.registrationsTable.item(i, j).setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)

        self.registrationsTable.resizeColumnsToContents()

    def add_filters(self):
        self.status.showMessage('')
        self.add_filters_widget = AddFiltersWidget(self)
        self.add_filters_widget.show()

    def del_filters(self):
        self.master_id = None
        self.start_date = None
        self.end_date = None
        self.update_registrations()

    def new_registration(self):
        self.status.showMessage('')
        self.add_registration_widget = ChooseDateWidget(self)
        self.add_registration_widget.show()

    def get_services(self):
        query = cur.execute("SELECT * from services").fetchall()
        return query

    def del_registration(self):
        self.status.showMessage('')
        row = self.registrationsTable.currentRow()
        if row == -1:
            self.status.showMessage('Для удаления выберите ячейку')
        else:
            unic = self.registrationsTable.item(row, 0).text()
            user_response = QMessageBox.question(self, 'Вы уверены?',
                                                f'Вы уверены, что хотите удалить запись с id = {unic}',
                                                QMessageBox.Yes | QMessageBox.No)

            if user_response == QMessageBox.Yes:
                cur.execute(f'DELETE from Registrations where id == {unic}')
                con.commit()
                self.update_registrations()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BarberShop()
    window.show()
    sys.exit(app.exec())

# Когда изменятся название услуги, на которую уже есть запись, название услуги в таблице записей не изменяется,
# ЭТО НЕ БАГ, А ФИЧА

# toDo: сброс статуса при перекдючении вкладки