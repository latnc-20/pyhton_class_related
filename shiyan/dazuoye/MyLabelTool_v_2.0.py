import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import os
import json


# 显现界面的高度和宽度
WIN_WIDTH = 1200
WIN_HEIGHT = 600
# 标注信息的文本的宽度
TEXT_WIDTH = 500
TEXT_HEIGHT = 350
# 标注矩形的最小面积，防止误操作
MINI_RECT_AREA = 100


# 标注图片，写入标注信息
class LabelImage:
    def __init__(self, win, position, texts):
        self.win = win
        self.text_width = TEXT_WIDTH
        self.text_height = TEXT_HEIGHT
        self.rect_pos = []  # 标注的矩形区域
        for i in position:  # 已画的区域
            p = (round(i[0], 2), round(i[1], 2), round(i[2], 2), round(i[3], 2))
            self.rect_pos.append(p)

        self.top = None  # TopLevel窗口
        self.label = None  #
        self.text = None
        self.button = None
        self.content = []  # 保存输入的内容
        self.content.append(texts)  # 上一次写的标注内容
        # 弹出的写入窗口
        self.text_ui()

    # 保存文本内容并退出
    def save_and_exit(self, event):
        self.content.append(self.text.get(1.0, 'end'))  # 保存写入的内容
        self.top.destroy()  # 关闭窗口

    # 获取写入的内容并返回
    def get_text(self):
        return self.content

    # 延时显示，以便主应用程序在继续执行代码之前等待对话框被销毁
    def wait_window(self, win):
        win.wait_window(self.top)

    # 弹出的写入窗口
    def text_ui(self):
        self.top = tk.Toplevel(self.win)
        self.top.title('图片的标注信息')
        screen_w = self.top.winfo_screenwidth()
        screen_h = self.top.winfo_screenheight()
        x_off = int((screen_w - self.text_width) / 2)
        y_off = int((screen_h - self.text_height) / 2)
        # 弹出的窗口置于屏幕中央
        self.top.geometry('{}x{}+{}+{}'.format(self.text_width, self.text_height, x_off, y_off))
        self.top.attributes('-topmost', 'true')  # 窗口永远置于顶层
        self.top.resizable(False, False)

        self.label = tk.Label(self.top, text='所要标注的区域的位置为：\n'
                              + str(self.rect_pos) + '\n可按Esc键保存并退出',
                              font=('宋体', 12))
        self.label.place(x=0, y=0, width=self.text_width, height=50)
        self.button = tk.Button(self.top, text='确定')
        self.button.place(x=self.text_width - 180, y=self.text_height - 40, width=150, height=30)
        self.button.bind('<Button-1>', self.save_and_exit)  # 点击按钮保存并关闭窗口

        self.text = tk.Text(self.top, bd=3, insertbackground='red', font=('宋体', 15))
        self.text.place(x=0, y=50, width=self.text_width, height=self.text_height - 100)
        self.text.bind('<KeyPress-Escape>', self.save_and_exit)  # 按Esc键保存并退出
        last_string = self.content[-1].rstrip('\n')  # 去掉其最右侧的换行符
        self.text.insert(1.0, last_string)  # 显示上一次输入的内容

        # print()


