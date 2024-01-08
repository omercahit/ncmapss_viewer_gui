#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
import os
import h5py
import numpy as np
import pandas as pd
from pandas import DataFrame
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from tkinter import ttk
import matplotlib.pyplot as plt

root = tk.Tk()
root.geometry("1920x1080")
root.attributes("-fullscreen",True)

LARGEFONT = ("Verdana", 35)

W_var = ""
X_s_var = ""
X_v_var = ""
T_var = ""
A_var = ""
                      
W = ""
X_s = ""
X_v = "" 
T = ""
Y = ""
A = ""

class tkinterApp(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, Page1, Page2, Page3, Page4, Page5, Page6):
            frame = F(container, self)
            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, width = 1920, height = 1080, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand = True)

        button1 = tk.Button(self, text="Exit", fg="white", bg="red", 
                            font=("Verdana",18), pady=10, width=18,
                            command=root.destroy)
        self.button1_canvas = self.canvas.create_window(1860, 1080*0.92, anchor="ne",window=button1)

        self.button2 = tk.Button(self, text="Başla", fg="black", bg="lightgray",
                                 font=("Verdana", 24), padx=30, pady=10,
                                 command=lambda: controller.show_frame(Page1))
        self.button2.place(relx=0.5, rely=0.5, anchor="center")


class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, width = 1920, height = 1080, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand = True)
        
        button1 = tk.Button(self, text="Exit", fg="white", bg="red", 
                            font=("Verdana",18), pady=10, width=18,
                            command=root.destroy)
        self.button1_canvas = self.canvas.create_window(1860, 1080*0.92, anchor="ne",window=button1)

        self.docs = []
        for i in os.listdir():
            if i.endswith('.h5'):
                self.docs.append(os.path.join(i))
            
        docs_var = tk.StringVar(value = self.docs)
        self.doclist = tk.Listbox(self, height=5, width=35, listvariable=docs_var, font=("Verdana", 12))
        self.doclist.place(relx=0.2, rely=0.1, anchor="e")
        
        scroll = tk.Scrollbar(self, orient="vertical", command=self.doclist.yview)
        scroll.place(relx=0.2, rely=0.1, anchor="w", height=100)
        self.doclist['yscrollcommand'] = scroll.set

        self.doclist.bind('<<ListboxSelect>>', self.on_select)
        self.selected_file = ""

        self.button_load_data = tk.Button(self, text="Load Data",fg="black", bg="lightgray",
                                          font=("Verdana", 24), padx=90,
                                          command=self.open_selected)
        self.button_load_data.place(relx=0.21, rely=0.2, anchor="e")


        self.button_auxiliary = tk.Button(self, text="Auxiliary Information", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=30,
                                 command=lambda: controller.show_frame(Page2))
        self.button_auxiliary.place(relx=0.5, y=200, anchor="center")

        self.button_operative = tk.Button(self, text="Operative Conditions", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=30,
                                 command=lambda: controller.show_frame(Page3))
        self.button_operative.place(relx=0.5, y=300, anchor="center")

        self.button_sensor_readings = tk.Button(self, text="Sensor Readings", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=30,
                                 command=lambda: controller.show_frame(Page4))
        self.button_sensor_readings.place(relx=0.5, y=400, anchor="center")

        self.button_virtual = tk.Button(self, text="Virtual Sensors", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=30,
                                 command=lambda: controller.show_frame(Page5))
        self.button_virtual.place(relx=0.5, y=500, anchor="center")

        self.button_health_state = tk.Button(self, text="Health State", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=30,
                                 command=lambda: controller.show_frame(Page6))
        self.button_health_state.place(relx=0.5, y=600, anchor="center")

        

    def on_select(self, event):
        index=self.doclist.curselection()[0]
        self.selected_file = self.docs[index]

    def open_selected(self):
        self.data_loader(self.selected_file)

    def data_loader(self, filename):
        global W_var, X_s_var, X_v_var, T_var, A_var
        global W, X_s, X_v, T, Y, A

        with h5py.File(filename, 'r') as hdf:
            # Development set
            W_dev = np.array(hdf.get('W_dev'))             # W
            X_s_dev = np.array(hdf.get('X_s_dev'))         # X_s
            X_v_dev = np.array(hdf.get('X_v_dev'))         # X_v
            T_dev = np.array(hdf.get('T_dev'))             # T
            Y_dev = np.array(hdf.get('Y_dev'))             # RUL  
            A_dev = np.array(hdf.get('A_dev'))             # Auxiliary

            # Test set
            W_test = np.array(hdf.get('W_test'))           # W
            X_s_test = np.array(hdf.get('X_s_test'))       # X_s
            X_v_test = np.array(hdf.get('X_v_test'))       # X_v
            T_test = np.array(hdf.get('T_test'))           # T
            Y_test = np.array(hdf.get('Y_test'))           # RUL  
            A_test = np.array(hdf.get('A_test'))           # Auxiliary
            
            # Varnams
            W_var = np.array(hdf.get('W_var'))
            X_s_var = np.array(hdf.get('X_s_var'))  
            X_v_var = np.array(hdf.get('X_v_var')) 
            T_var = np.array(hdf.get('T_var'))
            A_var = np.array(hdf.get('A_var'))
            
            # from np.array to list dtype U4/U5
            W_var = list(np.array(W_var, dtype='U20'))
            X_s_var = list(np.array(X_s_var, dtype='U20'))  
            X_v_var = list(np.array(X_v_var, dtype='U20')) 
            T_var = list(np.array(T_var, dtype='U20'))
            A_var = list(np.array(A_var, dtype='U20'))
                          
        W = np.concatenate((W_dev, W_test), axis=0)  
        X_s = np.concatenate((X_s_dev, X_s_test), axis=0)
        X_v = np.concatenate((X_v_dev, X_v_test), axis=0)
        T = np.concatenate((T_dev, T_test), axis=0)
        Y = np.concatenate((Y_dev, Y_test), axis=0) 
        A = np.concatenate((A_dev, A_test), axis=0) 

