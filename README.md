# 商店、银行、签到
注意：功能只适用于HoshinoBot，并未在NoneBot和NoneBot2中进行测试！

## 简介
这是一个附属功能，其中包含了商店购买、银行存取借还、签到功能，购买的道具可以使用于[猜数字](https://github.com/daycold1000/caishuzi)、[csgo开箱](https://github.com/daycold1000/csgo-nb)等娱乐功能

## 指令
签到 （就是签到）

go升级 （签到获得经验值用来升级，升级到一定等级可获得  本系列功能  的csgo道具）

旧道具商店（可以购买猜数字玩法的道具）

买XXY个（例子：买一眼看穿10个）（在旧道具商店里购买道具的指令）

我的背包（查看旧道具商店的道具持有数）

道具商店 娱乐（注意空格）（可以购买csgo开箱玩法的道具）

购买XXY个（例子：购买钥匙10个）（在道具商店里购买道具指令）

娱乐背包（查看道具商店的道具持有数）

看看银行（查看银行今日盈亏和剩余货币数量）

存、取、借、还XX石（XX为数字）（与银行交互用的指令）

我的卡（查看自己还有多少货币）

## 部署教程：
1.下载或git clone本插件：

在 HoshinoBot\hoshino\modules 目录下使用以下命令拉取本项目

git clone https://github.com/daycold1000/miaoshop

2.启用：

在 HoshinoBot\hoshino\config\ **bot**.py 文件的 MODULES_ON 加入 'miaoshop'

然后重启 HoshinoBot

## 多余的代码
功能是以我的机器人为主编写的，一些代码为旧版本更新后失效所保留下来的代码

这些代码我均在本次上传时进行了备注，如果能读代码的话，你可以去感受作者这菜只因般的代码水平...
