import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os


def close_window():  # 关闭整个界面
    global window
    # if tk.messagebox.askokcancel(title='提示', message='确定要退出吗？'):
    window.destroy()


def resize_img(img_name, show_width, show_height):
    # 将图片等比例缩小，传入要缩小的图片，要显示的屏幕的宽和高
    img_width, img_height = img_name.size  # 图片的高度和宽度
    w = 1.0 * show_width / img_width
    h = 1.0 * show_height / img_height
    f = min([h, w])  # 确定图片缩小比例
    w1 = int(f * img_width)
    h1 = int(f * img_height)
    return img_name.resize((w1, h1), Image.ANTIALIAS)  # 缩小后的图片


def show_image(img_path):  # 显示图片
    global win_width, win_height
    img = Image.open(img_path)
    img_0 = resize_img(img, win_width * 0.75, win_height / 2)  # 将要显示的图片等比例缩放
    im = ImageTk.PhotoImage(image=img_0)  # 利用PIL打开非gif的其他格式的图片
    img_label.configure(image=im)  # 动态显示label图片
    img_label.image = im


def select_img():  # 从本地文件中选择图片
    global os_path, img_lists, img_dirs, img_num
    img_format = ['jpg', 'png', 'gif', 'bmp', 'jpeg', 'JPG', 'PNG', 'GIF', 'BMP', 'JPEG']
    os_path = filedialog.askopenfilenames()  # 选择要打开的图片
    for path_name in os_path:  # 将路径与文件名分离
        img_dir, img_name = os.path.split(path_name)
        pos = img_name.find('.')
        if img_name[pos+1:] in img_format:  # 如果选择的是图片，则加入到img_lists列表
            img_dirs.append(img_dir)
            img_lists.append(img_name)

    if img_lists:
        img_num = 0
        show_image(os.path.join(img_dirs[img_num], img_lists[img_num]))

    print(os_path)
    print(img_lists)
    print(img_dirs)


def show_next_image():
    global img_num

    if img_lists:  # 列表不为空（空为False）
        img_num += 1
        if img_num < len(img_lists):
            print(img_num)
            img_path = os.path.join(img_dirs[img_num], img_lists[img_num])  # 要显示的图片的路径
            print(img_path)
            show_image(img_path)
        else:
            img_num -= 1
            tk.messagebox.showinfo(title='提示', message='已是最后一张图片！')
            print(img_num)
            print(img_lists)
            print(img_dirs)
            print(os_path)
            print('已是最后一张图片！')
    else:
        tk.messagebox.showerror(title='错误', message='未选择图片！')
        print('未选择图片！')


def show_last_image():  # 显示上一张图片，逻辑同show_next_image()
    global img_num
    if img_lists:
        img_num -= 1
        if img_num >= 0:
            print(img_num)
            img_path = os.path.join(img_dirs[img_num], img_lists[img_num])
            show_image(img_path)
        else:
            img_num += 1
            tk.messagebox.showinfo(title='提示', message='已是第一张图片！')
            print(img_num)
            print('已是第一张图片！')
    else:
        tk.messagebox.showerror(title='错误', message='未选择图片！')
        print('未选择图片！')


def screen_shoot():
    global window
    top_win = tk.Toplevel(window, width=win_width, height=win_height)
    # top_win.overrideredirect(True)  # 不显示最大化、最小化按钮
    top_win.attributes('-topmost', 'true')  # 窗口永远置于顶层，除非窗口被关闭或attributes改变
    top_canvas = tk.Canvas(top_win, width=win_width, height=win_height, bg='pink')
    img_canvas = top_canvas.create_image()
    top_canvas.pack()

    print('0000')


os_path = 'D:'
img_num = -1
# num = -1
img_lists = []  # 图片名列表
img_dirs = []  # 图片路径列表
# button设置
but_bg = '#D5E0EE'
but_active_bg = '#BBEEFF'
# 窗口宽度和高度
win_width = 1000
win_height = 720


# UI界面
window = tk.Tk()
window.title('场景文字图像标注小工具')
screen_width = window.winfo_screenwidth()  # 获取屏幕的宽和高
screen_height = window.winfo_screenheight()
screen_left = (screen_width - win_width) / 2
screen_top = (screen_height - win_height) / 2
window.geometry('%dx%d+%d+%d' % (win_width, win_height, screen_left, screen_top))  # 窗口居中显示
window.resizable(0, 0)  # 设置窗口是否可变，True可变或0 ，1


# 左边显示图片区域
img_Frame = tk.Frame(window, width=win_width * 0.75, height=win_height)
img_Frame.pack(side='left')

text_label = tk.Label(img_Frame, text='原始图片')
text_label.place(x=win_width * 0.2, y=0, width=100, height=20)
img_label = tk.Label(img_Frame, relief='ridge')  # 图片显示区域
img_label.place(x=0, y=20, width=win_width * 0.75, height=win_height / 2)

but1 = tk.Button(img_Frame, text='<', relief='ridge', bg=but_bg,
                 activebackground=but_active_bg, command=show_last_image)
but1.place(x=10, y=win_height / 4, width=20, height=30)
but2 = tk.Button(img_Frame, text='>', relief='ridge', bg=but_bg,
                 activebackground=but_active_bg, command=show_next_image)
but2.place(x=win_width * 0.75 - 30, y=win_height / 4, width=20, height=30)


# 右边显示操作区域
button_Frame = tk.Frame(window, width=win_width * 0.25, height=win_height, bg='white')
button_Frame.pack(side='right')

button0 = tk.Button(button_Frame, text='退出', command=close_window)
button0.place(x=win_width * 0.25 * 0.70, y=win_height * 0.85, width=50, height=30)
button1 = tk.Button(button_Frame, text='选择图片目录', bg=but_bg,
                    activebackground=but_active_bg, command=select_img)
button1.place(x=10, y=20, width=100, height=40)
button2 = tk.Button(button_Frame, text='标注图片', bg=but_bg,
                    activebackground=but_active_bg, command=screen_shoot)
button2.place(x=10, y=100, width=100, height=40)
"""
button3 = tk.Button(button_Frame, text='上一张图片', bg=but_bg,
                    activebackground=but_active_bg, command=show_last_image)
button3.place(x=10, y=180, width=100, height=40)
"""


window.mainloop()

