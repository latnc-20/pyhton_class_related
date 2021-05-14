from tkinter import Tk, Canvas, Frame, Button, SUNKEN, LEFT, RIGHT


def up():
    global x, y
    canvas.create_line(x, y, x, y - 10, fill='green', width=1)
    x, y = x, y - 10


def down():
    global x, y
    canvas.create_line(x, y, x, y + 10, fill='blue', width=1)
    x, y = x, y + 10


def right():
    global x, y
    canvas.create_line(x, y, x + 10, y, fill='red', width=1)
    x, y = x + 10, y


def left():
    global x, y
    canvas.create_line(x, y, x - 10, y, fill='black', width=1)
    x, y = x - 10, y


root = Tk()
canvas = Canvas(root, height=100, width=200, background='white',
                relief=SUNKEN, borderwidth=3)
canvas.pack(side=LEFT)

box = Frame(root)
box.pack(side=RIGHT)

button = Button(box, text='up', command=up)
button.grid(row=0, column=0, columnspan=2)
button = Button(box, text='left', command=left)
button.grid(row=1, column=0)
button = Button(box, text='right', command=right)
button.grid(row=1, column=1)
button = Button(box, text='down', command=down)
button.grid(row=2, column=0, columnspan=2)

x, y = 50, 100
root.mainloop()
