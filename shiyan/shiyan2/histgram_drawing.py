from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


I = Image.open('image.jpg')  # 读入图片
im = np.array(I)  # 将图片转换为二维数组的像素点值
r, g, b = Image.Image.split(I)  # 将R，G，B通道分离
# 将得到的R，G，B三路通道的图片分别转换为二维数组的像素值
r1 = np.array(r).flatten()  # flatten()将二维数组转化为一维数组
g1 = np.array(g).flatten()
b1 = np.array(b).flatten()
plt.subplot(2, 1, 1)
plt.hist(r1, bins=256, facecolor='r', edgecolor='r', alpha=0.5)  # hist()，绘制直方图
plt.hist(g1, bins=256, facecolor='g', edgecolor='g', alpha=0.5)
plt.hist(b1, bins=256, facecolor='b', edgecolor='b', alpha=0.5)  # 分别画出三通道的直方图，然后叠加在一起
plt.title('图像转换前的直方图')
plt.xlabel('每个像素点的灰度值')
plt.ylabel('每个像素点灰度值出现的频率')


# 进行图像转换，PPT52页内容
im1 = 255 - im  # 反变换
im2 = (100 / 255) * im + 150  # 区间变换
im3 = 255 * (im / 255) ** 2  # 像素平方处理
pil_im = Image.fromarray(np.uint8(im3))  # 分别对im1, im2, im3执行
# pil_im是转换后得到的新图像，操作同上
pil_r, pil_g, pil_b = Image.Image.split(pil_im)
pil_r1 = np.array(pil_r).flatten()
pil_g1 = np.array(pil_g).flatten()
pil_b1 = np.array(pil_b).flatten()
plt.subplot(2, 1, 2)
plt.hist(pil_r1, bins=256, facecolor='r', edgecolor='r', alpha=0.5)
plt.hist(pil_g1, bins=256, facecolor='g', edgecolor='g', alpha=0.5)
plt.hist(pil_b1, bins=256, facecolor='b', edgecolor='b', alpha=0.5)
plt.title('图像转换后的直方图')
plt.xlabel('每个像素点的灰度值')
plt.ylabel('每个像素点灰度值出现的频率')
# 下面两段代码是设置中文字体，即直方图的标题和x,y轴的标注
plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.show()


