# -*- coding:utf-8 -*-

import requests
import parsel
import os
import shutil
from time import sleep
# http://www.netbian.com/index_2.htm

if os.path.exists('../default_pic/'):
    pass
else:
    os.mkdir('../default_pic/')
    print('目录创建成功')

shutil.rmtree("../default_pic")
os.mkdir("../default_pic")

print("请输入下载图片的页码：")
index = input()

print("即将下载第"+index+"页图片！")

if(index == "1"):
    url = 'http://www.netbian.com/dongman/index.htm'
else:
    url = f'http://www.netbian.com/dongman/index_{index}.htm'
cookies = {
    'Cookie': '__cfduid=d892faf2d87d3fd9bd75b5606165cd68c1598431866; Hm_lvt_14b14198b6e26157b7eba06b390ab763=1598431867,1598516099; xygkqecookieinforecord=%2C12-22800%2C19-22803%2C12-22835%2C19-22699%2C19-22649%2C19-22775%2C; Hm_lpvt_14b14198b6e26157b7eba06b390ab763=1598516285'
}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
    'Referer': 'http://www.netbian.com/'
 
}
 
response = requests.get(url=url, headers=headers, cookies=cookies)
response.encoding = response.apparent_encoding
# print(response.text)
selector = parsel.Selector(response.text)
lis = selector.css('.list ul li a::attr(href)').getall()
# print(lis)
lis.pop(2)
lis.pop(2)
# http://www.netbian.com/desk/22847.htm
for i in lis:
    data_url = 'http://www.netbian.com' + i
    response = requests.get(url=data_url, headers=headers, cookies=cookies)
    response.encoding = response.apparent_encoding
    selector = parsel.Selector(response.text)
    img_url = selector.css('.pic p a img::attr(src)').get()
    title = selector.css('.pic p a img::attr(title)').get()
    img_url_response = requests.get(url=img_url, headers=headers, cookies=cookies)
    path = "/home/pi/live/default_pic/"+title+'.jpg'
 
    with open(path, mode='wb') as f:
        f.write(img_url_response.content)
    print('{}已经下载完'.format(title))

print("重命名图片文件……")
os.system("python3 /home/pi/live/gj/jrn.py")
os.system("sudo chmod -R 777 ../default_pic")
print("下载完成,将在3秒后关闭...")
sleep(1)
print("2")
sleep(1)
print("1")
sleep(1)
print("0")
