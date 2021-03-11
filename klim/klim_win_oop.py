import tkinter as tk
from check_serial_ports import serial_ports
from tkinter import ttk
import serial


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
        self.lable_t = False
        self.lable_v = False
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

    def chtenie_com_porta(self, select_com):
        try:
            serial_port_read = serial.Serial(
                port=select_com,
                baudrate=9600,
                parity=serial.PARITY_ODD,
                stopbits=serial.STOPBITS_TWO,
                bytesize=serial.SEVENBITS, timeout=1
            )
            print(serial_port_read)
            data_serial = serial_port_read.readline()
            print(data_serial)
            serial_port_read.close()
            return '_27.0_ b _45.0_'
        except (OSError, serial.SerialException) as oshimka_chteniya_com:
            print(oshimka_chteniya_com)
            return False

    def draw_lable(self, text_param, color_lb, color_font, idex):
        lable=tk.Label(self.win, text=f"{text_param} {idex}",
                         bg=color_lb,
                         fg=color_font,
                         font=('Arial', 25, 'bold'),
                 )
        return lable
    def destroy_lable(self):
        if self.lable_t and self.lable_t:
            self.lable_t.destroy()
            self.lable_v.destroy()
        else:
            pass

    def nazhali_stop(self):
        if self.loop_start_stop:
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
        self.select_com = self.combo_com.get()
        self.rezultat_chteniya_com = self.chtenie_com_porta(self.select_com)
        if self.rezultat_chteniya_com:
            sortirovka_rez_chten_com = self.rezultat_chteniya_com.split('_')
            print(sortirovka_rez_chten_com)
            if len(sortirovka_rez_chten_com) == 5:
                self.t = ''.join(sortirovka_rez_chten_com[1])
                self.v = ''.join(sortirovka_rez_chten_com[3])
                self.drow_lable_t_and_v()
            else:
                self.start_stop_zhach.set(False)
                self.nazhali_stop()
        else:
            self.start_stop_zhach.set(False)
            self.nazhali_stop()

    def drow_lable_t_and_v (self):
        idex_t = 'C°'
        idex_v = '%'
        color_lb_t = '#4BC98A'
        color_lb_v = '#6CB1DE'
        color_lb_t_2 = '#D0521D'
        color_lb_v_2 = '#3053B6'
        color_lb_t_3 = '#3261E1'
        color_lb_v_3 = '#CA9443'
        color_font = "#000000"
        t1 = float(self.t)
        v1 = float(self.v)
        if 26.0 > t1 > 17.0:
            self.lable_t = self.draw_lable(self.t, color_lb_t, color_font, idex_t)
        elif t1 >= 26.00:
            self.lable_t = self.draw_lable(self.t, color_lb_t_2, color_font, idex_t)
        elif t1 <= 17.00:
            self.lable_t = self.draw_lable(self.t, color_lb_t_3, color_font, idex_t)
        if 80.0 > v1 > 20.0:
            self.lable_v = self.draw_lable(self.v, color_lb_v, color_font, idex_v)
        elif v1 >= 80.0:
            self.lable_v = self.draw_lable(self.v, color_lb_v_2, color_font, idex_v)
        elif v1 <= 20.0:
            self.lable_v = self.draw_lable(v, color_lb_v_3, color_font, idex_v)
        self.lable_t.grid(row=1, column=1, stick='wens', padx=20, pady=10)
        self.lable_v.grid(row=1, column=0, stick='wens', padx=20, pady=10)




    def otslezhivanie_nazhatiya_start_stop(self):
        start_or_stop_zbach=self.start_stop_zhach.get()
        print(start_or_stop_zbach)
        if self.loop_start_stop:
            self.win.after_cancel(self.loop_start_stop)
        if start_or_stop_zbach:
            self.nazhali_start()
            if self.loop_start_stop:
                print(self.loop_start_stop)
            self.loop_start_stop = self.win.after(10000, self.otslezhivanie_nazhatiya_start_stop)
        else:
            self.nazhali_stop()

    def run(self):
        self.vibor_com_porta()
        self.button_start_stop_drow()
        self.win.mainloop()


if __name__ == "__main__":
    window = WindowKlim()
    window.run()