class CheckPassword:
    def __init__(self, password, login):
        self.login = login
        self.password = password
        # для проверки расположения букв на клавиатуре списки представлены в таком виде
        self.low_eng_1 = 'qwertyuiop'
        self.low_eng_2 = 'asdfghjkl'
        self.low_eng_3 = 'zxcvbnm'
        self.low_rus_1 = 'йцукенгшщзхъ'
        self.low_rus_2 = 'фывапролджэё'
        self.low_rus_3 = 'ячсмитьбю'
        self.symbols = '!"#$%& ()*+,-./:;<=>?@[]^_`{|}~'

    def check_pass(self):  # проверка надежности пароля
        password = self.password
        if len(password) < 9:
            return 'Пароль должен содержать не менее 9 символов'
        low = 0
        title = 0
        dig = 0
        symbols = 0
        # подсчет количества букв, цифр и иных символов в введенном пароле
        for el in password:
            if el.islower():
                low += 1
            elif el.istitle():
                title += 1
            elif el.isdigit():
                dig += 1
            elif el in self.symbols:
                symbols += 1
        if low == 0 or title == 0:
            return 'Пароль должен содержать символы разного регистра'
        if dig == 0:
            return 'Пароль должен содержать хотя бы одну цифру'
        if symbols == 0:
            return 'Пароль должен содержать хотя бы один из символов !"#$%& ()*+,-./:;<=>?@[]^_`{|}~'
        if ' ' in password:
            return 'Пароль не должен содержать пробелов'
        if self.login != '':  # проверка не корректна при генерации пароля, но в остальных случаях проверка осуществится
            if self.login in password:
                return 'Пароль не должен содержать в себе логин'
        for i in range(len(password) - 2):
            pas = password[i:i + 3]
            if (pas.lower() in self.low_eng_1 or pas.lower() in self.low_eng_2 or pas.lower() in self.low_eng_3
                    or pas.lower() in self.low_rus_1 or pas.lower() in self.low_rus_2 or pas.lower() in self.low_rus_3):
                return ('Пароле не должен содержать'
                        ' ни одной комбинации из 3 буквенных символов, стоящих рядом в строке клавиатуры')
        return 'Регистрация прошла успешна'  # проверка пароля последняя ступень при регистрации
