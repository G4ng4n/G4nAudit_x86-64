from Config import BaseConfig, FuncConfig, ArchConfig

def test_base_config():
    c = BaseConfig()
    print(c.banner())

def test_func_info_config(arch):
    c = FuncConfig(arch)
    # clist = c.get_func_by_name("fun")
    clist = c.get_func_by_name("fun")
    for i in clist:
        print(str(i))


if __name__ == "__main__":
    test_base_config()
    test_func_info_config('x86-64')