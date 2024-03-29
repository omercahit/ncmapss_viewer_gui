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
import matplotlib.pyplot as plt
from matplotlib import gridspec
import matplotlib
import seaborn as sns
from PIL import Image, ImageTk
from tkinter import scrolledtext
import optuna
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
import warnings
warnings.filterwarnings("ignore")
pd.DataFrame.iteritems = pd.DataFrame.items

root = tk.Tk()
root.geometry("1920x1080+3840+0")
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
df_A = ""
df_W = ""
df_T = ""
df_X_s = ""
df_X_v = ""
df_Y = ""

class tkinterApp(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, Page1, Page2, Page3, Page4, Page5, Page6, Page7, Page8):
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
                            font=("Verdana",18), pady=10, width=20,
                            command=root.destroy)
        self.button1_canvas = self.canvas.create_window(1860, 1080*0.92, anchor="ne",window=button1)

        self.button2 = tk.Button(self, text="Start", fg="black", bg="lightgray",
                                 font=("Verdana", 24), padx=30, pady=10,
                                 command=lambda: controller.show_frame(Page1))
        self.button2.place(relx=0.5, rely=0.7, anchor="center")

        self.header = tk.Label(self, text="Turbofan Engine Degradation\nSimulation", bg="black", fg="darkred",
                               font=("Verdana", 60))
        self.header.place(relx=0.5, rely=0.5, anchor="center")


class Page1(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, width = 1920, height = 1080, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand = True)
        
        button1 = tk.Button(self, text="Exit", fg="white", bg="red", 
                            font=("Verdana",18), pady=10, width=20,
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

        self.button_operative = tk.Button(self, text="Degradation", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=30,
                                 command=lambda: controller.show_frame(Page4))
        self.button_operative.place(relx=0.5, y=400, anchor="center")

        self.button_sensor_readings = tk.Button(self, text="Sensor Readings", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=30,
                                 command=lambda: controller.show_frame(Page5))
        self.button_sensor_readings.place(relx=0.5, y=500, anchor="center")

        self.button_virtual = tk.Button(self, text="Virtual Sensors", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=30,
                                 command=lambda: controller.show_frame(Page6))
        self.button_virtual.place(relx=0.5, y=600, anchor="center")

        self.button_health_state = tk.Button(self, text="Health State", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=30,
                                 command=lambda: controller.show_frame(Page7))
        self.button_health_state.place(relx=0.5, y=700, anchor="center")

        self.button_pred = tk.Button(self, text="Train and Predict", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=30,
                                 command=lambda: controller.show_frame(Page8))
        self.button_pred.place(relx=0.5, y=800, anchor="center")

    def on_select(self, event):
        if not event.widget.curselection():
            return
        index=self.doclist.curselection()[0]
        self.selected_file = self.docs[index]

    def open_selected(self):
        self.data_loader(self.selected_file)

    def data_loader(self, filename):
        global W_var, X_s_var, X_v_var, T_var, A_var, df_X_v, df_Y
        global W, X_s, X_v, T, Y, A, df_A, df_W, df_T, df_X_s

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

        df_A = DataFrame(data=A, columns=A_var)
        df_W = DataFrame(data=W, columns=W_var)
        df_T = DataFrame(data=T, columns=T_var)
        df_X_s = DataFrame(data=X_s, columns=X_s_var)
        df_X_v = DataFrame(data=X_v, columns=X_v_var)
        df_Y = DataFrame(data=Y, columns=['RUL'])

        df_W['unit'] = df_A['unit'].values

class Page2(tk.Frame):
    def __init__(self, parent, controller):
        global W_var, X_s_var, X_v_var, T_var, A_var, df_X_v, df_Y
        global W, X_s, X_v, T, Y, A, df_A, df_W, df_T, df_X_s

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, width = 1920, height = 1080, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand = True)

        button1 = tk.Button(self, text="Exit", fg="white", bg="red", 
                            font=("Verdana",18), pady=10, width=20,
                            command=root.destroy)
        self.button1_canvas = self.canvas.create_window(1860, 1080*0.92, anchor="ne",window=button1)

        self.button2 = tk.Button(self, text="Back to Home", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=20,
                                 command=lambda: controller.show_frame(Page1))
        self.button2.place(x=1860, y=1080*0.85, anchor="ne")

        self.button3 = tk.Button(self, text="Get Auxiliary\nInformation Describe", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=20,
                                 command=self.get_A)
        self.button3.place(x=1860, y=25, anchor="ne")

        self.info_text = tk.Label(self, text="", bg="black", fg="black", font=("Verdana", 12), padx=50, pady=50)
        self.info_text.place(relx=0.5, rely=0.5, anchor="center")

        self.draw_button = tk.Button(self, text="Plot Flight Classes", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=20, state="disabled",
                                 command=self.draw_Fc)
        self.draw_button.place(x=1860, y=140, anchor="ne")

        self.eof_button = tk.Button(self, text="Get End Of Failures", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=20, state="disabled",
                                 command=self.get_eof)
        self.eof_button.place(x=1860, y=230, anchor="ne")

    def get_A(self):
        self.info_text.configure(text=(str(df_A.describe())+"\n\nEngine units: "+str(np.unique(df_A['unit']))), bg="white")
        self.draw_button.configure(state="normal")
        self.eof_button.configure(state="normal")

    def draw_Fc(self):
        self.info_text.destroy()
        df = pd.DataFrame({'Unit # [-]':df_A.unit, 'Flight Class # [-]':df_A.Fc})

        fig = Figure(figsize=(10,10), dpi=100)
        ax = fig.add_subplot(111)

        df.plot(x='Unit # [-]', y='Flight Class # [-]', ax=ax, kind="scatter")

        self.canvas.create_rectangle(1920/2-500,1080/2-500,1920/2+500,1080/2+500, width=9, outline="darkred")

        canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor="center")

    def get_eof(self):
        text = ""
        for i in np.unique(df_A['unit']):
            text = text +'Unit: ' + str(i) + ' - Number of flight cycles (t_EOF): '+ str(len(np.unique(df_A.loc[df_A['unit'] == i, 'cycle']))) + "\n"
        self.info_text.configure(text=text)


