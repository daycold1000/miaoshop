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
DB_PATH2 = os.path.expanduser('~/.q2bot/shop.db')

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

# 创建DB数据
class shangdian:
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH2), exist_ok=True)
        self._create_daoju()
        self._create_jishu()
        

    def _connect(self):
        return sqlite3.connect(DB_PATH2)
#道具数量
    def _create_daoju(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS DAOJUI
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           DAOJUI           INT    NOT NULL,
                           PRIMARY KEY(GID, UID));''')
            self._connect().execute('''CREATE TABLE IF NOT EXISTS DAOJUII
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           DAOJUII           INT    NOT NULL,
                           PRIMARY KEY(GID, UID));''')
            self._connect().execute('''CREATE TABLE IF NOT EXISTS DAOJUIII
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           DAOJUIII           INT    NOT NULL,
                           PRIMARY KEY(GID, UID));''')
            self._connect().execute('''CREATE TABLE IF NOT EXISTS DAOJUIV
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           DAOJUIV           INT    NOT NULL,
                           PRIMARY KEY(GID, UID));''')
        except:
            raise Exception('创建表发生错误')
    def _set_daoju1(self, gid, uid, num):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO DAOJUI (GID, UID, DAOJUI) VALUES (?, ?, ?)",
                (gid, uid, num,),
            )
    def _set_daoju2(self, gid, uid, num):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO DAOJUII (GID, UID, DAOJUII) VALUES (?, ?, ?)",
                (gid, uid, num,),
            )
    def _set_daoju3(self, gid, uid, num):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO DAOJUIII (GID, UID, DAOJUIII) VALUES (?, ?, ?)",
                (gid, uid, num,),
            )
    def _set_daoju4(self, gid, uid, num):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO DAOJUIV (GID, UID, DAOJUIV) VALUES (?, ?, ?)",
                (gid, uid, num,),
            )

    def _get_daoju1(self, gid, uid):
        try:
            r = self._connect().execute("SELECT DAOJUI FROM DAOJUI WHERE GID=? AND UID=?", (gid, uid)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找表发生错误')
    def _get_daoju2(self, gid, uid):
        try:
            r = self._connect().execute("SELECT DAOJUII FROM DAOJUII WHERE GID=? AND UID=?", (gid, uid)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找表发生错误')
    def _get_daoju3(self, gid, uid):
        try:
            r = self._connect().execute("SELECT DAOJUIII FROM DAOJUIII WHERE GID=? AND UID=?", (gid, uid)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找表发生错误')
    def _get_daoju4(self, gid, uid):
        try:
            r = self._connect().execute("SELECT DAOJUIV FROM DAOJUIV WHERE GID=? AND UID=?", (gid, uid)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找表发生错误')

    def _add_daoju1(self, gid, uid, num):
        num1 = self._get_daoju1(gid, uid)
        if num1 == None:
            num1 = 0
        num1 += num
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO DAOJUI (GID, UID, DAOJUI) VALUES (?, ?, ?)",
                (gid, uid, num1),
            )
    def _add_daoju2(self, gid, uid, num):
        num1 = self._get_daoju2(gid, uid)
        if num1 == None:
            num1 = 0
        num1 += num
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO DAOJUII (GID, UID, DAOJUII) VALUES (?, ?, ?)",
                (gid, uid, num1),
            )
    def _add_daoju3(self, gid, uid, num):
        num1 = self._get_daoju3(gid, uid)
        if num1 == None:
            num1 = 0
        num1 += num
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO DAOJUIII (GID, UID, DAOJUIII) VALUES (?, ?, ?)",
                (gid, uid, num1),
            )
    def _add_daoju4(self, gid, uid, num):
        num1 = self._get_daoju4(gid, uid)
        if num1 == None:
            num1 = 0
        num1 += num
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO DAOJUIV (GID, UID, DAOJUIV) VALUES (?, ?, ?)",
                (gid, uid, num1),
            )

    def _reduce_daoju1(self, gid, uid, num):
        msg1 = self._get_daoju1(gid, uid)
        msg1 -= num
        msg1 = max(msg1,0)
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO DAOJUI (GID, UID, DAOJUI) VALUES (?, ?, ?)",
                (gid, uid, msg1),
            )
    def _reduce_daoju2(self, gid, uid, num):
        msg1 = self._get_daoju2(gid, uid)
        msg1 -= num
        msg1 = max(msg1,0)
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO DAOJUII (GID, UID, DAOJUII) VALUES (?, ?, ?)",
                (gid, uid, msg1),
            )
    def _reduce_daoju3(self, gid, uid, num):
        msg1 = self._get_daoju3(gid, uid)
        msg1 -= num
        msg1 = max(msg1,0)
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO DAOJUIII (GID, UID, DAOJUIII) VALUES (?, ?, ?)",
                (gid, uid, msg1),
            )
    def _reduce_daoju4(self, gid, uid, num):
        msg1 = self._get_daoju4(gid, uid)
        msg1 -= num
        msg1 = max(msg1,0)
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO DAOJUIV (GID, UID, DAOJUIV) VALUES (?, ?, ?)",
                (gid, uid, msg1),
            )
#购买计数
    def _create_jishu(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS JISHU
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           JISHU           INT    NOT NULL,
                           PRIMARY KEY(GID, UID));''')
            self._connect().execute('''CREATE TABLE IF NOT EXISTS SHIJIA
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           SHIJIA           INT    NOT NULL,
                           PRIMARY KEY(GID, UID));''')
        except:
            raise Exception('创建表发生错误')
    def _set_jishu(self, gid, uid, num):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO JISHU (GID, UID, JISHU) VALUES (?, ?, ?)",
                (gid, uid, num,),
            )
    def _set_shijia(self, gid, uid, num):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO SHIJIA (GID, UID, SHIJIA) VALUES (?, ?, ?)",
                (gid, uid, num,),
            )
    def _get_jishu(self, gid, uid):
        try:
            r = self._connect().execute("SELECT JISHU FROM JISHU WHERE GID=? AND UID=?", (gid, uid)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找表发生错误')
    def _get_shijia(self, gid, uid):
        try:
            r = self._connect().execute("SELECT SHIJIA FROM SHIJIA WHERE GID=? AND UID=?", (gid, uid)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找表发生错误')
    def _add_jishu(self, gid, uid, num):
        num1 = self._get_jishu(gid, uid)
        if num1 == None:
            num1 = 0
        num1 += num
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO JISHU (GID, UID, JISHU) VALUES (?, ?, ?)",
                (gid, uid, num1),
            )
    def _reduce_jishu(self, gid, uid, num):
        msg1 = self._get_jishu(gid, uid)
        msg1 -= num
        msg1 = max(msg1,0)
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO JISHU (GID, UID, JISHU) VALUES (?, ?, ?)",
                (gid, uid, msg1),
            )

