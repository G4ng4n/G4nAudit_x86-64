import lief

class FileInfo():

    __filepath = ''
    __procname = ''
    __bits = 0
    __fileobj = None

    def __init__(self):
        self.__filepath = get_input_file_path()
        self.__info = get_inf_structure()
        self.__procname = self.__info.procName
        self.__bits = 64 if self.__info.is_64bit() else (32 if self.__info.is_32bit() else 16)
        self.__parse()

    def __str__(self):
        head = "FileInfo:\n"
        head += "file path: " + str(self.__filepath) + '\n'
        head += "bits of executable file: " + str(self.__bits) + '\n'
        head += "processor name: " + str(self.__procname) + '\n'
        return head

    def get_filepath(self):
        return self.__filepath
    
    def get_procname(self):
        return self.__procname

    def get_bits(self):
        return self.__bits

    def __parse(self):
        self.__fileobj = lief.parse(self.__filepath)
    
    def get_fileobj(self):
        return self.__fileobj