class Page3(tk.Frame):
    def __init__(self, parent, controller):
        global W_var, X_s_var, X_v_var, T_var, A_var, df_X_v, df_Y
        global W, X_s, X_v, T, Y, A, df_A, df_W, df_T, df_X_s

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, width = 1920, height = 1080, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand = True)

        button1 = tk.Button(self, text="Exit", fg="white", bg="red", 
                            font=("Verdana",18), pady=10, width=20,
                            command=root.destroy)
        self.button1_canvas = self.canvas.create_window(1860, 1080*0.92, anchor="ne",window=button1)

        self.button2 = tk.Button(self, text="Back to Home", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=20,
                                 command=lambda: controller.show_frame(Page1))
        self.button2.place(x=1860, y=1080*0.85, anchor="ne")
        
        self.button3 = tk.Button(self, text="Get Operative\nConditions (w)", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=20,
                                 command=self.get_operative)
        self.button3.place(x=1860, y=25, anchor="ne")

        self.plot_ft_button = tk.Button(self, text="Plot Flight Traces", fg="black", bg="lightgray",
                                     font=("Verdana", 18), pady=10, width=20, state="disabled",
                                     command=self.plot_ft)
        self.plot_ft_button.place(x=1860, y=140, anchor="ne")

        self.plot_fe_button = tk.Button(self, text="Plot Flight Envelope", fg="black", bg="lightgray",
                                        font=("Verdana", 18), pady=10, width=20, state="disabled",
                                        command=self.plot_fe)
        self.plot_fe_button.place(x=1860, y=230, anchor="ne")

        self.plot_hist_button = tk.Button(self, text="Plot Histogram\nof\nFlight Conditions", fg="black", bg="lightgray",
                                        font=("Verdana", 18), pady=10, width=20, state="disabled",
                                        command=self.plot_hist)
        self.plot_hist_button.place(x=1860, y=320, anchor="ne")

        self.hist_unit_button = tk.Button(self, text="Histogram\nof\nSelected Unit", fg="black", bg="lightgray",
                                        font=("Verdana", 18), pady=10, width=20, state="disabled",
                                        command=self.plot_hist_unit)
        self.hist_unit_button.place(x=1860, y=460, anchor="ne")

        self.sing_cond_button = tk.Button(self, text="Plot Single\nCondition", fg="black", bg="lightgray",
                                        font=("Verdana", 18), pady=10, width=20, state="disabled",
                                        command=self.plot_ft_single)
        self.sing_cond_button.place(x=1860, y=600, anchor="ne")

        self.get_corr_button = tk.Button(self, text="Get Correlation", fg="black", bg="lightgray",
                                        font=("Verdana", 18), pady=10, width=20, state="disabled",
                                        command=self.get_corr)
        self.get_corr_button.place(x=1860, y=715, anchor="ne")

        self.scatter_button = tk.Button(self, text="Scatter Plot\nSelected Sensors", fg="black", bg="lightgray",
                                 font=("Verdana", 18), width=20, command=self.scatter_plot)
        self.scatter_button.place(relx=0.18, rely=0.9, anchor="se")

        self.box_plot_button = tk.Button(self, text="Box Plot\nSelected Sensor", fg="black", bg="lightgray",
                                 font=("Verdana", 18), width=20, command=self.box_plot)
        self.box_plot_button.place(relx=0.18, rely=0.98, anchor="se")

        self.selected_unit = ""
        self.selected_cycle = ""
        self.selected_condition = ""
        self.list_to_plot = []

        self.rect = self.canvas.create_rectangle(1840,1080*0.93,1840,1080*0.93, width=11, outline="darkred")


    def get_operative(self):
        self.units = list(np.unique(df_A['unit']))
        self.units = [int(x) for x in self.units]
        self.units_var = tk.StringVar(value = self.units)
        self.unit_list = tk.Listbox(self, height=5, width=25, listvariable=self.units_var, font=("Verdana", 12))
        self.unit_list.place(relx=0.15, rely=0.1, anchor="e")

        scroll = tk.Scrollbar(self, orient="vertical", command=self.unit_list.yview)
        scroll.place(relx=0.15, rely=0.1, anchor="w", height=100)
        self.unit_list['yscrollcommand'] = scroll.set

        self.cycles = list(np.unique(df_A['cycle']))
        self.cycles = [int(x) for x in self.cycles]
        self.cycles_var = tk.StringVar(value = self.cycles)
        self.cycles_list = tk.Listbox(self, height=9, width=25, listvariable=self.cycles_var, font=("Verdana", 12))
        self.cycles_list.place(relx=0.15, rely=0.35, anchor="e")

        scroll2 = tk.Scrollbar(self, orient="vertical", command=self.cycles_list.yview)
        scroll2.place(relx=0.15, rely=0.35, anchor="w", height=180)
        self.cycles_list['yscrollcommand'] = scroll2.set

        self.plot_fe_button.configure(state="normal")
        self.plot_hist_button.configure(state="normal")
        self.hist_unit_button.configure(state="normal")
        self.sing_cond_button.configure(state="normal")
        self.get_corr_button.configure(state="normal")

        self.choose_unit = tk.Button(self, text="Choose Unit",fg="black", bg="lightgray",
                                          font=("Verdana", 24), width=13,
                                          command=self.open_selected)
        self.choose_unit.place(relx=0.16, rely=0.2, anchor="e")

        self.choose_cycle = tk.Button(self, text="Choose Cycle",fg="black", bg="lightgray",
                                          font=("Verdana", 24), width=13,
                                          command=self.open_selected)
        self.choose_cycle.place(relx=0.16, rely=0.48, anchor="e")

        self.unit_list.bind('<<ListboxSelect>>', self.on_select_unit)
        self.cycles_list.bind('<<ListboxSelect>>', self.on_select_cycle)

        self.conditions = W_var
        self.conditions_var = tk.StringVar(value = self.conditions)
        self.conditions_list = tk.Listbox(self, height=6, width=25, listvariable=self.conditions_var, font=("Verdana", 12))
        self.conditions_list.place(relx=0.15, rely=0.63, anchor="e")

        scroll3 = tk.Scrollbar(self, orient="vertical", command=self.conditions_list.yview)
        scroll3.place(relx=0.15, rely=0.63, anchor="w", height=120)
        self.conditions_list['yscrollcommand'] = scroll3.set

        self.choose_condition = tk.Button(self, text="Choose\nCondition",fg="black", bg="lightgray",
                                          font=("Verdana", 24), width=13,
                                          command=self.open_selected)
        self.choose_condition.place(relx=0.16, rely=0.76, anchor="e")

        self.conditions_list.bind('<<ListboxSelect>>', self.on_select_condition)

    def on_select_unit(self, event1):
        if not event1.widget.curselection():
            return
        index = self.unit_list.curselection()[0]
        self.selected_unit = self.units[index]

    def on_select_cycle(self, event4):
        if not event4.widget.curselection():
            return
        index = self.cycles_list.curselection()[0]
        self.selected_cycle = self.cycles[index]

    def on_select_condition(self, event9):
        if not event9.widget.curselection():
            return
        index = self.conditions_list.curselection()[0]
        self.selected_condition = self.conditions[index]
        self.list_to_plot.append(self.selected_condition)

    def open_selected(self):
        print(self.selected_unit)
        self.plot_ft_button.configure(state="normal")

    def plot_ft(self):
        df_W_u = df_W.loc[(df_A.unit == self.selected_unit) & (df_A.cycle == self.selected_cycle)]
        df_W_u.reset_index(inplace=True, drop=True)
        labels = ['Altitude [ft]', 'Mach Number [-]', 'Throttle Resolver Angle [%]',
                  'Temperature at fan inlet (T2) [°R]']
        self.plot_df_color_per_unit(df_W_u, W_var, labels)

    def plot_ft_single(self):
        df_W_single = df_W[self.selected_condition].to_frame()
        df_W_single["unit"] = df_A["unit"].values
        df_W_u = df_W_single.loc[(df_A.unit == self.selected_unit) & (df_A.cycle == self.selected_cycle)]
        df_W_u.reset_index(inplace=True, drop=True)
        if self.selected_condition == "alt":
            labels = ['Altitude [ft]']
        elif self.selected_condition == "Mach":
            labels = ['Mach Number [-]']
        elif self.selected_condition == "TRA":
            labels = ['Throttle Resolver Angle [%]']
        elif self.selected_condition == "T2":
            labels = ['Temperature at fan inlet (T2) [°R]']
        self.plot_df_color_per_unit(df_W_u, [self.selected_condition], labels)

    def plot_df_color_per_unit(self, data, variables, labels, size=10, labelsize=17, option='Time', name=None):

        plt.clf()        
        input_dim = len(variables)
        cols = min(np.floor(input_dim**0.5).astype(int),4)
        rows = (np.ceil(input_dim / cols)).astype(int)
        gs   = gridspec.GridSpec(rows, cols)
        leg  = []
        fig  = plt.figure(figsize=(size,max(size,rows*2)))
        color_dic_unit = {'Unit 1': 'C0', 'Unit 2': 'C1', 'Unit 3': 'C2', 'Unit 4': 'C3', 'Unit 5': 'C4', 'Unit 6': 'C5',
                        'Unit 7': 'C6', 'Unit 8': 'C7', 'Unit 9': 'C8', 'Unit 10': 'C9', 'Unit 11': 'C10',
                        'Unit 12': 'C11', 'Unit 13': 'C12', 'Unit 14': 'C13', 'Unit 15': 'C14', 'Unit 16': 'C15',
                        'Unit 17': 'C16', 'Unit 18': 'C17', 'Unit 19': 'C18', 'Unit 20': 'C19'} 
        
        unit_sel  = np.unique(data['unit'])
        for n in range(input_dim):
            ax = fig.add_subplot(gs[n])
            for j in unit_sel:
                data_unit = data.loc[data['unit'] == j]
                if option=='cycle':
                    time_s = data.loc[data['unit'] == j, 'cycle']
                    label_x = 'Time [cycle]'
                else:
                    time_s = np.arange(len(data_unit))
                    label_x = 'Time [s]'
                ax.plot(time_s, data_unit[variables[n]], '-o', color=color_dic_unit['Unit ' + str(int(j))],
                        alpha=0.7, markersize=5)
                ax.tick_params(axis='x', labelsize=labelsize)
                ax.tick_params(axis='y', labelsize=labelsize)
                leg.append('Unit '+str(int(j)))
            plt.ylabel(labels[n], fontsize=labelsize)    
            plt.xlabel(label_x, fontsize=labelsize)
            ax.get_xaxis().set_major_formatter(
            matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
            if n==0:
                ax.get_yaxis().set_major_formatter(
                matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
        plt.legend(leg, loc='best', fontsize=labelsize-2) #lower left
        plt.tight_layout()
        plt.close()

        self.canvas.coords(self.rect, 1920/2-size*50,1080/2-size*50,1920/2+size*50,1080/2+size*50)

        self.fig_canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        self.fig_canvas.draw()
        self.fig_canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor="center")

    def plot_fe(self):
        labelsize = 17
        x = np.array([0.0, 0.2, 0.4, 0.6, 0.8])
        u = np.array([1.7, 1.7, 4.0, 4.0, 4.0]) * 10000
        l = np.array([0.0, 0.0, 0.0, 0.0, 1.0]) * 10000
        fig = plt.figure(figsize=(10,10))
        plt.fill_between(x, l, u, alpha=0.2)
        plt.plot(df_W.loc[df_A['Fc'] == 3, 'Mach'], df_W.loc[df_A['Fc'] == 3, 'alt'], '.', alpha=0.9)
        plt.plot(df_W.loc[df_A['Fc'] == 2, 'Mach'], df_W.loc[df_A['Fc'] == 2, 'alt'], '.', alpha=0.9)
        plt.plot(df_W.loc[df_A['Fc'] == 1, 'Mach'], df_W.loc[df_A['Fc'] == 1, 'alt'], '.', alpha=0.9)
        plt.tick_params(axis='x', labelsize=labelsize)
        plt.tick_params(axis='y', labelsize=labelsize)
        plt.xlim((0.0, 0.8))
        plt.ylim((0, 40000))
        plt.xlabel('Mach Number - [-]', fontsize=labelsize)
        plt.ylabel('Flight Altitude - [ft]', fontsize=labelsize)

        self.canvas.coords(self.rect, 1920 / 2 - 500, 1080 / 2 - 500, 1920 / 2 + 500, 1080 / 2 + 500)

        self.fig_canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        self.fig_canvas.draw()
        self.fig_canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor="center")

    def plot_kde(self, leg, variables, labels, size, units, df_W, df_A, labelsize=17, name=None):
        """
        """
        plt.clf()

        input_dim = len(variables)
        cols = min(np.floor(input_dim ** 0.5).astype(int), 4)
        rows = (np.ceil(input_dim / cols)).astype(int)
        gs = gridspec.GridSpec(rows, cols)

        color_dic_unit = {'Unit 1': 'C0', 'Unit 2': 'C1', 'Unit 3': 'C2', 'Unit 4': 'C3', 'Unit 5': 'C4',
                          'Unit 6': 'C5',
                          'Unit 7': 'C6', 'Unit 8': 'C7', 'Unit 9': 'C8', 'Unit 10': 'C9', 'Unit 11': 'C10',
                          'Unit 12': 'C11', 'Unit 13': 'C12', 'Unit 14': 'C13', 'Unit 15': 'C14', 'Unit 16': 'C15',
                          'Unit 17': 'C16', 'Unit 18': 'C17', 'Unit 19': 'C18', 'Unit 20': 'C19'}

        fig = plt.figure(figsize=(size, max(size, rows * 2)))

        for n in range(input_dim):
            ax = fig.add_subplot(gs[n])
            for k, elem in enumerate(units):
                sns.kdeplot(df_W.loc[df_A['unit'] == elem, variables[n]],
                            color=color_dic_unit[leg[k]], shade=True, gridsize=100)
                ax.tick_params(axis='x', labelsize=labelsize)
                ax.tick_params(axis='y', labelsize=labelsize)

            ax.get_xaxis().set_major_formatter(
                matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
            plt.xlabel(labels[n], fontsize=labelsize)
            plt.ylabel('Density [-]', fontsize=labelsize)
            if n == 0:
                plt.legend(leg, fontsize=labelsize - 4, loc=0)
            else:
                plt.legend(leg, fontsize=labelsize - 4, loc=2)
        plt.tight_layout()
        plt.close()

        self.canvas.coords(self.rect, 1920 / 2 - 500, 1080 / 2 - 500, 1920 / 2 + 500, 1080 / 2 + 500)

        self.fig_canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        self.fig_canvas.draw()
        self.fig_canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor="center")

    def plot_hist(self):
        variables = ['alt', 'Mach', 'TRA', 'T2']
        labels = ['Altitude [ft]', 'Mach Number [-]', 'Throttle Resolver Angle [%]', 'Temperature at fan inlet [°R]']
        size = 10

        units = list(np.unique(df_A['unit']))
        print(type(units[0]))
        leg = ['Unit ' + str(int(u)) for u in units]

        self.plot_kde(leg, variables, labels, size, units, df_W, df_A, labelsize=19)

    def plot_hist_unit(self):
        variables = ['alt', 'Mach', 'TRA', 'T2']
        labels = ['Altitude [ft]', 'Mach Number [-]', 'Throttle Resolver Angle [%]', 'Temperature at fan inlet [°R]']
        size = 10

        units = [float(self.selected_unit)]
        leg = ['Unit ' + str(int(u)) for u in units]

        self.plot_kde(leg, variables, labels, size, units, df_W, df_A, labelsize=19)

    def get_corr(self):
        correlation_matrix = df_W.corr(method='pearson')

        strongly_correlated_pairs = set()

        for i in range(len(correlation_matrix.columns)):
            for j in range(i + 1, len(correlation_matrix.columns)):
                variable1 = correlation_matrix.columns[i]
                variable2 = correlation_matrix.columns[j]
                correlation_value = correlation_matrix.iloc[i, j]

                if abs(correlation_value) >= 0.75:
                    strongly_correlated_pairs.add((variable1, variable2, correlation_value))

        text = ("Strongly Correlated Pairs (>%75):")
        for pair in strongly_correlated_pairs:
            text = text + "\n" + str(pair[0]) + " and " + str(pair[1]) + " : " + str(pair[2])

        self.corr_text = scrolledtext.ScrolledText(self, width=39, font=("Verdana",10),
                                  bg="lightgray", fg="green", highlightbackground="darkred",
                                  highlightthickness=2,  height=6)
        self.corr_text.insert(tk.END, text)
        self.corr_text.place(relx=0.97, rely=0.73, anchor="ne")

        fig = plt.figure(figsize=(10,10))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Correlation Matrix")
        plt.close()

        self.canvas.coords(self.rect, 1920 / 2 - 500, 1080 / 2 - 500, 1920 / 2 + 500, 1080 / 2 + 500)

        self.fig_canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        self.fig_canvas.draw()
        self.fig_canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor="center")

    def scatter_plot(self):
        plt.clf()
        df_W_single = df_W[self.list_to_plot[-2]].to_frame()
        df_W_scatter_1 = df_W_single.loc[(df_A.unit == self.selected_unit) & (df_A.cycle == self.selected_cycle)]
        df_W_scatter_1.reset_index(inplace=True, drop=True)

        df_W_single = df_W[self.list_to_plot[-1]].to_frame()
        df_W_scatter_2 = df_W_single.loc[(df_A.unit == self.selected_unit) & (df_A.cycle == self.selected_cycle)]
        df_W_scatter_2.reset_index(inplace=True, drop=True)

        fig = Figure(figsize=(10,10), dpi=100)

        ax=fig.add_subplot(111)

        ax.set_title(self.list_to_plot[-2] + " and " + self.list_to_plot[-1], fontsize="xx-large")

        ax.scatter(x=df_W_scatter_2, y=df_W_scatter_1)
        plt.close()

        self.canvas.create_rectangle(1920/2-500,1080/2-500,1920/2+500,1080/2+500, width=9, outline="darkred")

        canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor="center")
    
    def box_plot(self):
        plt.clf()
        df_W_single = df_W[self.list_to_plot[-2]].to_frame()
        df_W_box_1 = df_W_single.loc[(df_A.unit == self.selected_unit) & (df_A.cycle == self.selected_cycle)]
        df_W_box_1.reset_index(inplace=True, drop=True)

        df_W_single = df_W[self.list_to_plot[-1]].to_frame()
        df_W_box_2 = df_W_single.loc[(df_A.unit == self.selected_unit) & (df_A.cycle == self.selected_cycle)]
        df_W_box_2.reset_index(inplace=True, drop=True)

        fig = Figure(figsize=(10,10), dpi=100)

        ax=fig.add_subplot(111)

        ax.set_title(self.list_to_plot[-2] + " and " + self.list_to_plot[-1], fontsize="xx-large")

        ax.boxplot(x=[df_W_box_1.values.flatten(), df_W_box_2.values.flatten()])
        plt.close()

        self.canvas.create_rectangle(1920/2-500,1080/2-500,1920/2+500,1080/2+500, width=9, outline="darkred")

        canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor="center")

