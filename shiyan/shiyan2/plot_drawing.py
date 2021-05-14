# -*- coding: utf-8 -*-
"""
Created on Wed Apr 21 15:20:46 2021

@author: PC-001
"""
import matplotlib.pyplot as plt
import numpy as np

# 阴影区域
def Shadow(a, b):
    ix = (x > a) & (x < b)
    plt.fill_between(x, y, 0, where=ix, facecolor='grey', alpha=0.25)
    plt.text(0.5 * (a + b), 0.2, "$\int_a^b f(x)\mathrm{d}x$",
             horizontalalignment='center')
        
# 横纵坐标
def XY_Axis(x_start, x_end, y_start, y_end):
    plt.xlim(x_start, x_end)
    plt.ylim(y_start, y_end)
    plt.xticks([np.pi/3, 2 * np.pi/3, 1 * np.pi, 4 * np.pi/3, 5 * np.pi/3],
               ['$\pi/3$', '$2\pi/3$', '$\pi$', '$4\pi/3$', '$5\pi/3$'])
        
        
x = np.linspace(0.0, 6.0, 100)
y = np.cos(2 * np.pi * x) * np.exp(-x)+0.8
z = 0.5 * np.cos(x ** 2)+0.8
note_point, note_text, note_size = (1, np.cos(2 * np.pi) * np.exp(-1)+0.8), (1, 1.4), 10
plt.plot(x, y, 'b', label="$decay$", color='g', linewidth=4)  # 右上角图标说明
plt.plot(x, z, "r--", label="$cos(x^2)$", linewidth=2)
plt.xlabel('时间(s)')
plt.ylabel('幅度(mV)')
plt.title(u"阻尼衰减曲线绘制")
plt.rcParams['font.family'] = 'SimHei'
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.annotate('$\cos(2 \pi t) \exp(-t)$', xy=note_point, xytext=note_text, fontsize=note_size,
             arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=.1"))
XY_Axis(0, 5, 0, 1.8)
Shadow(0.8, 3)
plt.legend()
plt.show()

