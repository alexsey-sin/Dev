import os
import time
from datetime import datetime
from tkinter import *
# import tkinter as tk
import tkinter.ttk as ttk
from tkinter.ttk import Combobox
from tkinter.ttk import Progressbar
from tkinter import messagebox
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import ttk
from tkinter import Menu

# https://www.cyberforum.ru/python-db/thread2729424.html    SQlite + Tkinter приложение


window = Tk()
window.geometry('800x450')
window.title("Добро пожаловать в приложение PythonRu")

def clicked(): 
    res = f'Привет {txt.get()}'
    lbl.configure(text=res) 

def clicked2(): 
    # messagebox.showinfo('Заголовок', 'Текст')
    # messagebox.showwarning('Заголовок', 'Текст')  # показывает предупреждающее сообщение
    # messagebox.showerror('Заголовок', 'Текст')  # показывает сообщение об ошибке
    # res = messagebox.askquestion('Заголовок', 'Текст')  # yes/no
    # res = messagebox.askyesno('Заголовок', 'Текст')  # 1/0
    # res = messagebox.askyesnocancel('Заголовок', 'Текст')  # 1/0/None
    # res = messagebox.askokcancel('Заголовок', 'Текст')  # 1/0
    res = messagebox.askretrycancel('Заголовок', 'Текст')  #  1/0
    
    lbl.configure(text=res)

def clicked3():
    top = Toplevel(window)
    # top.geometry('400x250')
    print(window.winfo_x(), window.winfo_y())
    # file = filedialog.askopenfilename()
    # files = filedialog.askopenfilenames()
    w = window.winfo_screenwidth()
    h = window.winfo_screenheight()
    w = w//2 # середина экрана
    h = h//2 
    w = w - 200 # смещение от середины
    h = h - 200
    top.geometry('400x250+{}+{}'.format(w, h))
    button_top_level = Button(top, text='Нажми', command=lambda: lbl.config(text='Текст из модального окна')).pack()
    top.transient(window)
    top.grab_set()
    top.focus_set()
    top.wait_window()


def go_exit(): exit(0)
class Table(Frame):
    def __init__(self, parent=None, headings=tuple(), rows=tuple()):
        super().__init__(parent)

        table = ttk.Treeview(self, show="headings", selectmode="browse")
        table["columns"]=headings
        table["displaycolumns"]=headings

        for head in headings:
            table.heading(head, text=head, anchor=CENTER)
            table.column(head, anchor=CENTER)

        for row in rows:
            table.insert('', END, values=tuple(row), tag='gray')

        table.tag_configure('gray', background='#c1c4c5')
        scrolltable = Scrollbar(self, command=table.yview)
        table.configure(yscrollcommand=scrolltable.set)
        scrolltable.pack(side=RIGHT, fill=Y)
        table.pack(expand=YES, fill=BOTH, padx=5,pady=5)


menu = Menu(window)
new_item = Menu(menu, tearoff=0)  
new_item.add_command(label='Новый')
new_item.add_separator()  
new_item.add_command(label='Изменить', command=clicked) 
new_item.add_separator()  
new_item.add_command(label='Выход', command=go_exit) 
menu.add_cascade(label='Файл', menu=new_item)
window.config(menu=menu)

tab_control = ttk.Notebook(window)  
tab1 = ttk.Frame(tab_control)  
tab2 = ttk.Frame(tab_control)  
tab3 = ttk.Frame(tab_control)  
tab4 = ttk.Frame(tab_control)  
tab_control.add(tab1, text='Первая')  
tab_control.add(tab2, text='Вторая')  
tab_control.add(tab3, text='Остальное')  
tab_control.add(tab4, text='Таблица')  
lbl1 = Label(tab1, text='Вкладка 1', padx=5, pady=5)  
lbl1.grid(column=0, row=0)  
lbl2 = Label(tab2, text='Вкладка 2', padx=5, pady=5)  
lbl2.grid(column=0, row=0)  



