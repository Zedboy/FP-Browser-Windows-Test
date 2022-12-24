import sys
import os
from exception.chrome_driver_error_exception import ChromeDriverErrorException
from helper.aes import AESLibrary
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options as ChromeOptions


class Driver(object):
    @staticmethod
    def get_chrome_driver(version):
        """
        获得 chrome 驱动路径
        """
        platform = sys.platform
        dir = r'./drives/' + version
        if os.path.isdir(dir):
            if platform.startswith('win32'):
                path = dir + '/chromedriver.exe'
            elif platform.startswith('darwin'):
                # 这里直接引用实时编译好了的路径
                path = dir + '/chromedriver_mac64'  # 官方的
            else:
                path = dir + '/chromedriver_linux64'

            return os.path.abspath(path)
        else:
            raise ChromeDriverErrorException()

    @staticmethod
    def get_chromium_binary_executable_path(version, force_chrome_binary_location):
        """
        获得浏览器可执行目录
        """
        if force_chrome_binary_location and force_chrome_binary_location != "":
            return force_chrome_binary_location

        return os.path.realpath("chrome/{}/chrome.exe".format(version))

    @staticmethod
    def handle(driver_version, chrome_version, config, chrome_port, encrypt, force_chrome_binary_location=None,
               default_option_prefix="default-option"):
        """
        获得 driver 对象
        """
        settings_json = AESLibrary.format_chrome_driver_options(
            settions=config, default_option_prefix=default_option_prefix, encrypt=encrypt
        )

        chrome_agrs = [
            "--disable-popup-blocking",
            "--ignore-certificate-errors",
            "--ignore-ssl-errors",
            "--disable-web-security",
            "--disable-build-check",
            "--enable-logging",
            "--v=1",
            "--disable-dev-shm-usage",
            "--no-first-run",
            '--chrome-custom-settings-json={}'.format(settings_json),
        ]

        service = Service(executable_path=Driver.get_chrome_driver(driver_version))

        options = ChromeOptions()
        options.binary_location = Driver.get_chromium_binary_executable_path(chrome_version,
                                                                             force_chrome_binary_location)

        options.page_load_strategy = 'normal'
        options.add_experimental_option('excludeSwitches', ['enable-automation'])

        for arg in chrome_agrs:
            options.add_argument(arg)

        driver = webdriver.Chrome(
            service=service,
            port=chrome_port,
            options=options,
        )

        driver.set_page_load_timeout(15)
        driver.implicitly_wait(15)

        return driver
