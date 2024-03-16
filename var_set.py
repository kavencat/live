#encoding:utf-8
#需要修改的值

deviceType = "vps"
#设备类型，可选类型为"pi"和"vps"，区分大小写

path = '/home/pi/live'
#本文件的路径，请修改

roomid = '3702914'
#房间id（真实id，不一定是网址里的那个数）

maxsum = 20
#最大点播数量

cookie = "buvid3=1C77F26D-D369-4C3D-A667-956FD14152BA27566infoc; buvid4=718CF30F-A8CA-2C6D-51FB-69CC81C2D46903566-024022603-PZQXQrT1%2FA0OUWf6PmrR9smxHQ57ORqHQe1m9RhYAiHXoXTm6f%2BPl0G5mibCqH80; LIVE_BUVID=AUTO1517089196099778; _uuid=1838BB16-41046-1107C-38410-4856F5B6CF51000238infoc; fingerprint=3484128cd87d5439209cfba8657e5e78; buvid_fp_plain=undefined; SESSDATA=0b25b07d%2C1724471819%2C7ba51%2A21CjDwTGLjSCi-t51kb9-CGSyxsDYcm2QYzvuqwIeZwga8kR3RRQeXE8p-oulJ-V6I6QESVi1sR2dtdmNvcmdKTTNCWmRoREtKazRPZE9oYzlJMUpHNDBaWmhFcUtRT3pja1RORXF6Rnk1RF9xVEYxQlJVQ3Fzb0RRa2NVQ1FVNm1WWEpuMmlBcVNnIIEC; bili_jct=aed1c01f44880273b0cbaa9c2187d6f1; DedeUserID=31438300; DedeUserID__ckMd5=45b96a085d845b70; sid=6f84fn5c; buvid_fp=3484128cd87d5439209cfba8657e5e78; b_nut=100; enable_web_push=DISABLE; FEED_LIVE_VERSION=V8; header_theme_version=CLOSE; home_feed_column=4; browser_resolution=1358-646; CURRENT_FNVAL=4048; rpdid=|(um)~JkumuR0J'u~u|uRRRmu; bp_video_offset_31438300=907295700833796144; bp_article_offset_31438300=907295700833796144; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTA2Nzg2MDQsImlhdCI6MTcxMDQxOTM0NCwicGx0IjotMX0.HdY1kJQ9nIaaXVl5UxWTy5HdkeZGz1i-sPY5ngfSQkc; bili_ticket_expires=1710678544; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1709692447,1710521103; b_lsid=F22D29DF_18E46A7C670; bsource=search_bing; PVID=9"
#发送弹幕用的cookie

csrf_token = 'aed1c01f44880273b0cbaa9c2187d6f1'
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
