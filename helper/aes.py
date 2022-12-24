from Crypto.Cipher import AES
import base64
import json
from helper.base64_util import base64_encode, base64_decode


class AESLibrary(object):
    def __init__(self):
        self.key = b"bSmT4152SKC1XBhjpxZ446c1L0e5IGEf"
        self.iv = b"PoYF83GyaZryX9rT"

    @staticmethod
    def to_string(encrypt_data):
        """
        格式化成 base64 字符串
        """
        return base64.b64encode(encrypt_data).decode("utf8")

    def encrypt(self, context):
        """
        加密
        """
        bs = AES.block_size
        pad = lambda s: s + (bs - len(s) % bs) * chr(bs - len(s) % bs)
        encryption_suite = AES.new(self.key, AES.MODE_CBC, self.iv)
        return encryption_suite.encrypt(bytes(pad(context), 'utf-8'))

    def decrypt(self, cipher_text):
        """
        解密
        """
        decryption_suite = AES.new(self.key, AES.MODE_CBC, self.iv)
        return decryption_suite.decrypt(bytes(cipher_text, 'utf-8')).decode()

    @staticmethod
    def format_chrome_driver_options2(dict):
        """
        重新组合配置 dict
        """
        params = []

        for (key, item) in dict.items():
            params.append('--{0}={1}'.format(key, item))
        return params

    @staticmethod
    def format_chrome_driver_options(settions: dict, default_option_prefix: str, encrypt=True):
        """
        重新组合配置 dict
        """
        if encrypt is False:
            return AESLibrary.format_chrome_driver_options2(settions)

        params = []

        result = []
        ensure_ascii = True
        for (key, item) in settions.items():
            # 强制把数字类型转成字符串
            if isinstance(item, (int, float)):
                item = str(item)
            elif isinstance(item, (list, dict)):
                # 如果是 list 或者 dict，则先转换成 json
                if isinstance(item, list) and len(item) == 0:
                    item = ""
                elif isinstance(item, dict) and len(item.keys()) == 0:
                    item = ""
                else:
                    item = json.dumps(item, ensure_ascii=ensure_ascii)

            # 全部 base64，防止中文乱码
            if item and item != "":
                item = base64_encode(item)

            result.append({
                "name": "{}-{}".format(default_option_prefix, key),
                "value": item
            })
            pass

        cipher_text = AESLibrary().encrypt(json.dumps(result, ensure_ascii=ensure_ascii))

        return AESLibrary.to_string(cipher_text)