lbl = ttk.Label(tab3, text="Привет", font=("Arial Bold", 20))
lbl.grid(column=0, row=0)
txt = ttk.Entry(tab3,width=10, state='disabled')  
txt.grid(column=1, row=0) 
btn = ttk.Button(tab3, text="Не нажимать!", command=clicked)
btn.grid(column=2, row=0)
txt.focus()
combo = ttk.Combobox(tab3)
combo['values'] = (1, 2, 3, 4, 5, "Текст")
combo.current(3)  # установите вариант по умолчанию
combo.grid(column=0, row=1)

btn2 = ttk.Button(tab3, text="messagebox!", command=clicked2)
btn2.grid(column=1, row=1)

var = IntVar()
var.set(36)
spin = ttk.Spinbox(tab3, from_=0, to=100, width=5, textvariable=var)
spin.grid(column=2, row=1)

# bar = Progressbar(tab3, length=200)
bar = Progressbar(tab3, length=200, style='black.Horizontal.TProgressbar')
bar['value'] = 70
style = ttk.Style()
style.theme_use('default')  
style.configure("black.Horizontal.TProgressbar", background='green')
bar.grid(column=0, row=2)

btn3 = Button(tab3, text='File dialog', command=clicked3)
btn3.grid(column=1, row=2)

stxt = scrolledtext.ScrolledText(tab3,width=40,height=10)
stxt.grid(column=2, row=2) 
table = Table(tab4, headings=('aaa', 'bbb', 'ccc'), rows=((123, 456, 789), ('abc', 'def', 'ghk'), (123, 456, 789), ('abc', 'def', 'ghk'), (123, 456, 789), ('abc', 'def', 'ghk')))
table.pack(expand=YES, fill=BOTH)

tab_control.pack(expand=1, fill='both')

window.mainloop()


    
# # личный бот @infra     TELEGRAM_CHAT_ID, TELEGRAM_TOKEN
# TELEGRAM_CHAT_ID = '1740645090'
# TELEGRAM_TOKEN = '2009560099:AAHtYot6EOHh_qr9EUoCoczQhjyRdulKHYo'

# PERIOD_BETWEEN = 2

# if __name__ == '__main__':
    # while True:
        # #===============================================#

    #####################################################
# import tkinter as tk
# import tkinter.ttk as ttk






# from tkinter import ttk
# from tkinter import *
# root = Tk () # объявление исходного ящика
 # columns = ("имя", "IP-адрес")
 # treeview = ttk.Treeview (корень, высота = 18, show = "заголовки", столбцы = столбцы) # таблица
 
 # treeview.column («Имя», ширина = 100, якорь = «центр») # обозначает столбец, не отображаемый
 # treeview.column («IP-адрес», ширина = 300, якорь = «центр»)
 
 # treeview.heading ("Name", text = "Name") # показать заголовок таблицы
 # treeview.heading («IP-адрес», текст = «IP-адрес»)
 
# treeview.pack(side=LEFT, fill=BOTH)
 
 # name = ['Computer1', 'Server', 'Notebook']
# ipcode = ['10.13.71.223','10.25.61.186','10.25.11.163']
 # для i в диапазоне (min (len (имя), len (ipcode))): # запись данных
    # treeview.insert('', i, values=(name[i], ipcode[i]))
 
 
 # def treeview_sort_column (tv, col, reverse): # просмотр дерева, имя столбца, расположение
    # l = [(tv.set(k, col), k) for k in tv.get_children('')]
         # l.sort (reverse = reverse) # метод сортировки
    # # rearrange items in sorted positions
         # для индекса (val, k) в перечислении (l): # переместиться в соответствии с индексом после сортировки
        # tv.move(k, '', index)
         # tv.heading (col, command = lambda: treeview_sort_column (tv, col, not reverse)) # Переписать заголовок, чтобы сделать его заголовком наоборот
 
 # def set_cell_value (событие): # Двойной щелчок для входа в состояние редактирования
    # for item in treeview.selection():
        # #item = I001
        # item_text = treeview.item(item, "values")
                 # #print (item_text [0: 2]) # распечатать значение выбранной строки
         # column = treeview.identify_column (event.x) # столбец
         # row = treeview.identify_row (event.y) # row
    # cn = int(str(column).replace('#',''))
    # rn = int(str(row).replace('I',''))
    # entryedit = Text(root,width=10+(cn-1)*16,height = 1)
    # entryedit.place(x=16+(cn-1)*130, y=6+rn*20)
    # def saveedit():
        # treeview.set(item, column=column, value=entryedit.get(0.0, "end"))
        # entryedit.destroy()
        # okb.destroy()
    # okb = ttk.Button(root, text='OK', width=4, command=saveedit)
    # okb.place(x=90+(cn-1)*242,y=2+rn*20)
 
