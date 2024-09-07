from json import dumps, load


# 작성중
class FileHandle:
    def __init__(self):
        pass

    def read_keyfile(self):
        with open("AccessKeyInfo.json", 'r', encoding='utf-8') as file:
            _key_info = load(file)
        return _key_info

    def read_rolefile(self):
        with open("RoleSessionToken.json", 'r', encoding='utf-8') as file:
            _role_info = load(file)
        return _role_info

#    def append_rolefile(self):
#        with open("RoleSessionToken.json", 'a', encoding='utf-8') as file:
#            pass