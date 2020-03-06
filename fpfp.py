#! D:\python3\python
# -*- coding: utf-8 -*- 




import os
import sys
import time
from decimal import Decimal as 十进制
import copy
import re
import pdb

import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding=sys.stdout.encoding, errors='xmlcharrefreplace', line_buffering=True, write_through=False )


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
    def __init__(self):

        self.工作路径 = self.设置工作路径()
        self.规划文件 = self.检查规划文件()
        self.读取规划文件()
        """
        各变量读取后结构类似如下:
        self.配方文件 = r"D:\配方XXX\版本号0.18.XX.txt"
        self.生产目标 = { "穿甲弹匣":Decimal('1'), "红瓶":Decimal('0.33333'), ... ... }
        self.基础设备速度 = { "组装机":Decimal('0.75'), "炼油厂":Decimal('1'), ... ... }
        self.基础原料 = ["铁矿", "铜矿", ... ...]
        self.配方产能加成 = { "电路板":Decimal('1.4'), ... ... }
        self.配方加成后设备速度 = { "电路板":Decimal('8'),  ... ... }
        """
        self.可处理目标产品 = []
        self.配方 = {}
        self.配方对应设备 = {}
        """
        self.配方 = { "电路板" : { "电路板":十进制(2), "铁板":十进制(-2), "铜线":十进制(-6) }, ... ... }
        self.配方对应设备 = { "电路板":"组装机", ... ... }
        """
        self.检查配方文件()
        self.读取配方文件()
        self.检查目标产品是否可处理()

    def 设置工作路径(self):
        if not os.path.isdir(规划路径):
            报错退出(规划路径 + " 不存在")
        工作路径 = 规划路径
        os.chdir(工作路径)
        return(工作路径)

    def 检查规划文件(self):
        if not os.path.isfile(规划文件):
            报错退出(规划文件 + " 不存在")
        return(规划文件) 

    def 读取规划文件(self):
        """
        各变量读取后结构类似如下:
        self.配方文件 = r"D:\配方XXX\版本号0.18.XX.txt"
        self.生产目标 = { "穿甲弹匣"=Decimal('1'), "红瓶"=Decimal('0.33333'), ... ... }
        self.基础设备速度 = { "组装机"=Decimal('0.75'), "炼油厂"=Decimal('1'), ... ... }
        self.基础原料 = ["铁矿", "铜矿", ... ...]
        self.配方产能加成 = { "电路板"=Decimal('1.4'), ... ... }
        self.配方加成后设备速度 = { "电路板"=Decimal('8'),  ... ... }
        """
        self.配方文件 = r""
        self.生产目标 = {}
        self.基础设备速度 = {}
        self.基础原料 = []
        self.配方产能加成 = {}
        self.配方加成后设备速度 = {}
        类别切换器正则 = re.compile(r"""
                                        ^\[                      #行首第一个字符为'左方括号'
                                        (?!\s*\])                #然后直到下一个右方括号为止 不能全部是空白符
                                        ([^(\[|\])]+)            #方括号括起来的部分必须不能有额外的方括号本身
                                        \]\s*                    #然后接一个'右方括号'和若干空白符
                                        (\#.*)?$                 #最后注释部分出现0次或1次直到结束 
                                     """, re.VERBOSE)
        with open(self.规划文件, 'r', encoding='utf-8') as 基本数据文件:
            基本数据行 = 基本数据文件.readlines()
        try:
            当前设定类别 = ""
            for 行 in 基本数据行:
                当前行 = 行.strip()
                if 当前行:
                    try:
                        当前设定类别 = 类别切换器正则.match(当前行).group(1)
                        continue
                    except:
                        pass
                    if 当前设定类别 == "配方文件":
                        self.配方文件 = 当前行
                    elif 当前设定类别 == "基础原料":
                        self.基础原料.append(当前行.strip())
                    else:
                        (k,v) = 当前行.split("=")
                        k = k.strip()
                        v = v.strip()
                        try:
                            v = 十进制(v)
                        except:
                            pass
                        getattr(self, 当前设定类别)[k] = v
        except:
            #raise
            报错退出(self.规划文件 + " 的格式有问题 再对照原本的文件仔细检查一下")

    def 检查配方文件(self):
        #pdb.set_trace()
        if not os.path.isfile(self.配方文件):
            报错退出(self.配方文件 + " 不存在")

    def 读取配方文件(self):
        with open(self.配方文件, 'r', encoding='utf-8') as 配方文本:
            配方数据行s = 配方文本.readlines()

        try:
            for 行 in 配方数据行s:
                if 行.strip():
                    (配方所用设备, 配方内容) = 行.split(":")
                    配方所用设备 = 配方所用设备.strip()

                    (配方产品和名称, 配方原料和时间) = 配方内容.split("=")
                    配方产品和名称 = 配方产品和名称.split("@")
                    try:
                        配方名称 = 配方产品和名称[1]
                        配方产品 = 配方产品和名称[0].split("+")[:-1]
                    except:
                        配方名称 = 配方产品和名称[0].split("×")[0].strip()
                        配方产品 = 配方产品和名称[0].split("+")
                        self.可处理目标产品.append(配方名称)
                    self.配方[配方名称] = {}

                    for 产品和产量 in 配方产品:
                        (产品,产量) = 产品和产量.split("×")
                        self.配方[配方名称][产品.strip()] = 十进制(产量)

                    配方原料和时间 = 配方原料和时间.split("+")
                    时间 = 十进制(配方原料和时间.pop())
                    for 原料和耗量 in 配方原料和时间:
                        (原料,耗量) = 原料和耗量.split("×")
                        原料 = 原料.strip()
                        耗量 = 十进制(耗量) * 十进制(-1)
                        if 原料 in self.配方[配方名称]:
                            self.配方[配方名称][原料] = self.配方[配方名称][原料] + 耗量
                        else:
                            self.配方[配方名称][原料] = 耗量

                    for 产品或原料 in self.配方[配方名称].keys():
                        try:
                            配方速度 = self.配方加成后设备速度[配方名称]
                        except:
                            配方速度 = self.基础设备速度[配方所用设备]

                        self.配方[配方名称][产品或原料] = self.配方[配方名称][产品或原料] / 时间 * 配方速度

                        if (配方名称 in self.配方产能加成) and (self.配方[配方名称][产品或原料] > 0) :
                            self.配方[配方名称][产品或原料] = self.配方[配方名称][产品或原料] * self.配方产能加成[配方名称]
                    self.配方对应设备[配方名称] = 配方所用设备
                    #if 配方名称 == "电路板":
                    #    pdb.set_trace()
        except:
            #raise
            报错退出(self.配方文件 + " 的格式有问题 再对照原本的文件仔细检查一下")

    def 检查目标产品是否可处理(self):
        for 目标产品 in self.生产目标.keys():
            if not (目标产品 in self.可处理目标产品):
                for 可处理产品 in self.可处理目标产品:
                    print(可处理产品)
                报错退出("--------------------------------\n仅可处理以上目标产品\n" + 目标产品 + " 不存在于其中")