class Page2(tk.Frame):
    def __init__(self, parent, controller):
        global A, A_var

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, width = 1920, height = 1080, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand = True)

        button1 = tk.Button(self, text="Exit", fg="white", bg="red", 
                            font=("Verdana",18), pady=10, width=18,
                            command=root.destroy)
        self.button1_canvas = self.canvas.create_window(1860, 1080*0.92, anchor="ne",window=button1)

        self.button2 = tk.Button(self, text="Back to Home", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=18,
                                 command=lambda: controller.show_frame(Page1))
        self.button2.place(x=1860, y=1080*0.85, anchor="ne")

        self.button3 = tk.Button(self, text="Get Auxiliary\nInformation Describe", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=20,
                                 command=self.get_A)
        self.button3.place(x=1860, y=25, anchor="ne")

        self.info_text = tk.Label(self, text="", bg="black", fg="white", font=("Verdana", 12))
        self.info_text.place(x=960, y=20, anchor="n")

        self.draw_button = tk.Button(self, text="Plot Flight Classes", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=20, state="disabled",
                                 command=self.draw_Fc)
        self.draw_button.place(x=1860, y=140, anchor="ne")

        self.eof_button = tk.Button(self, text="Get End Of Failures", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=20, state="disabled",
                                 command=self.get_eof)
        self.eof_button.place(x=1860, y=230, anchor="ne")

        self.eof_text = tk.Label(self, text="", bg="black", fg="white", font=("Verdana", 12))
        self.eof_text.place(x=960, y=800, anchor="n")

    def get_A(self):
        self.df_A = DataFrame(data=A, columns=A_var)
        self.info_text.configure(text=(str(self.df_A.describe())+"\n\nEngine units: "+str(np.unique(self.df_A['unit']))))
        self.draw_button.configure(state="normal")
        self.eof_button.configure(state="normal")

    def draw_Fc(self):
        df = pd.DataFrame({'Unit # [-]':self.df_A.unit, 'Flight Class # [-]':self.df_A.Fc})

        fig = Figure(figsize=(5,4), dpi=100)
        ax = fig.add_subplot(111)

        df.plot(x='Unit # [-]', y='Flight Class # [-]', ax=ax, kind="scatter")

        self.canvas.create_rectangle(1920/2-250,1080/2-200,1920/2+250,1080/2+200, width=7, outline="red")

        canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor="center")

    def get_eof(self):
        text = ""
        for i in np.unique(self.df_A['unit']):
            text = text +'Unit: ' + str(i) + ' - Number of flight cyles (t_{EOF}): '+ str(len(np.unique(self.df_A.loc[self.df_A['unit'] == i, 'cycle']))) + "\n"
        self.eof_text.configure(text=text)


