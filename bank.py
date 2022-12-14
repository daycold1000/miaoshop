import asyncio
import base64
import os
import random
from re import T, match
import sqlite3
from datetime import datetime, timedelta
from io import SEEK_CUR, BytesIO
from PIL import Image
from hoshino import Service, priv
from hoshino.typing import CQEvent
from hoshino.util import DailyNumberLimiter
import copy
import json
import math
import pytz
import nonebot
from nonebot import on_command, on_request
from hoshino import sucmd
from nonebot import get_bot
from hoshino.typing import NoticeSession

sv = Service('q2bank', enable_on_default=True)

DB_PATH = os.path.expanduser('~/.q2bot/chouka.db')

# 创建DB数据
class chouka:
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self._create_shitou()
    def _connect(self):
        return sqlite3.connect(DB_PATH)
#母猪石数量
    def _create_shitou(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS SHITOU
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           SHITOU           INT    NOT NULL,
                           PRIMARY KEY(GID, UID));''')
        except:
            raise Exception('创建表发生错误')
    def _set_shitou(self, gid, uid, shitou):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO SHITOU (GID, UID, SHITOU) VALUES (?, ?, ?)",
                (gid, uid, shitou,),
            )
    def _get_shitou(self, gid, uid):
        try:
            r = self._connect().execute("SELECT SHITOU FROM SHITOU WHERE GID=? AND UID=?", (gid, uid)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找表发生错误')
    def _add_shitou(self, gid, uid, num):
        num1 = self._get_shitou(gid, uid)
        if num1 == None:
            num1 = 0
        num1 += num
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO SHITOU (GID, UID, SHITOU) VALUES (?, ?, ?)",
                (gid, uid, num1),
            )
    def _reduce_shitou(self, gid, uid, num):
        msg1 = self._get_shitou(gid, uid)
        msg1 -= num
        msg1 = max(msg1,0)
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO SHITOU (GID, UID, SHITOU) VALUES (?, ?, ?)",
                (gid, uid, msg1),
            )

#获取列表
    def _get_uid_list(self, gid):
        try:
            r = self._connect().execute("SELECT DISTINCT(UID) FROM SHITOU WHERE GID=? ", (gid,)).fetchall()
            return [u[0] for u in r] if r else {}
        except:
            raise Exception('查找uid表发生错误')

@sv.on_fullmatch(['看看银行'])
async def bank(bot,ev:CQEvent):
    ck = chouka()
    num1 = ck._get_shitou(0,0)
    num2 = ck._get_shitou(0,4)
    num3 = ck._get_shitou(0,5)
    num4 = ck._get_shitou(0,2)
    num5 = ck._get_shitou(0,3)
    
    msg = f'ようこそ銀行\n有 {num1}石💰'
    if num2 !=0:
        msg += f'(+{num2}✔️)'    #今日银行比昨日盈利的值
    if num3 !=0:
        msg += f'(-{num3}❌)'    #今日银行比昨日亏损的值
    msg += f'({num5}%✔️)({num4}%❌)\n使用可能なコマンド:\n<[存][借][还][取][数量]石>' 
    await bot.send(ev,msg)  #盈利率和亏损率展示，影响玩家在银行中存储（或借取）石头的利息结算 

@sv.on_rex(r'^存(.*)石$')
async def cun(bot,ev:CQEvent):
    ck = chouka()
    uid = ev.user_id
    num = ck._get_shitou(0,uid) #获取玩家在存入前持有的喵喵石头数量
    match = (ev['match'])
    num2 = int(match.group(1))  #获取玩家需要存入喵喵石头的数量
    if num2 > num:
        await bot.finish(ev,'你没那么多',at_sender=True)
    ck._reduce_shitou(0,uid,num2)   #扣除玩家的喵喵石头
    ck._add_shitou(1,uid,num2)  #增加玩家在银行存入的喵喵石头
    ck._add_shitou(0,0,num2)    #增加银行的喵喵石头
    num1 = ck._get_shitou(1,uid)    #获取玩家在银行已经存入的喵喵石头数量
    num = ck._get_shitou(0,uid) #获取玩家现在持有的喵喵石头数量
    await bot.send(ev,f'好了\n-{num2} ✔️\n💰 {num}\n💰✔️ {num1}')

@sv.on_rex(r'^取(.*)石$')
async def cun(bot,ev:CQEvent):
    ck = chouka()
    uid = ev.user_id
    num = ck._get_shitou(0,0)   #获取银行在玩家取出前持有的喵喵石头数量
    num10 = ck._get_shitou(1,uid)   #获取玩家取出前在银行存入的喵喵石头数量
    match = (ev['match'])
    num2 = int(match.group(1))  #获取玩家要取出多少喵喵石头
    if num2 > num:
        await bot.finish(ev,'bank low money!',at_sender=True)   #银行没钱了QAQ
    if num10 < num2:
        await bot.finish(ev,'你没存那么多',at_sender=True)    
    ck._reduce_shitou(0,0,num2) #扣除银行的喵喵石头
    ck._add_shitou(0,uid,num2)  #添加玩家的喵喵石头  
    ck._reduce_shitou(1,uid,num2)   #扣除玩家在银行存入的喵喵石头
    num1 = ck._get_shitou(1,uid)    #获取玩家在银行已经存入的喵喵石头数量
    num = ck._get_shitou(0,uid)     #获取玩家现在持有的喵喵石头数量
    await bot.send(ev,f'好了\n+{num2}\n💰 {num}\n💰✔️ {num1}')

@sv.on_rex(r'^借(.*)石$')
async def jie(bot,ev:CQEvent):
    ck = chouka()
    uid = ev.user_id
    num = ck._get_shitou(0,0)
    match = (ev['match'])
    num2 = int(match.group(1))
    if num2 > num:
        await bot.finish(ev,'bank low money!',at_sender=True)
    jie = ck._get_shitou(2,uid) #获取玩家已经从银行借了的石头数量
    xz_num = 1500       #这里控制玩家可借取石头的总数
    xz_num -= jie   #减去已借数量
    if num2 > xz_num:   
        await bot.finish(ev,'不要借的太多...人...人家怕你还不上嘛！')
    ck._reduce_shitou(0,0,num2) #扣除银行的喵喵石头
    ck._add_shitou(0,uid,num2)  #增加玩家的喵喵石头
    ck._add_shitou(2,uid,num2)  #增加玩家的负债
    num1 = ck._get_shitou(2,uid)    #获取玩家当前负债值
    num = ck._get_shitou(0,uid)     #获取玩家的喵喵石头数量
    await bot.send(ev,f'记得还\n+{num2} ❌\n💰 {num}\n💰❌ {num1}')

@sv.on_rex(r'^还(.*)石$')     #这里代码不用动了
async def jie(bot,ev:CQEvent):
    ck = chouka()
    uid = ev.user_id
    num = ck._get_shitou(0,uid)
    num10 = ck._get_shitou(2,uid)
    match = (ev['match'])
    num2 = int(match.group(1))
    if num2 > num:
        await bot.finish(ev,'你没那么多',at_sender=True)
    if num10 < num2:
        await bot.finish(ev,'不需要还那么多',at_sender=True)
    ck._reduce_shitou(0,uid,num2)
    ck._add_shitou(0,0,num2)
    ck._reduce_shitou(2,uid,num2)
    num1 = ck._get_shitou(2,uid)
    num = ck._get_shitou(0,uid)
    await bot.send(ev,f'收到了\n-{num2}\n💰 {num}\n💰❌ {num1}')

@sv.on_fullmatch(['我的卡'])
async def bank(bot,ev:CQEvent):
    ck = chouka()
    uid = ev.user_id
    msg = '\n喵喵石头：\n'
    num = ck._get_shitou(0,uid)
    msg += f'有 {num}'
    num1 = ck._get_shitou(1,uid)
    if num1 != 0:
        msg += f'(✔️{num1})'
    num2 = ck._get_shitou(2,uid)
    if num2 != 0:
        msg += f'(❌{num2})'
    msg += '\n精元碎片：\n'
    num100 = ck._get_shitou(100,uid)
    msg += f'有 {num100}'
    
    await bot.send(ev,msg,at_sender=True)

@sv.scheduled_job('cron', hour ='5',)
async def bank():
    ck = chouka()
    num1 = ck._get_shitou(0,1) #昨日    
    num2 = ck._get_shitou(0,0) #今日
    ck._set_shitou(0,1,num2)
    if num2 > num1: #今天的比昨天的多  赚
        ck._set_shitou(0,2,0.05)
        num3 = num2 - num1
        ck._set_shitou(0,4,num3)
        ck._set_shitou(0,5,0)
        num3 = num3 * 0.0000000088  #为毛那么小，银行看不惯玩家赚钱
        num3 = round(num3,5)
        ck._set_shitou(0,3,num3)

    if num1 > num2: #昨天的比今天的多  亏
        ck._set_shitou(0,3,0)
        num3 = num1 - num2
        ck._set_shitou(0,5,num3)
        ck._set_shitou(0,4,0)
        num3 = num3 *0.0000232  #为毛那么大，银行喜欢欠钱的玩家
        num3 = round(num3,5)
        ck._set_shitou(0,2,num3)
        
#下面为每日利息结算完成后响应到玩家账户的代码
#（哦吼，我记得曾经测试的时候，数值调错了导致某玩家拥有千亿资产，现在汇率改的超低应该不会再出这种问题了）
    uid_list_cun = ck._get_uid_list(1)
    uid_list_dai = ck._get_uid_list(2)
    for a in range(len(uid_list_cun)):
        uid = int(uid_list_cun[a])
        cun = ck._get_shitou(0,3)
        if uid != '':
            num10 = ck._get_shitou(1,uid)
            num10 = num10 * cun
            num10 = round(num10,0)
            ck._add_shitou(1,uid,num10)

    for b in range(len(uid_list_dai)):
        uid = int(uid_list_dai[b])
        dai = ck._get_shitou(0,2)
        if uid != '':
            num10 = ck._get_shitou(2,uid)
            num10 = num10 * dai
            num10 = round(num10,0)
            ck._add_shitou(2,uid,num10)    

    print('==============银行利息结算已完成==============')

