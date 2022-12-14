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

DB2_PATH = os.path.expanduser('~/.q2bot/qiandao.db')

DB_PATH3 = os.path.expanduser('~/.q2bot/shopnew.db')
# 新商店
class shopnew:
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH3), exist_ok=True)
        self._create_num()
        
        

    def _connect(self):
        return sqlite3.connect(DB_PATH3)

    def _create_num(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS SYSNUM
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           NUM1            INT    NOT  NULL,
                           NUM2           INT    NOT NULL,
                           PRIMARY KEY(GID, UID, NUM1));''')
        except:
            raise Exception('创建表发生错误')
    def _set_num(self, gid, uid, num1, num2):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO SYSNUM (GID, UID, NUM1, NUM2) VALUES (?, ?, ?, ?)",
                (gid, uid, num1, num2,),
            )
    def _get_num(self, gid, uid, num1):
        try:
            r = self._connect().execute("SELECT NUM2 FROM SYSNUM WHERE GID=? AND UID=? AND NUM1=?", (gid, uid, num1)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找表发生错误')
    def _add_num(self, gid, uid, num1, num2):
        num = self._get_num(gid, uid, num1)
        if num == None:
            num = 0
        num += num2
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO SYSNUM (GID, UID, NUM1, NUM2) VALUES (?, ?, ?, ?)",
                (gid, uid, num1, num),
            )
    def _reduce_num(self, gid, uid, num1, num2):
        num = self._get_num(gid, uid, num1)
        num -= num2
        num = max(num,0)
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO SYSNUM (GID, UID, NUM1, NUM2) VALUES (?, ?, ?, ?)",
                (gid, uid, num1, num),
            )

#获取列表
    def _get_uid_list(self, gid):
        try:
            r = self._connect().execute("SELECT DISTINCT(UID) FROM SYSNUM WHERE GID=? ", (gid,)).fetchall()
            return [u[0] for u in r] if r else {}
        except:
            raise Exception('查找uid表发生错误')

class qiandao:
    def __init__(self):
        os.makedirs(os.path.dirname(DB2_PATH), exist_ok=True)
        self._create_qd()
    def _connect(self):
        return sqlite3.connect(DB2_PATH)

    def _create_qd(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS QD
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           QD1           INT    NOT NULL,
                           QD2          INT NOT NULL,
                           PRIMARY KEY(GID, UID, QD1));''')
        except:
            raise Exception('创建表发生错误')
    def _get_qd(self, gid, uid, qd1):
        try:
            r = self._connect().execute("SELECT QD2 FROM QD WHERE GID=? AND UID=? AND QD1=?", (gid, uid, qd1)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找表发生错误')
    def _set_qd(self, gid, uid, qd1, qd2):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO QD (GID, UID, QD1, QD2) VALUES (?, ?, ?, ?)",
                (gid, uid, qd1, qd2),
            )
    def _add_qd(self, gid, uid, qd1, qd2):
        num1 = self._get_qd(gid, uid, qd1)
        if num1 == None:
            num1 = 0
        num1 += qd2
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO QD (GID, UID, QD1, QD2) VALUES (?, ?, ?, ?)",
                (gid, uid, qd1, num1),
            )
    def _reduce_qd(self, gid, uid, qd1, qd2):
        msg1 = self._get_qd(gid, uid, qd1)
        msg1 -= qd2
        msg1 = max(msg1,0)
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO QD (GID, UID, QD1, QD2) VALUES (?, ?, ?, ?)",
                (gid, uid, qd1, msg1),
            )

#获取列表
    def _get_uid_list(self, gid):
        try:
            r = self._connect().execute("SELECT DISTINCT(UID) FROM QD WHERE GID=? ", (gid,)).fetchall()
            return [u[0] for u in r] if r else {}
        except:
            raise Exception('查找uid表发生错误')

