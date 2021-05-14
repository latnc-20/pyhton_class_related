import random
import string


password_list = []  # 空列表，用于存放生成的随机密码
s = string.ascii_lowercase + string.ascii_uppercase + string.digits  # 包含大小写字母和数字

def pwdgen(length):
    # 生成随机密码且同时包含大小写字母和数字
    password = random.choice(string.ascii_uppercase)
    password += random.choice(string.ascii_lowercase)
    password += random.choice(string.digits)
    password_list.append(password)  # 密码至少为3位，已同时包含大小写字母和数字

    if length > 3:
        for i in range(length - 3):
            p = random.choice(s)  # 使用random函数从字符串s中随机挑选一个元素
            password_list.append(p)

    # 将列表中的元素提取出来并连接成新的字符串组成密码
    pass_result = "".join(password_list)
    print('系统随机生成的密码为：{}'.format(pass_result))


print("*****系统随机生成密码*****")
while True:
    try:
        length = int(input("请设置你想取几位数的密码："))
    except:
        print("请输入整数数字。")
    else:
        if length < 3:
            print("密码至少为3位，请重新输入。")
        else:
            pwdgen(length)
            break

print("********************")
