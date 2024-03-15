#encoding:utf-8

#需要修改的值

deviceType = "vps"
#设备类型，可选类型为"pi"和"vps"，区分大小写

path = '/home/pi/live'
#本文件的路径，请修改

roomid = '3702914'
#房间id（真实id，不一定是网址里的那个数）

maxsum = 20

cookie = "buvid3=B29DB91A-86D5-B06F-E478-55D90E9A105F00414infoc; b_nut=1706493800; buvid4=2836295E-E210-16C2-474B-DB49B88CD92400414-024012902-QF%2FWTB5IEMVtCQnSZPdgXr0h6rYhgERgM6K1Sozi5EczdD8QjIS4E0jwtTdbJfYr; LIVE_BUVID=AUTO2217064938017506; b_lsid=8110DF24A_18D52F506B2; _uuid=33DA7D103-1574-7A41-6B7D-C1B58F91D85106276infoc; fingerprint=d7f30e74504be317c7c43939ed8e9571; buvid_fp_plain=undefined; buvid_fp=d7f30e74504be317c7c43939ed8e9571; DedeUserID=31438300; DedeUserID__ckMd5=45b96a085d845b70; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDY3NTMyNjUsImlhdCI6MTcwNjQ5NDAwNSwicGx0IjotMX0.oQmPKlGGL-rDMQgA7mp9hMvmeORGWp6WX6JQuA0Jf84; bili_ticket_expires=1706753205; SESSDATA=190c6e04%2C1722046123%2C7d26b%2A11CjBsqpe2TEGP5lTYHKJiVIO3GTuP3gg_w5V_k9edDc1Y-6ihoUrDz_vrOdEpxydTUOQSVjZDY2hFcGNWQm00Q1poWVRjS2dNM3ZUYkl6d1RnZ25Od09oQWNvS2Flb3FVYmhPdnpXdXYtMVJBSy0yZ2xhQUhCZ1VaOG1lRk5FeHRBUGE2Z0g1Z1FRIIEC; bili_jct=af2214f37061c653508263ec9ed69478; sid=f7914ym7; PVID=3"
#发送弹幕用的cookie

csrf_token = 'af2214f37061c653508263ec9ed69478'
#发送弹幕用的csrf_token

download_api_url = 'http://localhost/php/'
#获取音乐链接的api网址，服务器性能有限，尽量请换成自己的，php文件在php文件夹

#直播形式
#stle = 'flv'
stle = 'mpegts'

#rtmp = 'rtmp://live-push.bilivideo.com/live-bvc/'
rtmp = 'srt://live-push.bilivideo.com:1937?streamid=#!::h=live-push.bilivideo.com,r=live-bvc/?streamname=live_31438300_3317297,key=f65261b78a388b59e1427f0b17dc5266,schedule=srtts,pflag=1'
#直播给的两个码，填在这里
#live_code = '?streamname=live_31438300_3317297&key=f65261b78a388b59e1427f0b17dc5266&schedule=rtmp&pflag=1'
live_code = ''

free_space=3360
#允许download/default_mp3文件夹占用空间大小，超过时自动按时间顺序删除视频/音乐，单位：MiB

maxrate='3000'

#bitrate='-maxrate 3500k -tune:v zerolatency -g 3'
#码率的种类-maxrate 2000k -bufsize 2000k -maxrate 2500k -bufsize 2500k -tune:v zerolatency -b:v 2500k -g 3
bitrate="-tune zerolatency -flags2 local_header -acodec aac -g 30 -pkt_size 1316 -flush_packets 0"


vb=''
#-f flv代码后-g 3 -b:v 2000k

r='-r 6'
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
