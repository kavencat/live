#encoding:utf-8
import urllib
import urllib.request
import http.cookiejar
import json
import time
import os
import sys
import datetime
import ass_maker
import var_set
import _thread
import random
import get_info
import numpy
import get_song_info
import shutil
import glob
from mutagen.mp3 import MP3


path = var_set.path         #引入设置路径
roomid = var_set.roomid     #引入设置房间号
cookie = var_set.cookie     #引入设置cookie
download_api_url = var_set.download_api_url #引入设置的音乐下载链接获取接口
csrf_token = var_set.csrf_token
deviceType = var_set.deviceType
av_lock = var_set.av_lock
maxsum = var_set.maxsum
mv_lock = var_set.mv_lock

dm_lock = False         #弹幕发送锁，用来排队
encode_lock = False     #视频渲染锁，用来排队

sensitive_word = ('64', '89') #容易误伤的和谐词汇表，待补充

def noctie():
    replay = ["点个关注？？", "你在这还好么！", "在这感受怎么样？", "关注个，下次好找点~", "感谢你的到来！","可以点歌哦！","免费点歌哦！","多多关照！"]
    send_dm_long('欢迎来到直播间！'.replay[random.randint(0, len(replay)-1)])

def get_v():
    if deviceType == "pi":
        return "h264_omx"
    elif deviceType == "vps":
        return "libx264"

def restart_program():
  python = sys.executable
  os.execl(python, python, * sys.argv)

#用于读取记录文件
def r_log(file,w):
    fo = open(file,w)
    line = fo.readline()
    while line:
        return(line)
    # 关闭文件
    fo.close()

#用于写入记录文件
def w_log(nr,file,w):#nr写入文件内容，file写入的文件名，wd文件打开方式
    try:
        lfile = open(file, w)
        lfile.writelines(nr)
        lfile.close()
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'写入记录成功！')
    except:
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'写入记录失败！')


#格式化时间，暂时没啥用，以后估计也没啥用
def convert_time(n):
    s = n%60
    m = int(n/60)
    return '00:'+"%02d"%m+':'+"%02d"%s

#用于删除下载文件，防止报错
def del_file(f):
    try:
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'delete'+path+'/downloads/'+f)
        os.remove(path+'/downloads/'+f)
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+f+"文件删除成功！")
    except:
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'delete error')

#用于删除存档文件，防止报错
def del_file_default_mp3(f):
    try:
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'delete'+path+'/default_mp3/'+f)
        os.remove(path+'/default_mp3/'+f)
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+f+"文件删除成功！")
    except:
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'delete error')

#用于删除id 1是过渡文件
def del_id(id,file,file1):
    try:
        f = open(file,"r",encoding='utf-8')
        f1 = open(file1,"w+",encoding='utf-8')
        lines = f.readlines()
        for ls in lines:
            if id not in ls:
                f1.write(ls)
        f.close
        f1.close
        os.remove(file)
        os.rename(file1,file)
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+"id"+id+"删除成功！")
    except:
        return False

#检查已使用空间是否超过设置大小
def check_free():
    files = os.listdir(path+'/downloads')  #获取下载文件夹下所有文件
    size = 1048576
    for f in files:          #遍历所有文件
        size += os.path.getsize(path+'/downloads/'+f)  #累加大小
    files = os.listdir(path+'/default_mp3')#获取缓存文件夹下所有文件
    for f in files:         #遍历所有文件
        size += os.path.getsize(path+'/default_mp3/'+f)#累加大小
    if(size > var_set.free_space*1024*1024):  #判断是否超过设定大小
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+"space size:"+str(size))
        return True
    else:
        return False

#检查已使用空间，并在超过时，自动删除缓存的视频
def clean_files():
    is_boom = True  #用来判断可用空间是否爆炸
    if(check_free()):  #检查已用空间是否超过设置大小
        files = os.listdir(path+'/default_mp3') #获取下载文件夹下所有文件
        files.sort()    #排序文件，以便按日期删除多余文件
        for f in files:
            if((f.find('.flv') != -1) & (check_free())):    #检查可用空间是否依旧超过设置大小，flv文件
                del_file_default_mp3(f)   #删除文件
                del_file_default_mp3(f.replace(".flv",'')+'ok.info')
                del_id(f[0:12:],"songs.log","songs2.log")
            elif((f.find('.mp3') != -1) & (check_free())):    #检查可用空间是否依旧超过设置大小，mp3文件
                del_file_default_mp3(f)   #删除文件
                del_file_default_mp3(f.replace(".mp3",'')+'.ass')
                del_file_default_mp3(f.replace(".mp3",'')+'.info')
                del_file_default_mp3(f.replace(".mp3",'')+'.jpg')
                del_id(f[0:12:],"songs.log","songs2.log")
            elif(check_free() == False):    #符合空间大小占用设置时，停止删除操作
                is_boom = False
    else:
        is_boom = False
    return is_boom

#删除之前残留的没渲染完的文件
def last_files():
    files = os.listdir(path+'/downloads') #获取下载文件夹下所有文件
    for f in files:
        if f.find('rendering.flv') != -1:
            del_file(f)   #删除文件
            del_file(f.replace('rendering.flv','ok.info'))
            del_file(f.replace('rendering.flv','ok.ass'))
            del_id(f[0:12:],"songs.log","songs2.log")
            del_id(f[0:12:],"play.log","play2.log")
        elif f.find('.mp4') != -1 or f.find('rendering1') != -1:
            del_file(f)
            del_id(f[0:12:],"songs.log","songs2.log")
            del_id(f[0:12:],"play.log","play2.log")
last_files()

#用于检查ID重复
def ck_id(id,file):
    try:
        f = open(file,"r",encoding='utf-8')
        lines = f.readlines()
        for lins in lines:
            if id in lins:
                return True
                break
        f.close
    except:
        return False

#重复歌曲信息写入
def w_play(id,fil,fil1):
    try:
        f = open(fil,"r",encoding='utf-8')
        f1 = open(fil1,"a+",encoding='utf-8')
        lines = f.readlines()
        for ls in lines:
            if id in ls:
                f1.write(ls)
        f.close
        f1.close
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+"id"+id+"添加成功！")
    except:
        return False

