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
        self.生产目标 = { "穿甲弹匣"=Decimal('1'), "红瓶"=Decimal('0.33333'), ... ... }
        self.基础设备速度 = { "组装机"=Decimal('0.75'), "炼油厂"=Decimal('1'), ... ... }
        self.基础原料 = ["铁矿", "铜矿", ... ...]
        self.配方产能加成 = { "电路板"=Decimal('1.4'), ... ... }
        self.配方加成后设备速度 = { "电路板"=Decimal('8'),  ... ... }
        """
        self.读取配方文件()



        
        pass


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
                                        ^\[                      #行首第一个字符为'左方括号''
                                        ([^(\[|\]|\s)]+)            #方括号括起来的部分必须有非空白字符且不能有额外的方括号本身
                                        +\]\s*                   #然后接一个'右方括号'和若干空白符
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
                    if 当前设定类别 == "生产目标":
                        (目标产品,目标产量) = 当前行.split("=")
                        self.生产目标[目标产品.strip()] = 十进制(目标产量)
                    if 当前设定类别 == "基础设备速度":
                        (设备类型,设备速度) = 当前行.split("=")
                        self.基础设备速度[设备类型.strip()] = 十进制(设备速度)
                    if 当前设定类别 == "基础原料":
                        self.基础原料.append(当前行.strip())
                    if 当前设定类别 == "配方产能加成":
                        (配方名,产能加成) = 当前行.split("=")
                        self.配方产能加成[配方名.strip()] = 十进制(产能加成)
                    if 当前设定类别 == "配方加成后设备速度":
                        (配方名,配方速度) = 当前行.split("=")
                        self.配方加成后设备速度[配方名.strip()] = 十进制(配方速度)
        except:
            raise
            #报错退出(self.规划文件 + " 的格式有问题 再对照原本的文件仔细检查一下")

    def 读取配方文件():
        
        pass















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
    a = 命令参数预处理()
    脚本路径 = a[0]
    脚本名称 = a[1]
    规划路径 = a[2]
    规划文件 = a[3]
    现在时间 = time.strftime("%y%m%d %H:%M:%S", time.localtime(time.time()))
    初始 = 初始化()
    print("--------------------------------------------------------------------")
    print(初始.配方文件)
    print(初始.生产目标)
    print(初始.基础设备速度)
    print(初始.基础原料)
    print(初始.配方产能加成)
    print(初始.配方加成后设备速度)
    print("--------------------------------------------------------------------")




