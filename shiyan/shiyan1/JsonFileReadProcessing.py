import os
import random
import json


def getFileList(path):
    filename = os.listdir(path)  # 所有图片的列表
    img_list = random.sample(filename, 5)  # 从所有图片列表中随机选取5张图片
    return img_list  # 返回所取5张图片的列表


def readJSON(json_path):
    with open(json_path, 'r') as f:  # 读取json文件内容
        temp = json.load(f)  # load将字符串解码为字典
    # print(type(temp))
    # print(type(temp['data']))
    return temp['data']  # 将字典temp中的‘data’(data为key)转换成list


path = 'C:\\Users\\24545\\Desktop\\Python\\1.Json_File_Read_Processing\\img'
json_path1 = 'TextVQA_0.5.1_val.json'
json_path2 = 'TextVQA_Rosetta_OCR_v0.2_val.json'

img = getFileList(path)
temp1 = readJSON(json_path1)  # 得到的列表其元素为字典类型
temp2 = readJSON(json_path2)

for img_id in img:
    img_name = img_id[0:-4]  # 去掉图片文件后缀名
    # print(img_name)
    print("图片的文件名是：{}".format(img_id))

    for it in temp1:  # it类型为字典
        if img_name in it.values():
            print("图片的宽度为：{}，高度为：{}".format(it['image_width'], it['image_height']))
            print("对应的问题是：{}".format(it['question']))
            print("问题的答案是：{}".format(it['answers']))
            break
    for it in temp2:
        if img_name in it.values():
            print("对应的光学字符识别是：{}".format(it['ocr_tokens']))
            print("============")
            break

# print(temp1[0])
# i = temp2[0]
# print(i.keys())


