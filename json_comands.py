import json
def read_credentials(file_path):
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
def get_last_user_id (credentials_path):
        credentials = read_credentials(credentials_path)
        last_id=0
        for user in credentials:
            last_id=user.split('_')[1]
        return int(last_id)

def check_user(login, file_path):
    credentials = read_credentials(file_path)
    for user in credentials.values():
        if user['login'] == login:
            return False
    return True

def add_user (login,password,credentials_path):
    user =check_user(login,file_path=credentials_path)
    if not user :
        return False
    id = get_last_user_id(credentials_path)+1
    credentials= read_credentials(credentials_path)
    credentials[f'user_{id}']={"login": login, "password": password}
    with open(credentials_path,'w',) as file:
        json.dump(credentials ,file,indent=4)
    return True


