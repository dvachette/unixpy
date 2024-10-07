import os
from .unixsys import Root
import pickle
import sys


def chose_instance():
    instances = [
        filename
        for filename in os.listdir('instances')
        if filename.endswith('.unyx')
    ]
    print('Choose an instance:')
    for i, instance in enumerate(instances):
        print(f'{i+1}. {instance}')
    while True:
        choice = input('Enter the number of the instance you want to use: ')
        if choice.isdigit() and 0 < int(choice) <= len(instances):
            return instances[int(choice)-1]
        else:
            print('Invalid input')


def create_instance():
    instance = Root()
    name = input('Enter the name of the instance: ')
    os.system(f'touch instances/{name}.unyx')
    try:
        with open(path := f'instances/{name}.unyx', 'wb') as f:
            pickle.dump(instance, f)
    except OSError as e:
        print(f'Invalid name {e}')
        return create_instance()
    except EOFError:
        sys.exit()
    return path

def delete_instance():
    instance = chose_instance()
    os.remove(f'instances/{instance}')
    print(f'{instance} has been deleted')

def start():
    print('1. Create a new instance')
    print('2. Use an existing instance')
    print('3. Delete an instance')
    choice = str()
    while choice not in ['1', '2', '3']:
        choice = input('Enter the number of the option you want to use: ')
        if choice == '1':
            return create_instance()
        elif choice == '2':
            return f'instances/{chose_instance()}'
        elif choice == '3':
            delete_instance()
        else:
            print('Invalid input')