class Page4(tk.Frame):
    def __init__(self, parent, controller):
        global W_var, X_s_var, X_v_var, T_var, A_var, df_X_v, df_Y
        global W, X_s, X_v, T, Y, A, df_A, df_W, df_T, df_X_s

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, width = 1920, height = 1080, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand = True)

        button1 = tk.Button(self, text="Exit", fg="white", bg="red", 
                            font=("Verdana",18), pady=10, width=20,
                            command=root.destroy)
        self.button1_canvas = self.canvas.create_window(1860, 1080*0.92, anchor="ne",window=button1)

        self.button2 = tk.Button(self, text="Back to Home", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=20,
                                 command=lambda: controller.show_frame(Page1))
        self.button2.place(x=1860, y=1080*0.85, anchor="ne")

        self.button3 = tk.Button(self, text="Get Degradation", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=20,
                                 command=self.get_degradation)
        self.button3.place(x=1860, y=25, anchor="ne")

        self.info_text = tk.Label(self, text="", bg="black", fg="white", font=("Verdana", 12))
        self.info_text.place(relx=0.5, rely=0.5, anchor="center")

        self.plot_parallel_button = tk.Button(self, text="Plot as Parallel\nCoordinates", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=20,
                                 command=self.plot_parallel_coordinates)
        self.plot_parallel_button.place(x=1860, y=115, anchor="ne")

        self.rect = self.canvas.create_rectangle(1840,1080*0.93,1840,1080*0.93, width=11, outline="darkred")

        self.plot_single = tk.Button(self, text="Plot Single Color", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=20,
                                 command=self.plotter_single_color)
        self.plot_single.place(x=1860, y=230, anchor="ne")

        self.plot_hpt = tk.Button(self, text="Plot HPT Eff.\nColor Per Unit", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=20,
                                 command=self.plotter_color_per_unit)
        self.plot_hpt.place(x=1860, y=320, anchor="ne")
        self.image_id = ""

        self.get_corr_button = tk.Button(self, text="Get Correlation", fg="black", bg="lightgray",
                                        font=("Verdana", 18), pady=10, width=20, state="disabled",
                                        command=self.get_corr)
        self.get_corr_button.place(x=1860, y=435, anchor="ne")


    def get_degradation(self):
        df_T['unit'] = df_A['unit'].values
        df_T['cycle'] = df_A['cycle'].values
        self.df_Ts = df_T.drop_duplicates()
        self.info_text.configure(text=(str(self.df_Ts.describe())))
        self.get_corr_button.configure(state="normal")

    def plot_parallel_coordinates(self):
        self.info_text.destroy()
        import plotly.express as px

        varsel = ['unit', 'HPT_eff_mod', 'LPT_eff_mod', 'LPT_flow_mod']
        df_Tss = self.df_Ts.loc[:,varsel]
        fig = px.parallel_coordinates(df_Tss, color="unit", labels={"unit": "Units",
                                    "HPT_eff_mod": "HPT_eff_mod", "LPT_eff_mod": "LPT_eff_mod",
                                    "LPT_flow_mod": "LPT_flow_mod", },
                                    color_continuous_scale=px.colors.diverging.Tealrose,
                                    color_continuous_midpoint=2)
        
        fig.write_image("fig1.png")
        img = Image.open('fig1.png')
        self.tkimage = ImageTk.PhotoImage(img)
        self.image_id = self.canvas.create_image(1920/2, 1080/2, image=self.tkimage)

        self.canvas.coords(self.rect, 1920 / 2 - 500, 1080 / 2 - 500, 1920 / 2 + 500, 1080 / 2 + 500)
        self.canvas.itemconfig(self.rect, fill="white")

    def plot_df_single_color(self, data, variables, labels, size=10, labelsize=17, name=None):
        plt.clf()        
        input_dim = len(variables)
        cols = min(np.floor(input_dim**0.5).astype(int),4)
        rows = (np.ceil(input_dim / cols)).astype(int)
        gs   = gridspec.GridSpec(rows, cols)    
        fig  = plt.figure(figsize=(size,max(size,rows*2))) 
        
        for n in range(input_dim):
            ax = fig.add_subplot(gs[n])
            ax.plot(data[variables[n]], marker='.', markerfacecolor='none', alpha = 0.7)
            ax.tick_params(axis='x', labelsize=labelsize)
            ax.tick_params(axis='y', labelsize=labelsize)
            plt.ylabel(labels[n], fontsize=labelsize)
            plt.xlabel('Time [s]', fontsize=labelsize)
        plt.tight_layout()
        plt.close()

        self.canvas.coords(self.rect, 1920/2-size*50,1080/2-size*50,1920/2+size*50,1080/2+size*50)

        self.fig_canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        self.fig_canvas.draw()
        self.fig_canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor="center")

    def plotter_single_color(self):
        self.plot_df_single_color(df_T,T_var,T_var)

    def plotter_color_per_unit(self):
        Page3.plot_df_color_per_unit(self, self.df_Ts, ['HPT_eff_mod'],[r'HPT Eff. - $\theta$ [-]'], size=10,  option='cycle')
        self.canvas.coords(self.rect, 1920/2-10*50,1080/2-10*50,1920/2+10*50,1080/2+10*50)

    def get_corr(self):
        correlation_matrix = df_T.corr(method='pearson')

        strongly_correlated_pairs = set()

        for i in range(len(correlation_matrix.columns)):
            for j in range(i + 1, len(correlation_matrix.columns)):
                variable1 = correlation_matrix.columns[i]
                variable2 = correlation_matrix.columns[j]
                correlation_value = correlation_matrix.iloc[i, j]

                if abs(correlation_value) >= 0.75:
                    strongly_correlated_pairs.add((variable1, variable2, correlation_value))

        text = ("Strongly Correlated Pairs (>%75):")
        for pair in strongly_correlated_pairs:
            text = text + "\n" + str(pair[0]) + " and " + str(pair[1]) + " : " + str(pair[2])

        self.corr_text = scrolledtext.ScrolledText(self, width=39, font=("Verdana",10),
                                  bg="lightgray", fg="green", highlightbackground="darkred",
                                  highlightthickness=2,  height=6)
        self.corr_text.insert(tk.END, text)
        self.corr_text.place(relx=0.97, rely=0.73, anchor="ne")

        fig = plt.figure(figsize=(10,10))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Correlation Matrix")
        plt.close()

        self.canvas.coords(self.rect, 1920 / 2 - 500, 1080 / 2 - 500, 1920 / 2 + 500, 1080 / 2 + 500)

        self.fig_canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        self.fig_canvas.draw()
        self.fig_canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor="center")

