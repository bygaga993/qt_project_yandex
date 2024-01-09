import sys

import sqlite3
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QButtonGroup, QFileDialog, QTableWidgetItem, QWidget

import check_log
from start import StartWindow

import csv  # библиотека для работы с csv файлами

import pandas as pd  # библиотке для работы с данными

import xlrd  # библиотека для работы с excel файлами

import traceback


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui_files/main.ui", self)

        self.InButton.clicked.connect(self.entry)

        # Определение радио кнопок(формат файла) в группу,
        # CSV файл отмечен по умолчанию
        self.button_group = QButtonGroup()
        self.csv_radio_button.setChecked(True)
        self.format_file = 0
        self.button_group.addButton(self.csv_radio_button)
        self.button_group.addButton(self.excel_radio_button)
        self.button_group.addButton(self.sql_radio_button)
        self.button_group.buttonClicked.connect(self.radio_button_clicked)

        self.open_file_button.clicked.connect(self.open_file)  # вызов функции открытия файла

        self.startButton.clicked.connect(self.start)  # вызов функции для работы с мерами центральной тенденции
        self.fname = ''

        for el in ['заполнение пропусков нулями', 'заполнение медианой', 'Заполнение средним арифметическим значением']:
            self.pass_comboBox.addItem(el)

        self.passButton.clicked.connect(self.clear_data)

    def entry(self):  # открытие виджета регистрации/входа
        self.start = StartWindow()
        self.start.show()

    def radio_button_clicked(self, button):  # Функция возвращающая выбранную кнопку
        if button.text() == 'CSV файл':
            self.format_file = 0
        elif button.text() == 'SQL':
            self.format_file = 2
        else:
            self.format_file = 1

    def open_file(self):  # получение пути файла для работы с ним
        self.clear_lines()
        if self.format_file == 0:
            if check_log.FLAG is False:  # проверка на то, что пользователь вошел в аккаунт
                self.statusBar().showMessage('Войдите пожалуйста в аккаунт')
                return
            self.statusBar().clearMessage()
            fname = QFileDialog.getOpenFileName(self, 'Выбрать csv файл ', '',
                                                'csv файл (*.csv)')[0]
            d = self.lineEdit.text()
            if d != '':
                self.csv_file(fname, d)
            else:
                self.csv_file(fname)
        elif self.format_file == 1:
            if check_log.FLAG is False:  # проверка на то, что пользователь вошел в аккаунт
                self.statusBar().showMessage('Войдите пожалуйста в аккаунт')
                return
            self.statusBar().clearMessage()
            fname = QFileDialog.getOpenFileName(self, 'Выбрать xls файл ', '',
                                                'xls файл (*.xls);;xlsx файл (*.xlsx')[0]
            self.excel_file(fname)
        else:
            try:
                if check_log.FLAG is False:  # проверка на то, что пользователь вошел в аккаунт
                    self.statusBar().showMessage('Войдите пожалуйста в аккаунт')
                    return
                self.statusBar().clearMessage()
                fname = QFileDialog.getOpenFileName(self, 'Выбрать sql файл ', '',
                                                    'sql файл (*.db)')[0]
                self.workwithsql = DBSample(fname)  # при работе с sql бд открывается специальный виджет
                self.workwithsql.show()
            except Exception as e:
                self.statusBar().showMessage('Возникла ошибка, убедитесь, что вы корректно выбрали файл')

    def csv_file(self, fname, d=','):  # открытие csv файла
        try:
            self.fname = fname
            with open(fname, 'r') as csvfile:
                reader = csv.reader(csvfile, delimiter=d, quotechar='"')
                title = next(reader)
                # вывод таблицы
                self.tableWidget.setColumnCount(len(title))
                self.tableWidget.setHorizontalHeaderLabels(title)
                self.tableWidget.setRowCount(0)
                for i, row in enumerate(reader):
                    self.tableWidget.setRowCount(
                        self.tableWidget.rowCount() + 1)
                    for j, elem in enumerate(row):
                        self.tableWidget.setItem(
                            i, j, QTableWidgetItem(elem))
                self.tableWidget.resizeColumnsToContents()
            self.column_comboBox.clear()
            for el in title:
                self.column_comboBox.addItem(el)
        except Exception as e:
            self.column_comboBox.clear()
            self.tableWidget.clear()
            self.statusBar().showMessage('Возникла ошибка, убедитесь, что вы корректно выбрали файл')

    def excel_file(self, fname):  # открытие excel файла
        try:
            self.fname = fname
            workbook = xlrd.open_workbook(fname, ignore_workbook_corruption=True)  # открытие файла
            df = pd.read_excel(workbook)  # образование в датафрэйм, для удобства работы
            header = df.columns.values.tolist()
            self.column_comboBox.clear()
            #  вывод таблицы
            self.tableWidget.setColumnCount(len(header))
            self.tableWidget.setHorizontalHeaderLabels(header)

            for i, row in df.iterrows():
                self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
                for j in range(self.tableWidget.columnCount()):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(row.iloc[j])))
            for el in header:
                self.column_comboBox.addItem(el)
        except Exception as e:
            # если файл не выбран
            self.column_comboBox.clear()
            self.tableWidget.clear()
            self.statusBar().showMessage('Возникла ошибка, убедитесь, что вы корректно выбрали файл')

    def start(self):
        self.clear_lines()
        # работа с мерами центральной тенденции в данных
        if self.format_file == 0:
            df = pd.read_csv(self.fname)
        else:
            workbook = xlrd.open_workbook(self.fname, ignore_workbook_corruption=True)
            df = pd.read_excel(workbook)
        column_name = self.column_comboBox.currentText()
        self.modeline.setText(str(list(df[column_name].mode())[0]))  # мода
        if df[column_name].dtype != 'int64' and df[column_name].dtype != 'float64':
            # вычисление медианы и среднего может происходить только с числовыми данными
            self.medianline.setText('Неверный формат данных')
            self.avgline.setText('Неверный формат данных')
        else:
            self.medianline.setText(str(df[column_name].median()))  # медиана
            self.avgline.setText(str(df[column_name].mean()))  # среднее

    def clear_data(self):  # работа с пропусками
        cd = self.pass_comboBox.currentText()
        column_name = self.column_comboBox.currentText()
        if self.format_file == 0:  # файл формата csv
            df = pd.read_csv(self.fname)
        else:  # файл формата excel
            workbook = xlrd.open_workbook(self.fname, ignore_workbook_corruption=True)
            df = pd.read_excel(workbook)
        if cd == 'заполнение пропусков нулями':
            self.labelError.setText('')
            df[column_name].fillna(0, inplace=True)  # функция заполнения пропусков нулями
            self.table_dataframe(df)
        elif cd == 'заполнение медианой' or cd == 'Заполнение средним арифметическим значением':
            if df[column_name].dtype != 'int64' and df[column_name].dtype != 'float64':
                # вычисление медианы и среднего может происходить только с числовыми данными
                self.labelError.setText('Неверный формат данных')
            else:
                if cd == 'заполнение медианой':
                    self.labelError.setText('')
                    df[column_name].fillna(df[column_name].median(),
                                           inplace=True)  # функция заполнения пропусков медианой
                    self.table_dataframe(df)
                else:
                    self.labelError.setText('')
                    df[column_name].fillna(df[column_name].mean(), inplace=True)  # функция заполнения пропусков средним
                    self.table_dataframe(df)

    def table_dataframe(self, df):  # функция вывода данных после заполнения пропусков
        header = df.columns.values.tolist()
        self.tableWidget.setColumnCount(len(header))
        self.tableWidget.setHorizontalHeaderLabels(header)

        for i, row in df.iterrows():
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            for j in range(self.tableWidget.columnCount()):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(row.iloc[j])))
        for el in header:
            self.column_comboBox.addItem(el)

    def clear_lines(self):
        self.modeline.setText('')
        self.avgline.setText('')
        self.medianline.setText('')


class DBSample(QWidget):  # виджет для работы с sql таблицами
    def __init__(self, fname):
        super().__init__()
        uic.loadUi('ui_files/workwithdb.ui', self)
        self.fname = fname
        self.connection = sqlite3.connect(self.fname)
        self.pushButton.clicked.connect(self.select_data)
        self.textEdit.setPlainText("")
        self.select_data()

    def select_data(self):
        try:
            self.Form.setText('')
            query = self.textEdit.toPlainText()
            res = self.connection.cursor().execute(query).fetchall()
            # Заполним размеры таблицы
            self.tableWidget.setColumnCount(5)
            self.tableWidget.setRowCount(0)
            # Заполняем таблицу элементами
            for i, row in enumerate(res):
                self.tableWidget.setRowCount(
                    self.tableWidget.rowCount() + 1)
                for j, elem in enumerate(row):
                    self.tableWidget.setItem(
                        i, j, QTableWidgetItem(str(elem)))
        except Exception as e:
            self.Form.setText('Произошла ошибка, повторите запрос')

    def closeEvent(self, event):
        # при закрытии закрывается и соединение с бд
        self.connection.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
