# -*- coding:utf-8 -*-

#需要修改的值

deviceType = "vps"
#设备类型，可选类型为"pi"和"vps"，区分大小写

path = ''
#本文件的路径，请修改

roomid = ''
#房间id（真实id，不一定是网址里的那个数）

maxsum = 20

cookie = ""
#发送弹幕用的cookie

csrf_token = ''
#发送弹幕用的csrf_token

download_api_url = 'http://localhost/php/'
#获取音乐链接的api网址，服务器性能有限，尽量请换成自己的，php文件在php文件夹

#直播串流形式
#stle = 'flv'
stle = 'mpegts'

#rtmp = 'rtmp://live-push.bilivideo.com/live-bvc/'
rtmp = ''
#直播给的两个码，填在这里
#live_code = '?streamname=live_31438300_3317297&key=923798e0d34e3758a810e855869f0ecb&schedule=rtmp&pflag=9'
live_code = ''

free_space=3360
#允许download/default_mp3文件夹占用空间大小，超过时自动按时间顺序删除视频/音乐，单位：MiB

maxrate='3000'

#bitrate='-maxrate 3500k -tune:v zerolatency -g 3'
#码率的种类-maxrate 2000k -bufsize 2000k -maxrate 2500k -bufsize 2500k -tune:v zerolatency -b:v 2500k -g 3
bitrate='-tune zerolatency -flags2 local_header -g 30 -pkt_size 1316 -flush_packets 0'


vb=''
#-f flv代码后-g 3 -b:v 2000k

r='-r 2'
#推流帧频

dm_size=30
#每段弹幕的最大长度（20级以后可发30字）

use_gift_check = False
#是否使用投礼物才让点歌的设定

av_lock = False
#是否启用视频点播的设定

mv_lock = True
#是否启用视频点播的设定

play_videos_when_night = False
#是否播放晚间专属视频？