DB_PATH3 = os.path.expanduser('~/.q2bot/shopnew.db')
# 创建DB数据
class shopnew:
    def __init__(self):
        os.makedirs(os.path.dirname(DB_PATH3), exist_ok=True)
        self._create_sysnum()
        
        

    def _connect(self):
        return sqlite3.connect(DB_PATH3)

    def _create_sysnum(self):
        try:
            self._connect().execute('''CREATE TABLE IF NOT EXISTS SYSNUM
                          (GID             INT    NOT NULL,
                           UID             INT    NOT NULL,
                           NUM1            INT    NOT  NULL,
                           NUM2           INT    NOT NULL,
                           PRIMARY KEY(GID, UID, NUM1));''')
        except:
            raise Exception('创建表发生错误')
    def _set_sysnum(self, gid, uid, num1, num2):
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO SYSNUM (GID, UID, NUM1, NUM2) VALUES (?, ?, ?, ?)",
                (gid, uid, num1, num2,),
            )
    def _get_sysnum(self, gid, uid, num1):
        try:
            r = self._connect().execute("SELECT NUM2 FROM SYSNUM WHERE GID=? AND UID=? AND NUM1=?", (gid, uid, num1)).fetchone()
            return 0 if r is None else r[0]
        except:
            raise Exception('查找表发生错误')
    def _add_sysnum(self, gid, uid, num1, num2):
        num = self._get_sysnum(gid, uid, num1)
        if num == None:
            num = 0
        num += num2
        with self._connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO SYSNUM (GID, UID, NUM1, NUM2) VALUES (?, ?, ?, ?)",
                (gid, uid, num1, num),
            )
    def _reduce_sysnum(self, gid, uid, num1, num2):
        num = self._get_sysnum(gid, uid, num1)
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

