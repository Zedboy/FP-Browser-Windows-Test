import pytest
from helper.util import get_driver, sleep, wait_el
import json
from fp_browser_sdk.ext.basic import Basic
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings
from fp_browser_sdk.ext.inject_js import InjectJS
from selenium.webdriver.common.by import By
from helper.cdp import loop_find_element, click_ele


class TestInjectJs(object):

    # @pytest.mark.skip()
    def test_inject_js(self):
        """
        测试 注入 js
        """
        settings = FPBrowserSettings()

        driver, config = get_driver(custom_url="https://tyua07.github.io/FP-Browser-Test/check_inject_js.html",
                                    custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return document.title;
               }
               return func();
           '''
        value = self.driver.execute_script(script)

        print("注入 js：", value)
        assert value == "xxxxxxx"
        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    def test_inject_js2(self):
        """
        测试 注入 js
        """
        settings = FPBrowserSettings()

        basic = Basic() \
            .set_inject_js(InjectJS().append_load_event("(function(){"
                                                        "document.title = '\u4f60\u597d\u5417';"
                                                        "})()"))

        settings.add_module(basic)

        driver, config = get_driver(custom_url="https://tyua07.github.io/FP-Browser-Test/check_inject_js_2.html",
                                    custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config
        script = '''
               function func(el)
               {
                  return document.title;
               }
               return func();
           '''
        value = self.driver.execute_script(script)

        print("注入 js：", value)
        assert value == "你好吗"
        sleep(10)
        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    def test_inject_js3(self):
        """
        测试 注入 js
        """
        settings = FPBrowserSettings()

        basic = Basic() \
            .set_inject_js(InjectJS().append_load_event("(function(){"
                                                        "document.title = 'test_inject_js3 sajsaj撒撒娇 099！！2';"
                                                        "})()"))

        settings.add_module(basic)

        driver, config = get_driver(custom_url="https://tyua07.github.io/FP-Browser-Test/check_inject_js_3.html",
                                    custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        document = self.driver.execute_cdp_cmd("DOM.getDocument", {})
        a = loop_find_element(driver=self.driver, selector="a", node_id=document)

        # 需要判断元素是否存在
        assert a is not None

        click_ele(driver=self.driver, ele=a)

        sleep(1)
        script = '''
               function func(el)
               {
                  return document.title;
               }
               return func();
           '''
        value = self.driver.execute_script(script)

        print("注入 js：", value)
        assert value == "test_inject_js3 sajsaj撒撒娇 099！！2"
        sleep(10)
        self.driver.close()
        self.driver.quit()
