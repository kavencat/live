#coding:utf-8
import os
import sys
import time
import random
from mutagen.mp3 import MP3
import var_set
import shutil
import _thread
import ass_maker

path = var_set.path #引入设置路径
rtmp = var_set.rtmp #引入设置的rtmp网址
live_code = var_set.live_code   #引入设置rtmp参数
deviceType = var_set.deviceType
vb = var_set.vb
stlf = var_set.stle #引入设置的直播形式

def get_v():
    if deviceType == "pi":
        return "h264_omx"
    elif deviceType == "vps":
        return "libx264"
        
def get_s():
    if stlf == "flv":
        return "flv"
    elif stlf == "mpegts":
        return "mpegts"

def w_log(nr,file,w):#nr写入文件内容，file写入的文件名，wd文件打开方式
    try:
        lfile = open(file, w)
        lfile.writelines(nr)
        lfile.close()
        print('写入记录成功！')
    except:
        print('写入记录失败！')

#格式化时间，暂时没啥用，以后估计也没啥用
def convert_time(n):
    s = n%60
    m = int(n/60)
    return '00:'+"%02d"%m+':'+"%02d"%s

#删除已palyID
def delpid(id):
    try:
        f = open ("play.log","r",encoding='utf-8')
        f1 = open ("play2.log",'w+',encoding='utf-8')
        lines = f.readlines()
        for lines in lines:
            if id not in lines:
                f1.write(lines)
        f.close
        f1.close
        os.remove("play.log")
        os.rename("play2.log","play.log")
    except:
        return False

#查找已点播歌曲文件名
def rname(id):
    try:
        f = open("songs.log","r",encoding='utf-8')
        lines = f.readlines()
        for lins in lines:
            if id in lins:
                return lins[-13:-1:]
                break
        f.close
    except:
        return False

#移动放完的视频到缓存文件夹
def remove_v(filename):
    try:
        shutil.move(path+'/downloads/'+filename,path+'/default_mp3/')
    except Exception as e:
        print(e)
    try:
        os.remove(path+'/downloads/'+filename.replace(".flv",'')+'ok.ass')
        #os.remove(path+'/downloads/'+filename.replace(".flv",'')+'ok.info')
        shutil.move(path+'/downloads/'+filename.replace(".flv",'')+'ok.info',path+'/default_mp3/')
    except Exception as e:
        print(e)
        print('delete error')