# def newrow():
         # name.append («Быть ​​названным»)
    # ipcode.append('IP')
    # treeview.insert('', len(name)-1, values=(name[len(name)-1], ipcode[len(name)-1]))
    # treeview.update()
    # newb.place(x=120, y=(len(name)-1)*20+45)
    # newb.update()
 
 # treeview.bind ('<Double-1>', set_cell_value) # Дважды нажмите левую кнопку, чтобы войти в редактирование
 # newb = ttk.Button (root, text = 'New Contact', width = 20, command = newrow)
# newb.place(x=120,y=(len(name)-1)*20+45)
 
 
 # для столбца в столбцах: функция # bind для сортировки заголовка
    # treeview.heading(col, text=col, command=lambda _col=col: treeview_sort_column(treeview, _col, False))
# '''
 # 1. Пройдите через стол
# t = treeview.get_children()
# for i in t:
    # print(treeview.item(i,'values'))
 # 2. Обязательный клик, чтобы покинуть событие
 # def treeviewClick (событие): # клик
    # for item in tree.selection():
        # item_text = tree.item(item, "values")
                 # print (item_text [0: 2]) # распечатать значение первого столбца выбранной строки
# tree.bind('<ButtonRelease-1>', treeviewClick)  
# ------------------------------
 # Щелкните левой кнопкой мыши и нажмите 1 / Button-1 / ButtonPress-1
 # Щелкните левой кнопкой мыши, чтобы выпустить ButtonRelease-1
 # Щелчок правой кнопкой мыши 3
 # Дважды щелкните Double-1 / Double-Button-1 левой кнопкой мыши
 # Щелкните правой кнопкой мыши Double-3
 # Колесо мыши нажмите 2
 # Колесо мыши, двойной щелчок, Double-2
 # Движение мыши B1-Motion
 # Наведите курсор мыши на область Enter
 # Мышь покинуть область Выйти
 # Получить фокус клавиатуры
 # Потерял фокус клавиатуры
 # Ключевое событие
 # Введите ключ Вернуться
 # Контроль размера изменения
# ------------------------------
# '''
 
 # root.mainloop () # войти в цикл сообщений
 

# Как сделать модальное окно в tkinter

# При помощи функции grab_set мы передаем поток данному виджету т.е. делаем его модальным(нельзя переключиться на главное окно).
# При помощи функции focus_set() мы фокусируем наше приложение на окне top, а при помощи функции wait_window() мы задаем приложению команду, что пока не будет закрыто окно top пользоваться другим окном будет нельзя. При помощи transient(root) можно убарть кнопки свернуть/развернуть, а так же расширить экран благодаря чему получим простое модальное диалоговое окно.

 # from tkinter import Tk, Toplevel, Button, Label
# def func():
    # top = Toplevel(root)
    # button_top_level = Button(top, text='Нажми', command=lambda: label.config(text='Текст из модального окна')).pack()
    # top.transient(root)
    # top.grab_set()
    # top.focus_set()
    # top.wait_window()
# root = Tk()
# label = Label(root, text='Текст')
# label.pack()
# button = Button(root, text='openModal', command=func).pack()
# root.mainloop()