# 在图片上画矩形
class DrawOnImg:
    def __init__(self, win, img, rect):
        self.win = win
        self.img_w = WIN_WIDTH
        self.img_h = WIN_HEIGHT
        self.img_now = img  # 当前选择的图片
        self.ImageScale = 1.0  # 图片缩放比例，用于还原矩形在图片中的实际坐标
        self.img_show = None  # 显示已缩小的图片
        self.im = None  # 通过ImageTk.PhotoImage()来显示的图片
        # 标注区域设置
        self.x, self.y = 0, 0
        self.loc = None  # 所画矩形的坐标
        self.select_area = []  # 存放所有所画矩形的坐标
        self.rect_pos = rect  # 已绘制的矩形的实际坐标

        self.topFrame = None  # 顶部容器TopLevel，用于展示所选中的图片
        self.top_canvas = None  # 展示图片并画图区域
        # 画矩形区域
        self.draw_on_img()

    # 计算图片缩小的比例
    def image_scale(self, img_name):
        img_width, img_height = img_name.size
        self.ImageScale = 1.0
        # 确定图片缩放比例，如果原图比图片显示区域大
        w = 1.0 * self.img_w / img_width
        h = 1.0 * self.img_h / img_height
        self.ImageScale = min([h, w])
        # 如果原始图片比显示区域小，则显示原图
        if w > 1.0 and h > 1.0:
            self.ImageScale = 1.0
        return self.ImageScale

    # 按下鼠标左键
    def left_button_press(self, event):
        self.x, self.y = event.x, event.y
        self.top_canvas.create_rectangle(self.x, self.y, event.x, event.y, outline='green', tags='L')
        # print('鼠标按下了')

    # 鼠标按下并移动，绘制矩形
    def mouse_move(self, event):
        # 通过Canvas中的coords方法绘制矩形
        self.top_canvas.coords('L', self.x, self.y, event.x, event.y)

    # 鼠标左键释放，保存所画的矩形
    def left_button_release(self, event):
        self.loc = self.top_canvas.bbox('L')  # 返回矩形的坐标
        area = (self.loc[2] - self.loc[0]) * (self.loc[3] - self.loc[1])
        if area > MINI_RECT_AREA:  # 所画矩形面积大于设置的最小值，才会保存
            self.select_area.append(self.loc)
        self.top_canvas.dtag('L', 'L')
        # print('鼠标松开了')

    # 按下鼠标右键，关闭画图区域
    def right_button_down(self, event):
        self.topFrame.destroy()

    # 延时显示，以便主应用程序在继续执行代码之前等待对话框被销毁
    def wait_window(self, win):
        win.wait_window(self.topFrame)

    # 选中矩形在图片的原始像素位置
    def ori_position(self):
        ori_p = []
        for p in self.select_area:
            ori_p.append((p[0] / self.ImageScale, p[1] / self.ImageScale,
                          p[2] / self.ImageScale, p[3] / self.ImageScale))
        return ori_p

    # 在图片上绘制矩形并显示
    def draw_on_img(self):
        self.ImageScale = self.image_scale(self.img_now)  # 调用方法，更新图片的实际缩放比例
        # 图片等比例缩放
        self.img_w = int(self.img_now.width * self.ImageScale)
        self.img_h = int(self.img_now.height * self.ImageScale)
        self.img_show = self.img_now.resize((self.img_w, self.img_h), Image.ANTIALIAS)

        for r in self.rect_pos:  # 传入已绘制的矩形的实际坐标
            self.select_area.append((r[0] * self.ImageScale, r[1] * self.ImageScale,
                                     r[2] * self.ImageScale, r[3] * self.ImageScale))

        # 创建顶部容器，放大图片，并绘制矩形
        self.topFrame = tk.Toplevel(self.win)
        # 使容器在屏幕中间显示
        screenwidth = self.topFrame.winfo_screenwidth()
        screenheight = self.topFrame.winfo_screenheight()
        x_offset = int((screenwidth - self.img_w) / 2)
        y_offset = int((screenheight - self.img_h) / 2)
        self.topFrame.geometry('{}x{}+{}+{}'.format(self.img_w, self.img_h, x_offset, y_offset))
        self.topFrame.overrideredirect(True)  # 不显示最大化、最小化按钮
        self.topFrame.attributes('-topmost', True)  # 窗口永远置于顶层
        self.top_canvas = tk.Canvas(self.topFrame, width=self.img_w, height=self.img_h, bg='white')
        self.im = ImageTk.PhotoImage(self.img_show)
        self.top_canvas.create_image(self.img_w // 2, self.img_h // 2, image=self.im)  # 使图片显示在中央

        if self.select_area:  # 显示已绘制的矩形
            for a in self.select_area:
                self.top_canvas.create_rectangle(a[0], a[1], a[2], a[3], outline='green')

        # 绑定鼠标事件，绘制矩形
        self.top_canvas.bind('<ButtonPress-1>', self.left_button_press)
        self.top_canvas.bind('<Button1-Motion>', self.mouse_move)  # 按下鼠标左键并拖动，绘制矩形
        self.top_canvas.bind('<ButtonRelease-1>', self.left_button_release)
        self.top_canvas.bind('<ButtonPress-3>', self.right_button_down)  # 按下鼠标右键，关闭画图区域
        self.top_canvas.pack(fill='both', expand=True)  # 使填满整个顶部容器


# 主程序，创建GUI并显示图片
class CreateUIAndShowImg(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        # 主窗口初始化
        self.title('场景文字图像标注小工具')
        self.win_width = WIN_WIDTH  # 窗口的高度和宽度
        self.win_height = WIN_HEIGHT
        self.screenwidth = self.winfo_screenwidth()
        self.screenheight = self.winfo_screenheight()
        self.x_offset = int((self.screenwidth - self.win_width) / 2)
        self.y_offset = int((self.screenheight - self.win_height) / 2)
        self.geometry("{}x{}+{}+{}".format(self.win_width, self.win_height,
                                           self.x_offset, self.y_offset))  # 使窗口在屏幕中央显示
        self.resizable(False, False)  # 窗口大小不可改变
        # 图片初始化
        self.image_now = None  # 原始图片
        self.img_scale = 1.0  # 图片缩放比例
        self.img_path = ''  # 文件路径
        self.num = -1  # 记录展示图片的顺序
        self.img_lists = []  # 图片名列表
        self.img_dirs = []  # 图片路径列表
        self.img_show_w = self.win_width * 0.8  # 图片显示的高度和宽度
        self.img_show_h = self.win_height
        self.img_show = None  # 显示已缩放的图片
        # 窗口内标签，按钮等初始化
        self.r_show_win_w = self.win_width - self.img_show_w
        self.r_show_win_h = self.win_height * 0.7  # 右边显示信息区域
        self.but_win_w = self.r_show_win_w  # 右边按钮区域
        self.but_win_h = self.win_height - self.r_show_win_h
        self.img_label = None  # 用于展示图片的label
        self.but_last = None  # 显示上一张图片按钮
        self.but_next = None  # 显示下一张图片按钮
        self.button1 = None  # 退出按钮
        self.button2 = None  # 选择本地图片按钮
        self.button3 = None  # 写入标注信息按钮
        self.button4 = None  # 删除选中区域按钮
        self.button5 = None  # 保存所有标注信息按钮
        self.listbox = None  # 显示所有标注位置的ListBox
        # label, button设置
        self.text_font = ('楷体', 13)
        self.label_h = 25
        self.but_width_1 = 25  # 显示上/下一张图片按钮
        self.but_height_1 = 35
        self.but_width_2 = 80  # 其他按钮
        self.but_height_2 = 30
        self.but_bg_1 = '#D5E0EE'
        self.but_active_bg_1 = '#BBEEFF'
        self.but_bg_2 = '#D2F0F4'
        self.but_active_bg_2 = '#70F3FF'
        # 选择区域
        self.clicks = 0  # 图片点击次数
        self.img_rect = []  # 记录矩形在原始图片的坐标
        self.be_selected_rect = []  # 被选中的矩形
        self.draw_rect = None  # 开始画矩形
        self.label_img = None  # 开始标记图片
        self.content = ''  # 标注的内容
        self.text1 = tk.StringVar(value='未选择标注区域！')
        self.init_str = '\n\t点击此处标注图片\n\n\t右击+Ctrl保存标注内容' \
                        '\n\t或点击“保存内容”按钮保存'
        self.text2 = tk.StringVar(value=self.init_str)
        # 写入的标注信息
        self.mess_list = []  # 标注位置和信息
        self.message_dict = {}  # 写入所有信息
        # 显示界面
        self.setup_ui()

    # 参数恢复初始化（点击上/下一张图片或重新选择图片时）
    def init_all(self):
        self.save_json()  # 防止误操作，提示是否保存所有标注信息为json文件
        self.img_rect.clear()  # 删除所有矩形坐标
        self.listbox.delete(0, 'end')  # 删除所有ListBox中的值
        self.text1.set('未选择标注区域！')
        self.content = ''
        self.be_selected_rect.clear()
        self.mess_list.clear()
        self.message_dict.clear()

    # 关闭窗口
    def close_win(self):
        if tk.messagebox.askokcancel(title='提示', message='确定要退出吗？'):
            self.destroy()

    # 缩放图片
    def resize_img(self, image_name):
        # 将图片等比例缩小，传入要缩放的图片
        img_width, img_height = image_name.size  # 图片的高度和宽度
        self.img_scale = 1.0
        # 确定图片缩放比例，如果原图比图片显示区域大
        w = 1.0 * self.img_show_w / img_width
        h = 1.0 * self.img_show_h / img_height
        self.img_scale = min([h, w])
        # 如果原始图片比显示区域小，则显示原图
        if w > 1.0 and h > 1.0:
            self.img_scale = 1.0
        w1 = int(self.img_scale * img_width)
        h1 = int(self.img_scale * img_height)
        return image_name.resize((w1, h1), Image.ANTIALIAS)  # 缩放后的图片

    # 在图片上标注矩形框并动态显示
    def show_and_draw_img(self):
        self.image_now = Image.open(self.img_path)
        self.img_show = self.resize_img(self.image_now)
        self.img_show = self.img_show.convert('RGB')  # 装换为RGB格式显示
        img_name = os.path.split(self.img_path)[-1]
        self.text2.set('\n\t当前显示的图片为：\n\t{}\n'.format(img_name) + self.init_str)
        draw = ImageDraw.Draw(self.img_show)  # 在图片上画出矩形标注区域
        for i in range(len(self.img_rect)):
            d = self.img_rect[i]
            if i in self.be_selected_rect:  # 如果是被选中的矩形，边界显示红色
                draw.rectangle((d[0] * self.img_scale, d[1] * self.img_scale,
                                d[2] * self.img_scale, d[3] * self.img_scale),
                               outline='red')
            else:  # 如果矩形未选中，边界显示绿色
                draw.rectangle((d[0] * self.img_scale, d[1] * self.img_scale,
                                d[2] * self.img_scale, d[3] * self.img_scale),
                               outline='green')
        im = ImageTk.PhotoImage(self.img_show)  # 显示已画了矩形的图片
        self.img_label.configure(image=im)  # Label动态显示图片
        self.img_label.image = im

    # 打开文件目录并显示选中最后一张图片
    def open_show_img(self):
        img_format = ['jpg', 'jpeg', 'png', 'gif', 'bmp']  # 要打开的图片的格式
        # 选择要打开的图片
        img_path = filedialog.askopenfilenames(filetypes=[("All Image File",
                                               "*.jpg *.jpeg *.png *.gif *.bmp")])
        if len(img_path) != 0:  # 选择了图片
            for path_name in img_path:  # 将路径与文件名分离
                img_dir, img_name = os.path.split(path_name)
                pos = img_name.find('.')
                if img_name[pos + 1:].lower() in img_format:  # 如果选择的是图片，则加入到img_lists列表
                    self.img_dirs.append(img_dir)
                    self.img_lists.append(img_name)

            # 显示所有选中的图片中的第一张
            if self.num < len(self.img_lists) - 1:
                self.num += 1
                self.img_path = os.path.join(self.img_dirs[self.num], self.img_lists[self.num])
                self.init_all()
                self.show_and_draw_img()
        else:
            self.text2.set('\n\t未选择图片！')

    # 显示下一张图片
    def show_next_img(self):  # 显示下一张图片
        if self.img_lists:  # 列表不为空（空为False）
            self.num += 1
            if self.num < len(self.img_lists):  # 如果图片列表不为空，且不是最后一张图片
                self.img_path = os.path.join(self.img_dirs[self.num], self.img_lists[self.num])
                # self.show_and_draw_img()
                self.init_all()  #
                self.show_and_draw_img()
            else:
                self.num -= 1
                # tk.messagebox.showinfo(title='提示', message='这是最后一张图片！')
                self.text2.set('\n\t这是最后一张图片！')
        else:
            self.text2.set('\n\t未选择图片！')

    # 显示上一张图片
    def show_last_img(self):  # 显示上一张图片
        if self.img_lists:  # 列表不为空（空为False）
            self.num -= 1
            if self.num >= 0:
                self.img_path = os.path.join(self.img_dirs[self.num], self.img_lists[self.num])
                self.init_all()  #
                self.show_and_draw_img()
            else:
                self.num += 1
                # tk.messagebox.showinfo(title='提示', message='这是第一张图片！')
                self.text2.set('\n\t这是第一张图片！')
        else:
            self.text2.set('\n\t未选择图片！')

    # 显示ListBox
    def show_listbox(self):
        self.listbox.delete(0, 'end')
        for i in self.img_rect:
            r = '({},{},{},{})'.format(round(i[0], 2), round(i[1], 2),
                                       round(i[2], 2), round(i[3], 2))
            self.listbox.insert('end', r)

    # 选中矩形
    def select_rect_on_listbox(self, event):
        be_selected_rect = self.listbox.curselection()
        self.be_selected_rect = list(be_selected_rect)
        if len(self.be_selected_rect) > 0:
            self.show_and_draw_img()  # 选中的矩形边界变为红色
            for i in self.be_selected_rect:
                p = self.img_rect[i]
                rect_pos = (round(p[0], 2), round(p[1], 2),
                            round(p[2], 2), round(p[3], 2))
                self.text1.set(str(rect_pos))
        else:
            self.text2.set('\n\t未选择标注区域！')

    # 删除选中的矩形
    def del_rect(self):
        if len(self.be_selected_rect) > 0:
            for i in range(len(self.img_rect)):
                if i in self.be_selected_rect:
                    self.be_selected_rect.remove(i)  # 删除i
                    self.img_rect.pop(i)  # 去掉第i位对应的值
            self.show_listbox()
            self.show_and_draw_img()
            self.text1.set('未选择标注区域！')
        else:
            self.text2.set('\n\t未选择标注区域！')

    # 点击图片，可放大图片并进行标注
    def click_img(self, event):
        if self.image_now is not None:  # 打开并显示了图片
            if self.draw_rect is None:  # 确保仅点击了一次图片
                self.draw_rect = DrawOnImg(self, self.image_now, self.img_rect)
                self.draw_rect.wait_window(self.draw_rect)  # 延时显示
                self.img_rect = self.draw_rect.ori_position()  # 所画矩形的原始坐标
                self.draw_rect = None
                self.show_listbox()  # 显示所画矩形的坐标
                self.show_and_draw_img()  # 显示图片和矩形
            else:
                self.text2.set('\n\t已点击图片！\n\t请画标注区域')
        else:
            self.text2.set('\n\t未选择图片！')

    # 输入文本内容，标注图片
    def label_image(self, event):
        if len(self.be_selected_rect) > 0:
            if self.label_img is None:  # 确保仅点击了一次
                pos = []  # 所要标注区域的位置
                for i in self.be_selected_rect:
                    pos.append(self.img_rect[i])

                self.label_img = LabelImage(self, pos, self.content)
                self.label_img.wait_window(self.label_img)  # 延时
                self.content = self.label_img.get_text()[-1]
                self.label_img = None
                self.text2.set('输入的标注内容为：\n'
                               + self.content + '\n\n\t内容未保存！'
                               + '\n\n\t右击+Ctrl保存标注内容'
                               + '\n\t或点击“保存内容”按钮保存')  # 动态显示内容
            else:
                self.text2.set('\n\t已点击！请输入标注信息！')
        else:
            # tk.messagebox.showinfo('提示', '未选择要标注的区域！')
            self.text2.set('\n\t未选择要标注的区域！')

    # 写入信息
    def write_json(self, event):
        if len(self.content) > 0:
            # 将图片名称更新到存有所有信息的字典中，键为image_name
            self.message_dict["image_name"] = self.img_lists[self.num]
            m0_dict = {}  # 存放标注位置和信息
            for i in self.be_selected_rect:  # 一次只能写入一个标注位置和信息，只会循环一次
                key_pos = "position" + str(i)
                key_con = "content" + str(i)
                m0_dict[key_pos] = self.img_rect[i]
                m0_dict[key_con] = self.content.rstrip('\n')
                if self.mess_list:  # 不为空
                    ind = []
                    for j in range(len(self.mess_list)):
                        if key_pos in self.mess_list[j]:  # 如果键在字典中
                            ind.append(j)
                    for k in ind:
                        self.mess_list.pop(k)  # 从列表中删除有key_pos键的这个字典
                    self.mess_list.append(m0_dict)  # 更新key_pos键的字典
                else:
                    self.mess_list.append(m0_dict)
            # 将标注位置和信息的列表更新到存有所有信息的字典中，键为label_message
            self.message_dict["label_message"] = self.mess_list
            # print(self.mess_list)
            # print(self.message_dict)
            self.text2.set(self.content + '\n\t图片标注成功！')
        else:
            self.text2.set('\n\t标注信息为空！')

    # 保存为json文件
    def save_json(self):
        if len(self.message_dict) > 0:
            if tk.messagebox.askokcancel('提示', '是否保存标注信息？'):
                l_format = -len(self.img_lists[self.num].split('.')[-1]) - 1
                # 打开要保存到本地的文件夹
                f_json = tk.filedialog.asksaveasfilename(
                    filetypes=[("Json File", "*.json")],
                    initialfile=self.img_lists[self.num][:l_format] + '.json')
                if f_json != '':
                    with open(f_json, 'w', encoding='utf-8') as f:
                        json.dump(self.message_dict, f, indent=4, ensure_ascii=False)
                    json_name = os.path.split(f_json)[-1]
                    self.text2.set('\n\t{}保存成功！'.format(json_name))
                else:
                    self.text2.set('\n\t未选择文件夹！\n\t标注信息未保存！')
            else:
                self.text2.set('\n\t标注信息未保存！')
        else:
            self.text2.set('\n\t标注信息为空！')

    def setup_ui(self):
        # 左边显示图片区域
        img_win = tk.Frame(self, width=self.img_show_w, height=self.img_show_h)
        img_win.pack(side='left')
        text_label = tk.Label(img_win, text='原始图片', font=('楷体', 15, 'bold'))
        text_label.place(x=0, y=0, width=self.img_show_w, height=self.label_h)
        self.img_label = tk.Label(img_win, relief='ridge', bg='white')  # 图片显示区域
        self.img_label.place(x=0, y=25, width=self.img_show_w, height=self.img_show_h - 25)
        self.img_label.bind('<ButtonPress-1>', self.click_img)

        self.but_last = tk.Button(img_win, text='<', relief='ridge', bg=self.but_bg_1,
                                  activebackground=self.but_active_bg_1,
                                  command=self.show_last_img)
        self.but_last.place(x=15, y=self.img_show_h / 2,
                            width=self.but_width_1, height=self.but_height_1)
        self.but_next = tk.Button(img_win, text='>', relief='ridge', bg=self.but_bg_1,
                                  activebackground=self.but_active_bg_1,
                                  command=self.show_next_img)
        self.but_next.place(x=self.img_show_w - 40, y=self.img_show_h / 2,
                            width=self.but_width_1, height=self.but_height_1)

        # 右边显示信息区域
        r_show_win = tk.Frame(self, width=self.r_show_win_w, height=self.r_show_win_h, bg='white')
        r_show_win.place(x=self.img_show_w, y=0)
        listbox_label = tk.Label(r_show_win, text='所有标注区域的坐标', font=self.text_font)
        listbox_label.place(x=0, y=0, width=self.r_show_win_w, height=self.label_h)
        # ListBox显示矩形的坐标
        self.listbox = tk.Listbox(r_show_win, bg='#DCF5FF', relief='ridge',
                                  selectbackground='#D5E0EE', selectborderwidth=3,
                                  selectforeground='#ED5736', selectmode='single')
        self.listbox.place(x=0, y=self.label_h, width=self.r_show_win_w, height=130)
        self.listbox.bind('<<ListboxSelect>>', self.select_rect_on_listbox)
        self.show_listbox()
        label_1 = tk.Label(r_show_win, text='所要标注的矩形位置为:', font=self.text_font)
        label_1.place(x=0, y=155, width=self.r_show_win_w, height=self.label_h)
        label_2 = tk.Label(r_show_win, textvariable=self.text1, bg='#DCF5FF', fg='red')  # 显示所选区域位置
        label_2.place(x=0, y=180, width=self.r_show_win_w, height=self.label_h)
        label_3 = tk.Label(r_show_win, text='提示操作区', font=self.text_font)
        label_3.place(x=0, y=205, width=self.r_show_win_w, height=self.label_h)
        label_4 = tk.Label(r_show_win, textvariable=self.text2, bg='#DCF5FF',
                           anchor='nw', justify='left', wraplength=self.r_show_win_w,
                           font=('楷体', 10))
        label_4.place(x=0, y=230, width=self.r_show_win_w, height=self.r_show_win_h - 230)
        label_4.bind('<Button-1>', self.label_image)  # 单击开始标注图片
        label_4.bind('<Control-Button-3>', self.write_json)  # 右击+Ctrl写入标注信息

        # 右边按钮区域
        but_win = tk.Frame(self, width=self.but_win_w, height=self.but_win_h, bg='white')
        but_win.place(x=self.img_show_w, y=self.r_show_win_h)
        self.button1 = tk.Button(but_win, text='退出', bg='#30dff3',
                                 activebackground=self.but_active_bg_2,
                                 command=self.close_win)
        self.button1.place(x=self.but_win_w - 80, y=self.but_win_h - 30,
                           width=80, height=30)
        self.button2 = tk.Button(but_win, text='选择图片', bg=self.but_bg_2,
                                 activebackground=self.but_active_bg_2,
                                 command=self.open_show_img)
        self.button2.place(x=self.but_win_w / 2 - self.but_width_2, y=20,
                           width=self.but_width_2 * 2, height=self.but_height_2)
        self.button3 = tk.Button(but_win, text='保存内容', bg=self.but_bg_2,
                                 activebackground=self.but_active_bg_2)
        self.button3.place(x=self.but_win_w / 2 - self.but_width_2 - 10, y=35 + self.but_height_2,
                           width=self.but_width_2, height=self.but_height_2)
        self.button3.bind('<Button-1>', self.write_json)
        self.button4 = tk.Button(but_win, text='删除矩形', bg=self.but_bg_2,
                                 activebackground=self.but_active_bg_2,
                                 command=self.del_rect)
        self.button4.place(x=self.but_win_w / 2 + 10, y=35 + self.but_height_2,
                           width=self.but_width_2, height=self.but_height_2)
        self.button5 = tk.Button(but_win, text='保存所有标注信息', bg=self.but_bg_2,
                                 activebackground=self.but_active_bg_2,
                                 command=self.save_json)
        self.button5.place(x=self.but_win_w / 2 - self.but_width_2, y=50 + self.but_height_2 * 2,
                           width=self.but_width_2 * 2, height=30)


if __name__ == '__main__':
    window = CreateUIAndShowImg()
    window.mainloop()
