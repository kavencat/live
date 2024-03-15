import requests
import time
import json
import var_set
import re

r = r'ATA=(.*?);'

SESSDATA = var_set.cookie[var_set.cookie.index('SESSDATA=')+1:var_set.cookie.index(';')]
SESSDATA = re.findall(r , var_set.cookie)

print(var_set.cookie)
print(SESSDATA[0])

url = 'https://api.live.bilibili.com/msg/send'      #这个是B站的弹幕，发送API接口
s = 'nihao'

header={       #构造请求头,这里只放一个cookie就可以了
'cookie':"buvid3=A395DBB5-847A-9287-06A8-62C5CD284B8062102infoc; b_nut=1702385562; CURRENT_FNVAL=4048; _uuid=35F102510D-352C-7C52-645F-9ED931088AEA563301infoc; buvid4=22F12A69-91C4-715E-59EE-72A25EB8F74D63148-023121212-; rpdid=0zbfVGh29A|lAdywI2m|2wH|3w1Rd2fH; LIVE_BUVID=AUTO6417023977257485; buvid_fp_plain=undefined; sid=8fjhsanf; CURRENT_QUALITY=80; hit-dyn-v2=1; bp_video_offset_97489590=887177567177539607; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDYzMjQ3MDIsImlhdCI6MTcwNjA2NTQ0MiwicGx0IjotMX0.v2hjIh0-V1o6xiP6Ux2ZvdvbKBW9jNeKdTGvM3s_rlU; bili_ticket_expires=1706324642; fingerprint=8f4bd45c34a2af8ad346de6135f9aa47; DedeUserID=31438300; DedeUserID__ckMd5=45b96a085d845b70; SESSDATA=04baf571%2C1721696998%2C284c2*11; bili_jct=8bacc57651c801bac389b1a2f603b4ff; buvid_fp=8f4bd45c34a2af8ad346de6135f9aa47; b_lsid=5169E4FE_18D3FC35B38; bsource=search_bing; PVID=6",
'origin': 'https://live.bilibili.com',
'referer': 'https://live.bilibili.com/blanc/1029?liteVersion=true',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
}

data = {        #构造请求数据
'bubble': '0',
'msg': s,
'color': '16777215',
'mode': '1',
'fontsize': '25',
'rnd': str(int(time.time())),
'roomid': '3702914',
'csrf': '8bacc57651c801bac389b1a2f603b4ff',
'csrf_token': '8bacc57651c801bac389b1a2f603b4ff'
}


result =  requests.post(url=url, headers=header, data=data).text        #发送弹幕
print("result:", result)        #显示返回结果
result = json.loads(result)
if len(result['msg']) > 0:
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'[error]弹幕发送失败：'+s)
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+dm_result)
else:
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+' '+'[log]发送弹幕：'+s)
