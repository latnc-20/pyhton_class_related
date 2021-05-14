import random


n = 100  # 范围上限
i = 0  # 猜数的次数
num = random.randint(1, n)  # 随机生成一个整数


class InputError(Exception):
    # 自定义异常类，继承普通异常基类 Exception
    def __init__(self, error):
        self.error = error
    def __str__(self):
        return self.error


while True:
    try:
        guess = int(input('输入一个1~{}之间的整数：'.format(n)))
        if guess < 1 or guess > n:  # 判断输入是否超出范围
            raise InputError(guess)  # raise 手动抛出异常

    except ValueError as v:
        print('输入错误，请输入1~{}之间的整数，你输入的是：'.format(n), v.args)
    except InputError as e:
        print('输入错误，请输入1~{}之间的整数，你输入的是：'.format(n), e.error)

    else:
        i += 1
        if guess == num:
            if i == 1:
                print('牛逼牛逼哈！一次就猜对了呢！')
            elif 1 < i <= 5:
                print('不错哈，一共猜了{}次猜对了。'.format(i))
            elif i > 5:
                print('真菜啊，一共猜了{}次猜对了。'.format(i))
            break
        elif n >= guess > num:
            print("比这个小")
        elif 1 <= guess < num:
            print('比这个大')

print('游戏结束！！！')
