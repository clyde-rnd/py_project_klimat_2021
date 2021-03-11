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
        self.lable1=False
        self.loop_start_stop=False

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
                                      indicatoron=0, command=self.otslezhivanie_nazhatiya_start_stop)
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

    def draw_lable(self, text_param, color_lb, color_font, idex):
        lable=tk.Label(self.win, text=f"{text_param} {idex}",
                         bg=color_lb,
                         fg=color_font,
                         font=('Arial', 25, 'bold'),
                 )
        return lable
    def destroy_lable(self):
        if self.lable1:
            self.lable1.destroy()
        else:
            pass

    def nazhali_stop(self):
        self.win.after_cancel(self.loop_start_stop)
        self.destroy_lable()
        self.vibor_com_porta()
        self.start_stop_text.set('Start')
        self.combo_com['state'] = 'NORMAL'
        print('Нажали кнопку STOP')

    def nazhali_start(self):
        self.destroy_lable()
        self.start_stop_text.set("Stop")
        self.combo_com['state'] = 'disabled'
        self.lable1 = self.draw_lable("Мой лйбл", '#4BC98A', "#000000", "27")
        self.lable1.grid(row=1, column=0, stick='wens', padx=20, pady=10)
        print('Нажали кнопку START')
        if self.loop_start_stop:
            print(self.loop_start_stop)
        self.loop_start_stop = self.win.after(10000, self.otslezhivanie_nazhatiya_start_stop)

    def otslezhivanie_nazhatiya_start_stop(self):
        start_or_stop_zbach=self.start_stop_zhach.get()
        print(start_or_stop_zbach)
        if start_or_stop_zbach:
            self.nazhali_start()
        else:
            self.nazhali_stop()


    def run(self):
        self.vibor_com_porta()
        self.button_start_stop_drow()
        self.win.mainloop()


if __name__ == "__main__":
    window = WindowKlim()
    window.run()