class Page3(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, width = 1920, height = 1080, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand = True)

        button1 = tk.Button(self, text="Exit", fg="white", bg="red", 
                            font=("Verdana",18), pady=10, width=18,
                            command=root.destroy)
        self.button1_canvas = self.canvas.create_window(1860, 1080*0.92, anchor="ne",window=button1)

        self.button2 = tk.Button(self, text="Back to Home", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=18,
                                 command=lambda: controller.show_frame(Page1))
        self.button2.place(x=1860, y=1080*0.85, anchor="ne")


class Page4(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, width = 1920, height = 1080, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand = True)

        button1 = tk.Button(self, text="Exit", fg="white", bg="red", 
                            font=("Verdana",18), pady=10, width=18,
                            command=root.destroy)
        self.button1_canvas = self.canvas.create_window(1860, 1080*0.92, anchor="ne",window=button1)

        self.button2 = tk.Button(self, text="Back to Home", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=18,
                                 command=lambda: controller.show_frame(Page1))
        self.button2.place(x=1860, y=1080*0.85, anchor="ne")

class Page5(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, width = 1920, height = 1080, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand = True)

        button1 = tk.Button(self, text="Exit", fg="white", bg="red", 
                            font=("Verdana",18), pady=10, width=18,
                            command=root.destroy)
        self.button1_canvas = self.canvas.create_window(1860, 1080*0.92, anchor="ne",window=button1)

        self.button2 = tk.Button(self, text="Back to Home", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=18,
                                 command=lambda: controller.show_frame(Page1))
        self.button2.place(x=1860, y=1080*0.85, anchor="ne")

class Page6(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, width = 1920, height = 1080, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand = True)

        button1 = tk.Button(self, text="Exit", fg="white", bg="red", 
                            font=("Verdana",18), pady=10, width=18,
                            command=root.destroy)
        self.button1_canvas = self.canvas.create_window(1860, 1080*0.92, anchor="ne",window=button1)

        self.button2 = tk.Button(self, text="Back to Home", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=18,
                                 command=lambda: controller.show_frame(Page1))
        self.button2.place(x=1860, y=1080*0.85, anchor="ne")


if __name__ == "__main__":
    tkinterApp(root).pack()
    root.mainloop()




"""
import matplotlib
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pandas as pd
import tkinter as tk
from tkinter import ttk

root = tk.Tk()

lf = ttk.Labelframe(root, text='Plot Area')
lf.grid(row=0, column=0, sticky='nwes', padx=3, pady=3)

t = np.arange(0.0,3.0,0.01)
df = pd.DataFrame({'t':t, 's':np.sin(2*np.pi*t)})

fig = Figure(figsize=(5,4), dpi=100)
ax = fig.add_subplot(111)

df.plot(x='t', y='s', ax=ax)

canvas = FigureCanvasTkAgg(fig, master=lf)
canvas.draw()
canvas.get_tk_widget().grid(row=0, column=0)

root.mainloop()
"""