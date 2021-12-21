import argparse

from storage import Store

parser = argparse.ArgumentParser(description="KVStorager - key value storage on local files")
store = Store()
while True:
    args = input("Enter command: ").strip().split(' ')
    command = args[0]
    if command == 'help':
        print(" help - command info \n"
              " set <TABLE_NAME> <KEY> <VALUE> - set value in table \n"
              " get <TABLE_NAME> <KEY> - get value from table \n"
              " deltable <TABLE_NAME> - remove table with all his key \n"
              " exit - exit from live mode")
    elif command == 'exit':
        break
    elif command == 'set':
        table = store.make_table(args[1])
        store.set(table, args[2], args[3])
        print("Done")
    elif command == 'get':
        table = store.make_table(args[1])
        print(store.get(table, args[2]))
    elif command == 'deltable':
        table = store.make_table(args[1])
        store.del_table(table)
        print("Done")

