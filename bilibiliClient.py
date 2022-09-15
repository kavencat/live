# -*- coding:utf-8 -*-
import asyncio
import aiohttp
import xml.dom.minidom
import random
import json
from struct import *
import json
import re
import var_set
import numpy
import os
import post_dm
import urllib
import urllib.request
import json
import blivedm
import threading
from threading import Timer
import time

def check_sizes(f):
    size = os.path.getsize('/home/pi/live/log/screenlog_'+f+'.log')
    size2 = round(size/1024/1024,2)
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+f+'log文件大小：'+str(size2)+'MB')
    if(size2>1):
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' 删除'+f+'log文件！')
        os.remove('/home/pi/live/log/screenlog_'+f+'.log')

roomId = int(var_set.roomid)

class MyBLiveClient(blivedm.BLiveClient):
    # 演示如何自定义handler
    _COMMAND_HANDLERS = blivedm.BLiveClient._COMMAND_HANDLERS.copy()

    async def __on_vip_enter(self, command):
        if(command['cmd'] == 'WELCOME'):
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' 欢迎月费老爷'+command['data']['uname']+'进入直播间！')
            post_dm.send_dm_long('欢迎老爷'+command['data']['uname']+'进入直播间！')
        if(command['cmd'] == 'LIVE'):
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' 准备直播中……')
            check_sizes('danmu')
            check_sizes('play')
            check_sizes('playing')
            
        if(command['cmd'] == 'INTERACT_WORD'):
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' 有用户进入')
            post_dm.send_dm_long('欢迎'+command['data']['uname']+'进入直播间！')
            replay = ["点个关注？？", "关注个，以后可以坐“飞机”直达~", "感谢你的到来！","可以点歌哦！","免费点歌哦！","多多关照！"]
            post_dm.send_dm_long(f'欢迎来到直播间！{replay[random.randint(0, len(replay)-1)]}')
            
            
    _COMMAND_HANDLERS['WELCOME'] = __on_vip_enter
    _COMMAND_HANDLERS['LIVE'] = __on_vip_enter
    _COMMAND_HANDLERS['INTERACT_WORD'] = __on_vip_enter
    _COMMAND_HANDLERS['GUIARD_MSG'] = __on_vip_enter
    _COMMAND_HANDLERS['CLOSE'] = __on_vip_enter
    _COMMAND_HANDLERS['GUARD_MSG'] = __on_vip_enter
    _COMMAND_HANDLERS['WELCOME_GUARD'] = __on_vip_enter
    _COMMAND_HANDLERS['WARNING'] = __on_vip_enter
        
    async def _on_receive_popularity(self, popularity: int):
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+f' 当前人气值：{popularity}')

    async def _on_receive_danmaku(self, danmaku: blivedm.DanmakuMessage):
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+f' {danmaku.uname}：{danmaku.msg}')
        post_dm.pick_msg(danmaku.msg,danmaku.uname)
        post_dm.w_log(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" "+danmaku.uname+":"+danmaku.msg+'\r\n','/home/pi/live/log/screenlog_dmlog.log','a')

    async def _on_receive_gift(self, gift: blivedm.GiftMessage):
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+f' {gift.uname} 赠送{gift.gift_name}x{gift.num} （{gift.num}瓜子x{gift.total_coin}）')
        try:
            gift_count = 0
            try:
                gift_count = numpy.load('users/'+gift.uname+'.npy')
            except:
                gift_count = 0
            try:
                os.remove('users/'+gift.uname+'.npy')
            except:
                print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'delete error')
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'获取'+gift.uname+'送过'+str(gift_count)+'个瓜子')
            f = urllib.request.urlopen("https://api.live.bilibili.com/gift/v3/live/gift_config")
            gift_info = json.loads(f.read().decode('utf-8'))
            for i in gift_info['data']:
                if i['name'] == gift.gift_name:
                    gift_count = gift_count + gift.num * i['price']
                    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'[log]gift match',i['name'],i['price'])
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+gift.uname+'瓜子数改为'+str(gift_count))
            try:
                numpy.save('users/'+gift.uname+'.npy', gift_count)
            except:
                print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'create error')
            post_dm.send_dm_long('感谢'+gift.uname+'送的'+str(gift.num)+'个'+gift.gift_name+'！')
        except:
            pass

    async def _on_buy_guard(self, message: blivedm.GuardBuyMessage):
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+f' {message.username} 购买{message.gift_name}')

    async def _on_super_chat(self, message: blivedm.SuperChatMessage):
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+f' 醒目留言 ¥{message.price} {message.uname}：{message.message}')


async def main():
    # 参数1是直播间ID
    # 如果SSL验证失败就把ssl设为False
    client = MyBLiveClient(roomId, ssl=True)
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' 正在连接直播间…………')
    future = client.start()
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' 进入直播间…………')
    
    i = 0
    
    #用于写入记录文件

    def w_fanlog():
        bili = blivedm.BiliSpider()
        res = bili.get_fans_info("31438300","1","1")
        try:
            post_dm.w_log('[昵称]'+res['data']['list'][i]['uname']+'[mid]'+str(res['data']['list'][i]['mid']),'fans.log','w')
        except:
            print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'读取关注用户失败！')
            
    w_fanlog()
    
    def cheakfans():
        wfan=post_dm.r_log('fans.log','r')
        i=0
        bili = blivedm.BiliSpider()
        res = bili.get_fans_info("31438300","1","1")
        try:
            #print("检查是否有听众关注！")
            sfan ='[昵称]'+res['data']['list'][i]['uname']+'[mid]'+str(res['data']['list'][i]['mid'])
            if(sfan == wfan):
                i=0
            else:
                print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' 有用户关注！')
                post_dm.w_log(sfan,'fans.log','w')
                nfans = post_dm.r_log('fans.log','r')
                post_dm.send_dm_long('感谢'+nfans+'的关注！')
        except:
            sfan = wfan
        t = threading.Timer(2, cheakfans)
        t.start()
        
    t = threading.Timer(2, cheakfans)
    t.start()
    
    #def send():
    #    replay = ["点个关注？？", "关注个，以后可以坐“飞机”直达~", "感谢你的到来！","可以点歌哦！","免费点歌哦！","多多关照！","歌曲限制为1分钟以上6分钟以下！","歌曲不正确请查看简介有解决办法！","请理性点播歌曲！"]
    #    post_dm.send_dm_long(f'欢迎来到直播间！{replay[random.randint(0, len(replay)-1)]}')
    #    t = threading.Timer(600, send)
    #    t.start()
        
    #t = threading.Timer(600, send)
    #t.start()

    try:
        # 5秒后停止，测试用
        # await asyncio.sleep(5)
        # future = client.stop()
        # 或者
        # future.cancel()
        
        await future
    finally:
        await client.close()



if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
