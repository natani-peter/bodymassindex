from logging import exception
import customtkinter as ctk
import tkinter as tk
from settings import *


try:
    from ctypes import windll, c_int, byref, sizeof
except exception as e:
    print(e)


class Window(ctk.CTk):
    def __init__(self):
        super(Window, self).__init__(fg_color=green)

        # attributes
        self.title('FIND YOUR BMI')
        self.geometry('400x500+600+5')
        self.attributes('-topmost', 1)
        self.resizable(False, False)
        self.set_title_color()

        # layout
        self.columnconfigure(0, weight=1, uniform='a')
        self.rowconfigure((0, 1, 2, 3), weight=1, uniform='a')
        # variables
        self.country_units = tk.BooleanVar(value=True)
        self.weight = tk.DoubleVar(value=65.5)
        self.height = tk.IntVar(value=170)
        self.bmi = tk.StringVar()
        self.comment = tk.StringVar(value='NORMAL WEIGHT')
        self.update_bmi(self)

        # tracing
        self.weight.trace('w', self.update_bmi)
        self.height.trace('w', self.update_bmi)
        self.country_units.trace('w', self.change_units)

        # widgets
        Results(self, self.bmi)
        self.weight_input = Weight(self, self.weight, self.country_units)
        self.length_units = Length(self, self.height, self.country_units)
        Comment(self, self.comment)
        Switch(self, self.country_units)
        self.mainloop()

    def change_units(self, *args):
        self.length_units.update_length(self.height.get())
        self.weight_input.use(self.weight.get())

    def update_bmi(self, *args):
        weight = self.weight.get()
        height = self.height.get() / 100
        bmi = round((weight / height ** 2), 2)
        self.bmi.set(str(bmi))

        if bmi < 18.5:
            self.comment.set('UNDER WEIGHT')
        elif 18.5 <= bmi <= 24.9:
            self.comment.set('NORMAL WEIGHT')
        elif bmi > 25:
            self.comment.set('OVER WEIGHT')

    def set_title_color(self):
        try:
            current_window_id = windll.user32.GetParent(self.winfo_id())
            windll.dwmapi.DwmSetWindowAttribute(current_window_id, 35, byref(c_int(title_color)), sizeof(c_int))
        except exception as ee:
            print(ee)


class Results(ctk.CTkLabel):
    def __init__(self, parent, results):
        font = ctk.CTkFont(family='Times New Roman', size=main_text, weight='bold')
        super(Results, self).__init__(master=parent, textvariable=results, text='24.1', font=font, text_color=white)
        self.grid(row=0, column=0, rowspan=2, sticky='news')


