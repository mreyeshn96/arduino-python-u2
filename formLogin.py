from core.app_config import *
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from core.classLogin import *
import center_tk_window
from formArduino import *


class FormLogin:
    txtUsername = None
    txtPassword = None
    btnLogin = None
    handleLogin = None
    __valPassword = None
    instanceForm = None
    Controller = None

    def __init__(self, tk_master):
        self.instanceForm = tk_master
        tk_master.geometry("300x80")
        tk_master.title("{} - Inicio de sesion".format(APP_NAME))
        center_tk_window.center_on_screen(tk_master)
        tk_master.resizable(0,0)
        self.handleLogin = LoginController()
        self.__valPassword = StringVar()

        lblUsername = Label(tk_master, text="Nombre de usuario:")
        lblUsername.grid(row=0, column=0)
        self.txtUsername = Entry(tk_master)
        self.txtUsername.grid(row=0, column=1)

        lblPassword = Label(tk_master, text="Contraseña:")
        lblPassword.grid(row=1, column=0)
        self.txtPassword = Entry(tk_master, show="*", textvariable=self.__valPassword)
        self.txtPassword.grid(row=1, column=1)

        self.btnLogin = Button(tk_master, text="Entrar", command=lambda:self.actionLogin())
        self.btnLogin.grid(row=2, column=0)

    def actionLogin(self):
        if self.handleLogin.check(self.txtUsername.get(), self.txtPassword.get()):
            messagebox.showinfo(title="Informacion", message="Se ha iniciado sesion correctamente.")
            newWindow = Toplevel()
            fArduino = FormArduino(newWindow)

        else:
            messagebox.showerror(title="ERROR", message="El nombre de usuario o conttaseña son incorrectos.")
