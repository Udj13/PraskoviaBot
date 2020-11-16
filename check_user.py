from conf import users

def check_user(id):
    for user in users:
        if user == id:
            return True
    return False


def security(user_id, text):
    if check_user(user_id):
        return text
    else:
        return 'Абырвалг'