#用于文件名读取
def r_name(id,file):
    try:
        f = open(file,"r",encoding='utf-8')
        lines = f.readlines()
        for line in lines:
            if id in line:
                return line[-13:-1:]
                break
        f.close
    except:
        return False

#用于搜索文件
def seach_file(file,path):
    try:
        files = os.listdir(path)
        files.sort()
        for f in files:
            if(f.find(file) != -1):
                return True
                break
    except:
        return False

#用于重复点播文件移动1移动到2
def movef(f):
    try:
        shutil.move(path+"/default_mp3/"+f,path+"/downloads")
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+"[log]"+f+"移动完成！")
    except:
        return False

def del_xml(f):
    try:
        del_file(f+".cmt.xml")
    except:
        return False



#下载歌曲，传入参数：
#s：数值型，传入歌曲/mv的id
#t：type，类型，mv或id
#user：字符串型，点播者
#song：歌名，点播时用的关键字，可选
def get_download_url(s, t, user, song = "nothing"):
    global encode_lock  #视频渲染锁，用来排队
    if(clean_files()):  #检查空间是否在设定值以内，并自动删除多余视频缓存
        send_dm_long('树莓存储空间已爆炸，请联系up')
        return
    if t == 'id' and var_set.use_gift_check:   #检查送过的礼物数量
        if check_coin(user, 100) == False:
            send_dm_long('用户'+user+'赠送的瓜子不够点歌哦,还差'+str(100-get_coin(user))+'瓜子的礼物')
            return
    elif t == 'mv' and var_set.use_gift_check:
        if check_coin(user, 500) == False:
            send_dm_long('用户'+user+'赠送的瓜子不够点mv哦,还差'+str(500-get_coin(user))+'瓜子的礼物')
            return
    send_dm_long('正在下载'+t+str(s))
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'[log]getting url:'+t+str(s))
    try:
        filename = str(time.mktime(datetime.datetime.now().timetuple()))    #获取时间戳，用来当作文件名
        if(t == 'id'):  #当参数为歌曲时
            #伪装浏览器，防止屏蔽
            opener=urllib.request.build_opener()
            opener.addheaders=[('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36')]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve("http://music.163.com/song/media/outer/url?id="+str(s), path+'/downloads/'+filename+'.mp3') #下载歌曲

            #print("http://music.163.com/song/media/outer/url?id="+str(s))

            lyric_get = urllib.parse.urlencode({'lyric': s})    #格式化参数

            #print(download_api_url)
            lyric_w = urllib.request.urlopen(download_api_url + "?%s" % lyric_get,timeout=5)  #设定获取歌词的网址
            lyric = lyric_w.read().decode('utf-8')  #获取歌词文件

            tlyric_get = urllib.parse.urlencode({'tlyric': s})    #格式化参数
            tlyric_w = urllib.request.urlopen(download_api_url + "?%s" % tlyric_get,timeout=5)  #设定获取歌词的网址
            tlyric = tlyric_w.read().decode('utf-8')  #获取歌词文件
            (song_temp,pic_url) = get_song_info.get_song_info(s)#获取歌曲信息
            if song_temp != "":
                if(song_temp == "nothing"):
                    send_dm_long("你所点播歌曲id"+str(s)+"不正确，请重新点播……")
                    return
                song = "歌名："+song_temp
                song2 = song_temp
            else:
                song = "关键词："+song
                song2 = song
            pic_url = ""
            if pic_url != "":
                try:
                    #伪装浏览器，防止屏蔽
                    opener=urllib.request.build_opener()
                    opener.addheaders=[('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36')]
                    urllib.request.install_opener(opener)
                    urllib.request.urlretrieve(pic_url+"?param=200y200", path+'/downloads/'+filename+'.jpg') #下载封面
                except Exception as e: #下载出错
                    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'[log]下载封面出错：'+pic_url)
                    print(e)
                    del_file(filename+'.jpg')

            seconds = 420
            bitrate = 0
            try:
                audio = MP3(path+'/downloads/'+filename+'.mp3')   #获取mp3文件信息
                seconds=audio.info.length   #获取时长
                bitrate=audio.info.bitrate  #获取码率
            except Exception as e:
                print(e)
                bitrate = 99999999999
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'mp3时长:'+convert_time(seconds))

            if(seconds==0):
                send_dm_long('id'+str(s)+'下载失败！')
                return()

            if((seconds < 30) | (seconds > 421) | (bitrate > 400000)):  #大于十分钟就不播放/码率限制400k以下
                send_dm_long('id'+str(s)+'歌曲时长超7分钟或小于30秒不予播放')
                del_file(filename+'.mp3')
                del_file(filename+'.ass')
                del_file(filename+'.info')
                del_file(filename+'.jpg')
                print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'too long/too big,delete')
                return()
            ass_maker.make_ass(filename,'当前网易云id：'+str(s)+"\\N"+song+"\\N点播人："+user,path,lyric,tlyric)   #生成字幕
            #ass_maker.make_ass(filename,'当前网易云id：'+str(s)+"\\N"+song+"\\N点播人："+user,path)   #生成字幕
            ass_maker.make_info(filename,'id：'+str(s)+","+song+",点播人："+user,path)    #生成介绍信息，用来查询
            send_dm_long('歌曲['+song2+']下载完成，加入播放队列')
            time.sleep(5)
            #send_dm_long(t+str(s)+'下载完成，已加入播放队列')
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'[log]已添加排队项目：'+t+str(s))
        elif(t == 'mv'):    #当参数为mv时
            params = urllib.parse.urlencode({t: s}) #格式化参数
            f = urllib.request.urlopen(download_api_url + "?%s" % params,timeout=5)   #设定获取的网址
            url = f.read().decode('utf-8')  #读取结果
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'[log]获取'+t+str(s)+'网址：'+url)

            #伪装浏览器，防止屏蔽
            opener=urllib.request.build_opener()
            opener.addheaders=[('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36')]
            urllib.request.install_opener(opener)

            #print(url)

            urllib.request.urlretrieve(url, path+'/downloads/'+filename+'.mp4') #下载mv
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'[log]'+t+str(s)+'下载完成')
            if(song == "nothing"):  #当直接用id点mv时
                ass_maker.make_ass(filename+'ok','当前MV网易云id：'+str(s)+"\\N点播人："+user,path)#生成字幕
                ass_maker.make_info(filename+'ok','MVid：'+str(s)+",点播人："+user,path)#生成介绍信息，用来查询
            else:   #当用关键字搜索点mv时
                ass_maker.make_ass(filename+'ok','当前MV网易云id：'+str(s)+"\\NMV点播关键词："+song+"\\N点播人："+user,path)#生成字幕
                ass_maker.make_info(filename+'ok','MVid：'+str(s)+",关键词："+song+",点播人："+user,path)#生成介绍信息，用来查询
            send_dm_long(t+str(s)+'下载完成，等待渲染')
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'[log]获取'+t+str(s)+'下载完成，等待渲染')
            while (encode_lock):    #渲染锁，如果现在有渲染任务，则无限循环等待
                time.sleep(1)   #等待
            encode_lock = True  #进入渲染，加上渲染锁，防止其他视频一起渲染
            send_dm_long(t+str(s)+'正在渲染')
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'[log]获取'+t+str(s)+'正在渲染')
            os.system('ffmpeg -threads 1 -i "'+path+'/downloads/'+filename+'.mp4" -aspect 16:9 -vf "scale=1280:720, ass='+path+"/downloads/"+filename+'ok.ass'+'" -c:v '+get_v()+' -preset ultrafast -maxrate '+var_set.maxrate+'k -tune fastdecode -acodec aac -b:a 192k "'+path+'/downloads/'+filename+'rendering.flv"')
            encode_lock = False #关闭渲染锁，以便其他任务继续渲染
            del_file(filename+'.mp4')   #删除渲染所用的原文件
            os.rename(path+'/downloads/'+filename+'rendering.flv',path+'/downloads/'+filename+'ok.flv') #重命名文件，标记为渲染完毕（ok）
            send_dm_long(t+str(s)+'渲染完毕，已加入播放队列')
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'[log]获取'+t+str(s)+'渲染完毕，已加入播放队列')
            #os.remove(path+'/downloads/'+video_title+'.cmt.xml')
        try:    #记录日志，已接近废弃
            log_file = open(path+'/songs.log', 'a')
            log_file.writelines(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ','+user+','+t+str(s)+','+song+','+filename+'\r\n')
            log_file.close()
            log_playfile = open(path+'/play.log', 'a')
            log_playfile.writelines(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ','+user+','+t+str(s)+','+song+','+filename+'\r\n')
            log_playfile.close()
        except:
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'[error]log error')
    except Exception as e: #下载出错
        send_dm_long('出错了：请检查命令或重试')
        if t == 'id' and var_set.use_gift_check:   #归还用掉的瓜子
            give_coin(user,100)
        elif t == 'mv' and var_set.use_gift_check:
            give_coin(user,500)
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'[log]下载文件出错：'+t+str(s))
        print(e)
        del_file(filename+'.mp4')
        del_file(filename+'.mp3')
        del_id(filename,"songs.log","songs2.log")
        del_id(filename,"play.log","play2.log")
        del_file(filename+'.flv')
        del_file(filename+'.ass')
        del_file(filename+'.info')
        del_file(filename+'ok.ass')
        del_file(filename+'ok.info')
        del_xml(filename)

