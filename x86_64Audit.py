# import idc
import json
from audit_config import *

__func = None

# IN    None
# RET   None
# Load function info from json, read more at audit_config.py
# call when this plugin start
def get_audit_func():
    with open(AUDIT_FUNC_JSON) as f_j:
        print("Open json file at ", AUDIT_FUNC_JSON)
        __func = json.load(f_j)
        if DEBUG:
            print(__func['debug'])
        print(BANNER)
        return True
    return False
        

# IN    Function name
# RET   whether audit() call successful
# core function, audit a function
def audit(func_name):
    func_addr = get_func_addr(func_name)
    if not func_addr:
        return False

    if func_name in __func['one_arg_function']:
        arg_num = 1
    elif func_name in __func['two_arg_function']:
        arg_num = 2
    elif func_name in __func['three_arg_function']:
        arg_num = 3
    elif func_name in __func['format_function_offset_dict']:
        arg_num =  __func['format_function_offset_dict'][func_name] + 1
    else:
        print("The %s function didn't write in the describe arg num of function array,please add it to,such as add to `two_arg_function` arary" % func_name)
        return

def get_func_addr(func_name):
    addr = idc.get_name_ea_simple(func_name)
    if DEBUG:
        print("addr of " + func_name + ": ", addr)
    if addr != BADADDR:
        print('\n'.ljust(41, '*') + func_name.ljust(40, '*') + '\n')
        return addr
    return False


if __name__ == "__main__":
    get_audit_func()
