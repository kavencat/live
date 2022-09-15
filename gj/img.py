# -*- coding:utf-8 -*-
import re
import os
import requests
import shutil
from time import sleep
 
#在bing下载图片 
 
headers = {
  "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) "
          "Gecko/20100101 Firefox/64.0")
}
 
def get_index(resolution, index=1):
  #url = f"https://bing.ioliu.cn/ranking?p={index}"
  url = f"https://bing.ioliu.cn/?p={index}"
  res = requests.get(url, headers=headers)
  urls = re.findall('pic=(.*?)\\.jpg', res.text)
  _old_resolution = urls[1].split("_")[-1]
  return {url.split("/")[-1].replace(_old_resolution, resolution): url.replace(_old_resolution, resolution) + ".jpg"
      for url in urls}
 
def download_pic(pics):
  if os.path.exists('../default_pic/'):
    pass
  else:
    os.mkdir('../default_pic/')
    print('目录创建成功')
  try:
    for pic_name, pic_url in pics.items():
      res = requests.get(pic_url, headers=headers)
      with open(f"../default_pic/{pic_name}.jpg", mode="wb") as f:
        f.write(res.content)
      print(f"{pic_name} 下载完成")
  except Exception as e:
    print("下载出错", e)
 
def input_index():
  #print("必应壁纸下载工具, 本工具未经资源站授权.")
  #print("仅做学习和交流之用, 随时有可能停止维护.")
  #print("目前资源站收容页数为87,当前仅提供1920x1080分辨率下载")
  while True:
    sleep(0.1)
    index = input("请输入要下载的页数(Max=150):")
    try:
      if index == "Q":
        exit()
      index = 150 if int(index) > 150 else int(index)
      return index
    except ValueError:
      print("请输入数字, 或输入Q退出!")
 
def main():
  shutil.rmtree("/home/pi/live/default_pic")
  os.mkdir("/home/pi/live/default_pic")
  index = input_index()
  i = 1
  while i <= index:
    print(f"当前第{i}页,共需要下载{index}页")
    pics = get_index("1920x1080", i)
    #print(pics)
    download_pic(pics)
    i += 1
    
  print("重命名图片文件……")
  os.system("python3 /home/pi/live/gj/jrn.py")
  print("下载完成,将在3秒后关闭...")
  sleep(1)
  print("2")
  sleep(1)
  print("1")
  sleep(1)
  print("0")
 
if __name__ == '__main__':
  main()