# 纪念品商店数据
JNP_DB = os.path.expanduser('~/.q2bot/shopjnp.db')
class shopjnp:
    def __init__(self):
        os.makedirs(os.path.dirname(JNP_DB), exist_ok=True)
        self._create_num()
        
        

    def _connect(self):
        return sqlite3.connect(JNP_DB)

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
sv = Service('q2商店')

@sv.on_fullmatch(('旧道具商店'))     #在一次大更新前使用的旧商店，代码不想优化了就在这里当纪念了
async def shop(bot,ev):
    ck = chouka()
    shop = shangdian()
    uid = ev.user_id
    
    shijia = shop._get_shijia(1,1)

    shop1 = shop._get_jishu(1,1)
    shop2 = shop._get_jishu(1,2)
    
    shop4 = shop._get_jishu(1,4)

    money1 = 610*shijia
    money2 = 499*shijia
    money3 = 76.5*shijia
    money4 = 685*shijia

    await bot.send(ev,f'''一眼看穿 {money1}石/个 剩余{shop1}个
暗中调换 {money2}石/个 剩余{shop2}个 
再来两戳 {money4}石/个 剩余{shop4}个
精元碎片 {money3}石/个
使用可能なコマンド：
<买[物品名][数量]个>
<使用道具 [道具名]>\n<我的卡>''')

@sv.on_fullmatch(('道具商店 生鲜'))   #这里本来打算做一个虚拟人生的大玩法，累了
async def shop(bot,ev):
    ck = chouka()
    shop = shopnew()
    uid = ev.user_id

    shijia1 = shop._get_sysnum(0,0,100000000001) #价格
    shijia2 = shop._get_sysnum(0,0,100000000002) 

    shop1 = shop._get_sysnum(0,1,100000000001) #剩余数量
    shop2 = shop._get_sysnum(0,1,100000000002)

    await bot.send(ev,f'''破旧的钓鱼竿 {shijia1}石/个 剩余{shop1}个
普通的钓鱼竿 {shijia2}石/个 剩余{shop2}个
使用可能なコマンド：
<购买[物品名][数量]个>
<使用 [道具名]>
<我的卡>''')

@sv.on_fullmatch(('纪念品商店'))     #我所在的群里有些特殊的群会做一些活动，因此才有了这个纪念品商店
async def shop(bot,ev):
    shop = shopjnp()
    uid = ev.user_id
    await bot.send(ev,f'''2022小彩旗
使用可能なコマンド：
<获取[物品名]>
<纪念品背包>''')

@sv.on_rex(r'^获取(2022小彩旗|某人亲手做的烤羊腿|3|4)$')      #如果觉得这个不是很需要，可以删了这些
async def buy(bot, ev: CQEvent):
    uid = ev.user_id
    shop = shopjnp()
    match = (ev['match'])
    buy = match.group(1)
    if buy == '2022小彩旗':
        #shop._set_num(0,uid,20221001,1)
        await bot.send(ev,'来迟了，小彩旗已经拿完了~')
    if buy == '某人亲手做的烤羊腿':
        #shop._set_num(0,uid,20221002,1)
        await bot.send(ev,'来迟了，羊腿已经分完了~')

jnp = {20220910:'2022喵喵口味月饼',20221001:'2022小彩旗',20221002:'神秘的烤羊腿'}
jnp_id = [20220910,20221001,20221002]

@sv.on_fullmatch(('纪念品背包'))     #我也很好奇当初为什么要做一个纪念品商店呢？唉
async def shop(bot,ev):
    uid = ev.user_id
    shop = shopjnp()
    msg = '纪念品背包：\n'
    for id in jnp_id:
        have = shop._get_num(0,uid,id)
        if have !=0:
            msg += f'{jnp[id]} 获得！\n'
        else: 
            msg += f'{jnp[id]} 未获得\n'
    await bot.send(ev,msg,at_sender=True)

    