#下载歌单
def playlist_download(id,user):
    params = urllib.parse.urlencode({'playlist': str(id)}) #格式化参数
    #f = urllib.request.urlopen(download_api_url + "?%s" % params,timeout=3)   #设定获取的网址
    f = urllib.request.urlopen("https://api.yimian.xyz/msc/?type=playlist&id="+str(id))#设定获取的网址
    #https://music.163.com/api/playlist/detail?id=
    try:
        playlists = json.loads(f.read().decode('utf-8'))  #获取结果，并反序化
        #print(playlists)
        if len(playlists)*100 > get_coin(user) and var_set.use_gift_check:
            send_dm_long('用户'+user+'赠送的瓜子不够点'+str(len(playlists))+'首歌哦,还差'+str(len(playlists)*100-get_coin(user))+'瓜子的礼物')
            return
        else:
            #send_dm_long('正在下载歌单：'+playlists['name']+'，前'+str(len(playlists['data']))+'首')
            if(len(playlists)>maxsum + 15 - psum()):
                send_dm_long('正在下载歌单前'+str(maxsum + 15 - psum())+'首')
            else:
                send_dm_long('正在下载歌单前'+str(len(playlists))+'首')
    except Exception as e:  #防炸
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'shit(playlist)')
        print(e)
        send_dm_long('出错了：请检查命令或重试')

    for song in playlists:
        #print(song['url'])
        mid = str(song['id'])
        #str(song['url'].replace('http://music.163.com/song/media/outer/url?id=',''))
        print(mid)
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'name:'+song['name']+'id:'+mid)
        if(ck_id('id:'+mid,"jsongs.log")):
            send_dm_long('您所点播的歌曲['+song['name']+']，在禁播列表，请重新点播…')
            return
        if(psum()>maxsum + 15):
            send_dm_long('目前点播数量已经超过最多点播数量，暂不接受点播……')
            return
        if(ck_id('id'+mid,"songs.log")):
            f = r_name('id'+mid,"songs.log")
            if(seach_file(f+".mp3",path+"/downloads")):
                send_dm_long('id'+mid+"的歌曲重复，但未播放，稍后播放……")
            else:
                w_play('id'+mid,'songs.log','play.log')
                movef(f+".mp3")
                movef(f+".ass")
                movef(f+".info")
                if(os.path.isfile(path+"/default_mp3/"+f+".jpg")):
                    movef(f+".jpg")
                send_dm_long('id:'+mid+"的歌曲重复，稍后播放……")
        else:
            if(psum()>maxsum+10):
                send_dm_long('目前点播数量已经超过最多点播数量，暂不接受点播……')
                return
            get_download_url(mid, 'id', user, song['name'])

