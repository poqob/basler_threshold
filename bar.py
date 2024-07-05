import tkinter as tk
from tkinter import ttk
import run
import basler
# root window
root = tk.Tk()
root.geometry('400x300')  # Adjust window size to accommodate two sliders
root.resizable(False, False)
root.title('Slider Demo')

# 9 99
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)


# Define variables for each slider
slider1_value = tk.DoubleVar()
slider2_value = tk.DoubleVar()


def get_slider1_value():
    return '{: .2f}'.format(slider1_value.get())


def get_slider2_value():
    return '{: .2f}'.format(slider2_value.get())


def slider1_changed(event):
    value_label1.configure(text=get_slider1_value())
    basler.setvar(float(event))


def slider2_changed(event):
    value_label2.configure(text=get_slider2_value())
    basler.setvar0(float(event))

# Label for slider 1
slider_label1 = ttk.Label(
    root,
    text='Slider 1:'
)

slider_label1.grid(
    column=0,
    row=0,
    sticky='w'
)

# Slider 1
slider1 = ttk.Scale(
    root,
    from_=0,
    to=255,
    orient='horizontal',
    command=slider1_changed,
    variable=slider1_value
)

slider1.grid(
    column=1,
    row=0,
    sticky='we'
)

# Label for current value of slider 1
current_value_label1 = ttk.Label(
    root,
    text='Current Value:'
)

current_value_label1.grid(
    row=1,
    columnspan=2,
    sticky='n',
    ipadx=10,
    ipady=10
)

# Label to display current value of slider 1
value_label1 = ttk.Label(
    root,
    text=get_slider1_value()
)
value_label1.grid(
    row=2,
    columnspan=2,
    sticky='n'
)


# Label for slider 2 (similar structure)
slider_label2 = ttk.Label(
    root,
    text='Slider 2:'
)

slider_label2.grid(
    column=0,
    row=3,
    sticky='w'
)

slider2 = ttk.Scale(
    root,
    from_=0,
    to=255,
    orient='horizontal',  # Can adjust orientation here if desired
    command=slider2_changed,
    variable=slider2_value
)

slider2.grid(
    column=1,
    row=3,
    sticky='we'
)

current_value_label2 = ttk.Label(
    root,
    text='Current Value:'
)

current_value_label2.grid(
    row=4,
    columnspan=2,
    sticky='n',
    ipadx=10,
    ipady=10
)

value_label2 = ttk.Label(
    root,
    text=get_slider2_value()
)
value_label2.grid(
    row=5,
    columnspan=2,
    sticky='n'
)

import threading




# Dummy implementation of basler.run()
def basler_run():
    # Simulate running an OpenCV process
    basler.run()
# Tkinter GUI setup
def tkinter_run():
    root.mainloop()


def run():
    basler_thread = threading.Thread(target=basler_run)
    basler_thread.start()

    # Run tkinter in the main thread
    tkinter_run()

    # Wait for the basler thread to complete
    basler_thread.join()