@sv.on_fullmatch(('道具商店 饮料'))   #同上面的生鲜商店
async def shop(bot,ev):
    ck = chouka()
    shop = shopnew()
    uid = ev.user_id
    await bot.send(ev,f'''当前分区无上架商品
使用可能なコマンド：
<购买[物品名][数量]个>
<使用 [道具名]>
<我的卡>''')

shop_yule = {100000001000:'钥匙',100000001001:'命悬一线武器箱',100000001002:'梦魇武器箱'}
arc_shop_yule = {'钥匙':100000001000,'命悬一线武器箱':100000001001,'梦魇武器箱':100000001002}

@sv.on_fullmatch(('道具商店 娱乐'))   #这里是csgo开箱玩法的商店，和功能 csgo开箱 联动
async def shop(bot,ev):
    ck = chouka()
    shop = shopnew()
    uid = ev.user_id

    msg = ''
    for a in shop_yule:
        name1 = shop_yule.get(a) #获取名称
        shijia1 = shop._get_sysnum(0,0,a)
        shop1 = shop._get_sysnum(0,1,a)
        msg += f'{name1} {shijia1}碎片/个 剩余{shop1}个\n'
    msg += '使用可能なコマンド：\n<购买[物品名][数量]个>'
    await bot.send(ev,msg)

@sv.on_rex(r'^购买(钥匙|命悬一线武器箱|梦魇武器箱)(.*)个$')
async def buy(bot, ev: CQEvent):
    ck = chouka()
    shop = shopnew()
    uid = ev.user_id
    gid = int(ev.group_id)
    match = (ev['match'])
    buy = match.group(1)
    num = int(match.group(2))
    if buy =='钥匙':
        shop_id = 100000001000
        shop._set_sysnum(0,0,shop_id,380) #价格在这里设置（临时写的，在下一次大更新的时候会写定时更变价格代码）
    if buy =='命悬一线武器箱':                 #2022年12月3日01:10上传github记：没有大更新了，这里的代码就这样吧....
        shop_id = 100000001001
        shop._set_sysnum(0,0,shop_id,50) 
    if buy == '梦魇武器箱':
        shop_id = 100000001002
        shop._set_sysnum(0,0,shop_id,190) 

    shijia1 = shop._get_sysnum(0,0,shop_id)
    shop1 = shop._get_sysnum(0,1,shop_id)
    num1 = ck._get_shitou(100,uid)
    num2 = int(shijia1)*int(num)
    if shop1 < num:
        await bot.finish(ev,'货物不足，等待补货')
    if num1 < num2:
        await bot.finish(ev,'精元碎片不足')
    ck._reduce_shitou(100,uid,num2)
    shop._add_sysnum(0,uid,shop_id,num)
    shop._reduce_sysnum(0,1,shop_id,num)
    await bot.finish(ev,'買い物が終わった',at_sender=True)