#下载b站任意视频，传入值：网址、点播人用户名
def download_av(video_url,user):
    global encode_lock  #视频渲染锁，用来排队
    if(clean_files()):  #检查空间是否在设定值以内，并自动删除多余视频缓存
        send_dm_long('树莓存储空间已爆炸，请联系up')
        return
    if check_coin(user, 500) == False and var_set.use_gift_check:   #扣掉瓜子数
        send_dm_long('用户'+user+'赠送的瓜子不够点视频哦,还差'+str(500-get_coin(user))+'瓜子的礼物')
        return
    try:
        v_format = 'flv'
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'[log]downloading bilibili video:'+str(video_url))
        #if(vieo_url.find('page')):
        #    print(video_url('https://www.bilibili.com/video/BV','')[1:13:])
        #else:
        #    print(video_url[-14:-1:])
        #print('you-get '+video_url+' --json')
        video_info = json.loads(os.popen('you-get '+video_url+' --json').read())    #获取视频标题，标题错误则说明点播参数不对，跳到except
        video_title = video_info["title"]   #获取标题
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+video_title)
        send_dm_long('正在下载'+video_title)
        #send_dm('注意，视频下载十分费时，请耐心等待')
        filename = str(time.mktime(datetime.datetime.now().timetuple()))    #用时间戳设定文件名
        os.system('you-get '+video_url+' -o '+path+'/tmp -O '+filename+'rendering1')  #下载视频文件
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'you-get '+video_url+' -o '+path+'/tmp -O '+filename+'rendering1')
        if(os.path.isfile(path+'/downloads/'+filename+'rendering1.flv')):   #判断视频格式
            v_format = 'flv'
        elif(os.path.isfile(path+'/downloads/'+filename+'rendering1.mp4')):
            v_format = 'mp4'
        else:
            send_dm_long('视频'+video_title+'下载失败，请重试')
            if var_set.use_gift_check:
                give_coin(user,500)
            return
        ass_maker.make_ass(filename+'ok','点播人：'+user+"\\N视频："+video_title+"\\N"+video_url,path)  #生成字幕
        ass_maker.make_info(filename+'ok','视频：'+video_title+",点播人："+user,path)   #生成介绍信息，用来查询
        send_dm_long('视频'+video_title+'下载完成，等待渲染')
        while (encode_lock):    #渲染锁，如果现在有渲染任务，则无限循环等待
            time.sleep(1)   #等待
        encode_lock = True  #进入渲染，加上渲染锁，防止其他视频一起渲染
        send_dm_long('视频'+video_title+'正在渲染')
        os.system('ffmpeg -threads 1 -i "'+path+'/downloads/'+filename+'rendering1.'+v_format+'" -aspect 16:9 -vf "scale=1280:720, ass='+path+"/downloads/"+filename+'ok.ass'+'" -c:v '+get_v()+' -preset ultrafast -maxrate '+var_set.maxrate+'k -tune fastdecode -acodec aac -b:a 192k "'+path+'/downloads/'+filename+'rendering.flv"')
        encode_lock = False #关闭渲染锁，以便其他任务继续渲染
        del_file(filename+'rendering1.'+v_format)   #删除渲染所用的原文件
        os.rename(path+'/downloads/'+filename+'rendering.flv',path+'/downloads/'+filename+'ok.flv') #重命名文件，标记为渲染完毕（ok）
        send_dm_long('视频'+video_title+'渲染完毕，已加入播放队列')
        del_xml(video_title)
        try:    #记录日志，已接近废弃
            log_file = open(path+'/songs.log', 'a')
            log_file.writelines(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ','+user+','+str(video_url.replace("https://www.bilibili.com/video/",""))+','+video_title+','+filename+'\r\n')
            log_file.close()
            log_playfile = open(path+'/play.log', 'a')
            log_playfile.writelines(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + ','+user+','+str(video_url.replace("https://www.bilibili.com/video/",""))+','+video_title+','+filename+'\r\n')
            log_playfile.close()
        except:
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'[error]log error')
    except: #报错提示，一般只会出现在获取标题失败时出现，就是点播参数不对
        send_dm_long('出错了：请检查命令或重试')
        if var_set.use_gift_check:
            give_coin(user,500)
        del_id(filename,"songs.log","songs2.log")
        del_id(filename,"play.log","play2.log")
        del_file(filename+'.flv')
        del_file(filename+'ok.ass')
        del_file(filename+'ok.info')
        del_file(filename+'.mp4')
        del_file(filename+'rendering1.mp4')
        del_xml(video_title)
        #os.remove(path+'/downloads/'+video_title+'.cmt.xml')

#搜索歌曲并下载
def search_song(s,user):
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'[log]searching song:'+s)
    params = urllib.parse.urlencode({'type': 1, 's': s})    #格式化参数
    f = urllib.request.urlopen("http://s.music.163.com/search/get/?%s" % params,timeout=3)    #设置接口网址
    search_result = json.loads(f.read().decode('utf-8'))    #获取结果
    result_id = search_result["result"]["songs"][0]["id"]   #提取歌曲id
    songname = search_result["result"]["songs"][0]["name"]
    if(ck_id('id'+str(result_id),"jsongs.log")):
        send_dm_long('您所点播的['+songname+']的歌曲，在禁播列表，请重新点播…')
        return
    if(ck_id('id'+str(result_id),"songs.log")):
        f = r_name('id'+str(result_id),"songs.log")
        if(seach_file(f+".mp3",path+"/downloads")):
            send_dm_long('歌曲['+songname+"]已点播，但未播放，稍后播放……")
            return
        #print(f)
        w_play('id'+str(result_id),'songs.log','play.log')
        movef(f+".mp3")
        movef(f+".ass")
        movef(f+".info")
        if(seach_file(f+".jpg",path+"/default_mp3")):
            movef(f+".jpg")
        send_dm_long('歌曲['+songname+"]已点播过，稍后播放……")
        return
    _thread.start_new_thread(get_download_url, (result_id, 'id', user,s))   #扔到下载那里下载

