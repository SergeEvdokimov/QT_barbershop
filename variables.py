ChooseDateWidget = '''<?xml version="1.0" encoding="UTF-8"?>
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
</ui>'''

FiltersWidget = '''<?xml version="1.0" encoding="UTF-8"?>
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
</ui>'''

weekdays = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
months = {1: 'январь', 2: 'февраль', 3: 'март', 4: 'апрель', 5: 'май', 6: 'июнь', 7: 'июль', 8: 'август',
          9: 'сентябрь', 10: 'октябрь', 11: 'ноябрь', 12: 'декабрь'}