@sv.on_rex(r'^买(一眼看穿|暗中调换|再来两戳|精元碎片)(.*)个$')    #这里是旧商店的代码，并不想优化了（可以很明显的看出上面csgo的新代码多简洁啊~
async def buy(bot, ev: CQEvent):
    ck = chouka()
    shop = shangdian()
    uid = ev.user_id
    gid = int(ev.group_id)
    match = (ev['match'])
    buy = match.group(1)
    num = match.group(2)
    if buy =='一眼看穿':
        shuliang = shop._get_jishu(1,1)
        shijia = shop._get_shijia(1,1)
        num1 = ck._get_shitou(0,uid)
        num11 = 610*shijia
        num2 = int(num11)*int(num)
        num3 = int(num)
        if int(shuliang) < int(num):
            await bot.finish(ev,'货物不足，等待补货')
        if int(num1) < int(num2):
            await bot.finish(ev,'货币不足',at_sender=True) 
        ck._reduce_shitou(0,uid,num2)
        ck._add_shitou(0,0,num2)
        shop._add_daoju1(0,uid,num3)
        shop._reduce_jishu(1,1,num3)
        await bot.finish(ev,'買い物が終わった',at_sender=True)
    if buy =='暗中调换':
        shuliang = shop._get_jishu(1,2)
        shijia = shop._get_shijia(1,1)
        num1 = ck._get_shitou(0,uid)
        num11 = 499*shijia
        num2 = int(num11)*int(num)
        num3 = int(num)
        if int(shuliang) < int(num):
            await bot.finish(ev,'货物不足，等待补货')
        if int(num1) < int(num2):
            await bot.finish(ev,'货币不足',at_sender=True) 
        ck._reduce_shitou(0,uid,num2)
        ck._add_shitou(0,0,num2)
        shop._add_daoju2(0,uid,num3)
        shop._reduce_jishu(1,2,num3)
        await bot.finish(ev,'買い物が終わった',at_sender=True)
    if buy =='再来两戳':
        shuliang = shop._get_jishu(1,4)
        shijia = shop._get_shijia(1,1)
        num1 = ck._get_shitou(0,uid)
        num11 = 685*shijia
        num2 = int(num11)*int(num)
        num3 = int(num)
        if int(shuliang) < int(num):
            await bot.finish(ev,'货物不足，等待补货')
        if int(num1) < int(num2):
            await bot.finish(ev,'货币不足',at_sender=True) 
        ck._reduce_shitou(0,uid,num2)
        ck._add_shitou(0,0,num2)
        shop._add_daoju4(0,uid,num3)
        shop._reduce_jishu(1,4,num3)
        await bot.finish(ev,'買い物が終わった',at_sender=True)
    if buy =='精元碎片':
        shijia = shop._get_shijia(1,1)
        num1 = ck._get_shitou(0,uid)
        num11 = 76.5*shijia
        num2 = int(num11)*int(num)
        num3 = int(num)
        num4 = round(num1 / num11,1)
        if int(num1) < int(num2):
            await bot.finish(ev,f'货币不足，最多能购买{num4}个',at_sender=True) 
        ck._reduce_shitou(0,uid,num2)
        ck._add_shitou(0,0,num2)
        ck._add_shitou(100,uid,num3)
        await bot.finish(ev,'買い物が終わった',at_sender=True)

@sv.scheduled_job('cron', hour ='5',)   #每天5点准时补货
async def clock():
    shop = shangdian()
    shopnew = shopnew()
    add1 = random.randint(1,7)
    add2 = random.randint(2,8)
    #add3 = random.randint(2,5)
    add4 = random.randint(1,2)
    shop._add_jishu(1,1,add1)
    shop._add_jishu(1,2,add2)
    #shop._add_jishu(1,3,add3)
    shop._add_jishu(1,4,add4)
    #下面是csgo那几个东西的进货，也是在2022年12月3日传github时加的...
    shopnew._add_sysnum(0,1,100000001000,add2)
    shopnew._add_sysnum(0,1,100000001001,add1)
    shopnew._add_sysnum(0,1,100000001002,add1)
    print('==============商店补货完成！================')



@sv.on_fullmatch(('我的背包'))
async def gacha_cangku(bot, ev: CQEvent):
    uid = ev.user_id
    shop = shangdian()

    
    shop1 = shop._get_daoju1(0,uid)
    shop2 = shop._get_daoju2(0,uid)
    #shop3 = shop._get_daoju3(0,uid)
    shop4 = shop._get_daoju4(0,uid)

    msg = f'一眼看穿 {shop1}个\n暗中调换 {shop2}个\n再来两戳 {shop4}个\n\n使用可能なコマンド：\n<使用道具 [道具名]>\n<我的卡>'
    await bot.send(ev,msg,at_sender=True)
@sv.on_fullmatch(('娱乐背包'))
async def gacha_cangku(bot, ev: CQEvent):
    uid = ev.user_id
    shop = shopnew()
    msg = '\n'
    for a in shop_yule:
        name1 = shop_yule.get(a) #获取名称
        have1 = shop._get_sysnum(0,uid,a)
        msg += f'{name1} {have1}个\n'

    await bot.send(ev,msg,at_sender=True)

@sv.on_fullmatch(('出售再来一井'))    #怀念旧功能公主连结抽卡所保留的指令，本来在大更新后删除的
async def buy(bot, ev: CQEvent):
    ck = chouka()
    shop = shangdian()
    uid = ev.user_id
    num = shop._get_daoju3(0,uid)
    coin = num*1250
    shop._set_daoju3(0,uid,0)
    ck._add_shitou(0,uid,coin)
    ck._reduce_shitou(0,0,coin)
    await bot.send(ev,f'出售完成，你持有“再来一井”{num}个，获得了 {coin}*喵喵石头')