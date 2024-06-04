from json import dumps, load

# 작성중
class FileHandle:
    def __init__(self, kind):
        self._file = kind

    def read_file(self):
        with open("Access"+self._file+"Info.json", 'r', encoding='utf-8') as file:
            _keyinfo = load(file)
        return _keyinfo

    def append_file(self):
        with open("Access"+self._file+"Info.json", 'a', encoding='utf-8') as file:

tmp = FileHandle('key')
print(tmp.read_file())
