class ConfigErrorException(Exception):
    def __init__(self):
        self.msg = '配置文件不存在'

    def __str__(self):
        return self.msg