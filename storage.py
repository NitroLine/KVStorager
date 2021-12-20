import json
import os
from timeit import default_timer
from collections import defaultdict
from functools import partial


class Table:
    def __init__(self, name, filename):
        self.name = name
        self.filename = filename


class Store:
    DEFAULT_PATH = ''

    def __init__(self, path=DEFAULT_PATH):
        self.path = path
        self.global_record = {}
        self.record_d = defaultdict(partial(defaultdict, defaultdict))  # infinitely deep
        self.format = '.json'

    def make_table(self, table_name: str):
        if table_name not in self.global_record:
            filepath = os.path.join(self.path, table_name + self.format)
            fp = open(filepath, "a+")
            self.global_record[table_name] = Table(table_name, filepath)
            fp.close()
        return self.global_record[table_name]

    def del_table(self, table: Table):
        table_name = table.name
        del self.global_record[table_name]

    def set(self, table: Table, key: str, value: any):
        key = key[:32]
        table_name = table.name
        self.record_d[table_name][key] = value
        fp = open(table.filename, "w")
        data = self.record_d[table_name]
        json.dump(data, fp, indent=2)
        fp.close()

    def get(self, table: Table, key: str):
        data = json.loads(open(table.filename).read())
        return data[key]

if __name__ == '__main__':
    store = Store()
    newrecord = store.make_table("new record")
    start = default_timer()
    store.set(newrecord, "u1", {"name": "Darshan"})
    print(store.get(newrecord, "u1"))
    store.set(newrecord, "utka", {"name": "SOME_MORE_THIBG"})
    store.set(newrecord, "utka", {"name": "SOME_MORE_THIBG"})
    print(default_timer() - start)