class Page5(tk.Frame):
    def __init__(self, parent, controller):
        global W_var, X_s_var, X_v_var, T_var, A_var, df_X_v, df_Y
        global W, X_s, X_v, T, Y, A, df_A, df_W, df_T, df_X_s

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, width = 1920, height = 1080, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand = True)

        button1 = tk.Button(self, text="Exit", fg="white", bg="red", 
                            font=("Verdana",18), pady=10, width=20,
                            command=root.destroy)
        self.button1_canvas = self.canvas.create_window(1860, 1080*0.92, anchor="ne",window=button1)

        self.button2 = tk.Button(self, text="Back to Home", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=20,
                                 command=lambda: controller.show_frame(Page1))
        self.button2.place(x=1860, y=1080*0.85, anchor="ne")

        self.button3 = tk.Button(self, text="Get Sensor\nReadings (Xs)", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=20,
                                 command=self.get_xs)
        self.button3.place(x=1860, y=25, anchor="ne")

        self.selected_unit = ""
        self.selected_cycle = ""
        self.selected_sensor = ""
        self.list_to_plot = []

        self.rect = self.canvas.create_rectangle(1840,1080*0.93,1840,1080*0.93, width=11, outline="darkred")

        self.plot_single_unit_button = tk.Button(self, text="Plot\nSingle Unit", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=20, state="disabled",
                                 command=self.plot_single_xs)
        self.plot_single_unit_button.place(x=1860, y=140, anchor="ne")

        self.plot_single_cycle_button = tk.Button(self, text="Plot for Single\nFlight Cycle", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=20, state="disabled",
                                 command=self.plot_single_fc)
        self.plot_single_cycle_button.place(x=1860, y=255, anchor="ne")

        self.plot_single_sensor_button = tk.Button(self, text="Plot Single\nSensor", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=20, state="disabled",
                                 command=self.plot_single_sensor)
        self.plot_single_sensor_button.place(x=1860, y=370, anchor="ne")

        self.get_correlations_button = tk.Button(self, text="Get Correlations", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=20, state="disabled",
                                 command=self.get_corr)
        self.get_correlations_button.place(x=1860, y=485, anchor="ne")

        self.scatter_button = tk.Button(self, text="Scatter Plot\nSelected Sensors", fg="black", bg="lightgray",
                                 font=("Verdana", 18), width=20, command=self.scatter_plot)
        self.scatter_button.place(relx=0.18, rely=0.9, anchor="se")

        self.box_plot_button = tk.Button(self, text="Box Plot\nSelected Sensor", fg="black", bg="lightgray",
                                 font=("Verdana", 18), width=20, command=self.box_plot)
        self.box_plot_button.place(relx=0.18, rely=0.98, anchor="se")

    def get_xs(self):
        self.units = list(np.unique(df_A['unit']))
        self.units_var = tk.StringVar(value = self.units)
        self.unit_list = tk.Listbox(self, height=5, width=25, listvariable=self.units_var, font=("Verdana", 12))
        self.unit_list.place(relx=0.15, rely=0.1, anchor="e")

        scroll = tk.Scrollbar(self, orient="vertical", command=self.unit_list.yview)
        scroll.place(relx=0.15, rely=0.1, anchor="w", height=100)
        self.unit_list['yscrollcommand'] = scroll.set

        self.choose_unit = tk.Button(self, text="Choose Unit",fg="black", bg="lightgray",
                                          font=("Verdana", 24), width=13,
                                          command=self.open_selected)
        self.choose_unit.place(relx=0.16, rely=0.2, anchor="e")

        self.unit_list.bind('<<ListboxSelect>>', self.on_select_unit)

        self.cycles = list(np.unique(df_A['cycle']))
        self.cycles = [int(x) for x in self.cycles]
        self.cycles_var = tk.StringVar(value = self.cycles)
        self.cycles_list = tk.Listbox(self, height=9, width=25, listvariable=self.cycles_var, font=("Verdana", 12))
        self.cycles_list.place(relx=0.15, rely=0.35, anchor="e")

        scroll2 = tk.Scrollbar(self, orient="vertical", command=self.cycles_list.yview)
        scroll2.place(relx=0.15, rely=0.35, anchor="w", height=180)
        self.cycles_list['yscrollcommand'] = scroll2.set

        self.choose_cycle = tk.Button(self, text="Choose Cycle",fg="black", bg="lightgray",
                                          font=("Verdana", 24), width=13,
                                          command=self.open_selected)
        self.choose_cycle.place(relx=0.16, rely=0.48, anchor="e")

        self.cycles_list.bind('<<ListboxSelect>>', self.on_select_cycle)

        self.sensors = X_s_var
        self.sensors_var = tk.StringVar(value = self.sensors)
        self.sensors_list = tk.Listbox(self, height=9, width=25, listvariable=self.sensors_var, font=("Verdana", 12))
        self.sensors_list.place(relx=0.15, rely=0.63, anchor="e")

        scroll3 = tk.Scrollbar(self, orient="vertical", command=self.sensors_list.yview)
        scroll3.place(relx=0.15, rely=0.63, anchor="w", height=180)
        self.sensors_list['yscrollcommand'] = scroll3.set

        self.choose_sensor = tk.Button(self, text="Choose Sensor",fg="black", bg="lightgray",
                                          font=("Verdana", 24), width=13,
                                          command=self.open_selected)
        self.choose_sensor.place(relx=0.16, rely=0.76, anchor="e")

        self.sensors_list.bind('<<ListboxSelect>>', self.on_select_sensor)

    def on_select_unit(self, event2):
        if not event2.widget.curselection():
            return
        index = self.unit_list.curselection()[0]
        self.selected_unit = self.units[index]

    def on_select_cycle(self, event5):
        if not event5.widget.curselection():
            return
        index = self.cycles_list.curselection()[0]
        self.selected_cycle = self.cycles[index]

    def on_select_sensor(self, event8):
        if not event8.widget.curselection():
            return
        index = self.sensors_list.curselection()[0]
        self.selected_sensor = self.sensors[index]
        self.list_to_plot.append(self.selected_sensor)

    def open_selected(self):
        print(self.selected_unit)
        self.plot_single_unit_button.configure(state="normal")
        self.plot_single_cycle_button.configure(state="normal")
        self.get_correlations_button.configure(state="normal")
        self.plot_single_sensor_button.configure(state="normal")

    def plot_single_xs(self):
        df_X_s_u = df_X_s.loc[df_A.unit == self.selected_unit]
        df_X_s_u.reset_index(inplace=True, drop=True)
        labels = X_s_var
        Page4.plot_df_single_color(self,df_X_s_u, X_s_var, labels)

    def plot_single_fc(self):
        df_X_s_u_c = df_X_s.loc[(df_A.unit == self.selected_unit) & (df_A.cycle == self.selected_cycle)]
        df_X_s_u_c.reset_index(inplace=True, drop=True)
        Page4.plot_df_single_color(self, df_X_s_u_c, X_s_var, X_s_var)

    def plot_single_sensor(self):
        df_X_s_single = df_X_s[self.selected_sensor].to_frame()
        df_X_s_u_c = df_X_s_single.loc[(df_A.unit == self.selected_unit) & (df_A.cycle == self.selected_cycle)]
        df_X_s_u_c.reset_index(inplace=True, drop=True)
        Page4.plot_df_single_color(self, df_X_s_u_c, [self.selected_sensor], [self.selected_sensor])

    def get_corr(self):
        correlation_matrix = df_X_s.corr(method='pearson')

        strongly_correlated_pairs = set()

        for i in range(len(correlation_matrix.columns)):
            for j in range(i + 1, len(correlation_matrix.columns)):
                variable1 = correlation_matrix.columns[i]
                variable2 = correlation_matrix.columns[j]
                correlation_value = correlation_matrix.iloc[i, j]

                if abs(correlation_value) >= 0.75:
                    strongly_correlated_pairs.add((variable1, variable2, correlation_value))

        text = ("Strongly Correlated Pairs (>%75):")
        for pair in strongly_correlated_pairs:
            text = text + "\n" + str(pair[0]) + " and " + str(pair[1]) + " : " + str(pair[2])

        self.corr_text = scrolledtext.ScrolledText(self, width=40, font=("Verdana",10),
                                  bg="lightgray", fg="green", highlightbackground="darkred",
                                  highlightthickness=2, height=15)
        self.corr_text.insert(tk.END, text)
        self.corr_text.place(relx=0.97, rely=0.52, anchor="ne")

        fig = plt.figure(figsize=(10,10))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Correlation Matrix")
        plt.close()

        self.canvas.coords(self.rect, 1920 / 2 - 500, 1080 / 2 - 500, 1920 / 2 + 500, 1080 / 2 + 500)

        self.fig_canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        self.fig_canvas.draw()
        self.fig_canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor="center")

    def scatter_plot(self):
        plt.clf()
        df_X_s_single = df_X_s[self.list_to_plot[-2]].to_frame()
        df_X_s_scatter_1 = df_X_s_single.loc[(df_A.unit == self.selected_unit) & (df_A.cycle == self.selected_cycle)]
        df_X_s_scatter_1.reset_index(inplace=True, drop=True)

        df_X_s_single = df_X_s[self.list_to_plot[-1]].to_frame()
        df_X_s_scatter_2 = df_X_s_single.loc[(df_A.unit == self.selected_unit) & (df_A.cycle == self.selected_cycle)]
        df_X_s_scatter_2.reset_index(inplace=True, drop=True)

        fig = Figure(figsize=(10,10), dpi=100)

        ax=fig.add_subplot(111)

        ax.set_title(self.list_to_plot[-2] + " and " + self.list_to_plot[-1], fontsize="xx-large")

        ax.scatter(x=df_X_s_scatter_2, y=df_X_s_scatter_1)
        plt.close()

        self.canvas.create_rectangle(1920/2-500,1080/2-500,1920/2+500,1080/2+500, width=9, outline="darkred")

        canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor="center")

    def box_plot(self):
        plt.clf()
        df_X_s_single = df_X_s[self.list_to_plot[-2]].to_frame()
        df_X_s_box_1 = df_X_s_single.loc[(df_A.unit == self.selected_unit) & (df_A.cycle == self.selected_cycle)]
        df_X_s_box_1.reset_index(inplace=True, drop=True)

        df_X_s_single = df_X_s[self.list_to_plot[-1]].to_frame()
        df_X_s_box_2 = df_X_s_single.loc[(df_A.unit == self.selected_unit) & (df_A.cycle == self.selected_cycle)]
        df_X_s_box_2.reset_index(inplace=True, drop=True)

        fig = Figure(figsize=(10,10), dpi=100)

        ax=fig.add_subplot(111)

        ax.set_title(self.list_to_plot[-2] + " and " + self.list_to_plot[-1], fontsize="xx-large")

        ax.boxplot(x=[df_X_s_box_1.values.flatten(), df_X_s_box_2.values.flatten()])
        plt.close()

        self.canvas.create_rectangle(1920/2-500,1080/2-500,1920/2+500,1080/2+500, width=9, outline="darkred")

        canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor="center")