while True:
    try:
        if (time.localtime()[3] >= 22 or time.localtime()[3] <= 5) and var_set.play_videos_when_night:
            print('night is comming~')  #晚上到咯~
            night_files = os.listdir(path+'/night') #获取所有缓存文件
            night_files.sort()    #排序文件
            night_ran = random.randint(0,len(night_files)-1)    #随机抽一个文件
            if(night_files[night_ran].find('.flv') != -1):  #如果为flv视频
                #直接暴力推流
                print('ffmpeg -threads 0 -re -i "'+path+"/night/"+night_files[night_ran]+'" -vcodec copy -acodec aac -f flv "'+rtmp+live_code+'"')
                os.system('ffmpeg -threads 0 -re -i "'+path+"/night/"+night_files[night_ran]+'" -vcodec copy -acodec aac -f flv "'+rtmp+live_code+'"')
            if(night_files[night_ran].find('.mp3') != -1):  #如果为mp3
                pic_files = os.listdir(path+'/default_pic') #获取准备的图片文件夹中的所有图片
                pic_files.sort()    #排序数组
                pic_ran = random.randint(0,len(pic_files)-1)    #随机选一张图片
                audio = MP3(path+'/night/'+night_files[night_ran])    #获取mp3文件信息
                seconds=audio.info.length   #获取时长
                print('mp3 long:'+convert_time(seconds))
                if not os.path.isfile(path+'/night/'+night_files[night_ran]+'.ass'):
                    ass_maker.make_ass('../night/'+night_files[night_ran].replace('.mp3',''),'当前是晚间专属时间哦~时间范围：晚上22点-凌晨5点\\N大家晚安哦~做个好梦~\\N当前文件名：'+night_files[night_ran],path)
                print('ffmpeg -threads 0 -re -loop 1 '+var_set.r+' -t '+str(int(seconds))+' -f image2 -i "'+path+'/default_pic/'+pic_files[pic_ran]+'" -i "'+path+'/night/'+night_files[night_ran]+'" -vf ass="'+path+'/night/'+night_files[night_ran]+'.ass" -pix_fmt yuvj420p -c:v '+get_v()+' -preset:v superfast '+var_set.bitrate+' -acodec aac -f '+get_s()+var_set.vb+' "'+rtmp+live_code+'"')
                os.system('ffmpeg -threads 0 -re -loop 1 '+var_set.r+' -t '+str(int(seconds))+' -f image2 -i "'+path+'/default_pic/'+pic_files[pic_ran]+'" -i "'+path+'/night/'+night_files[night_ran]+'" -vf ass="'+path+'/night/'+night_files[night_ran]+'.ass" -pix_fmt yuvj420p -c:v '+get_v()+' -preset:v superfast '+var_set.bitrate+' -acodec aac -f '+get_s()+var_set.vb+' "'+rtmp+live_code+'"')
            continue
        
        if(len(os.listdir(path+'/downloads'))==0):
            print("空")
            mp3_files = os.listdir(path+'/default_mp3') #获取所有缓存文件
            mp3_files.sort()    #排序文件
            mp3_ran = random.randint(0,len(mp3_files)-1)    #随机抽一个文件
            if(mp3_files[mp3_ran].find('.mp3') != -1):  #如果是mp3文件
                pic_files = os.listdir(path+'/default_pic') #获取准备的图片文件夹中的所有图片
                pic_files.sort()    #排序数组
                pic_ran = random.randint(0,len(pic_files)-1)    #随机选一张图片
                audio = MP3(path+'/default_mp3/'+mp3_files[mp3_ran])    #获取mp3文件信息
                seconds=audio.info.length   #获取时长
                print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' MP3文件为：'+mp3_files[mp3_ran])
                print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' 背景文件为：'+pic_files[pic_ran])
                w_log(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n'+'MP3文件为：'+mp3_files[mp3_ran]+'\n'+'背景文件为：'+pic_files[pic_ran]+'\n',path+'/log/screenlog_playing.log',"a+")
                print('mp3 long:'+convert_time(seconds))
                #推流
                if(os.path.isfile(path+'/default_mp3/'+mp3_files[mp3_ran].replace(".mp3",'')+'.ass')):
                    if os.path.isfile(path+"/default_mp3/"+mp3_files[mp3_ran].replace(".mp3",'')+'.jpg'):
                        print('ffmpeg -threads 0 -re -loop 1 '+var_set.r+' -t '+str(int(seconds))+' -f image2 -i "'+path+'/default_pic/'+pic_files[pic_ran]+'" -i "'+path+"/default_mp3/"+mp3_files[mp3_ran].replace(".mp3",'')+'.jpg'+'" -filter_complex "[0:v][1:v]overlay=30:390[cover];[cover]ass='+path+"/default_mp3/"+mp3_files[mp3_ran].replace(".mp3",'')+'.ass'+'[result]" -i "'+path+'/default_mp3/'+mp3_files[mp3_ran]+'" -map "[result]" -map 2,0 -pix_fmt yuvj420p -c:v '+get_v()+' -preset:v superfast '+var_set.bitrate+' -acodec aac -f '+get_s()+var_set.vb+' "'+rtmp+live_code+'"')
                        os.system('ffmpeg -threads 0 -re -loop 1 '+var_set.r+' -t '+str(int(seconds))+' -f image2 -i "'+path+'/default_pic/'+pic_files[pic_ran]+'" -i "'+path+"/default_mp3/"+mp3_files[mp3_ran].replace(".mp3",'')+'.jpg'+'" -filter_complex "[0:v][1:v]overlay=30:390[cover];[cover]ass='+path+"/default_mp3/"+mp3_files[mp3_ran].replace(".mp3",'')+'.ass'+'[result]" -i "'+path+'/default_mp3/'+mp3_files[mp3_ran]+'" -map "[result]" -map 2,0 -pix_fmt yuvj420p -c:v '+get_v()+' -preset:v superfast '+var_set.bitrate+' -acodec aac -f '+get_s()+var_set.vb+' "'+rtmp+live_code+'"')
                    else:
                        print('ffmpeg -threads 0 -re -loop 1 '+var_set.r+' -t '+str(int(seconds))+' -f image2 -i "'+path+'/default_pic/'+pic_files[pic_ran]+'" -i "'+path+'/default_mp3/'+mp3_files[mp3_ran]+'" -vf ass="'+path+"/default_mp3/"+mp3_files[mp3_ran].replace(".mp3",'')+'.ass'+'" -pix_fmt yuvj420p -c:v '+get_v()+' -preset:v superfast '+var_set.bitrate+' -acodec aac -f '+get_s()+var_set.vb+' "'+rtmp+live_code+'"')
                        os.system('ffmpeg -threads 0 -re -loop 1 '+var_set.r+' -t '+str(int(seconds))+' -f image2 -i "'+path+'/default_pic/'+pic_files[pic_ran]+'" -i "'+path+'/default_mp3/'+mp3_files[mp3_ran]+'" -vf ass="'+path+"/default_mp3/"+mp3_files[mp3_ran].replace(".mp3",'')+'.ass'+'" -pix_fmt yuvj420p -c:v '+get_v()+' -preset:v superfast '+var_set.bitrate+' -acodec aac -f '+get_s()+var_set.vb+' "'+rtmp+live_code+'"')
                else:
                    print('ffmpeg -threads 0 -re -loop 1 '+var_set.r+' -t '+str(int(seconds))+' -f image2 -i "'+path+'/default_pic/'+pic_files[pic_ran]+'" -i "'+path+'/default_mp3/'+mp3_files[mp3_ran]+'" -vf ass="'+path+'/default.ass" -pix_fmt yuvj420p -c:v '+get_v()+' -preset:v superfast '+var_set.bitrate+' -acodec aac -f '+get_s()+var_set.vb+' "'+rtmp+live_code+'"')
                    os.system('ffmpeg -threads 0 -re -loop 1 '+var_set.r+' -t '+str(int(seconds))+' -f image2 -i "'+path+'/default_pic/'+pic_files[pic_ran]+'"  -i "'+path+'/default_mp3/'+mp3_files[mp3_ran]+'" -vf ass="'+path+'/default.ass" -pix_fmt yuvj420p -c:v '+get_v()+' -preset:v superfast '+var_set.bitrate+' -acodec aac -f '+get_s()+var_set.vb+' "'+rtmp+live_code+'"')
            if(mp3_files[mp3_ran].find('.flv') != -1):  #如果为flv视频
                #直接推流
                print('ffmpeg -threads 0 -re -i "'+path+"/default_mp3/"+mp3_files[mp3_ran]+'" -vcodec copy -acodec copy -f flv "'+rtmp+live_code+'"')
                os.system('ffmpeg -threads 0 -re -i "'+path+"/default_mp3/"+mp3_files[mp3_ran]+'" -vcodec copy -acodec copy -f flv "'+rtmp+live_code+'"')
        else:
            print("非空")
            files = os.listdir(path+'/downloads')   #获取文件夹下全部文件
            files.sort()    #排序文件，按文件名（点播时间）排序
            count=0     #总共匹配到的点播文件统计
            for f in files:
                if((f.find('.mp3') != -1) and (f.find('.download') == -1)): #如果是mp3文件
                    print(path+'/downloads/'+f)
                    seconds = 420
                    bitrate = 0
                    try:
                        audio = MP3(path+'/downloads/'+f)   #获取mp3文件信息
                        seconds=audio.info.length   #获取时长
                        bitrate=audio.info.bitrate  #获取码率
                    except Exception as e:
                        print(e)
                        bitrate = 99999999999

                    print('mp3 long:'+convert_time(seconds))
                    if((seconds > 420) | (bitrate > 400000)):  #大于十分钟就不播放/码率限制400k以下
                        print('too long/too big,delete')
                    else:
                        pic_files = os.listdir(path+'/default_pic') #获取准备的图片文件夹中的所有图片
                        pic_files.sort()    #排序数组
                        pic_ran = random.randint(0,len(pic_files)-1)    #随机选一张图片
                    
                        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' MP3文件为：'+f)
                        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' 背景文件为：'+pic_files[pic_ran])
                        w_log(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+'\n'+'MP3文件为：'+f+'\n'+'背景文件为：'+pic_files[pic_ran]+'\n',path+'/log/screenlog_playing.log',"a+")
                        print('mp3 long:'+convert_time(seconds))
                        #推流

                        #如果存在封面
                        if os.path.isfile(path+'/downloads/'+f.replace(".mp3",'')+'.jpg'):
                            print('ffmpeg -threads 0 -re -loop 1 '+var_set.r+' -t '+str(int(seconds))+' -f image2 -i "'+path+'/default_pic/'+pic_files[pic_ran]+'" -i "'+path+'/downloads/'+f.replace(".mp3",'')+'.jpg'+'" -filter_complex "[0:v][1:v]overlay=30:390[cover];[cover]ass='+path+"/downloads/"+f.replace(".mp3",'')+'.ass'+'[result]" -i "'+path+'/downloads/'+f+'" -map "[result]" -map 2,0 -pix_fmt yuvj420p -c:v '+get_v()+' -preset:v superfast '+var_set.bitrate+' -acodec aac -f '+get_s()+var_set.vb+' "'+rtmp+live_code+'"')
                            os.system('ffmpeg -threads 0 -re -loop 1 '+var_set.r+' -t '+str(int(seconds))+' -f image2 -i "'+path+'/default_pic/'+pic_files[pic_ran]+'" -i "'+path+'/downloads/'+f.replace(".mp3",'')+'.jpg'+'" -filter_complex "[0:v][1:v]overlay=30:390[cover];[cover]ass='+path+"/downloads/"+f.replace(".mp3",'')+'.ass'+'[result]" -i "'+path+'/downloads/'+f+'" -map "[result]" -map 2,0 -pix_fmt yuvj420p -c:v '+get_v()+' -preset:v superfast '+var_set.bitrate+' -acodec aac -f '+get_s()+var_set.vb+' "'+rtmp+live_code+'"')
                        else:#如果不存在封面
                            print('ffmpeg -threads 0 -re -loop 1 '+var_set.r+' -t '+str(int(seconds))+' -f image2 -i "'+path+'/default_pic/'+pic_files[pic_ran]+'" -i "'+path+'/downloads/'+f+'" -vf ass="'+path+"/downloads/"+f.replace(".mp3",'')+'.ass'+'" -pix_fmt yuvj420p -c:v '+get_v()+' -preset:v superfast '+var_set.bitrate+' -acodec aac -f '+get_s()+var_set.vb+' "'+rtmp+live_code+'"')
                            os.system('ffmpeg -threads 0 -re -loop 1 '+var_set.r+' -t '+str(int(seconds))+' -f image2 -i "'+path+'/default_pic/'+pic_files[pic_ran]+'" -i "'+path+'/downloads/'+f+'" -vf ass="'+path+"/downloads/"+f.replace(".mp3",'')+'.ass'+'" -pix_fmt yuvj420p -c:v '+get_v()+' -preset:v superfast '+var_set.bitrate+' -acodec aac -f '+get_s()+var_set.vb+' "'+rtmp+live_code+'"')
                        try:    #放完后删除mp3文件、删除字幕、删除点播信息、封面图片
                            shutil.move(path+'/downloads/'+f,path+'/default_mp3/')
                            shutil.move(path+'/downloads/'+f.replace(".mp3",'')+'.ass',path+'/default_mp3/')
                            shutil.move(path+'/downloads/'+f.replace(".mp3",'')+'.info',path+'/default_mp3/')
                            if os.path.isfile(path+'/downloads/'+f.replace(".mp3",'')+'.jpg'):
                                shutil.move(path+'/downloads/'+f.replace(".mp3",'')+'.jpg',path+'/default_mp3/')
                            delpid(f.replace(".mp3",''))
                        except Exception as e:
                            print(e)
                    try:
                        os.remove(path+'/downloads/'+f)
                        os.remove(path+'/downloads/'+f.replace(".mp3",'')+'.info')
                        os.remove(path+'/downloads/'+f.replace(".mp3",'')+'.ass')
                        os.remove(path+'/downloads/'+f.replace(".mp3",'')+'.jpg')
                        delpid(f.replace(".mp3",''))
                    except:
                        print('delete error')
                    count+=1    #点播统计加一
                    break
                if((f.find('ok.flv') != -1) and (f.find('.download') == -1) and (f.find('rendering') == -1)):   #如果是有ok标记的flv文件
                    print('flv:'+f)
                    #直接推流
                    print('ffmpeg -threads 0 -re -i "'+path+"/downloads/"+f+'" -vcodec copy -acodec aac -f flv "'+rtmp+live_code+'"')
                    os.system('ffmpeg -threads 0 -re -i "'+path+"/downloads/"+f+'" -vcodec copy -acodec aac -f flv "'+rtmp+live_code+'"')
                    os.rename(path+'/downloads/'+f,path+'/downloads/'+f.replace("ok",""))   #修改文件名，以免下次循环再次匹配
                    _thread.start_new_thread(remove_v, (f.replace("ok",""),))   #异步搬走文件，以免推流卡顿
                    _thread.start_new_thread(remove_v, (f.replace(".flv","")+".info",))   #异步搬走文件，以免推流卡顿
                    delpid(f.replace("ok.flv",''))
                    #os.remove(path+'/downloads/*.xml')
                    count+=1    #点播统计加一
                    break
                
    except Exception as e:
        print(e)