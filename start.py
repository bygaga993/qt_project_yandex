import sqlite3

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QButtonGroup

import check_log
from StartWindow.password import CheckPassword

from StartWindow.random_generation import Generation


class StartWindow(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi("ui_files/startWindow.ui", self)
        self.con = sqlite3.connect("StartWindow/users.db")

        # Определение радио кнопок(Зарегестрироваться и войти) в группу,
        # Зарегестрироваться отмечена по умолчанию
        self.radioLogIn.setChecked(True)
        self.input = 1  # 0 - Зарегестрироваться, 1 - Войти
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.radioLogIn)
        self.button_group.addButton(self.radioSignIn)
        self.button_group.buttonClicked.connect(self.radio_button_clicked)

        self.nextButton.clicked.connect(self.start)

        self.passwordGeneration.clicked.connect(self.password_generation)
        self.loginGeneration.clicked.connect(self.login_generation)

    def start(self):
        cur = self.con.cursor()
        login = self.loginLine.text()
        password = self.PasswordLine.text()

        # проверка введен ли логин и пароль
        if login == '':
            self.labelstatus.setText('Введите логин')
            return
        elif password == '':
            self.labelstatus.setText('Введите пароль')
            return

        if self.input == 0:  # Если пользователь хочет войти
            self.labelstatus.setText('')
            # получение из БД логина и пароля по введеным данным
            result = cur.execute("SELECT * FROM users WHERE login = ?",
                                 (login,)).fetchone()
            if not result:
                self.labelstatus.setText('Пользователь не найден')
            else:
                if password != result[2]:
                    self.labelstatus.setText('Неверный пароль')
                else:
                    self.labelstatus.setText('Вход выполнен')
                    check_log.check_log(True)
        else:  # Если пользователь хочет зарегестрироваться
            if self.is_login_in_database(login) is True:
                self.labelstatus.setText('Пользователь с таким логином уже существует')
            else:
                status_pas = CheckPassword.check_pass(CheckPassword(password, login))
                self.labelstatus.setText(status_pas)
                if status_pas == 'Регистрация прошла успешна':
                    cur.execute("""INSERT INTO users(login, password) 
                            VALUES(?, ?)""", (login, password))
                    self.con.commit()

    def radio_button_clicked(self, button):  # Функция возвращающая выбранную кнопку
        if button.text() == 'Зарегистрироваться':
            self.input = 1
        else:
            self.loginLine.setText('')
            self.PasswordLine.setText('')
            self.input = 0

    def password_generation(self):
        #  получение сгенерированного пароля
        login = self.loginLine.text()
        self.PasswordLine.setText(str(Generation.password_generation(Generation(login))))

    def login_generation(self):
        #  получение сгенерированного логина
        g_log = str(Generation.final_login(Generation('')))
        while self.is_login_in_database(g_log) is True:
            g_log = str(Generation.final_login(Generation('')))
        self.loginLine.setText(g_log)

    def is_login_in_database(self, login):
        #  проверка наличия пользователя с таким логином
        cur = self.con.cursor()
        result = cur.execute("SELECT * FROM users WHERE login = ?",
                             (login,)).fetchone()
        if result:
            return True
        else:
            return False