class Page6(tk.Frame):
    def __init__(self, parent, controller):
        global W_var, X_s_var, X_v_var, T_var, A_var, df_X_v, df_Y
        global W, X_s, X_v, T, Y, A, df_A, df_W, df_T, df_X_s

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, width = 1920, height = 1080, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand = True)

        button1 = tk.Button(self, text="Exit", fg="white", bg="red", 
                            font=("Verdana",18), pady=10, width=20,
                            command=root.destroy)
        self.button1_canvas = self.canvas.create_window(1860, 1080*0.92, anchor="ne",window=button1)

        self.button2 = tk.Button(self, text="Back to Home", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=20,
                                 command=lambda: controller.show_frame(Page1))
        self.button2.place(x=1860, y=1080*0.85, anchor="ne")

        self.button3 = tk.Button(self, text="Get Virtual\nSensors (Xv)", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=20,
                                 command=self.get_xv)
        self.button3.place(x=1860, y=25, anchor="ne")

        self.plot_xv_button = tk.Button(self, text="Plot Single Unit\nVirtual Sensors", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=20, state="disabled",
                                 command=self.plot_xv)
        self.plot_xv_button.place(x=1860, y=140, anchor="ne")

        self.plot_xv_single_button = tk.Button(self, text="Plot Single Unit and\nCycle Virtual Sensors", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=20, state="disabled",
                                 command=self.plot_xv_single)
        self.plot_xv_single_button.place(x=1860, y=255, anchor="ne")

        self.selected_unit = ""
        self.selected_cycle = ""
        self.selected_sensor = ""
        self.list_to_plot = []

        self.rect = self.canvas.create_rectangle(1840,1080*0.93,1840,1080*0.93, width=11, outline="darkred")

        self.plot_single_sensor_button = tk.Button(self, text="Plot Single\nSensor", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=20, state="disabled",
                                 command=self.plot_single_sensor)
        self.plot_single_sensor_button.place(x=1860, y=370, anchor="ne")

        self.get_correlations_button = tk.Button(self, text="Get Correlations", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=20, state="disabled",
                                 command=self.get_corr)
        self.get_correlations_button.place(x=1860, y=485, anchor="ne")

        self.scatter_button = tk.Button(self, text="Scatter Plot\nSelected Sensors", fg="black", bg="lightgray",
                                 font=("Verdana", 18), width=20, command=self.scatter_plot)
        self.scatter_button.place(relx=0.18, rely=0.9, anchor="se")

        self.box_plot_button = tk.Button(self, text="Box Plot\nSelected Sensor", fg="black", bg="lightgray",
                                 font=("Verdana", 18), width=20, command=self.box_plot)
        self.box_plot_button.place(relx=0.18, rely=0.98, anchor="se")

    def get_xv(self):
        self.units = list(np.unique(df_A['unit']))
        self.units_var = tk.StringVar(value = self.units)
        self.unit_list = tk.Listbox(self, height=5, width=25, listvariable=self.units_var, font=("Verdana", 12))
        self.unit_list.place(relx=0.15, rely=0.1, anchor="e")

        scroll = tk.Scrollbar(self, orient="vertical", command=self.unit_list.yview)
        scroll.place(relx=0.15, rely=0.1, anchor="w", height=100)
        self.unit_list['yscrollcommand'] = scroll.set

        self.cycles = list(np.unique(df_A['cycle']))
        self.cycles = [int(x) for x in self.cycles]
        self.cycles_var = tk.StringVar(value = self.cycles)
        self.cycles_list = tk.Listbox(self, height=9, width=25, listvariable=self.cycles_var, font=("Verdana", 12))
        self.cycles_list.place(relx=0.15, rely=0.35, anchor="e")

        scroll2 = tk.Scrollbar(self, orient="vertical", command=self.cycles_list.yview)
        scroll2.place(relx=0.15, rely=0.35, anchor="w", height=180)
        self.cycles_list['yscrollcommand'] = scroll2.set

        self.choose_unit = tk.Button(self, text="Choose Unit",fg="black", bg="lightgray",
                                          font=("Verdana", 24), width=13,
                                          command=self.open_selected)
        self.choose_unit.place(relx=0.16, rely=0.2, anchor="e")

        self.choose_cycle = tk.Button(self, text="Choose Cycle",fg="black", bg="lightgray",
                                          font=("Verdana", 24), width=13,
                                          command=self.open_selected)
        self.choose_cycle.place(relx=0.16, rely=0.48, anchor="e")

        self.unit_list.bind('<<ListboxSelect>>', self.on_select_unit)
        self.cycles_list.bind('<<ListboxSelect>>', self.on_select_cycle)

        self.sensors = X_v_var
        self.sensors_var = tk.StringVar(value = self.sensors)
        self.sensors_list = tk.Listbox(self, height=9, width=25, listvariable=self.sensors_var, font=("Verdana", 12))
        self.sensors_list.place(relx=0.15, rely=0.63, anchor="e")

        scroll3 = tk.Scrollbar(self, orient="vertical", command=self.sensors_list.yview)
        scroll3.place(relx=0.15, rely=0.63, anchor="w", height=180)
        self.sensors_list['yscrollcommand'] = scroll3.set

        self.choose_sensor = tk.Button(self, text="Choose Sensor",fg="black", bg="lightgray",
                                          font=("Verdana", 24), width=13,
                                          command=self.open_selected)
        self.choose_sensor.place(relx=0.16, rely=0.76, anchor="e")

        self.sensors_list.bind('<<ListboxSelect>>', self.on_select_sensor)

    def on_select_unit(self, event3):
        if not event3.widget.curselection():
            return
        index = self.unit_list.curselection()[0]
        self.selected_unit = self.units[index]

    def on_select_cycle(self, event6):
        if not event6.widget.curselection():
            return
        index = self.cycles_list.curselection()[0]
        self.selected_cycle = self.cycles[index]

    def on_select_sensor(self, event7):
        if not event7.widget.curselection():
            return
        index = self.sensors_list.curselection()[0]
        self.selected_sensor = self.sensors[index]
        self.list_to_plot.append(self.selected_sensor)

    def open_selected(self):
        print(self.selected_unit)
        self.plot_xv_button.configure(state="normal")
        self.plot_xv_single_button.configure(state="normal")
        self.plot_single_sensor_button.configure(state="normal")
        self.get_correlations_button.configure(state="normal")

    def plot_xv(self):
        df_X_v_u_c = df_X_v.loc[(df_A.unit == self.selected_unit) & (df_A.cycle == 1)]
        df_X_v_u_c.reset_index(inplace=True, drop=True)
        Page4.plot_df_single_color(self,df_X_v_u_c, X_v_var, X_v_var)

    def plot_xv_single(self):
        df_X_v_u_c = df_X_v.loc[(df_A.unit == self.selected_unit) & (df_A.cycle == self.selected_cycle)]
        df_X_v_u_c.reset_index(inplace=True, drop=True)
        Page4.plot_df_single_color(self,df_X_v_u_c, X_v_var, X_v_var)

    def plot_single_sensor(self):
        df_X_v_single = df_X_v[self.selected_sensor].to_frame()
        df_X_v_u_c = df_X_v_single.loc[(df_A.unit == self.selected_unit) & (df_A.cycle == self.selected_cycle)]
        df_X_v_u_c.reset_index(inplace=True, drop=True)
        Page4.plot_df_single_color(self, df_X_v_u_c, [self.selected_sensor], [self.selected_sensor])

    def get_corr(self):
        correlation_matrix = df_X_v.corr(method='pearson')

        strongly_correlated_pairs = set()

        for i in range(len(correlation_matrix.columns)):
            for j in range(i + 1, len(correlation_matrix.columns)):
                variable1 = correlation_matrix.columns[i]
                variable2 = correlation_matrix.columns[j]
                correlation_value = correlation_matrix.iloc[i, j]

                if abs(correlation_value) >= 0.75:
                    strongly_correlated_pairs.add((variable1, variable2, correlation_value))

        text = ("Strongly Correlated Pairs (>%75):")
        for pair in strongly_correlated_pairs:
            text = text + "\n" + str(pair[0]) + " and " + str(pair[1]) + " : " + str(pair[2])

        self.corr_text = scrolledtext.ScrolledText(self, width=40, font=("Verdana",10),
                                  bg="lightgray", fg="green", highlightbackground="darkred",
                                  highlightthickness=2,  height=15)
        self.corr_text.insert(tk.END, text)
        self.corr_text.place(relx=0.97, rely=0.52, anchor="ne")

        fig = plt.figure(figsize=(10,10))
        sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f")
        plt.title("Correlation Matrix")
        plt.close()

        self.canvas.coords(self.rect, 1920 / 2 - 500, 1080 / 2 - 500, 1920 / 2 + 500, 1080 / 2 + 500)

        self.fig_canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        self.fig_canvas.draw()
        self.fig_canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor="center")

    def scatter_plot(self):
        plt.clf()
        df_X_v_single = df_X_v[self.list_to_plot[-2]].to_frame()
        df_X_v_scatter_1 = df_X_v_single.loc[(df_A.unit == self.selected_unit) & (df_A.cycle == self.selected_cycle)]
        df_X_v_scatter_1.reset_index(inplace=True, drop=True)

        df_X_v_single = df_X_v[self.list_to_plot[-1]].to_frame()
        df_X_v_scatter_2 = df_X_v_single.loc[(df_A.unit == self.selected_unit) & (df_A.cycle == self.selected_cycle)]
        df_X_v_scatter_2.reset_index(inplace=True, drop=True)

        fig = Figure(figsize=(10,10), dpi=100)

        ax=fig.add_subplot(111)

        plt.ylabel(self.list_to_plot[-2], fontsize=17)
        plt.xlabel(self.list_to_plot[-1], fontsize=17)

        ax.scatter(x=df_X_v_scatter_2, y=df_X_v_scatter_1)
        plt.close()

        self.canvas.create_rectangle(1920/2-500,1080/2-500,1920/2+500,1080/2+500, width=9, outline="darkred")

        canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor="center")

    def box_plot(self):
        plt.clf()
        df_X_v_single = df_X_v[self.list_to_plot[-2]].to_frame()
        df_X_v_box_1 = df_X_v_single.loc[(df_A.unit == self.selected_unit) & (df_A.cycle == self.selected_cycle)]
        df_X_v_box_1.reset_index(inplace=True, drop=True)

        df_X_v_single = df_X_v[self.list_to_plot[-1]].to_frame()
        df_X_v_box_2 = df_X_v_single.loc[(df_A.unit == self.selected_unit) & (df_A.cycle == self.selected_cycle)]
        df_X_v_box_2.reset_index(inplace=True, drop=True)

        fig = Figure(figsize=(10,10), dpi=100)

        ax=fig.add_subplot(111)

        ax.set_title(self.list_to_plot[-2] + " and " + self.list_to_plot[-1], fontsize="xx-large")

        ax.boxplot(x=[df_X_v_box_1.values.flatten(), df_X_v_box_2.values.flatten()])
        plt.close()

        self.canvas.create_rectangle(1920/2-500,1080/2-500,1920/2+500,1080/2+500, width=9, outline="darkred")

        canvas = FigureCanvasTkAgg(fig, master=self.canvas)
        canvas.draw()
        canvas.get_tk_widget().place(relx=0.5, rely=0.5, anchor="center")

