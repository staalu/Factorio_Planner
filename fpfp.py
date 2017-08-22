#! D:\python36\python3
# -*- coding: utf-8 -*- 




import os
import sys
import time
from decimal import Decimal as 十进制
import copy
import pdb

import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=sys.stdout.encoding, errors='xmlcharrefreplace')


class 出错文本:
    错误0 = """
    不知道哪里出错啦 总之是出错啦
    """
出错 = 出错文本()

def 暂停(显示=""):
    if not 显示:
        显示 = "要继续就按回车哦"
    print(显示)
    input("")

def 退出程序(code=1):
    暂停("按回車退出")
    os._exit(code)

def 报错退出(报错文本=出错.错误0):
    print(报错文本)
    退出程序()



class 初始化:
    """
    初始化类
    """
    工作路径 = r""
    游戏数据路径 = r""
    基本数据文件 = r""
    生产配方文件 = r""

    传送带运力 = {}
    管道运输流体 = []
    设备速度 = {}
    生产方案 = {}
    基础原料 = []
    生产配方列表 = []

    def __init__(self):
        """開始初始化"""
        self.设置工作路径()
        self.检查游戏数据路径()
        self.检查游戏数据文件()
        self.读取基本数据()
        self.读取生产配方()
        print("++++++++++++++++++++++++++++\n" + 现在时间 + "\n初始化完成\n\n")

    def 设置工作路径(self):
        """设置当前工作路径到脚本文件所在路径 self.工作路径"""
        self.工作路径 = 脚本路径和脚本名称[0]
        os.chdir(self.工作路径)

    def 检查游戏数据路径(self):
        """检查游戏数据文件夹是否存在"""
        self.游戏数据路径 = os.path.abspath(执行参数)
        if not os.path.isdir(self.游戏数据路径):
            报错退出( 报错文本 = "找不到 " + self.游戏数据路径 )

    def 检查游戏数据文件(self):
        """生产配方.txt 和 基本数据.txt"""
        self.基本数据文件 = r"基本数据.txt"
        self.生产配方文件 = r"生产配方.txt"
        self.基本数据文件 = os.path.join(self.游戏数据路径 , self.基本数据文件)
        self.生产配方文件 = os.path.join(self.游戏数据路径 , self.生产配方文件)
        if not os.path.isfile(self.生产配方文件):
            报错退出( 报错文本 = "找不到 " + self.基本数据文件 )
        if not os.path.isfile(self.生产配方文件):
            报错退出( 报错文本 = "找不到 " + self.生产配方文件 )

    def 读取基本数据(self):
        with open(self.基本数据文件, 'r', encoding='utf-8') as 基本数据文件:
            基本数据行 = 基本数据文件.readlines()

        传送带运力 = {}
        管道运输流体 = []
        设备速度 = {}
        生产方案 = {}
        基础原料 = []

        try:
            for 行 in 基本数据行:
                if 行[0] == "!" and len(行) > 1 :
                    当前类别 = 行[1:-1].strip()
                elif 行.strip() and 当前类别 == "传送带运力":
                    分割行 = 行.split("=")
                    locals()[当前类别][分割行[0].strip()] = 十进制(分割行[1].strip())
                elif 行.strip() and 当前类别 == "管道运输流体":
                    locals()[当前类别].append(行.strip())
                elif 行.strip() and 当前类别 == "设备速度":
                    分割行 = 行.split("=")
                    locals()[当前类别][分割行[0].strip()] = 十进制(分割行[1].strip())
                elif 行.strip() and 当前类别 == "生产方案":
                    分割行 = 行.split("@")
                    locals()[当前类别][分割行[0].strip()] = 分割行[1].strip()
                elif 行.strip() and 当前类别 == "基础原料":
                    locals()[当前类别].append(行.strip())
            
            半条传送带运力 = []
            for 传送带类型 in 传送带运力.keys():
                半条传送带运力.append(["半条" + 传送带类型 ,传送带运力[传送带类型] / 2])
            for 半条传送带类型 in 半条传送带运力:
                传送带运力[半条传送带类型[0]] = 半条传送带类型[1]

            传送带运力 = list(传送带运力.items())
            def 按速度排序(元素):
                return 元素[1]
            传送带运力 = sorted(传送带运力,key=按速度排序)

            self.传送带运力 = 传送带运力
            self.管道运输流体 = 管道运输流体
            self.设备速度 = 设备速度
            self.生产方案 = 生产方案
            self.基础原料 = 基础原料
        except:
            报错退出(self.基本数据文件 + " 的格式有问题 再对照原本的文件仔细检查一下吧")

    def 读取生产配方(self):
        with open(self.生产配方文件, 'r', encoding='utf-8') as 生产配方文件:
            生产配方行 = 生产配方文件.readlines()
        try:
            for 行 in 生产配方行:
                if 行.strip():
                    self.处理生产配方行(行)
        except:
            报错退出(self.生产配方文件 + " 的格式有问题 再对照原本的文件仔细检查一下吧")

    def 处理生产配方行( self, 行字串 ):
        配方 = []

        分割配方行 = 行字串.split(":")
        生产设备 = 分割配方行[0].strip()
        配方.append(生产设备)

        分割配方 = 分割配方行[1].split("=")
        产品部分 = 分割配方[0].strip()
        材料部分 = 分割配方[1].strip()

        分割材料部分 = 材料部分.split("+")
        配方生产时间 = 十进制(分割材料部分.pop())
        材料s = {}
        for 材料 in 分割材料部分:
            分割材料名和数量 = 材料.split("×")
            材料s[分割材料名和数量[0].strip()] = 十进制(分割材料名和数量[1])

        生产方案 = ""
        分割产品部分 = 产品部分.split("+")
        if 分割产品部分[-1].strip()[0] == "@":
            生产方案 = 分割产品部分.pop().strip()
            生产方案 = 生产方案.replace( "@", "at" )
        
        产品s = {}
        产品s2 = {}
        for 产品 in 分割产品部分:
            分割产品名和数量 = 产品.split("×")
            产品s[分割产品名和数量[0].strip()] = 十进制(分割产品名和数量[1])
        产品s2 = copy.deepcopy(产品s)
        for 产品 in 产品s.keys():                             #这里用来处理产品本身同时也是催化剂存在于材料中的状况 比如铀增值处理这个配方
            if 产品 in 材料s.keys():
                增值还是消耗 = 产品s2[产品] - 材料s[产品]
                if 增值还是消耗 == 0:
                    del 产品s2[产品]
                    del 材料s[产品]
                elif 增值还是消耗 > 0:
                    产品s2[产品] = 增值还是消耗
                    del 材料s[产品]
                elif 增值还是消耗 < 0:
                    del 产品s2[产品]
                    材料s[产品] = abs(增值还是消耗)
        配方.append(材料s)
        配方.append(配方生产时间)
        for 产品 in 产品s2.keys():
            产品at生产方案 = 产品
            if 产品 in self.生产方案.keys():
                产品at生产方案 = 产品 + 生产方案
            配方对象数据源 = copy.deepcopy(配方)
            配方对象数据源.insert(1,[产品at生产方案,产品s2[产品]])
            self.生产配方列表.append(配方对象数据源)