CSGO_PATH = os.path.expanduser('~/.q2bot/csgo.db')
# 存储csgo玩法数据
class getcsgo:
    def __init__(self):
        os.makedirs(os.path.dirname(CSGO_PATH), exist_ok=True)
        self._create_level()
        
        

    def _connect(self):
        return sqlite3.connect(CSGO_PATH)

    def _create_level(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS CSGOLEVEL
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           NUM1            INT    NOT  NULL,
                           NUM2           INT    NOT NULL,
                           PRIMARY KEY(GID, UID, NUM1));''')
        except:
            raise Exception('创建表发生错误')
    def _set_level(self, gid, uid, num1, num2):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO CSGOLEVEL (GID, UID, NUM1, NUM2) VALUES (?, ?, ?, ?)",
                (gid, uid, num1, num2,),
            )
    def _get_level(self, gid, uid, num1):
        try:
            r = self._connect().execute("SELECT NUM2 FROM CSGOLEVEL WHERE GID=? AND UID=? AND NUM1=?", (gid, uid, num1)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找表发生错误')
    def _add_level(self, gid, uid, num1, num2):
        num = self._get_level(gid, uid, num1)
        if num == None:
            num = 1
        num += num2
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO CSGOLEVEL (GID, UID, NUM1, NUM2) VALUES (?, ?, ?, ?)",
                (gid, uid, num1, num),
            )
    def _reduce_level(self, gid, uid, num1, num2):
        num = self._get_level(gid, uid, num1)
        num -= num2
        num = max(num,0)
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO CSGOLEVEL (GID, UID, NUM1, NUM2) VALUES (?, ?, ?, ?)",
                (gid, uid, num1, num),
            )

#获取列表
    def _get_uid_level_list(self, gid):
        try:
            r = self._connect().execute("SELECT DISTINCT(UID) FROM CSGOLEVEL WHERE GID=? ", (gid,)).fetchall()
            return [u[0] for u in r] if r else {}
        except:
            raise Exception('查找uid表发生错误')




#签到部分 0：当日是否签到  1：记录签到连续日 2：记录签到累计日  3:今日幸运值 
#csgo部分 0：用户等级  1：用户经验值

sv = Service('q2签到', enable_on_default=True)

shop_yule = {100000001000:'钥匙',100000001001:'命悬一线武器箱',100000001002:'梦魇武器箱'}
arc_shop_yule = {'钥匙':100000001000,'命悬一线武器箱':100000001001,'梦魇武器箱':100000001002}

@sv.on_fullmatch(['签到'])
async def qd(bot,ev:CQEvent):
    qd = qiandao()
    ck = chouka()
    shop = shopnew()
    csgo = getcsgo()
    uid = ev.user_id
    num4 = random.randint(0,100)
    qd._set_qd(0,uid,3,num4)
    if qd._get_qd(0,uid,0) !=0:
        await bot.finish(ev,f'已经签过了',at_sender=True)

    msg_send = '签到成功'
    
    
    qd._set_qd(0,uid,0,1)
    qd._add_qd(0,uid,1,1)
    qd._add_qd(0,uid,2,1)
    num = qd._get_qd(0,uid,1)
    num2 = qd._get_qd(0,uid,2)
    num3 = num*5
    num3 += 10
    ck._add_shitou(100,uid,num3)
    num4 = num3 *2  #转换为经验值
    shitou = random.randint(0,2333)
    ck._add_shitou(0,uid,shitou)

    list1 = [100000001000,100000001001,100000001002]
    get_list_id = random.choice(list1)
                                         #\n今日幸运值：{num4}
    csgo._add_level(0,uid,1,num4) # 加经验
    xp = csgo._get_level(0,uid,1) # 获取经验
    level = csgo._get_level(0,uid,0) # 获取等级
    up_level = level * 500 #提升一级需要（级数*500）经验
    if level >=10: #达到10级后将会随机1~6个奖励
        addnum = random.randint(1,6)
    else:    #否则只会掉落1个
        addnum = 1
    shop._add_num(0,uid,get_list_id,addnum)  

    msg_send += f'\n精元碎片+{num3} 喵喵石头+{shitou}\n喵go等级：{level}({xp}/{up_level}) +{num4}\n连续/累积：{num}/{num2}天\n幸运掉落：{shop_yule[get_list_id]}x{addnum}'
    await bot.send(ev,msg_send,at_sender=True)

@sv.on_fullmatch(('go升级'))
async def level_up(bot,ev:CQEvent):
    csgo = getcsgo()
    shop = shopnew()
    uid = ev.user_id
    xp = csgo._get_level(0,uid,1) # 获取经验
    level = csgo._get_level(0,uid,0) # 获取等级
    up_level = level * 500 #提升一级需要（级数*500）经验
    msg = ''
    if xp >= up_level: #满足后提升一级，并扣除经验值
        csgo._add_level(0,uid,0,1)
        csgo._reduce_level(0,uid,1,up_level)
        msg += 'gogo升级了！'
    xp = csgo._get_level(0,uid,1) # 再获取一下
    level = csgo._get_level(0,uid,0) 
    up_level = level * 500
    if level == 10: #10级奖励
        shop._add_num(0,uid,100000001000,288)
        shop._add_num(0,uid,100000001001,288)
        shop._add_num(0,uid,100000001002,288)
        msg += '恭喜升到10级\n奖励：钥匙x288，命悬一线武器箱x288，梦魇武器箱x288！\n请再接再厉'
    if level == 15:
        shop._add_num(0,uid,100000001000,328)
        shop._add_num(0,uid,100000001001,328)
        shop._add_num(0,uid,100000001002,328)
        msg += '恭喜升到15级\n奖励：钥匙x328，命悬一线武器箱x328，梦魇武器箱x328！\n请再接再厉'   
    msg += f'喵go等级：{level}({xp}/{up_level})'
    await bot.send(ev,msg,at_sender=True)

@sv.scheduled_job('cron', hour ='5',)
async def clock():
    qd = qiandao()
    uid_list = qd._get_uid_list(0)
    for a in uid_list:
        if qd._get_qd(0,a,0) ==0:
            qd._set_qd(0,a,1,0)
        qd._set_qd(0,a,0,0)
        qd._set_qd(0,a,3,0)

    print('==============今日签到已恢复！==============')