class 量化计算:
    def __init__(self):
        """
        .各配方设备计数 = [ [电路板,组装机,十进制(1)], [穿甲弹匣, 组装机, 十进制(6)], ... ... ]
        .中间产物计数 = [ [铜丝,3], [铁板,1], ... ...    ]
        .基础原料计数 = [ [铁矿,1], [铜矿,1], ... ....     ]
        """
        self.各配方设备计数 = {}        
        self.中间产物计数 = {}
        self.基础原料计数 = {}
        self.特殊产品计数 = {}

        self.石化量化目标 = {"重油":十进制(0), "轻油":十进制(0), "石油气":十进制(0),}
        self.铀处理目标 = {}

    def 量化计算(self, 目标产品, 产量):
        #print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
        #print("目标产物 " + 目标产品)
        #print("设备计数 " + str(self.各配方设备计数))
        #print("产物计数 " + str(self.中间产物计数))
        #print("原料计数 " + str(self.基础原料计数))
        #print("TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT")
        #if 目标产品 = 铁板 : 
        #pdb.set_trace()
        if 目标产品 in 初始.基础原料:
            try:
                self.基础原料计数[目标产品] = self.基础原料计数[目标产品] + 产量
            except:
                self.基础原料计数[目标产品] = 产量
        elif not (目标产品 in 初始.配方):
            try:
                self.特殊产品计数[目标产品] = self.特殊产品计数[目标产品] + 产量
            except:
                self.特殊产品计数[目标产品] = 产量
        else:
            try:
                self.各配方设备计数[目标产品] = self.各配方设备计数[目标产品] + ( 产量 / 初始.配方[目标产品][目标产品] )
            except:
                self.各配方设备计数[目标产品] = 产量 / 初始.配方[目标产品][目标产品]
            try:
                self.中间产物计数[目标产品] = self.中间产物计数[目标产品] + 产量
            except:
                self.中间产物计数[目标产品] = 产量
            for (k,v) in 初始.配方[目标产品].items():
                if v < 0 :
                    原料 = k
                    耗量 = abs(v) * self.各配方设备计数[目标产品]
                    self.量化计算( 原料, 耗量 )
        #pdb.set_trace()

    def 特殊产品处理(self):
        石化开关 = 0
        铀处理产品 = ["铀238", "铀235"]
        铀处理开关 = 0 
        for key in self.特殊产品计数.keys():
            if key in self.石化量化目标:
                石化开关 = 1
                self.石化量化目标[key] = self.石化量化目标[key] + self.特殊产品计数[key]
        if 石化开关:
            self.石化量化计算()



    def 石化量化计算(self):
        多余重油 = 十进制(0)
        多余轻油 = 十进制(0)
        多余石油气 = 十进制(0)



        重油炼油厂数量 = self.石化量化目标["重油"] / 初始.配方["高阶原油处理"]["重油"]
        初始.配方["高阶原油处理"]["轻油"] * 







    def 显示内容(self):

        for (k,v) in 初始.生产目标.items():
            print("生产目标: 每秒 {0} 个 {1}".format(v,k))
        
        print("\n为达成以上目标 你需要: " )
        for key in self.各配方设备计数.keys():
            print("你需要 {0:.3f} 个 {1} 生产 {2}".format( self.各配方设备计数[key], 初始.配方对应设备[key], key ))

        print("\n各产品生成状况如下: ")
        for key in self.中间产物计数.keys():
            print("每秒钟会有 {0:.3f} 个 {1} 生成".format( self.中间产物计数[key], key ))

        print("\n基础原料消耗状况如下: ")
        for key in self.基础原料计数.keys():
            print("每秒钟会有 {0:.3f} 个 {1} 被消耗".format( self.基础原料计数[key], key ))













        #初始.配方[目标产品]










