class 单位时间配方条目类:
    """ 单位为 每个生产设备每秒 """

    def __init__( self, 数据源 , 设备速度 ):

        设备 = 数据源[0]
        特定设备速度 = 初始.设备速度[设备]
        配方时间 = 数据源[3]

        self.产品 = 数据源[1][0]
        self.产量 = self.计算每秒量( 数据源[1][1], 配方时间, 特定设备速度 )

        材料字典 = 数据源[2]

        for 材料名 in 材料字典:
            配方材料消耗 = 材料字典[材料名]
            每秒耗材量 = self.计算每秒量(配方材料消耗, 配方时间, 特定设备速度)
            材料字典[材料名] = 每秒耗材量

        self.材料字典 = 材料字典
        self.生产设备 = 设备

    def 计算每秒量(self, 配方产量, 配方时间, 设备速度):
        每秒每设备产量 = 设备速度*(配方产量/配方时间)
        return 每秒每设备产量



class 生产规划:
    """生产规划计划"""
    def __init__(self, 目标产品, 目标产量):
        self.设备类别数量={}
        self.基础原料数量={}
        self.中间产物数量={}
        self.目标产量加成计算(目标产品, 目标产量)
        pass

    def 目标产量加成计算(self, 目标产品, 目标产量):

        if 目标产品 in 初始.生产方案.keys():
            目标产品 = 目标产品 + "at" + 初始.生产方案[目标产品]

        原始产品配方 = eval(目标产品)
        目标产品配方 = copy.deepcopy(eval(目标产品))

        目标产品配方.产量 = 目标产量
        产品名称 = 目标产品配方.产品
        产品产量 = 目标产品配方.产量
        改字典 = self.字典记录更动值(self.中间产物数量,产品名称 ,产品产量 )
        
        所需设备数量 = 目标产量 / 原始产品配方.产量

        设备类别名称 = 目标产品配方.生产设备 + " 生产 " + 产品名称
        改字典 = self.字典记录更动值(self.设备类别数量,设备类别名称 ,所需设备数量 )

        for 材料名 in 目标产品配方.材料字典.keys():
            目标产品配方.材料字典[材料名] = 原始产品配方.材料字典[材料名] * 所需设备数量
            if not 材料名.split("at")[0] in 初始.基础原料:
                self.目标产量加成计算( 材料名, 目标产品配方.材料字典[材料名] )
            else:
                基础原料名称 = 材料名.split("at")[0]
                基础原料数量 = 目标产品配方.材料字典[材料名]
                改字典 = self.字典记录更动值(self.基础原料数量,基础原料名称 ,基础原料数量 )
                pass

    def 字典记录更动值(self,传入字典,传入key,传入数据):
        if not 传入key in 传入字典.keys():
            传入字典[传入key] = 传入数据
        else:
            传入字典[传入key] = 传入字典[传入key] + 传入数据