#搜索mv并下载
def search_mv(s,user):
    url = "http://music.163.com/api/search/get/"
    postdata =urllib.parse.urlencode({
    's':s,
    'offset':'1',
    'limit':'10',
    'type':'1004'
    }).encode('utf-8')
    header = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding":"utf-8",
    "Accept-Language":"zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
    "Connection":"keep-alive",
    "Host":"music.163.com",
    "Referer":"http://music.163.com/",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0"
    }
    req = urllib.request.Request(url,postdata,header)   #设置接口网址
    result = json.loads(urllib.request.urlopen(req,timeout=3).read().decode('utf-8')) #获取结果
    result_id = result['result']['mvs'][0]['id']    #提取mv id
    if(ck_id("mv"+str(result_id),"songs.log")):
        f = r_name("mv"+str(result_id),"songs.log")
        if(seach_file(f+"ok.flv",path+"/downloads") or seach_file(f+"rendering.flv",path+"/downloads")):
            send_dm_long("mv"+str(result_id)+"的视频重复，但未播放，稍后播放……")
            return
        #print(f)
        w_play("mv"+str(result_id),"songs.log","play.log")
        movef(f+".flv")
        os.rename(path+"/downloads/"+f+".flv",path+"/downloads/"+f+"ok.flv")
        movef(f+"ok.info")
        send_dm_long("mv"+str(result_id)+"的视频重复，稍后播放……")
        return
    _thread.start_new_thread(get_download_url, (result_id, 'mv', user,s))   #扔到下载那里下载

#获取赠送过的瓜子数量
def get_coin(user):
    gift_count = 0
    try:
        gift_count = numpy.load('users/'+user+'.npy')
    except:
        gift_count = 0
    return gift_count

#扣除赠送过的瓜子数量
def take_coin(user, take_sum):
    gift_count = 0
    try:
        gift_count = numpy.load('users/'+user+'.npy')
    except:
        gift_count = 0
    gift_count = gift_count - take_sum
    try:
        numpy.save('users/'+user+'.npy', gift_count)
    except:
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'create error')

#检查并扣除指定数量的瓜子
def check_coin(user, take_sum):
    if get_coin(user) >= take_sum:
        take_coin(user, take_sum)
        return True
    else:
        return False

#给予赠送过的瓜子数量
def give_coin(user, give_sum):
    gift_count = 0
    try:
        gift_count = numpy.load('users/'+user+'.npy')
    except:
        gift_count = 0
    gift_count = gift_count + give_sum
    try:
        numpy.save('users/'+user+'.npy', gift_count)
    except:
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'create error')

def check_night():
    print(time.localtime()[3])
    if (time.localtime()[3] >= 22 or time.localtime()[3] <= 5) and var_set.play_videos_when_night:
        send_dm_long('现在是晚间专场哦~命令无效')
        return True

#点播歌曲的总数
def psum():
    files = os.listdir(path+'/downloads') #获取播放完文件夹下所有文件
    files.sort()
    i=0
    for f in files:
        if(f.find(".mp3") != -1 or f.find(".flv") != -1):
            i=i+1
    return i

