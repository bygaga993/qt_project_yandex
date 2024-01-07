from random import randrange, choice

from StartWindow.password import CheckPassword


class Generation:
    def __init__(self, log):
        # логин нужен при генерации надежного пароля, чтобы исключить попадания логина в пароль
        self.login = log
        self.eng = 'qwertyuiopasdfghjklzxcvbnm'
        self.rus = 'йцукенгшщзхъфывапролджэёячсмитьбю'
        self.symbols = '!"#$%&()*+,-./:;<=>?@[]^_`{|}~'

    def password_generation(self):  # генерация символов/букв/цифр, которые будут входить в пароль
        pas = []
        #  генерация двух различных цифр
        dig1 = randrange(10)
        dig2 = randrange(10)
        while dig2 != dig1:
            dig2 = randrange(10)
        pas.append(dig1)
        pas.append(dig2)
        #  генерация двух различных символов
        symbols = [i for i in self.symbols]
        sym1 = choice(symbols)
        symbols.remove(sym1)
        sym2 = choice(symbols)
        pas.append(sym1)
        pas.append(sym2)
        #  генерация одной маленькой и одной заглавной русской буквы
        rus_alph = [i for i in self.rus]
        letter1 = choice(rus_alph).capitalize()
        rus_alph.remove(letter1.lower())
        pas.append(letter1)
        letter2 = choice(rus_alph).lower()
        pas.append(letter2)
        #  генерация одной маленькой и одной заглавной английской буквы
        eng_alph = [i for i in self.eng]
        letter3 = choice(eng_alph).capitalize()
        eng_alph.remove(letter3.lower())
        pas.append(letter3)
        letter4 = choice(eng_alph).lower()
        pas.append(letter4)
        #  добавление случайного количества символов/цифр/букв
        random_num = randrange(2, 5)
        for i in range(random_num):
            random_symbol = randrange(4)
            if random_symbol == 0:
                pas.append(randrange(10))
            elif random_symbol == 1:
                pas.append(choice([i for i in self.symbols]))
            elif random_symbol == 2:
                low_or_cap = randrange(2)
                if low_or_cap == 0:
                    pas.append((choice(rus_alph)).capitalize())
                else:
                    pas.append((choice(rus_alph)).lower())
            elif random_symbol == 3:
                low_or_cap = randrange(2)
                if low_or_cap == 0:
                    pas.append((choice(eng_alph)).capitalize())
                else:
                    pas.append((choice(eng_alph)).lower())

        password = final_pas(pas)
        status_pas = CheckPassword.check_pass(
            CheckPassword(password, self.login))  # проверка сгенерированного пароля на надежность
        while status_pas != 'Регистрация прошла успешна':
            password = final_pas(pas)
            status_pas = CheckPassword.check_pass(CheckPassword(password, self.login))
        return password

    def final_login(self):  # Создание логина(используются английские символы и цифры)
        final_login = ''
        eng_alph = [i for i in self.eng]
        for i in range(randrange(3, 8)):
            final_login += choice(eng_alph)
        for i in range(randrange(4)):
            final_login += str(randrange(10))
        return final_login


def final_pas(pasw):
    pas = pasw.copy()  # создание уже готового пароля, при перемешивании символов
    generation_password = ''
    for i in range(len(pas)):
        letter = choice(pas)
        generation_password += str(letter)
        pas.remove(letter)
    return generation_password
