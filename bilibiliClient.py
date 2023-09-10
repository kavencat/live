# -*- coding: utf-8 -*-
import asyncio
import http.cookies
import random
from typing import *
import var_set
import time
import post_dm

import aiohttp

import blivedm
import blivedm.models.web as web_models

# 直播间ID的取值看直播间URL
TEST_ROOM_IDS = [
    var_set.roomid,
]

# 这里填一个已登录账号的cookie。不填cookie也可以连接，但是收到弹幕的用户名会打码，UID会变成0
SESSDATA = var_set.cookie[var_set.cookie.index('ATA=')+4:var_set.cookie.index('; bi')]

session: Optional[aiohttp.ClientSession] = None


async def main():
    init_session()
    try:
        await run_single_client()
        await run_multi_clients()
    finally:
        await session.close()


def init_session():
    cookies = http.cookies.SimpleCookie()
    cookies['SESSDATA'] = SESSDATA
    cookies['SESSDATA']['domain'] = 'bilibili.com'

    global session
    session = aiohttp.ClientSession()
    session.cookie_jar.update_cookies(cookies)


async def run_single_client():
    """
    演示监听一个直播间
    """
    room_id = random.choice(TEST_ROOM_IDS)
    client = blivedm.BLiveClient(room_id, session=session)
    handler = MyHandler()
    client.set_handler(handler)

    client.start()
    try:
        # 演示5秒后停止
        await asyncio.sleep(5)
        client.stop()

        await client.join()
    finally:
        await client.stop_and_close()


async def run_multi_clients():
    """
    演示同时监听多个直播间
    """
    clients = [blivedm.BLiveClient(room_id, session=session) for room_id in TEST_ROOM_IDS]
    handler = MyHandler()
    
    for client in clients:
        client.set_handler(handler)
        client.start()

    try:
        await asyncio.gather(*(
            client.join() for client in clients
        ))
    finally:
        await asyncio.gather(*(
            client.stop_and_close() for client in clients
        ))


class MyHandler(blivedm.BaseHandler):
    # # 演示如何添加自定义回调
    _CMD_CALLBACK_DICT = blivedm.BaseHandler._CMD_CALLBACK_DICT.copy()
    print(_CMD_CALLBACK_DICT)
    
    #async def __on_vip_enter(self,client: blivedm.BLiveClient,command):
    #    print(command['cmd'])
    #    if(command['cmd'] == 'LIVE'):
    #        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' 正在直播中……')
            
    #    if(command['cmd'] == 'INTERACT_WORD'):
    #        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' 听众['+command['data']['uname']+'] 进入直播……')
    #        post_dm.send_dm_long('欢迎【'+command['data']['uname']+'】进入直播间！')
            
    #_CMD_CALLBACK_DICT['LIVE'] = __on_vip_enter
    #_CMD_CALLBACK_DICT['INTERACT_WORD'] = __on_vip_enter
    #_CMD_CALLBACK_DICT['ENTRY_EFFECT_MUST_RECEIVE'] = __on_vip_enter
    
    #
    # # 入场消息回调
    # def __interact_word_callback(self, client: blivedm.BLiveClient, command: dict):
    #     print(f"[{client.room_id}] INTERACT_WORD: self_type={type(self).__name__}, room_id={client.room_id},"
    #           f" uname={command['data']['uname']}")
    # _CMD_CALLBACK_DICT['INTERACT_WORD'] = __interact_word_callback  # noqa

    def _on_heartbeat(self, client: blivedm.BLiveClient, message: web_models.HeartbeatMessage):
        #print(f'[{client.room_id}] 心跳')
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+f' [{client.room_id}] 当前人气值：{message.popularity}')

    def _on_danmaku(self, client: blivedm.BLiveClient, message: web_models.DanmakuMessage):
        #print(f'[{client.room_id}] {message.uname}：{message.msg}')
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+f' [{client.room_id}] {message.uname}：{message.msg}')
        post_dm.pick_msg(message.msg,message.uname)
        post_dm.w_log(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" "+message.uname+":"+message.msg+'\r\n',var_set.path+'/log/screenlog_dmlog.log','a')

    def _on_gift(self, client: blivedm.BLiveClient, message: web_models.GiftMessage):
        #print(f'[{client.room_id}] {message.uname} 赠送{message.gift_name}x{message.num}'
        #      f' （{message.coin_type}瓜子x{message.total_coin}）')
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+f' [{client.room_id}] {message.uname} 赠送{message.gift_name}x{message.num}'
              f' （{message.coin_type}瓜子x{message.total_coin}）')
        post_dm.send_dm_long('感谢['+message.uname+']赠送的['+message.gift_name+']'+str(message.num)+'个！')
        git_count = post_dm.get_coin(message.uname)
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' 观众['+message.uname+']已有'+str(git_count)+message.coin_type+'瓜子！')
        post_dm.give_coin(message.uname,message.num*message.total_coin)
        git_count = post_dm.get_coin(message.uname)
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' 观众['+message.uname+']现有'+str(git_count)+message.coin_type+'瓜子！')

    def _on_buy_guard(self, client: blivedm.BLiveClient, message: web_models.GuardBuyMessage):
        #print(f'[{client.room_id}] {message.username} 购买{message.gift_name}')
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+f' [{client.room_id}] {message.username} 购买{message.gift_name}')

    def _on_super_chat(self, client: blivedm.BLiveClient, message: web_models.SuperChatMessage):
        #print(f'[{client.room_id}] 醒目留言 ¥{message.price} {message.uname}：{message.message}')
        print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+f' [{client.room_id}] 醒目留言 ¥{message.price} {message.uname}：{message.message}')


if __name__ == '__main__':
    asyncio.run(main())