#切歌请求次数统计
jump_to_next_counter = 0
rp_lock = False
def pick_msg(s, user):
    global jump_to_next_counter #切歌请求次数统计
    global encode_lock  #视频渲染任务锁
    global rp_lock
    s = s.replace(' ','')
    if ((user=='kavencat') | (user=='柠檬0325') | (user=='兼职的bh3舰长')):    #debug使用，请自己修改
        if(s=='锁定'):
            rp_lock = True
            send_dm_long('已锁定点播功能，不响应任何弹幕')
        if(s=='解锁'):
            rp_lock = False
            send_dm_long('已解锁点播功能，开始响应弹幕请求')
        if(s=='清空列表'):
            if(encode_lock):
                send_dm_long('有渲染任务，无法清空')
                return
            #获取目录下所有文件
            for i in os.listdir(path+'/downloads'):
                del_file(i)
                del_id(i[0:12:],"songs.log","songs2.log")
                del_id(i[0:12:],"play.log","play2.log")
            os.system('killall ffmpeg')
            send_dm_long('已经清空列表~')
        if(s=='清空已点列表'):
            if(encode_lock):
                send_dm_long('有渲染任务，无法清空')
                return
            #获取目录下所有文件
            for i in os.listdir(path+'/default_mp3'):
                del_file_default_mp3(i)
                del_id(i[0:12:],"songs.log","songs2.log")
            os.system('killall ffmpeg')
            send_dm_long('已经清空列表~')
        if(s.find('加入禁单')==0):
            w_log(s.replace('加入禁单','')+'\r\n',path+'/jsongs.log','a+')
            #os.system('killall ffmpeg')
            send_dm_long('['+s.replace('加入禁单','')+']已加入禁播列表~')
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'重启脚本……')
            os.system('killall ffmpeg') #强行结束ffmpeg进程
            restart_program()
        if(s=='重启点播脚本'):
            send_dm_long('点播脚本重启中……')
            restart_program()
        if(s=='切歌'):
            send_dm_long('已执行切歌动作')
            os.system('killall ffmpeg') #强行结束ffmpeg进程
            return
    if((user == '柠檬0325') | rp_lock):  #防止自循环
        return
    #下面的不作解释，很简单一看就懂
    if(s.find('mvid+') == 0):
        if check_night():
            return
        send_dm_long('已收到'+user+'的指令')
        s = s.replace(' ', '')   #剔除弹幕中的所有空格
        if(psum()>maxsum):
            send_dm_long('目前点播数量已经超过最多点播数量，暂不接受点播……')
            return
        if(mv_lock):
            send_dm_long('目前已锁定视频点播功能，暂不接受视频点播……')
            return
        _thread.start_new_thread(get_download_url, (s.replace('mvid+', '', 1), 'mv',user))
    elif (s.find('mv+') == 0):
        if check_night():
            return
        send_dm_long('已收到'+user+'的指令')
        if(psum()>maxsum):
            send_dm_long('目前点播数量已经超过最多点播数量，暂不接受点播……')
            return
        if(mv_lock):
            send_dm_long('目前已锁定视频点播功能，暂不接受视频点播……')
            return
        try:
            search_mv(s.replace('mv+', '', 1),user)
        except:
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'[log]mv not found')
            send_dm_long('出错了：没这mv')
    elif(s.find('mvid') == 0):
        if check_night():
            return
        send_dm_long('已收到'+user+'的指令')
        s = s.replace(' ', '')   #剔除弹幕中的所有空格
        if(psum()>maxsum):
            send_dm_long('目前点播数量已经超过最多点播数量，暂不接受点播……')
            return
        if(mv_lock):
            send_dm_long('目前已锁定视频点播功能，暂不接受视频点播……')
            return
        if (ck_id(s.replace('id',''),"songs.log")):
            f = r_name(s.replace('id',''),"songs.log")
            if(seach_file(f+"ok.flv",path+"/downloads") or seach_file(f+"rendering.flv",path+"/downloads")):
                send_dm_long(s.replace('id','')+"的视频重复，但未播放，稍后播放……")
                return
            #print(f)
            w_play(s.replace('id',''),"songs.log","play.log")
            movef(f+".flv")
            os.rename(path+"/downloads/"+f+".flv",path+"/downloads/"+f+"ok.flv")
            movef(f+"ok.info")
            send_dm_long(s.replace('id','')+"的视频重复，稍后播放……")
            return
        _thread.start_new_thread(get_download_url, (s.replace('mvid', '', 1), 'mv',user))
    elif (s.find('mv') == 0):
        if check_night():
            return
        send_dm_long('已收到'+user+'的指令')
        if(mv_lock):
            send_dm_long('目前已锁定视频点播功能，暂不接受视频点播……')
            return
        if(psum()>maxsum):
            send_dm_long('目前点播数量已经超过最多点播数量，暂不接受点播……')
            return
        try:
            if (ck_id(s,"songs.log")):
                f = r_name(s,"songs.log")
                if(seach_file(f+"ok.flv",path+"/downloads") or seach_file(f+"rendering.flv",path+"/downloads")):
                    send_dm_long(s+"的视频重复，但未播放，稍后播放……")
                    return
                #print(f)
                w_play(s,"songs.log","play.log")
                movef(f+".flv")
                os.rename(path+"/downloads/"+f+".flv",path+"/downloads/"+f+"ok.flv")
                movef(f+"ok.info")
                send_dm_long(s+"的视频重复，稍后播放……")
                return
            search_mv(s.replace('mv', '', 1),user)
        except:
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'[log]mv not found')
            send_dm_long('出错了：没这mv')
    elif (s.find('id') == 0):
        if check_night():
            return
        s = s.replace(' ', '')   #剔除弹幕中的所有空格
        send_dm_long('已收到'+user+'的指令')
        if(ck_id(s,"jsongs.log")):
            send_dm_long('您所点播的歌曲，在禁播列表，请重新点播…')
            return
        if(psum()>maxsum):
            send_dm_long('目前点播数量已经超过最多点播数量，暂不接受点播……')
            return
        if(ck_id(s,"songs.log")):
            f = r_name(s,"songs.log")
            if(seach_file(f+".mp3",path+"/downloads")):
                send_dm_long(s+"的歌曲重复，但未播放，稍后播放……")
                return
            #print(f)
            w_play(s,"songs.log","play.log")
            movef(f+".mp3")
            movef(f+".ass")
            movef(f+".info")
            if(seach_file(f+".jpg",path+"/default_mp3")):
                movef(f+".jpg")
            send_dm_long(s+"的歌曲重复，稍后播放……")
            return
        _thread.start_new_thread(get_download_url, (s.replace('id', '', 1), 'id',user))
    elif (s.find('点歌') == 0):
        if check_night():
            return
        s = s.replace(' ', '')   #剔除弹幕中的所有空格
        send_dm_long('已收到'+user+'的指令')
        if(ck_id(s.replace('点歌', '', 1),"jsongs.log")):
            send_dm_long('您所点播['+s.replace('点歌', '', 1)+']的歌曲，在禁播列表，请重新点播…')
            return
        if(psum()>maxsum):
            send_dm_long('目前点播数量已经超过最多点播数量，暂不接受点播……')
            return
        if(s.replace('点歌', '', 1).isdigit()):
            if(ck_id(s,"jsongs.log")):
                send_dm_long('点播'+s+'的歌曲，在禁播列表，请重新点播…')
                return
            if(ck_id('id'+s.replace('点歌', '', 1),"songs.log")):
                f = r_name('id'+s.replace('点歌', '', 1),"songs.log")
                if(seach_file(f+".mp3",path+"/downloads")):
                    send_dm_long('id'+s.replace('点歌', '', 1)+"的歌曲重复，但未播放，稍后播放……")
                    return
                #print(f)
                w_play(s,"songs.log","play.log")
                movef(f+".mp3")
                movef(f+".ass")
                movef(f+".info")
                if(seach_file(f+".jpg",path+"/default_mp3")):
                    movef(f+".jpg")
                send_dm_long(s+"的歌曲重复，稍后播放……")
                return
            _thread.start_new_thread(get_download_url, (s.replace('点歌', '', 1), 'id',user))
            return
        try:
            search_song(s.replace('点歌', '', 1),user)
        except:
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'[log]song not found')
            send_dm_long('出错了：没这首歌')
    elif (s.find('喵') > -1):
        replay = ["喵？？", "喵喵！", "喵。。喵？", "喵喵喵~", "喵！"]
        send_dm_long(replay[random.randint(0, len(replay)-1)])  #用于测试是否崩掉
    elif (s == '切歌'):   #切歌请求
        if(encode_lock):    #切歌原理为killall ffmpeg，但是如果有渲染任务，kill后也会结束渲染进程，会出错
            send_dm_long('有渲染任务，无法切歌')
            return
        jump_to_next_counter += 1   #切歌次数统计加一
        #if((user=='kavencat') | (user=='兼职的bh3舰长')): #debug使用，请自己修改
        #    jump_to_next_counter=5
        if(jump_to_next_counter < 3):   #次数未达到五次
            send_dm_long('已收到'+str(jump_to_next_counter)+'次切歌请求，达到三次将切歌')
        else:   #次数达到五次
            jump_to_next_counter = 0    #次数统计清零
            send_dm_long('已执行切歌动作')
            os.system('killall ffmpeg') #强行结束ffmpeg进程
    elif ((s == '点播列表') or (s == '歌曲列表')):
        if check_night():
            return
        send_dm_long('已收到'+user+'的指令，正在查询')
        files = os.listdir(path+'/downloads')   #获取目录下所有文件
        files.sort()    #按文件名（下载时间）排序
        songs_count = 0 #项目数量
        all_the_text = ""
        for f in files:
            if((f.find('.mp3') != -1) and (f.find('.download') == -1)): #如果是mp3文件
                try:
                    info_file = open(path+'/downloads/'+f.replace(".mp3",'')+'.info', 'r')  #读取相应的info文件
                    all_the_text = info_file.read()
                    info_file.close()
                except Exception as e:
                    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+e)
                if(songs_count < 10):
                    send_dm_long(all_the_text)
                songs_count += 1
            if((f.find('ok.flv') != -1) and (f.find('.download') == -1) and (f.find('rendering') == -1)):#如果是有ok标记的flv文件
                try:
                    info_file = open(path+'/downloads/'+f.replace(".flv",'')+'.info', 'r')  #读取相应的info文件
                    all_the_text = info_file.read()
                    info_file.close()
                except Exception as e:
                    print(e)
                if(songs_count < 10):
                    send_dm_long(all_the_text)
                songs_count += 1
        if(songs_count <= 10):
            send_dm_long('点播列表展示完毕，一共'+str(songs_count)+'个')
        else:
            send_dm_long('点播列表前十个展示完毕，一共'+str(songs_count)+'个')
    elif (s == '渲染列表'):
        if check_night():
            return
        send_dm_long('已收到'+user+'的指令，正在查询')
        files = os.listdir(path+'/downloads')   #获取目录下所有文件
        files.sort()    #按文件名（下载时间）排序
        songs_count = 0 #项目数量
        all_the_text = ""
        for f in files:
            if(f.find('rendering1.flv') != -1): #如果是没有ok标记的flv文件
                try:
                    info_file = open(path+'/downloads/'+f.replace("rendering1.flv",'')+'ok.info', 'r')  #读取相应的info文件
                    all_the_text = info_file.read()
                    info_file.close()
                except Exception as e:
                    print(e)
                if(songs_count < 5):
                    send_dm_long(all_the_text)
                songs_count += 1
            if(f.find('.mp4') != -1):   #如果是mp4文件
                try:
                    info_file = open(path+'/downloads/'+f.replace(".mp4",'')+'ok.info', 'r')    #读取相应的info文件
                    all_the_text = info_file.read()
                    info_file.close()
                except Exception as e:
                    print(e)
                if(songs_count < 5):
                    send_dm_long(all_the_text)
                songs_count += 1
        if(songs_count <= 5):
            send_dm_long('渲染列表展示完毕，一共'+str(songs_count)+'个')
        else:
            send_dm_long('渲染列表前5个展示完毕，一共'+str(songs_count)+'个')
    elif (s.find('BV') == 0):
        if check_night():
            return
        send_dm_long('已收到'+user+'的指令')
        if(psum()>maxsum):
            send_dm_long('目前点播数量已经超过最多点播数量，暂不接受点播……')
            return
        s = s.replace(' ', '')   #剔除弹幕中的所有空格
        if(av_lock):
            send_dm_long('由于B站视频接口调整，暂不接受视频点播……')
            return
        try:
            if(ck_id(s,"songs.log")):
                f = r_name(s,"songs.log")
                if(seach_file(f+"ok.flv",path+"/downloads") or seach_file(f+"rendering.flv",path+"/downloads")):
                    send_dm_long(s+"的视频重复，但未播放，稍后播放……")
                    return
                #print(f)
                w_play(s,"songs.log","play.log")
                movef(f+".flv")
                os.rename(path+"/downloads/"+f+".flv",path+"/downloads/"+f+"ok.flv")
                movef(f+"ok.info")
                send_dm_long(s+"的视频重复，稍后播放……")
                return
            if(s.find('#p') == -1):
                #视频网址格式：https://www.bilibili.com/video/avxxxxx
                ture_url=s.replace('BV','https://www.bilibili.com/video/BV')
                _thread.start_new_thread(download_av, (ture_url,user))
            else:
                #视频网址格式：https://www.bilibili.com/video/avxxxx/#page=x
                ture_url=s.replace('#p','?p=')
                print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+ture_url)
                ture_url=ture_url.replace('BV','https://www.bilibili.com/video/BV')
                _thread.start_new_thread(download_av, (ture_url,user))
        except:
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'[log]video not found')
    elif (s.find('温度') > -1 and deviceType == "pi"):
        send_dm_long("CPU "+os.popen('vcgencmd measure_temp').readline())   #读取命令行得到的温度
        send_dm_long(get_info.getInfo())
    elif (s.find('歌单') == 0):
        if check_night():
            return
        send_dm_long('已收到'+user+'的指令')
        s = s.replace(' ', '')   #剔除弹幕中的所有空格
        _thread.start_new_thread(playlist_download, (s.replace('歌单', '', 1),user))
    elif (s.find('查询') == 0):
        send_dm_long(user+'的瓜子余额还剩'+str(get_coin(user))+'个')
    elif (s.find('删id') == 0):
        if check_night():
            return
        send_dm_long('已收到'+user+'的指令')
        s = s.replace(" ","")
        if(ck_id(s.replace('删','',1),'songs.log')):
            f = r_name(s.replace('删','',1),'songs.log')
            if(s.replace('删','',1).find('id') == 0):
                if(seach_file((f+".mp3"),path+"/default_mp3")):
                    del_file_default_mp3(f+".mp3")
                    del_file_default_mp3(f+".jpg")
                    del_file_default_mp3(f+".ass")
                    del_file_default_mp3(f+".info")
                else:
                    del_file(f+".mp3")
                    del_file(f+".jpg")
                    del_file(f+".ass")
                    del_file(f+".info")
                del_id(f,"songs.log","songs2.log")
                del_id(f,"play.log","play2.log")
            else:
                if(encode_lock):
                    send_dm_long("视频"+s.replace('删','',1)+"正在渲染无法删除……")
                    return
                if(seach_file((f+".flv"),path+"/default_mp3")):
                    del_file_default_mp3(f+".flv")
                    del_file_default_mp3(f+"ok.info")
                else:
                    del_file(f+"ok.flv")
                    del_file(f+"ok.ass")
                    del_file(f+"ok.info")
                    del_file("*.xml")
                del_id(f,"songs.log","songs2.log")
                del_id(f,"play.log","play2.log")
            send_dm_long("已点播，现已删除!"+s.replace('删','',1)+"的点播")
        else:
            send_dm_long(s.replace('删','',1)+"未点播过！")
    elif(s == '点播总数'):
        try:
            send_dm_long('已收到'+user+'的指令')
            if(psum() >= 1 ):
                send_dm_long("当前已点播歌曲总数为"+str(psum())+"首!")
            else:
                send_dm_long("当前直播间无点播歌曲！")
        except Exception as e:
            print(e)
    elif (s.find('Q群') == 0):
        try:
            send_dm_long('QQ互动群号为：77257099 4')
        except Exception as e:
            print(e)
    elif (s.find('打卡') == 0):
        try:
            send_dm_long('欢迎'+user+'来到直播间……')
        except Exception as e:
            print(e)
    elif (s.find('早') == 0):
        try:
            send_dm_long('早上好，欢迎'+user+'来到直播间……')
        except Exception as e:
            print(e)
    elif (s.find('中') == 0):
        try:
            send_dm_long('中午好，欢迎'+user+'来到直播间……')
        except Exception as e:
            print(e)
    elif (s.find('晚上好') == 0):
        try:
            send_dm_long('晚上好，欢迎'+user+'来到直播间……')
        except Exception as e:
            print(e)
    elif (s.find('晚安') == 0):
        try:
            send_dm_long('晚安，欢迎以后再次来到直播间……')
        except Exception as e:
            print(e)

    # else:
    #     print('not match anything')

