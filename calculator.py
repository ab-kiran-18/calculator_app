import tkinter as tk
from tkinter import NSEW, font
from tkinter.ttk import Button

LARGE_FONT_STYLE = ("San-Andreas", 25)
SMALL_FONT_STYLE = ("San-Andreas", 16)
DIGITS_FONT_STYLE = ("San-Andreas", 16)
DEFAULT_FONT_STYLE = ("San-Andreas", 16)
AC_FONT = ("San-Andreas", 16)
BRAC_FONT = ("San-Andreas" ,15)

OFF_WHITE = "#1a256e"  
LIGHT_BLUE = "cyan"
LIGHT_GREY = '#f5d78c'
LABEL_COLOR = 'white'
DIS_COLOR = '#11d448'

class calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry('310x500')
        # self.window.resizable(0,0)
        self.window.title('Calc')
        self.window.attributes('-alpha', 0.89)

        self.total_expression = ''
        self.current_expression = ''

        self.display_frame = self.create_display_frame()

        self.total_label, self.label = self.create_display_labels()


        self.digits={
            7:(1,1), 8:(1,2), 9:(1,3),
            4:(2,1), 5:(2,2), 6:(2,3),
            1:(3,1), 2:(3,2), 3:(3,3),
            '.':(4,1), 0:(4,2)  
        }
        self.operators = {
            "^" : "^",
            "/" : "\u00F7",
            "*" : "\u00D7",
            "-" : "-",
            "+" : "+"
        }
        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0,weight=1)
        for x in range(1,5):
            self.buttons_frame.rowconfigure(x,weight=1)
            self.buttons_frame.columnconfigure(x,weight=1)

        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()


    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equalsto_button()
        self.create_open_button()
        self.create_close_button()
        self.create_del_button()


    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg='#ebeef2',
                                 fg='black',padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True,fill='both')
    
        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg='#ebeef2',
                                 fg='black',padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True,fill='both')

        return total_label,label

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GREY)
        frame.pack(expand=True, fill='both')
        return frame

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()
    
    def changeonHover(self,button,HoverColor,LeaveColor):
        button.bind("<Enter>", func=lambda e: button.config(
                    background=HoverColor))
  
        button.bind("<Leave>", func=lambda e: button.config(
                    background=LeaveColor))


    def create_digit_buttons(self):
        for digit,grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg='white', fg='black', 
                                font=DIGITS_FONT_STYLE, borderwidth=0,command=lambda x=digit: self.add_to_expression(x)) 
            self.changeonHover(button,'#bec5cc','white')
            button.grid(row=grid_value[0],column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        if operator == '^':
            operator = '**'
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ''
        self.update_total_label()
        self.update_label()

    def create_operator_buttons(self):
        i=1
        for operator, symbol in self.operators.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg='#e1e4e8', fg='black',
                                 font=DEFAULT_FONT_STYLE, borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i,column=4,sticky=tk.NSEW)
            self.changeonHover(button,'#bec5cc','#e1e4e8')
            i+=1

    def clear(self):
        self.current_expression = ''
        self.total_expression = ''
        self.update_total_label()
        self.update_label()
        self.bind_keys()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text='CLEAR', bg='#e1e4e8', fg="black",
                             font=AC_FONT, borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW, columnspan=2)
        self.changeonHover(button,'#bec5cc','#e1e4e8')

    def delete(self):
        if self.current_expression == 'ERROR':
            self.total_expression = ''
            self.clear()
        else:
            c = len(self.current_expression)
            self.current_expression = self.current_expression[:c-1]
            t = len(self.total_expression)
            self.total_expression = self.total_expression[:t-1]
        self.update_total_label()
        self.update_label()

    def create_del_button(self):
        button = tk.Button(self.buttons_frame, text='\u2190', bg='#e1e4e8', fg='black',
                             font=AC_FONT, borderwidth=0, command=self.delete)
        button.grid(row=0, column=3, sticky=tk.NSEW, columnspan=2)
        self.changeonHover(button,'#bec5cc','#e1e4e8')

    def create_open_button(self):
        button = tk.Button(self.buttons_frame, text='(', bg='#e1e4e8', fg='black',
                             font=BRAC_FONT, borderwidth=0, command=lambda x='(': self.append_operator(x))
        button.grid(row=5, column=1, sticky=tk.NSEW) 
        self.changeonHover(button,'#bec5cc','#e1e4e8')

    def create_close_button(self):
        button = tk.Button(self.buttons_frame, text=')', bg='#e1e4e8', fg='black',
                            font=BRAC_FONT, borderwidth=0, command=lambda x=')': self.append_operator(x))
        button.grid(row=5,column=2,sticky=NSEW)
        self.changeonHover(button,'#bec5cc','#e1e4e8')

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = ''
        except Exception as e:
            self.current_expression = 'ERROR'
        finally:
            self.update_label()

    def create_equalsto_button(self):
        button = tk.Button(self.buttons_frame, text='=', bg='#71aef0', fg='white',
                             font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.evaluate)
        self.changeonHover(button,'#518ee8','#71aef0')
        button.grid(row=4, column=3, sticky=tk.NSEW, rowspan=2)


    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill='both')
        return frame

    def update_total_label(self):
        expression = self.total_expression
        if '**' in expression:
            op = '^'
            expression = expression.replace('**',f' {op} ')
        else:
            for operator,symbol in self.operators.items():
                expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)
    
    def update_label(self):
        self.current_expression = self.current_expression[:16]
        self.label.config(text=self.current_expression)

    def run(self):
        self.window.mainloop()

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event,digit=key: self.add_to_expression(digit))
        for key in self.operators:
            self.window.bind(key , lambda event, operator=key: self.add_to_expression(operator))
            
if __name__ == "__main__":
    calc = calculator()
    calc.run()