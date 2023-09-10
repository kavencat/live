# coding:utf8
import os;
#替换字符串

old = "文泉驿微米黑";#需要替换的字符串
new = "WenQuanYi Micro Hei";#替换后的字符串
hz = ".ass";#需要替换文件的后缀
def reset():
    i = 0
    path = "/home/pi/live/downloads/";
    print("---------下载文件夹---------")
    #path = "/home/pi/live/default_mp3/";
    filelist = os.listdir(path)  # 该文件夹下所有的文件（包括文件夹）
    filelist.sort();
    for files in filelist:  # 遍历所有文件
        i = i + 1
        Olddir = os.path.join(path, files);  # 原来的文件路径
        if os.path.isdir(Olddir):  # 如果是文件夹则跳过
            continue;
        filename = os.path.splitext(files)[0];  # 文件名
        filetype = hz;  # 文件扩展名
        #filetype = '.info';  # 文件扩展名
        filePath=path+filename+filetype
        if os.path.splitext(files)[1] == hz and os.path.isfile(filePath):
            print(filePath)
            alter(filePath,old, new)

def reset1():
    i = 0
    #path = "/home/pi/live/downloads/";
    path = "/home/pi/live/default_mp3/";
    print("---------已播放文件夹---------")
    filelist = os.listdir(path)  # 该文件夹下所有的文件（包括文件夹）
    filelist.sort();
    for files in filelist:  # 遍历所有文件
        i = i + 1
        Olddir = os.path.join(path, files);  # 原来的文件路径
        if os.path.isdir(Olddir):  # 如果是文件夹则跳过
            continue;
        filename = os.path.splitext(files)[0];  # 文件名
        filetype = hz;  # 文件扩展名
        #filetype = '.info';  # 文件扩展名
        filePath=path+filename+filetype
        if os.path.splitext(files)[1] == hz and os.path.isfile(filePath):
            print(filePath)
            alter(filePath,old, new)

def alter(file,old_str,new_str):
    """
    将替换的字符串写到一个新的文件中，然后将原文件删除，新文件改为原来文件的名字
    :param file: 文件路径
    :param old_str: 需要替换的字符串
    :param new_str: 替换的字符串
    :return: None
    """
    with open(file, "r", encoding="utf-8") as f1,open("%s.bak" % file, "w", encoding="utf-8") as f2:
        for line in f1:
            if old_str in line:
                line = line.replace(old_str, new_str)
            f2.write(line)
    os.remove(file)
    os.rename("%s.bak" % file, file)
 
if __name__=='__main__':
    reset()
    reset1()