#发送弹幕函数，通过post完成，具体可以自行使用浏览器，进入审查元素，监控network选项卡研究
def send_dm(s):
    global cookie
    global roomid
    global dm_lock
    global csrf_token
    while (dm_lock):
        #print('[log]wait for send dm')
        time.sleep(1)
    dm_lock = True
    try:
        url = "https://api.live.bilibili.com/msg/send"
        postdata =urllib.parse.urlencode({
        'color':'16777215',
        'fontsize':'25',
        'mode':'1',
        'msg':s,
        'rnd':str(int(time.time())),
        'roomid':roomid,
        'csrf_token':csrf_token,
        'csrf':csrf_token
        }).encode("utf8","ignore")
        header = {
        "Accept":"application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding":"utf-8, zip, deflate, br",
        "Accept-Language":"zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
        "Connection":"keep-alive",
        "Cookie":cookie,
        "Host":"api.live.bilibili.com",
        "Referer":"https://live.bilibili.com/"+roomid,
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36 Vivaldi/2.2.1388.37"
        }
        req = urllib.request.Request(url,postdata,header)
        dm_result = json.loads(urllib.request.urlopen(req,timeout=3).read().decode("utf8"))
        if len(dm_result['msg']) > 0:
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'[error]弹幕发送失败：'+s)
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+dm_result)
        else:
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'[log]发送弹幕：'+s)
    except Exception as e:
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'[error]send dm error')
        print(e)
    time.sleep(1.5)
    dm_lock = False

