import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import ttk
import pickle
import os
from .unixsys import Root
def select_instance():
    system = None
    root = tk.Tk()
    root.title('Unyx Starter')
    root.geometry('400x400')
    root.resizable(False, False)
    liste = os.listdir('instances')

    instanceslist = [file.split(".")[:-1] for file in liste if file.endswith('.unyx')]
    instances = ttk.Combobox(root, values=instanceslist)
    instances.pack()
    instances.set('Select Instance')
    def new_instance():
        name = simpledialog.askstring('New Instance', 'Enter a name for the new instance')
        if name:
            system = Root()
            with open(os.path.join('instances', name+'.unyx'),'wb') as f:
                pickle.dump(system, f)
            instanceslist.append(name)
            instances['values'] = instanceslist
            instances.set(name)
    def start():
        nonlocal system
        if instances.get() == 'Select Instance':
            messagebox.showinfo('Error', 'Please select an instance')
        else:
            system = os.path.join('instances', instances.get()+'.unyx')
            root.destroy()
    def delete_instance():
        name = instances.get()
        if name == 'Select Instance':
            messagebox.showinfo('Error', 'Please select an instance')
        else:
            if messagebox.askokcancel('Delete Instance', f'Are you sure you want to delete {name}?'):
                os.remove(os.path.join('instances', name+'.unyx'))
                instanceslist.remove(name)
                instances['values'] = instanceslist
                instances.set('Select Instance')
    deletebutton = tk.Button(root, text='Delete Instance', command=delete_instance)
    deletebutton.pack()
    newbutton = tk.Button(root, text='New Instance', command=new_instance)
    newbutton.pack()
    startbutton = tk.Button(root, text='Start', command=start)
    startbutton.pack()
    root.mainloop()
    return system
