import tkinter as tk
from check_serial_ports import serial_ports
from tkinter import ttk


class WindowKlim:

    def __init__(self, imag='icont.png'):
        self.win = tk.Tk()
        self.win.geometry('440x400+700+300')
        self.win.resizable(False, False)
        self.win.title("Модуль климатического контроля ЛАЗ")
        try:
            self.photo = tk.PhotoImage(file=imag)
            self.win.iconphoto(False, self.photo)
        except Exception:
            pass
        self.win.grid_columnconfigure(0, minsize=220)
        self.win.grid_columnconfigure(1, minsize=220)
        self.win.grid_rowconfigure(1, minsize=220)
        self.win.grid_rowconfigure(0, minsize=10)

    def button_start_stop_drow(self):
        self.start_stop_text = tk.StringVar()
        self.start_stop_text.set("Strart")
        self.start_stop_zhach = tk.BooleanVar()
        self.start_stop_zhach.set(False)
        self.start_button = tk.Checkbutton(self.win, textvariable=self.start_stop_text,
                                      variable=self.start_stop_zhach,
                                      onvalue=True,
                                      offvalue=False,
                                      width=6,
                                      highlightcolor='#1183CE', font=('Arial', 15, 'bold'),
                                      indicatoron=0)
        self.start_button.grid(row=0, column=1, stick='w', padx=20, pady=10)

    def vibor_com_porta(self):
        self.poumolchaniu_com = 0
        self.com_name = serial_ports()
        try:
            self.select_com = self.combo_com.get()
            try:
                self.poumolchaniu_com = self.com_name.index(self.select_com)
            except ValueError:
                self.poumolchaniu_com = 0
        except AttributeError:
            self.select_com = "Не выбран"
        self.combo_com = ttk.Combobox(self.win, values=self.com_name, width=10, font=('Arial', 13))
        self.combo_com.current(self.poumolchaniu_com)
        self.combo_com.grid(row=0, column=0, stick='wens', padx=20, pady=10)

    def run(self):
        self.vibor_com_porta()
        self.button_start_stop_drow()
        self.start_stop_zhach.get()
        print(self.start_stop_zhach.get())
        self.win.mainloop()

if __name__ == "__main__":
    window = WindowKlim()
    window.run()