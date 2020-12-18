import pymysql

from core.app_config import *
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

import center_tk_window


class FormReport:
    btnSearch = None
    btnReset = None
    treeReport = None
    cbFilter = None
    txtSearch = None

    def __init__(self, tk_master):
        tk_master.geometry("710x500")
        tk_master.title("{} - Reportes".format(APP_NAME))
        center_tk_window.center_on_screen(tk_master)
        tk_master.resizable(0, 0)

        frameContainer__Filter = Frame(tk_master)




        frameContainer__Filter.grid(row=1, column=1, sticky="nw")
        lblFilter = Label(frameContainer__Filter, text="Opciones de filtrado:")
        lblFilter.grid(row=0, column=0, padx=(0, 500))

        self.txtSearch = Entry(frameContainer__Filter)
        self.txtSearch.insert(0, "Escriba palabra clave.")
        self.txtSearch.grid(row=0, column=0, padx=(200, 0))

        self.cbFilter = ttk.Combobox(frameContainer__Filter, state="readonly")
        self.cbFilter["values"] = ["Indistinto", "Numero de PIN", "Usuario", "Fecha"]
        self.cbFilter.grid(row=0, column=0, padx=(0, 150))

        self.btnSearch = Button(frameContainer__Filter, text="Buscar", command=lambda:self.loadSearchData())
        self.btnSearch.grid(row=0, column=0, padx=(450, 0))

        self.btnReset = Button(frameContainer__Filter, text="Restaurar", command=lambda:self.defaultLoadData())
        self.btnReset.grid(row=0, column=0, padx=(620, 0))

        frameTree = Frame(frameContainer__Filter)
        frameTree.grid(row=1, column=0)
        self.treeReport = ttk.Treeview(frameTree, height=22)
        self.treeReport["columns"] = ("one", "two", "three", "four", "five")
        self.treeReport.heading("one", text="ID")
        self.treeReport.heading("two", text="Num Pin")
        self.treeReport.heading("three", text="Valor")
        self.treeReport.heading("four", text="Usuario")
        self.treeReport.heading("five", text="Fecha")

        self.treeReport.column("one", width=50)
        self.treeReport.column("two", width=80)
        self.treeReport.column("three", width=80)
        self.treeReport.column("four", width=144)
        self.treeReport.column("five", width=150)
        self.treeReport.grid(row=0, column=0)

        self.defaultLoadData()

    def defaultLoadData(self):
        conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME, charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
        currentCursor = conn.cursor()
        query = "SELECT pinInfo.log_id, userInfo.user_name, pinInfo.pin_num, pinInfo.pin_value, pinInfo.created_at FROM user userInfo INNER JOIN log_pin pinInfo ON userInfo.user_id = pinInfo.user_id"
        currentCursor.execute(query)
        result = currentCursor.fetchall()
        self.treeReport.delete(*self.treeReport.get_children())

        for item in result:
            tmpValue = item['pin_value']
            if (tmpValue % 2 != 0):
                tmpValue = 1
            else:
                tmpValue = 0
            self.treeReport.insert('', 'end', values=(item['log_id'], item['pin_num'], tmpValue, item['user_name'], item['created_at']))

    def loadSearchData(self):
        if len(self.txtSearch.get()) == 0:
            messagebox.showerror(title="ERROR", message="Para poder filtrar debe escribir una o mas palabras claves.")
        else:
            conn = pymysql.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db=DB_NAME, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
            currentCursor = conn.cursor()
            self.treeReport.delete(*self.treeReport.get_children())

            if self.cbFilter.current() == -1:
                messagebox.showerror(title="ERROR", message="Para filtrar es necesario colocar un modo de filtro.")
            elif self.cbFilter.current() == 0:
                query = "SELECT pinInfo.log_id, userInfo.user_name AS userName, pinInfo.pin_num, pinInfo.pin_value, pinInfo.created_at FROM user userInfo INNER JOIN log_pin pinInfo ON userInfo.user_id = pinInfo.user_id WHERE pinInfo.log_id = {0} OR pinInfo.pin_num = {1} OR userName LIKE '%{2}%' OR pinInfo.pin_value = {3} OR pinInfo.created_at LIKE '%{4}%'".format(self.txtSearch.get(), self.txtSearch.get(), self.txtSearch.get(), self.txtSearch.get(), self.txtSearch.get())
                print(query)
                currentCursor.execute(query)
                result = currentCursor.fetchall()
                for item in result:
                    self.treeReport.insert('', 'end', values=(
                        item['log_id'], item['userName'], item['pin_num'], item['pin_value'], item['created_at']))
            elif self.cbFilter.current() == 1:
                query = "SELECT pinInfo.log_id, userInfo.user_name AS userName, pinInfo.pin_num, pinInfo.pin_value, pinInfo.created_at FROM user userInfo INNER JOIN log_pin pinInfo ON userInfo.user_id = pinInfo.user_id WHERE pinInfo.pin_num = {0}".format(self.txtSearch.get())
                print(query)
                currentCursor.execute(query)
                result = currentCursor.fetchall()
                for item in result:
                    self.treeReport.insert('', 'end', values=(
                        item['log_id'], item['userName'], item['pin_num'], item['pin_value'], item['created_at']))
            elif self.cbFilter.current() == 2:
                query = "SELECT pinInfo.log_id, userInfo.user_name AS userName, pinInfo.pin_num, pinInfo.pin_value, pinInfo.created_at FROM user userInfo INNER JOIN log_pin pinInfo ON userInfo.user_id = pinInfo.user_id WHERE userName LIKE '%{0}%'".format(self.txtSearch.get())
                print(query)
                currentCursor.execute(query)
                result = currentCursor.fetchall()
                for item in result:
                    self.treeReport.insert('', 'end', values=(
                        item['log_id'], item['userName'], item['pin_num'], item['pin_value'], item['created_at']))
            elif self.cbFilter.current() == 3:
                query = "SELECT pinInfo.log_id, userInfo.user_name AS userName, pinInfo.pin_num, pinInfo.pin_value, pinInfo.created_at FROM user userInfo INNER JOIN log_pin pinInfo ON userInfo.user_id = pinInfo.user_id WHERE pinInfo.created_at LIKE '%{0}%'".format(self.txtSearch.get())
                print(query)
                currentCursor.execute(query)
                result = currentCursor.fetchall()
                for item in result:
                    self.treeReport.insert('', 'end', values=(
                        item['log_id'], item['userName'], item['pin_num'], item['pin_value'], item['created_at']))
            else:
                print("xdd")