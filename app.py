"""
Copyright <2022> <howhowkhain>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import tkinter as tk
from tkinter import messagebox


# closing the main window with a pop-up window for confirmation
def close_app():
    window.bell()
    if messagebox.askyesno(title="Quit?", message="Are you sure you want\nto quit this beautiful Calculator?"):
        window.destroy()


# function used for selecting which type of operation to be done and executing it.
# it is included also the protection against Error divizion by zero in which case the display will show "Error".
def op_execution():
    global result, first_number, second_number, number_1, number_2, operator_symbol
    if operator_symbol == "+":
        result = number_1 + number_2
    elif operator_symbol == "-":
        result = number_1 - number_2
    elif operator_symbol == "*":
        result = number_1 * number_2
    else:
        try:
            result = number_1 / number_2
        except ZeroDivisionError:
            result = "Error"
            display.delete(first=0, last=tk.END)
            display.insert(0, result)
        else:
            number.set(result)
    number_1 = 0
    number_2 = 0
    operator_symbol = ""


# function converting first_number and second_number from strings to integers or floats
def evaluate_numbers():
    global number_1, number_2, equality_count
    try:
        number_1 = int(first_number)
    except ValueError:
        try:
            number_1 = float(first_number)
            try:
                number_2 = int(second_number)
                op_execution()
                equality_count = True
                number.set(result)
            except ValueError:
                try:
                    number_2 = float(second_number)
                    op_execution()
                    equality_count = True
                    number.set(result)
                except ValueError as e:
                    display.delete(first=0, last=tk.END)
                    display.insert(0, e)
        except ValueError as e:
            display.delete(first=0, last=tk.END)
            display.insert(0, e)
    else:
        try:
            number_2 = int(second_number)
            op_execution()
            equality_count = True
            number.set(result)
        except ValueError:
            try:
                number_2 = float(second_number)
                op_execution()
                equality_count = True
                number.set(result)
            except ValueError as e:
                display.delete(first=0, last=tk.END)
                display.insert(0, e)


# complex function
# to store the first input as a first number when no 2nd input exist and performe calculation only with 1st number
# to store the second input as a second number and performe calculations with both numbers
# if already calculation done it will re-distribute the values of the first_number and of the second_number so to continue calculations if still equality simbol "=" not press yet.
def operator(b):
    global operator_count, string_1, operator_symbol, first_number, last_operator_symbol_used, string_2, second_number, number_1, number_2, equality_count, constant_number
    operator_symbol = b["text"]
    last_operator_symbol_used = b["text"]
    # if no Division by zero Error the process continue
    if result != "Error":
        # for initial calculations, when "=" not pressed yet
        if not equality_count:
            # initial calculation (the very first calculation) and "=" not yet pressed
            if result == None:
                if first_number != "" and string_2 != "":
                    second_number = string_2
                    string_2 = ""
                    constant_number = second_number
                    evaluate_numbers()
                    first_number = result
                    second_number = ""
                    operator_count += 1
                elif string_2 != "":
                    first_number = display.get()
                    second_number = display.get()
                    constant_number = second_number
                    evaluate_numbers()
                    first_number = result
                    second_number = ""
                    operator_count += 1
                elif string_1 != "":
                    first_number = string_1
                    string_1 = ""
                    operator_count += 1
                else:
                    first_number = "0"
                    operator_count += 1
            # if already calculations were done and following others but still "=" not yet pressed.
            else:
                if first_number != "" and string_2 != "":
                    second_number = string_2
                    string_2 = ""
                    constant_number = second_number
                    evaluate_numbers()
                    first_number = result
                    second_number = ""
                    operator_count += 1
        # if already "=" pressed at least once
        else:
            # if no 2nd input exist
            if string_2 == "":
                first_number = result
                operator_count += 1
            # if 2nd input exist
            else:
                second_number = string_2
                string_2 = ""
                constant_number = second_number
                evaluate_numbers()
                first_number = result
                second_number = ""
                operator_count += 1


# function executing calculation after each press of equality symbol "="
def equal():
    global number_1, number_2, string_2, first_number, second_number, constant_number, operator_symbol, constant_number, equality_count, string_1
    # if no Division by zero Error the process continue
    if result != "Error":
        # for initial calculations, when "=" not pressed yet
        if not equality_count:
            if operator_symbol != "" and string_2 != "":
                second_number = string_2
                string_2 = ""
                constant_number = second_number
                evaluate_numbers()
            elif operator_symbol != "" and string_2 == "":
                first_number = display.get()
                second_number = display.get()
                constant_number = second_number
                evaluate_numbers()
            elif result != None:
                operator_symbol = last_operator_symbol_used
                constant_number = display.get()
                second_number = display.get()
                evaluate_numbers()
            elif operator_symbol == "" and string_1 == "" and string_2 == "":
                number.set("0")
            elif operator_symbol == "" and string_1 == "-0" and string_2 == "":
                number.set("0")
                string_1 = ""
            elif string_1 != "" and string_2 == "":
                first_number = string_1
                number.set(first_number)
            elif operator_symbol == "" and string_2 == "":
                operator_symbol = last_operator_symbol_used
                first_number = constant_number
                second_number = result
                evaluate_numbers()
        # if already "=" pressed at least once
        else:
            if operator_symbol == "" and second_number == "":
                constant_number = result
                second_number = display.get()
                operator_symbol = last_operator_symbol_used
                evaluate_numbers()
            elif operator_symbol == "" and string_2 == "":
                first_number = constant_number
                second_number = result
                operator_symbol = last_operator_symbol_used
                evaluate_numbers()
            elif operator_symbol != "" and string_2 != "":
                second_number = string_2
                string_2 = ""
                constant_number = second_number
                evaluate_numbers()


# to determine if pozitive "+" sign or negative "-" sign are used in front of the number
def sign(b):
    global string_1, operator_count
    digit_pressed = b["text"]
    if digit_pressed == "+/-":
        if string_1 != "":
            if string_1[0] != "-":
                sign = "-"
                string_1 = sign + string_1
                number.set(string_1)
            else:
                sign = string_1[0]
                string_1 = string_1.replace(
                    sign, "")
                number.set(string_1)
        else:
            string_1 = "-0"
            number.set(string_1)
            string_1 = ""


# to initialize to zero all variables (reset)
def cancel():
    global string_1, string_2, operator_count, first_number, second_number, number_1, number_2, result, constant_number, last_operator_symbol_used, equality_count
    string_1 = ""
    string_2 = ""
    operator_count = 0
    first_number = ""
    second_number = ""
    constant_number = ""
    number_1 = 0
    number_2 = 0
    last_operator_symbol_used = ""
    equality_count = False
    result = None
    number.set("0")


# to store input as a strings and to filter which input to store as per operator_count variable
def clicked_button(b):
    global string_1, string_2
    digit_pressed = b["text"]
    if operator_count == 0:
        if digit_pressed == "0" and display.get() == "0":
            number.set("0")
        elif digit_pressed == "." or digit_pressed.isdigit():
            string_1 += digit_pressed
            number.set(string_1)
    else:
        if digit_pressed == "0" and display.get() == "0":
            number.set("0")
        elif digit_pressed == "." or digit_pressed.isdigit():
            string_2 += digit_pressed
            number.set(string_2)


# operator_count used to count how many times an operator was pressed before cancel button pressed
operator_count = 0
# strings used to store input digits
string_1 = ""
string_2 = ""
# variable used to store different operator symbols
# "+", "-", "*", "/"
operator_symbol = ""
# variable used to store first number input
first_number = ""
# variable used to store second number input
second_number = ""
# variable used to store a constant useful when no opearators are used in calculations
# except equality operator "="
constant_number = ""
# input numbers converted as a integer or float
number_1 = 0
number_2 = 0
# to track when a calculation was completed in which case the values are different than None
# this is default value
result = None
# same as the constant_number; used in calculation where no operator symbols are used
# except equality operator "="
last_operator_symbol_used = ""
# variable used to track first time use of equality operator
# False for no calculation done so far (initial value)
# True for if it was used at least one time
equality_count = False

# create GUI
window = tk.Tk()
window.title("Calculator")
window.config(background="#3cc1fa")
image = tk.PhotoImage(file="calculator-64.png")
window.tk.call("wm", "iconphoto", window._w, image)
# window.geometry("300x300+200+300")
window.resizable(width=False, height=False)
# create display
number = tk.StringVar()
number.set("0")
display_frame = tk.Frame(window, background="#3cc1fa")
display = tk.Entry(display_frame, width=10, font=(
    "Helvetica", "40", "bold"), textvariable=number, justify="right", background="#02f5ed")
display.pack()
display_frame.grid(row=0, columnspan=5)

# create buttons
b1 = tk.Button(window, text="1", width=4, height=2, font=(
    "Helvetica", "15", "bold"), command=lambda: clicked_button(b1), activebackground="#f0d5d3", background="#fabe3c")
b1.grid(row=3, column=0)
b2 = tk.Button(window, text="2", width=4, height=2, font=(
    "Helvetica", "15", "bold"), command=lambda: clicked_button(b2), activebackground="#f0d5d3", background="#fabe3c")
b2.grid(row=3, column=1)
b3 = tk.Button(window, text="3", width=4, height=2, font=(
    "Helvetica", "15", "bold"), command=lambda: clicked_button(b3), activebackground="#f0d5d3", background="#fabe3c")
b3.grid(row=3, column=2)
b4 = tk.Button(window, text="4", width=4, height=2, font=(
    "Helvetica", "15", "bold"), command=lambda: clicked_button(b4), activebackground="#f0d5d3", background="#fabe3c")
b4.grid(row=2, column=0)
b5 = tk.Button(window, text="5", width=4, height=2, font=(
    "Helvetica", "15", "bold"), command=lambda: clicked_button(b5), activebackground="#f0d5d3", background="#fabe3c")
b5.grid(row=2, column=1)
b6 = tk.Button(window, text="6", width=4, height=2, font=(
    "Helvetica", "15", "bold"), command=lambda: clicked_button(b6), activebackground="#f0d5d3", background="#fabe3c")
b6.grid(row=2, column=2)
b7 = tk.Button(window, text="7", width=4, height=2, font=(
    "Helvetica", "15", "bold"), command=lambda: clicked_button(b7), activebackground="#f0d5d3", background="#fabe3c")
b7.grid(row=1, column=0)
b8 = tk.Button(window, text="8", width=4, height=2, font=(
    "Helvetica", "15", "bold"), command=lambda: clicked_button(b8), activebackground="#f0d5d3", background="#fabe3c")
b8.grid(row=1, column=1)
b9 = tk.Button(window, text="9", width=4, height=2, font=(
    "Helvetica", "15", "bold"), command=lambda: clicked_button(b9), activebackground="#f0d5d3", background="#fabe3c")
b9.grid(row=1, column=2)
b0 = tk.Button(window, text="0", width=4, height=2, font=(
    "Helvetica", "15", "bold"), command=lambda: clicked_button(b0), activebackground="#f0d5d3", background="#fabe3c")
b0.grid(row=4, column=1)
c = tk.Button(window, text="C", width=4, height=2, font=(
    "Helvetica", "15", "bold"), command=cancel, activebackground="#f0d5d3", background="#fa723c")
c.grid(row=4, column=0)
decimal_b = tk.Button(window, text=".", width=4, height=2, font=(
    "Helvetica", "15", "bold"), command=lambda: clicked_button(decimal_b), activebackground="#f0d5d3", background="#fabe3c")
decimal_b.grid(row=4, column=2)
equal_b = tk.Button(window, text="=", width=4, height=2, font=(
    "Helvetica", "15", "bold"), command=equal, activebackground="#f0d5d3", background="#3cc1fa")
equal_b.grid(row=3, column=3)
sign_b = tk.Button(window, text="+/-", width=4, height=2, font=(
    "Helvetica", "15", "bold"), command=lambda: sign(sign_b), activebackground="#f0d5d3", background="#3cc1fa")
sign_b.grid(row=4, column=3)
plus_b = tk.Button(window, text="+", width=4, height=2, font=(
    "Helvetica", "15", "bold"), command=lambda: operator(plus_b), activebackground="#f0d5d3", background="#3cc1fa")
plus_b.grid(row=1, column=4)
minus_b = tk.Button(window, text="-", width=4, height=2, font=(
    "Helvetica", "15", "bold"), command=lambda: operator(minus_b), activebackground="#f0d5d3", background="#3cc1fa")
minus_b.grid(row=2, column=4)
multiply_b = tk.Button(window, text="*", width=4, height=2, font=(
    "Helvetica", "15", "bold"), command=lambda: operator(multiply_b), activebackground="#f0d5d3", background="#3cc1fa")
multiply_b.grid(row=3, column=4)
devide_b = tk.Button(window, text="/", width=4, height=2, font=(
    "Helvetica", "15", "bold"), command=lambda: operator(devide_b), activebackground="#f0d5d3", background="#3cc1fa")
devide_b.grid(row=4, column=4)

window.protocol("WM_DELETE_WINDOW", close_app)

# create a loop for main window so to be visible
window.mainloop()