class Page7(tk.Frame):
    def __init__(self, parent, controller):
        global W_var, X_s_var, X_v_var, T_var, A_var, df_X_v, df_Y
        global W, X_s, X_v, T, Y, A, df_A, df_W, df_T, df_X_s

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

        self.hs_plot_button = tk.Button(self, text="Plot Health\nState", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=20,
                                 command=self.plot_hs)
        self.hs_plot_button.place(x=1860, y=25, anchor="ne")

        self.rect = self.canvas.create_rectangle(1840,1080*0.93,1840,1080*0.93, width=11, outline="darkred")

    def plot_hs(self):
        Page3.plot_df_color_per_unit(self, df_A, ['hs'],[r'$h_s$ [-]'], option='cycle', size=8)

class Page8(tk.Frame):
    def __init__(self, parent, controller):
        global W_var, X_s_var, X_v_var, T_var, A_var
        global W, X_s, X_v, T, Y, A

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

        self.concat = tk.Button(self, text="Get Concat", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=18,
                                 command=self.get_concat)
        self.concat.place(x=1860, y=25, anchor="ne")

        self.selected_unit = ""
        self.selected_feat = ""

        self.optimize_button = tk.Button(self, text="Optimize", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=18,
                                 command=self.optimize)
        self.optimize_button.place(x=1860, y=115, anchor="ne")

        self.train_button = tk.Button(self, text="Train", fg="black", bg="lightgray",
                                 font=("Verdana", 18), pady=10, width=18,
                                 command=self.train)
        self.train_button.place(x=1860, y=205, anchor="ne")
        
    def get_concat(self):
        self.df_W = DataFrame(data=W, columns=W_var)
        self.df_X_s = DataFrame(data=X_s, columns=X_s_var)
        self.df_X_v = DataFrame(data=X_v, columns=X_v_var)
        self.df_T = DataFrame(data=T, columns=T_var)
        self.df_Y = DataFrame(data=Y, columns=['RUL'])
        self.df_A = DataFrame(data=A, columns=A_var)

        self.df_all = pd.concat([self.df_W, self.df_X_s, self.df_X_v,
                                 self.df_T, self.df_Y, self.df_A], axis=1)
        
        #self.df_all = self.df_all.loc[0:10000]

        self.units = list(np.unique(self.df_all['unit']))
        self.units_var = tk.StringVar(value = self.units)
        self.unit_list = tk.Listbox(self, height=5, width=25, listvariable=self.units_var, font=("Verdana", 12))
        self.unit_list.place(relx=0.15, rely=0.1, anchor="e")

        scroll = tk.Scrollbar(self, orient="vertical", command=self.unit_list.yview)
        scroll.place(relx=0.15, rely=0.1, anchor="w", height=100)
        self.unit_list['yscrollcommand'] = scroll.set

        self.choose_unit = tk.Button(self, text="Choose Unit",fg="black", bg="lightgray",
                                          font=("Verdana", 24), width=13,
                                          command=self.open_selected)
        self.choose_unit.place(relx=0.16, rely=0.2, anchor="e")

        self.unit_list.bind('<<ListboxSelect>>', self.on_select_unit)

        self.features = list(self.df_all.columns)
        self.features_var = tk.StringVar(value = self.features)
        self.features_list = tk.Listbox(self, height=5, width=25, listvariable=self.features_var, font=("Verdana", 12))
        self.features_list.place(relx=0.15, rely=0.35, anchor="e")

        scroll2 = tk.Scrollbar(self, orient="vertical", command=self.features_list.yview)
        scroll2.place(relx=0.15, rely=0.35, anchor="w", height=100)
        self.features_list['yscrollcommand'] = scroll2.set

        self.choose_feat = tk.Button(self, text="Choose Feature",fg="black", bg="lightgray",
                                          font=("Verdana", 24), width=13,
                                          command=self.open_selected)
        self.choose_feat.place(relx=0.16, rely=0.48, anchor="e")

        self.features_list.bind('<<ListboxSelect>>', self.on_select_feat)

    def open_selected(self):
        self.single_unit = self.df_all[self.df_all['unit'] == self.selected_unit]
        #print(self.single_unit)


    def on_select_unit(self, event10):
        if not event10.widget.curselection():
            return
        index = self.unit_list.curselection()[0]
        self.selected_unit = self.units[index]

    def on_select_feat(self, event11):
        if not event11.widget.curselection():
            return
        index = self.features_list.curselection()[0]
        self.selected_feat = self.features[index]

    def optimize(self):
        self.x = self.single_unit.drop(self.selected_feat, axis=1)
        self.y = self.single_unit[self.selected_feat].to_frame()

        print(self.x.describe)
        print(self.y.describe)

        self.x = self.x.rename(str,axis="columns") 
        #self.y = self.y.rename(str,axis="columns") 

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, test_size=0.2, random_state=42)

        lab_enc = preprocessing.LabelEncoder()
        self.y_train = lab_enc.fit_transform(self.y_train)

        study = optuna.create_study(direction='maximize')
        study.optimize(self.objective, n_trials=100)

        best_params = study.best_params
        best_accuracy = study.best_value

        print(f"Best parameters: {best_params}")
        print(f"Best accuracy: {best_accuracy}")

    def objective(self, trial):
        n_estimators = trial.suggest_int('n_estimators', 10, 100)
        max_depth = trial.suggest_int('max_depth', 2, 32, log=True)

        model = RandomForestClassifier(n_estimators=n_estimators, max_depth=max_depth, random_state=42)

        model.fit(self.x_train, self.y_train)

        self.y_pred = model.predict(self.x_test)
        accuracy = accuracy_score(self.y_test, self.y_pred)

        return accuracy
    
    def train(self):
        self.x = self.single_unit.drop(self.selected_feat, axis=1)
        self.y = self.single_unit[self.selected_feat].to_frame()

        print(self.x.describe)
        print(self.y.describe)

        self.x = self.x.rename(str,axis="columns") 

        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x, self.y, test_size=0.2, random_state=42)

        lab_enc = preprocessing.LabelEncoder()
        self.y_train = lab_enc.fit_transform(self.y_train)

        model = RandomForestClassifier(n_estimators=51, max_depth=3, random_state=42)

        model.fit(self.x_train, self.y_train)

        self.y_pred = model.predict(self.x_test)
        accuracy = accuracy_score(self.y_test, self.y_pred)
        print(accuracy)

if __name__ == "__main__":
    tkinterApp(root).pack()
    root.mainloop()