def 输入目标产品(期望输入值列表):
    目标产品 = input("请输入你期望的最终产品: ")
    if not 目标产品 in 期望输入值列表:
        print("生产配方文件中并没有记录这种产品的配方喔!\n请在以下产品中选择一种重新输入\n")
        期望输入s = ""
        for 期望输入 in 期望输入值列表:
            期望输入s = 期望输入s + 期望输入 + " "
        print(期望输入s)
        print("\n")
        目标产品 = 输入目标产品(期望输入值列表)
        return 目标产品
    else:
        return 目标产品


def 输入目标产量():
    目标产量 = input("请输入你期望的每秒产量(可以是小数): ")
    try:
        return 十进制(目标产量)
    except:
        print("你输入的不是一个数字!!,请重新输入!\n")
        return 输入目标产量()






if __name__ == '__main__':
    脚本路径和脚本名称 = os.path.split(os.path.abspath(sys.argv[0]))
    执行参数 = r"gamedata\0.15.31"
    try:
        执行参数 = sys.argv[1]
    except:
    	pass
    现在时间 = time.strftime("%y%m%d %H:%M:%S", time.localtime(time.time()))

    初始 = 初始化()
    期望输入值列表 = []
    for 配方 in 初始.生产配方列表:
        locals()[配方[1][0]] = 单位时间配方条目类(配方, 初始.设备速度)
        期望输入 = 配方[1][0].split("at")[0]
        期望输入值列表.append(期望输入)

    while True:
        目标产品 = 输入目标产品(期望输入值列表)
        目标产量 = 输入目标产量()

        规划 = 生产规划(目标产品, 目标产量)

        print("你需要: \n")

        for (生产设备,设备数量) in 规划.设备类别数量.items():
            print("{0:.3f} 个 {1}".format(设备数量,生产设备))
        print("")

        for (基础原料,原料数量) in 规划.基础原料数量.items():
            超运力字段 = ""
            for (传送带类型,此类型的速度) in 初始.传送带运力:
                if 原料数量 > 此类型的速度:
                    超运力字段 = "    这已经超过 {0} 的运力".format(传送带类型)
            if 基础原料.split("at")[0] in 初始.管道运输流体:
                超运力字段 = ""
            print("每秒钟会有 {0:.3f} 单位的 {1} 被消耗".format(原料数量,基础原料) + 超运力字段)
        print("")

        for (产物名称,产物数量) in 规划.中间产物数量.items():
            超运力字段 = ""
            for (传送带类型,此类型的速度) in 初始.传送带运力:
                if 产物数量 > 此类型的速度:
                    超运力字段 = "    这已经超过 {0} 的运力".format(传送带类型)
            if 基础原料.split("at")[0] in 初始.管道运输流体:
                超运力字段 = ""
            print("每秒钟会有 {0:.3f} 单位的 {1} 生成".format(产物数量,产物名称) + 超运力字段)
        print("")