#每条弹幕最长只能发送20字符，过长的弹幕分段发送
def send_dm_long(s):
    n=var_set.dm_size
    for hx in sensitive_word:                  #处理和谐词，防止点播机的回复被和谐
        if (s.find(hx) > -1):
            s = s.replace(hx, hx[0]+"-"+hx[1:])    #在和谐词第一个字符后加上一个空格
    for i in range(0, len(s), n):
        send_dm(s[i:i+n])

#获取原始弹幕数组
#本函数不作注释，具体也请自己通过浏览器审查元素研究
def get_dm():
    global temp_dm
    global roomid
    global csrf_token
    url = "https://api.live.bilibili.com/ajax/msg"
    postdata =urllib.parse.urlencode({
    'token:':'',
    'csrf_token:':csrf_token,
    'roomid':roomid
    }).encode("utf8","ignore")
    header = {
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding":"utf-8",
    "Accept-Language":"zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3",
    "Connection":"keep-alive",
    "Host":"api.live.bilibili.com",
    "Referer":"http://live.bilibili.com/"+roomid,
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0"
    }
    req = urllib.request.Request(url,postdata,header)
    dm_result = json.loads(urllib.request.urlopen(req,timeout=1).read().decode("utf8"))
    #for t_get in dm_result['data']['room']:
        #print('[log]['+t_get['timeline']+']'+t_get['nickname']+':'+t_get['text']).decode("utf8")
    return dm_result

#检查某弹幕是否与前一次获取的弹幕数组有重复
def check_dm(dm):
    global temp_dm
    for t_get in temp_dm['data']['room']:
        if((t_get['text'] == dm['text']) & (t_get['timeline'] == dm['timeline'])):
            return False
    return True

#弹幕获取函数，原理为不断循环获取指定直播间的初始弹幕，并剔除前一次已经获取到的弹幕，余下的即为新弹幕
def get_dm_loop():
    global temp_dm
    temp_dm = get_dm()
    while True:
        dm_result = get_dm()
        for t_get in dm_result['data']['room']:
            if(check_dm(t_get)):
                print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'[log]['+t_get['timeline']+']'+t_get['nickname']+':'+t_get['text'])
                #send_dm('用户'+t_get['nickname']+'发送了'+t_get['text']) #别开，会死循环
                text = t_get['text']
                pick_msg(text,t_get['nickname'])   #新弹幕检测是否匹配为命令
        temp_dm = dm_result
        time.sleep(1)

def test():
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'ok')

print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'程序已启动，连接房间id：'+roomid)
send_dm_long('弹幕监控已启动，可以点歌了')

# while True: #防炸
#     try:
#         get_dm_loop()   #开启弹幕获取循环函数
#     except Exception as e:  #防炸
#         print('shit')
#         print(e)
#         dm_lock = False #解开弹幕锁，以免因炸了而导致弹幕锁没解开，进而导致一直锁着发不出弹幕
#time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
