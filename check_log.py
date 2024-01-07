FLAG = False


# Проверка на то, что пользователь вошел в аккаунт прежде, чем пользоваться программой
def check_log(flag=False):
    if flag is True:
        global FLAG
        FLAG = True
    return
