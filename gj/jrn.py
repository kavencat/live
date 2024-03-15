# -*- coding:utf-8 -*-
import os
from PIL import Image
import time
#照片重命名

class ImageRename():
    def __init__(self):
        self.path = '../default_pic'
        
    def rename(self):
        filelist = os.listdir(self.path)
        total_num = len(filelist)
    
        i = 1
        for item in filelist:
            if item.endswith('.jpg'):
                src = os.path.join(os.path.abspath(self.path), item)
                dst = os.path.join(os.path.abspath(self.path), '000000' + format(str(i), '0>3s') + '.jpg')
                im = Image.open(src)
                img = im.resize((1280,720))
                img.save(src)
                os.rename(src, dst)
                print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' 转换 %s to %s ...' %(src, dst))
                i = i + 1
            print (time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' 共 %d 张图片重命名及尺寸转换 %d' %(total_num, i-1))
        
 
if __name__ == '__main__':
    newname = ImageRename()
    newname.rename()