def 命令参数预处理():
    脚本路径和脚本名称 = os.path.split(os.path.abspath(sys.argv[0]))
    脚本路径 = 脚本路径和脚本名称[0]
    脚本名称 = 脚本路径和脚本名称[1]
    try:
        命令参数 = sys.argv[1:]
        规划文件 = 命令参数[0]
    except:
        规划文件 = r"默认规划.txt"
    try:
        规划路径 = os.path.split(os.path.abspath(os.path.normpath(规划文件)))[0]
        规划文件 = os.path.split(os.path.abspath(os.path.normpath(规划文件)))[1]
    except:
        报错退出(规划文件 + "出错了")
    return([脚本路径,脚本名称,规划路径,规划文件])




if __name__ == '__main__':
    (脚本路径,脚本名称,规划路径,规划文件) = 命令参数预处理()
    现在时间 = time.strftime("%y%m%d %H:%M:%S", time.localtime(time.time()))
    print(规划路径)
    初始 = 初始化()
    print("--------------------------------------------------------------------")
    #print(初始.配方文件)
    #print(初始.生产目标)
    #print(初始.基础设备速度)
    #print(初始.基础原料)
    #print(初始.配方产能加成)
    #print(初始.配方加成后设备速度)
    #print(初始.配方对应设备)
    ##print("--------------------------------------------------------------------")
    #for k,v in 初始.配方对应设备.items():
    #    print(k)
    #    print(v)
    #    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
    规划 = 量化计算()
    #print(初始.生产目标)
    for (k,v) in 初始.生产目标.items():
        规划.量化计算(k, v)

    规划.特殊产品处理()

    #print(规划.各配方设备计数)
    print("-----------------------------------------------------------------------")
    规划.显示内容()




