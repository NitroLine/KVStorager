import json
import os
from timeit import default_timer
from collections import defaultdict
from functools import partial


class Table:
    def __init__(self, name, filename, is_exist):
        self.is_exist = is_exist
        self.name = name
        self.filename = filename


class Store:
    DEFAULT_PATH = ''

    def __init__(self, path=DEFAULT_PATH, is_live = True):
        self.path = path
        self.global_record = {}
        self.record_d = defaultdict(partial(defaultdict, defaultdict))  # infinitely deep
        self.format = '.json'
        self.is_live = is_live

    def make_table(self, table_name: str):
        if table_name not in self.global_record:
            filepath = os.path.join(self.path, table_name + self.format)
            is_exist = False
            if os.path.isfile(filepath):
                is_exist = True
                fp = open(filepath, "r")
                self.record_d[table_name] = json.load(fp)
                fp.close()
            self.global_record[table_name] = Table(table_name, filepath, is_exist)
        return self.global_record[table_name]

    def del_table(self, table: Table):
        table_name = table.name
        if table.is_exist:
            os.remove(table.filename)
            table.is_exist = False
        del self.global_record[table_name]

    def save(self, table):
        fp = open(table.filename, "w")
        self.global_record[table.name].is_exist = True
        data = self.record_d[table.name]
        json.dump(data, fp, indent=2)
        fp.close()

    def set(self, table: Table, key: str, value: any):
        key = key[:32]
        table_name = table.name
        self.record_d[table_name][key] = value
        self.save(table)

    def get(self, table: Table, key: str):
        if not table.is_exist:
            raise KeyError("Table not exist.")
        if not self.is_live:
            data = json.load(open(table.filename))
            return data[key]
        else:
            return self.record_d[table.name][key]

if __name__ == '__main__':
    store = Store()
    newrecord = store.make_table("new record")
    start = default_timer()
    store.set(newrecord, "u1", {"name": "Darshan"})
    print(store.get(newrecord, "u1"))
    store.set(newrecord, "utka", {"name": "SOME_MORE_THIBG"})
    store.set(newrecord, "utka", {"name": "SOME_MORE_THIBG"})
    print(default_timer() - start)

