from core.app_config import *
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from core.classPin import *
from formLogin import *
from formReport import *

import center_tk_window

class FormArduino:
    txtHI = None
    txtMI = None
    txtHF = None
    txtMF = None
    statePin13 = None
    statePin12 = None
    statePin11 = None
    statePin8 = None
    statePin7 = None
    btnSave = None
    btnClear = None
    btnReport = None
    imageOn = None
    imageOff = None
    cbMode = None
    instanceForm = None
    handlePin = None

    def __init__(self, tk):
        self.instanceForm = tk
        tk.geometry("750x500")
        tk.config()
        tk.title(APP_NAME)
        center_tk_window.center_on_screen(tk)
        tk.resizable(0,0)

        self.imageOn = PhotoImage(file="core/img/on.png")
        self.imageOff = PhotoImage(file="core/img/off.png")

        frameContainer__Title = Frame(tk)
        frameContainer__Title.pack()

        lblTitle = Label(frameContainer__Title, text=APP_NAME, font="Arial 22 bold")
        lblTitle.pack(pady=50)

        frameContainer__State = Frame(tk)
        frameContainer__State.pack(fill=NONE, expand=False)

        self.statePin13 = Label(frameContainer__State, image=self.imageOn, text="image size 30x30")
        self.statePin12 = Label(frameContainer__State, image=self.imageOn, text="image size 30x30")
        self.statePin11 = Label(frameContainer__State, image=self.imageOn, text="image size 30x30")
        self.statePin8 = Label(frameContainer__State, image=self.imageOn, text="image size 30x30")
        self.statePin7 = Label(frameContainer__State, image=self.imageOn, text="image size 30x30")
        self.statePin13.grid(row=0, column=0)
        self.statePin12.grid(row=0, column=1)
        self.statePin11.grid(row=0, column=2)
        self.statePin8.grid(row=0, column=3)
        self.statePin7.grid(row=0, column=4)

        frame_container__input = Frame(tk)
        frame_container__input.pack(fill=NONE, expand=False, pady=2, ipady=3)

        lblHI = Label(frame_container__input, text="Hora inicial (HI):")
        lblMI = Label(frame_container__input, text="Minuto inicial (MI):")
        lblHF = Label(frame_container__input, text="Hora final (HF):")
        lblMF = Label(frame_container__input, text="Minuto final (MF):")
        lblMode = Label(frame_container__input, text="Modo:")

        lblHI.grid(row=0, column=0)
        lblMI.grid(row=1, column=0)
        lblHF.grid(row=2, column=0)
        lblMF.grid(row=3, column=0)
        lblMode.grid(row=4, column=0, pady=(5, 0))

        self.cbMode = ttk.Combobox(frame_container__input, state="readonly")
        self.cbMode["values"] = ["Normal", "Inverso"]
        self.cbMode.grid(row=4, column=1)

        self.txtHI = Entry(frame_container__input)
        self.txtMI = Entry(frame_container__input)
        self.txtHF = Entry(frame_container__input)
        self.txtMF = Entry(frame_container__input)

        self.txtHI.grid(row=0, column=1)
        self.txtMI.grid(row=1, column=1)
        self.txtHF.grid(row=2, column=1)
        self.txtMF.grid(row=3, column=1)

        self.btnSave = Button(frame_container__input, text="Guardar", command=lambda:self.saveCron())
        self.btnSave.grid(row=5, column=0)

        self.btnClear = Button(frame_container__input, text="Limpiar", command=lambda:self.clearInputText())
        self.btnClear.grid(row=5, column=1)

        self.btnReport = Button(frame_container__input, text="Reportes", command=lambda: self.openReport())
        self.btnReport.grid(row=5, column=2)

        self.btnReport = Button(frame_container__input, text="Apagar", command=lambda: self.OffLed())
        self.btnReport.grid(row=5, column=3)

        self.handlePin = Pin()
        self.handlePin.send(13, 8, False)
        self.handlePin.send(12, 6, False)
        self.handlePin.send(11, 4, False)
        self.handlePin.send(8, 2, False)
        self.handlePin.send(7, 0, False)
        self.updateForm()

    def OffLed(self):
        self.handlePin = Pin()
        self.handlePin.send(13, 8)
        self.handlePin.send(12, 6)
        self.handlePin.send(11, 4)
        self.handlePin.send(8, 2)
        self.handlePin.send(7, 0)

    def clearInputText(self):
        self.txtHI.delete(0, 'end')
        self.txtMI.delete(0, 'end')
        self.txtHF.delete(0, 'end')
        self.txtMF.delete(0, 'end')

    def openReport(self):
        newWindow = Toplevel()
        fReport = FormReport(newWindow)

    def saveCron(self):

        if len(self.txtHI.get()) == 0:
            messagebox.showerror(title="Informacion requerida", message="Es necesario llenar el campo hora fnicial")
        elif len(self.txtMI.get()) == 0:
            messagebox.showerror(title="Informacion requerida", message="Es necesario llenar el campo hora fnicial")
        elif len(self.txtHF.get()) == 0:
            messagebox.showerror(title="Informacion requerida", message="Es necesario llenar el campo hora final")
        elif len(self.txtMF.get()) == 0:
            messagebox.showerror(title="Informacion requerida", message="Es necesario llenar el campo minuto final")
        elif self.cbMode.current() == -1:
            messagebox.showerror(title="Informacion requerida", message="Es necesario seleccionar la modalidad.")
        else:

            if self.cbMode.current() == 0:
                self.handlePin.createTaskStandard(self.txtHI.get(), self.txtMI.get(), self.txtHF.get(), self.txtMF.get())
            elif self.cbMode.current() == 1:
                self.handlePin.createTaskeverse(self.txtHI.get(), self.txtMI.get(), self.txtHF.get(), self.txtMF.get())

            self.clearInputText()
            messagebox.showinfo(title="Tarea guardada", message="Se ha creado con exito el CRON.")

    def updateForm(self):
        fileStateLed13 = open("core/state/arduino_state_pin_13.txt", "r")
        fileStateLed12 = open("core/state/arduino_state_pin_12.txt", "r")
        fileStateLed11 = open("core/state/arduino_state_pin_11.txt", "r")
        fileStateLed8 = open("core/state/arduino_state_pin_8.txt", "r")
        fileStateLed7 = open("core/state/arduino_state_pin_7.txt", "r")

        for line in fileStateLed13:
            field = line.split("\n")
            statePin = field[0]
            if int(statePin) == 1:
                self.statePin13['image'] = self.imageOn
            else:
                self.statePin13['image'] = self.imageOff
        fileStateLed13.close()

        for line in fileStateLed12:
            field = line.split("\n")
            statePin = field[0]
            if int(statePin) == 1:
                self.statePin12['image'] = self.imageOn
            else:
                self.statePin12['image'] = self.imageOff
        fileStateLed12.close()

        for line in fileStateLed11:
            field = line.split("\n")
            statePin = field[0]
            if int(statePin) == 1:
                self.statePin11['image'] = self.imageOn
            else:
                self.statePin11['image'] = self.imageOff
        fileStateLed11.close()

        for line in fileStateLed8:
            field = line.split("\n")
            statePin = field[0]
            if int(statePin) == 1:
                self.statePin8['image'] = self.imageOn
            else:
                self.statePin8['image'] = self.imageOff
        fileStateLed8.close()

        for line in fileStateLed7:
            field = line.split("\n")
            statePin = field[0]
            if int(statePin) == 1:
                self.statePin7['image'] = self.imageOn
            else:
                self.statePin7['image'] = self.imageOff
        fileStateLed7.close()

        self.instanceForm.after(1000, self.updateForm)