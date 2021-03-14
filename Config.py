'''
所有的config相关类信息都是从配置文件中读取
读取解析通过ConfigParse类实现
配置文件统一固定保存在插件所在目录的./config_json/下（或者修改此文件）
'''

import json
from pyfiglet import figlet_format

'''
解析目录下的配置文件，该类应当只被该文件下的需要读取配置文件的类所调用
构造方法传入文件名
使用data()方法返回已经解析的数据
'''
class ConfigParse():
    __data = None

    def __init__(self, filename):
        filepath = "./config_json/" + filename
        with open(filepath, 'r') as f:
            self.__data = json.load(f)
    
    def data(self):
        return self.__data

'''
解析插件设置
debug()返回布尔值，表示是否开启调试信息输出
banner()返回打印的banner信息
'''
class BaseConfig():
    __BANNER = ""
    __DEBUG_MOD = True
    __data = None

    def __init__(self):
        self.__data = ConfigParse("base_config.json").data()
        self.__BANNER = self.__data['BANNER']
        self.__DEBUG_MODE = self.__data['DEBUG_MODE']

    def __str__(self):
        s = "DEBUG_MODE : " + ('On' if self.debug() else "Off")
        s += '\n' + self.banner + '\n'
        return s

    def debug(self):
        return self.__DEBUG_MODE

    def banner(self):
        return figlet_format(self.__BANNER['content'], font=self.__BANNER['font'])

'''
插件本次解析文件采用的架构信息
构造方法传入架构名
get_arg_area()返回参数位置（内存/寄存器）
get_arg()返回参数符号列表，可传入数字指定返回第n个参数符号
'''
class ArchConfig():
    
    __data = None
    __arch = None
    __args_list = None
    __arg_area = None

    def __init__(self, arch):
        self.__data = ConfigParse("arch_config.json").data()
        if arch.lower() in ['x86', 'i386', '86']:
            self.__arch = 'x86'
        elif arch.lower() in ['x86-64', 'x86_64']:
            self.__arch = 'x86_64'
        else:
            self.__arch = arch
        self.__arg_area, self.__args_list = self.__data[self.__arch]["arg_area"], self.__data[self.__arch]["args"]

    def get_arg_area(self):
        return self.__arg_area
    
    def get_arg(self, num=-1):
        if num < 0:
            return self.__args_list
        else :
            return self.__args_list[num]

'''
待审计的函数信息
构造方法传入arch（暂时为可选参数）
get_func_by_name()返回名字中包含了指定字符串的的函数列表（如print返回printf,sprintf等），子串匹配
get_func_by_tag()返回tag成员含有指定字符串对应tag的函数列表（如fmt_str返回所有标签带fmt_str的函数，但fmt不会返回任何函数，因为标签名不使用子串匹配）
内部类FuncInfo：
    用于提供方便使用的函数信息集合，是get_func_by_name()和get_func_by_tag()所返回列表的成员类型
    构造方法中，arch为可选参数（暂时这么定义），设置了arch后，str(FuncInfo)时会输出参数设置的名称和对应的参数位置符号名称
    上述设计用于将常规定的函数参数名称与寄存器、内存对应。如x86_64下，printf的第一个参数会打印显示为 [rdi] format
'''
class FuncConfig():
    
    __data = None
    __func_list = []

    # 对外部使用此结构描述函数
    class FuncInfo():
        # 由json中导出的FUNC下属成员描述
        name = ''
        tag = []
        argc = -1
        argv = None
        __parsed_argv = None
        comment = ''

        def __init__(self, func, *arch):
            func = func[1]
            self.name = func['name']
            self.tag = func['tag']
            self.argv = func['argv']
            self.argc = func['argc']
            self.comment = func['comment']

            if arch != ():
                self.__parsed_argv = {}
                self.__parse_func_arg_by_arch(arch)

        def __str__(self):
            # function name
            info = ''
            info += '\nfunction name :\t' + self.name

            # function tag
            a=''
            for i in self.tag:
                a += i + ', '
            a = a[:-2] + '\n'
            info += '\nfunction tag :\t' + a

            # function argc
            info += 'function argc :\t' + str(self.argc)

            # function argv, argv can be None
            a = ''
            if self.__parsed_argv is not None:
                for i in self.__parsed_argv :
                    a += "[{}]".format(self.__parsed_argv[i])
                    a += " {}".format(i)
                    a += ", "
                a = a[:-2]
                info += '\nfunction argv name :\t' + a
            else:
                if self.argv is not None:
                    for i in self.argv:
                        a += i + ', ' 
                    a = a[:-2]
                    info += '\nfunction argv name :\t' + a
                else:
                    info += "\nfunction argv name :\t No argv in this function"
            # function comment
            info += '\nfunction comment :\t' + self.comment
            info += '\n'

            return info

        def __parse_func_arg_by_arch(self, arch):
            arch = arch[0][0]
            c = ArchConfig(arch)
            if self.argv is not None:
                for i in range(self.argc):
                    self.__parsed_argv[self.argv[i]] = c.get_arg(i)

    def __init__(self, *arch):
        self.__data = ConfigParse("func_config.json").data()
        for i in self.__data['FUNC'].items():
            if arch == ():
                self.__func_list.append(self.FuncInfo(i))
            else:
                self.__func_list.append(self.FuncInfo(i, arch))

    # 返回FuncInfo的列表

    def get_func_by_name(self, func_name):
        ret_list = []
        for i in self.__func_list : 
            if func_name in i.name:
                ret_list.append(i)
        return ret_list

    def get_func_by_tag(self, tag):
        ret_list = []
        for i in self.__func_list:
            # argv might be None!
            if i.tag is not None and tag in i.tag:
                ret_list.append(i)
                continue
        return ret_list

