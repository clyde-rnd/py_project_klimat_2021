import tkinter as tk
import sys
import glob
import serial
from tkinter import ttk

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    print("Список COM сформирован")
    print(result)
    return result

def chtenie_porta(select_com) :
   try:
       ser = serial.Serial(
           port=select_com,
           baudrate=9600,
           parity=serial.PARITY_ODD,
           stopbits=serial.STOPBITS_TWO,
           bytesize=serial.SEVENBITS, timeout=2
       )
       print(ser)
       x = ser.readline()
       print(x)
       x = list(str(x))
       print(x)
       ser.close()
       return x
   except (OSError, serial.SerialException) as osh:
       print(osh)
       pass

def sotr_temp_and_vlazh(spis, triger):
    param = None
    for i in spis:
        if i == triger:
            ind_t = spis.index(i)
            param = ''.join(spis[(ind_t + 2):(ind_t + 6)])
    print(param)
    return param

def draw_lable(text_param, color_lb, color_font, idex):
    lable = tk.Label(win, text=f"{text_param} {idex}",
                    bg=color_lb,
                    fg=color_font,
                    font=('Arial', 25, 'bold'),
                    )
    return lable

def vibor_com_porta():
    com_name = serial_ports()
    print(com_name, "тут")
    global combo_com
    global poumolchaniu_com
    try:
        select_com = combo_com.get()
        try:
            poumolchaniu_com = com_name.index(select_com)
        except ValueError:
            poumolchaniu_com = 0
    except AttributeError:
        select_com = "Не выбран"
    print(poumolchaniu_com, 'poumolchaniu_com')
    print(select_com, 'select_com')
    combo_com = ttk.Combobox(win, values=com_name, width=10, font=('Arial', 13))
    combo_com.current(poumolchaniu_com)
    combo_com.grid(row=0, column=0, stick='wens', padx=20, pady=10)


def remuve_lable():
    global lable_v
    global lable_t
    print(lable_t, lable_t)
    if lable_v and lable_t != None:
        lable_v.grid_forget()
        lable_t.grid_forget()

def nazhali_stop():
    global loopp
    remuve_lable()
    vibor_com_porta()
    start_stop_zhach.set(False)
    start_stop_text.set('Start')
    combo_com['state'] = 'NORMAL'
    print('Нажали кнопку STOP')
    if loopp:
        win.after_cancel(loopp)

def nazhali_start():
    global lable_v
    global lable_t
    select_com = combo_com.get()
    start_stop_text.set("Stop")
    combo_com['state'] = 'disabled'
    rezultat_chteniya_com = chtenie_porta(select_com)
    print(rezultat_chteniya_com, 'rezultat_chteniya_com')
    if rezultat_chteniya_com == None:
        nazhali_stop()
    else:
        if lable_v and lable_t != None:
            lable_v.grid_remove()
            lable_t.grid_remove()
        triger_t = '*'
        triger_v = '%'
        t = sotr_temp_and_vlazh(rezultat_chteniya_com, triger_t)
        v = sotr_temp_and_vlazh(rezultat_chteniya_com, triger_v)
        if t == None or v == None:
            nazhali_stop()
        else:
            t1 = float(t)
            v1 = float(v)
            if 26.0>t1>17.0:
                lable_t = draw_lable(t, color_lb_t, color_font, idex_t)
            elif t1>=26.00:
                lable_t = draw_lable(t, color_lb_t_2, color_font, idex_t)
            elif t1 <= 17.00:
                lable_t = draw_lable(t, color_lb_t_3, color_font, idex_t)
            if 80.0 > v1 > 20.0:
                lable_v = draw_lable(v, color_lb_v, color_font, idex_v)
            elif v1 >= 80.0:
                lable_v = draw_lable(v, color_lb_v_2, color_font, idex_v)
            elif v1 <= 20.0:
                lable_v = draw_lable(v, color_lb_v_3, color_font, idex_v)
            lable_t.grid(row=1, column=1, stick='wens', padx=20, pady=10)
            lable_v.grid(row=1, column=0, stick='wens', padx=20, pady=10)
            global loopp
            loopp = win.after(10000, checkbutton_start_stop)

def checkbutton_start_stop():
    """"
    Функция обрабатывает нажатие на кнопку старт\стоп

    Вызывая вункции nazhali_stop или nazhali_start
    """
    s = start_stop_zhach.get()
    print(s, 'Какая кнопка нажата сейчас')
    if s == False:
        nazhali_stop()
    elif s == True:
        nazhali_start()

poumolchaniu_com = 0
lable_t = None
lable_v = None
combo_com = None
loopp = None
idex_t = 'C°'
idex_v = '%'
color_lb_t = '#4BC98A'
color_lb_v = '#6CB1DE'
color_lb_t_2 = '#D0521D'
color_lb_v_2 = '#3053B6'
color_lb_t_3 = '#3261E1'
color_lb_v_3 = '#CA9443'
color_font = "#000000"
win = tk.Tk()
start_stop_text = tk.StringVar()
start_stop_text.set("Strart")
start_stop_zhach = tk.BooleanVar()
start_stop_zhach.set(False)
photo = tk.PhotoImage(file='icont.png')
win.title("Модуль климатического контроля ЛАЗ")
win.geometry('440x400+700+300')
win.resizable(False, False)
win.iconphoto(False, photo)
win.grid_columnconfigure(0, minsize=220)
win.grid_columnconfigure(1, minsize=220)
win.grid_rowconfigure(1, minsize=220)
win.grid_rowconfigure(0, minsize=10)

vibor_com_porta()
start_button = tk.Checkbutton(win, textvariable=start_stop_text,
                        variable = start_stop_zhach,
                        onvalue = True,
                        offvalue = False,
                        width=6,
                        highlightcolor='#1183CE', font=('Arial', 15, 'bold'),
                        indicatoron=0, command=checkbutton_start_stop)
start_button.grid(row=0, column=1, stick='w', padx=20, pady=10)

win.mainloop()