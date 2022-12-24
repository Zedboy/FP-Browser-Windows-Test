import json

import numpy
import pytest
from helper.util import get_driver, sleep, split_cookie, stop_browser_app
from urllib.parse import urlparse
from fp_browser_sdk.ext.header import Cookie, Header
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings
from fp_browser_sdk.ext.browser_enum import CookieSameSite, MatchType


class TestCookie(object):
    def setup_method(self):
        stop_browser_app()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [True, False])
    def test_status(self, value):
        """
        测试 是否开启 cookie 「1：true; 0：false」
        """
        settings = FPBrowserSettings()

        header = Header() \
            .set_cookie_status(value)

        settings.add_module(header)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return navigator.cookieEnabled
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = int(self.config.get('cookie.status')) == 1

        print("设置 是否开启 cookie 「1：true; 0：false」:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    def test_cookie(self):
        """
        测试 注入 Cookie 值
        """
        settings = FPBrowserSettings()

        header = Header() \
            .append_cookie(Cookie().set_domain(".so.com").set_name("name2").set_value("aaaaa2").set_port("80").set_same_site(
                CookieSameSite.NO_RESTRICTION).set_secure(True)) \
            .append_cookie(Cookie().set_domain(".so.com").set_name("name3").set_value("aaaaa3").set_port("80").set_same_site(
                CookieSameSite.NO_RESTRICTION).set_secure(True)) \
            .append_cookie(Cookie().set_domain(".so.com").set_name("从").set_value("哪里").set_port("80").set_same_site(
                CookieSameSite.NO_RESTRICTION).set_secure(True)) \
            .append_cookie(Cookie().set_domain(".sm.cn").set_name("从").set_value("哪里").set_port("80").set_same_site(
                CookieSameSite.NO_RESTRICTION).set_secure(True))

        settings.add_module(header)

        driver, config = get_driver(custom_url="https://m.so.com", custom_config=settings.parse(),
                                    only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return document.cookie
               }
               return func();
           '''
        value = split_cookie(self.driver.execute_script(script))
        setting_value = self.config.get('cookie.json')

        print("设置 注入 Cookie 值:")
        print(value)
        print(setting_value)
        for item in setting_value:
            # 手动判断
            if item['domain'].find('so.com') >= 0:
                assert item['value'] == value[item['name']]

        self.driver.close()
        self.driver.quit()