class Weight(ctk.CTkFrame):
    def __init__(self, parent, weight, units):
        super(Weight, self).__init__(master=parent, fg_color=white)
        self.grid(row=2, column=0, sticky='news', padx=8, pady=8)
        self.weight = weight
        self.units = units
        self.columnconfigure(0, weight=2, uniform='a')
        self.columnconfigure(1, weight=1, uniform='a')
        self.columnconfigure(2, weight=3, uniform='a')
        self.columnconfigure(3, weight=1, uniform='a')
        self.columnconfigure(4, weight=2, uniform='a')
        self.rowconfigure(0, weight=2, uniform='a')
        self.rowconfigure(1, weight=1, uniform='a')

        big_plus_button = ctk.CTkButton(self, command=lambda: self.update_weight(('big', 'plus')), text='+',
                                        fg_color=gray, text_color=black, hover_color=light_gray)
        big_plus_button.grid(row=0, column=4, sticky='news', pady=8, padx=8)

        small_plus_button = ctk.CTkButton(self, command=lambda: self.update_weight(('small', 'plus')), text='+',
                                          fg_color=light_gray, text_color=black, hover_color=gray)
        small_plus_button.grid(row=0, column=3, sticky='news', pady=10)

        self.weight_value = tk.StringVar(value=str(self.weight.get()) + 'kg')
        font = ctk.CTkFont(family=family, size=input_text)
        weight_label = ctk.CTkLabel(self, textvariable=self.weight_value, text_color=black, font=font)
        weight_label.grid(row=0, column=2, sticky='news')

        big_minus_button = ctk.CTkButton(self, command=lambda: self.update_weight(('big', 'minus')), text='-',
                                         fg_color=gray, text_color=black, hover_color=light_gray)
        big_minus_button.grid(row=0, column=0, sticky='news', pady=8, padx=8)

        small_minus_button = ctk.CTkButton(self, command=lambda: self.update_weight(('small', 'minus')), text='-',
                                           fg_color=light_gray, text_color=black, hover_color=gray)
        small_minus_button.grid(row=0, column=1, sticky='news', pady=10)

        ctk.CTkSlider(self, command=self.use, from_=0, to=215, variable=self.weight, progress_color=green,
                      fg_color=white, button_color=green, button_hover_color=dark_green).grid(column=0, columnspan=5,
                                                                                              row=1, sticky='we')

    def update_weight(self, info=None):
        if info:
            if self.units.get():
                amount = 1 if info[0] == 'big' else 0.1
            else:
                amount = 0.453592 if info[0] == 'big' else 0.453592 / 16

            if info[1] == 'plus':
                self.weight.set(round((self.weight.get() + amount), 2))
            else:
                self.weight.set(round((self.weight.get() - amount), 2))

            if self.units.get():
                self.weight_value.set(f'{self.weight.get()}kg')
            else:
                raw_ounces = self.weight.get() * 2.20462 * 16
                pound, ounce = divmod(raw_ounces, 16)
                self.weight_value.set(f'{int(pound)}lb {int(ounce)}oz')

    def use(self, value):
        now = round(value, 2)
        self.weight.set(now)

        if self.units.get():
            self.weight_value.set(f'{self.weight.get()}kg')
        else:
            raw_ounces = now * 2.20462 * 16
            pound, ounce = divmod(raw_ounces, 16)
            self.weight_value.set(f'{int(pound)}lb {int(ounce)}oz')


class Length(ctk.CTkFrame):
    def __init__(self, parent, height, units):
        super(Length, self).__init__(master=parent, fg_color=white)
        self.grid(row=3, column=0, sticky='news', pady=8, padx=8)
        self.height = height
        self.units = units
        self.height_value = tk.StringVar(value=str(float(self.height.get()) / 100))
        slider = ctk.CTkSlider(self, command=self.update_length, fg_color=gray, progress_color=green,
                               button_color=green,
                               button_hover_color=dark_green, from_=50, to=300)
        slider.pack(side='left', expand=True, fill='x')
        font = ctk.CTkFont(family=family, size=input_text)
        self.output_length = tk.StringVar(value=f'{self.height_value.get()}m')
        length = ctk.CTkLabel(self, text_color=black, textvariable=self.output_length, text='1.65m', font=font)
        length.pack(side='left', fill='y', padx=5)

    def update_length(self, value):
        if self.units.get():
            centimeters = round(value, 5)
            meters = value / 100
            self.output_length.set(f'{round(meters, 2)}m')
            self.height.set(centimeters)
        else:
            feet, inch = divmod(value / 2.54, 12)
            self.output_length.set(f'{int(feet)}\' {int(inch)}"')


class Switch(ctk.CTkLabel):
    def __init__(self, parent, units):
        font = ctk.CTkFont(family=family, size=24, weight='bold')
        super(Switch, self).__init__(master=parent, fg_color=green, text_color=black, text='METRIC', font=font)
        self.country = units
        self.place(relx=0.98, rely=0.02, anchor='ne')

        self.bind('<Button>', self.change_units)

    def change_units(self, event):
        self.country.set(not self.country.get())

        if self.country.get():
            self.configure(text='METRIC')
        else:
            self.configure(text='IMPERIAL')


class Comment(ctk.CTkLabel):
    def __init__(self, parent, comment):
        font = ctk.CTkFont(family=family, size=26, weight='bold')
        self.comment = comment
        super(Comment, self).__init__(master=parent, fg_color=green, text_color=black, text='METRIC', font=font,
                                      textvariable=self.comment)
        self.place(relx=0.5, rely=0.45, anchor='center')


if __name__ == '__main__':
    Window()
