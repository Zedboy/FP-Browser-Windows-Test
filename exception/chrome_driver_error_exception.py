class ChromeDriverErrorException(Exception):
    def __init__(self):
        self.msg = 'Chrome 驱动未找到'

    def __str__(self):
        return self.msg
