import random


class Player:  # 基类
    def __init__(self, name):
        self.name = name
        self.number = 0

    def get_name(self):
        return self.name


class Human(Player):  # 继承Player类
    def get_number(self):
        while True:
            try:
                self.number = int(input("{}选择的1~10之间的整数为：".format(self.name)))
            except:
                print("输入错误，请重新输入。")
            else:
                if 1 <= self.number <= 10:
                    return self.number
                else:
                    print("输入的数字超出范围，请重新输入。")


class Computer(Player):  # 继承Player类
    def get_number(self):
        self.number = random.randint(1, 10)
        print("{}选择的1~10之间的整数为：{}".format(self.name, self.number))
        return self.number


def undercut(player1, player2):
    player1_name = player1.get_name()
    player2_name = player2.get_name()
    num1 = player1.get_number()
    num2 = player2.get_number()
    if num1 - num2 == 1:
        print("{} WIN!".format(player2_name))
    elif num2 - num1 == 1:
        print("{} WIN!".format(player1_name))
    else:
        print("No winner!")


h1 = Human('Tom')
h2 = Human('Jerry')
c1 = Computer('Computer1')
c2 = Computer('Computer2')
undercut(h1, c1)
print("===============")
undercut(h1, h2)
print("===============")
undercut(c1, c2)
