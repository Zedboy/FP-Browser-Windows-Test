import pytest
import json
import time
from helper.util import get_driver, sleep, get_file_script_context, parse_version_number, get_chromium_major_version, stop_browser_app
from fp_browser_sdk.ext.basic import Basic
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings
from fp_browser_sdk.ext.client_hints import ClientHints
from fp_browser_sdk.ext.browser_enum import  BaseEnum, TLSVersion, Platform, PrefersColor, \
    CompatMode, MatchType, SpeechSynthesisVoiceAppendMode, PerformanceNavigationType, DoNotTrackType, MaxTouchPoint, \
    ScreenColorDepth, ScreenOrientationType, MediaKind, WebEffectiveConnectionType, WebConnectionType


class TestNavigatorUserAgentData(object):
    def setup_method(self):
        stop_browser_app()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [True, False])
    def test_mobile(self, value):
        """
        测试 client hints platform
        """
        settings = FPBrowserSettings()

        clientHints = ClientHints() \
            .set_viewport_width(900) \
            .set_viewport_height(900) \
            .set_prefers_color(PrefersColor.DARK) \
            .set_platform_version("10.0.0") \
            .set_architecture("set_architecture") \
            .set_bitness("set_bitness") \
            .set_wow64(True) \
            .set_mobile(value) \
            .set_model('SM-G9600') \
            .set_disable(False)

        settings.add_module(clientHints)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = get_file_script_context('./script/client_hints.js')
        value = self.driver.execute_script(script)
        print(value)
        value = value.get('mobile')
        setting_value = int(self.config.get('client-hints.mobile')) == 1

        print("测试 client hints mobile:", value, setting_value)
        assert value == setting_value

        script = '''
               function func() {
                   return navigator.userAgentData.mobile;
               }

               const value = func()
               return value
          '''
        user_agent_data_value = self.driver.execute_script(script)
        print("测试 client hints mobile 两种方式是否获取一样:", value, user_agent_data_value)
        assert value == user_agent_data_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ['Android', 'Windows'])
    def test_platform(self, value):
        """
        测试 client hints platform
        """
        settings = FPBrowserSettings()

        clientHints = ClientHints() \
            .set_viewport_width(900) \
            .set_viewport_height(900) \
            .set_platform(value) \
            .set_prefers_color(PrefersColor.DARK) \
            .set_platform_version("10.0.0") \
            .set_architecture("set_architecture") \
            .set_bitness("set_bitness") \
            .set_wow64(True) \
            .set_model('SM-G9600') \
            .set_disable(False)

        settings.add_module(clientHints)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = get_file_script_context('./script/client_hints.js')
        value = self.driver.execute_script(script).get('platform')
        setting_value = self.config.get('client-hints.platform')

        print("测试 client hints platform:", value, setting_value)
        assert value == setting_value

        script = '''
                       function func() {
                           return navigator.userAgentData.platform;
                       }

                       const value = func()
                       return value
                  '''
        user_agent_data_value = self.driver.execute_script(script)
        print("测试 client hints platform 两种方式是否获取一样:", value, user_agent_data_value)
        # 还需要判断 navigator.userAgentData.platform 和 navigator.userAgentData.getHighEntropyValues 获取的是否一致
        assert value == user_agent_data_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ["10.0.0", "12.0.0", "9.2.1"])
    def test_platform_version(self, value):
        """
        测试 client hints platform version
        """
        settings = FPBrowserSettings()

        clientHints = ClientHints() \
            .set_viewport_width(900) \
            .set_viewport_height(900) \
            .set_prefers_color(PrefersColor.DARK) \
            .set_platform_version(value) \
            .set_architecture("set_architecture") \
            .set_bitness("set_bitness") \
            .set_wow64(True) \
            .set_model('SM-G9600') \
            .set_disable(False)

        settings.add_module(clientHints)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = get_file_script_context('./script/client_hints.js')
        value = self.driver.execute_script(script).get('platformVersion')
        setting_value = self.config.get('client-hints.platform-version')

        print("测试 client hints platform version:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ["", "set_architecture"])
    def test_architecture(self, value):
        """
        测试 client hints architecture
        """
        settings = FPBrowserSettings()

        clientHints = ClientHints() \
            .set_viewport_width(900) \
            .set_viewport_height(900) \
            .set_prefers_color(PrefersColor.DARK) \
            .set_platform_version("10.0.0") \
            .set_architecture(value) \
            .set_bitness("set_bitness") \
            .set_wow64(True) \
            .set_model('SM-G9600') \
            .set_disable(False)

        settings.add_module(clientHints)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = get_file_script_context('./script/client_hints.js')
        value = self.driver.execute_script(script).get('architecture')
        setting_value = self.config.get('client-hints.architecture')

        print("测试 client hints architecture:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ["", "set_bitness"])
    def test_bitness(self, value):
        """
        测试 client hints bitness
        """
        settings = FPBrowserSettings()

        clientHints = ClientHints() \
            .set_viewport_width(900) \
            .set_viewport_height(900) \
            .set_prefers_color(PrefersColor.DARK) \
            .set_platform_version("10.0.0") \
            .set_architecture("set_architecture") \
            .set_bitness(value) \
            .set_wow64(True) \
            .set_model('SM-G9600') \
            .set_disable(False)

        settings.add_module(clientHints)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = get_file_script_context('./script/client_hints.js')
        value = self.driver.execute_script(script).get('bitness')
        setting_value = self.config.get('client-hints.bitness')

        print("测试 client hints bitness:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [True, False])
    def test_wow64(self, value):
        """
        测试 client hints wow64
        """
        # 如果是小于等于 93 的浏览器版本，则跳过
        chromium_version = get_chromium_major_version()
        if chromium_version is not None and int(chromium_version) <= 93:
            assert True
            return

        settings = FPBrowserSettings()

        clientHints = ClientHints() \
            .set_viewport_width(900) \
            .set_viewport_height(900) \
            .set_prefers_color(PrefersColor.DARK) \
            .set_platform_version("10.0.0") \
            .set_architecture("set_architecture") \
            .set_bitness("set_bitness") \
            .set_wow64(value) \
            .set_model('SM-G9600') \
            .set_disable(False)

        settings.add_module(clientHints)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = get_file_script_context('./script/client_hints.js')
        value = self.driver.execute_script(script).get('wow64')
        setting_value = int(self.config.get('client-hints.wow64')) == 1

        print("测试 client hints wow64:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ['SM-G9600', 'PCCM00'])
    def test_model(self, value):
        """
        测试 client hints model
        """
        settings = FPBrowserSettings()

        clientHints = ClientHints() \
            .set_viewport_width(900) \
            .set_viewport_height(900) \
            .set_prefers_color(PrefersColor.DARK) \
            .set_platform_version("10.0.0") \
            .set_architecture("set_architecture") \
            .set_bitness("set_bitness") \
            .set_wow64(True) \
            .set_model(value) \
            .set_disable(False)

        settings.add_module(clientHints)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = get_file_script_context('./script/client_hints.js')
        value = self.driver.execute_script(script).get('model')
        setting_value = self.config.get('client-hints.model')

        print("测试 client hints model:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ['106.0.5236.0', '99.0.4844.51', '43.0.2344.2'])
    def test_full_version(self, value):
        """
        测试 client hints full-version
        """
        settings = FPBrowserSettings()

        clientHints = ClientHints() \
            .set_viewport_width(900) \
            .set_viewport_height(900) \
            .set_prefers_color(PrefersColor.DARK) \
            .set_platform_version("10.0.0") \
            .set_architecture("set_architecture") \
            .set_bitness("set_bitness") \
            .set_wow64(True) \
            .set_model('SM-G9600') \
            .set_disable(False)

        settings.add_module(clientHints)

        basic = Basic() \
            .set_info_number(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = get_file_script_context('./script/client_hints.js')
        value = self.driver.execute_script(script).get('uaFullVersion')
        setting_value = self.config.get('version-info.number')

        print("测试 client hints full-version:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ["Google Chrome", None])
    def test_full_version_list(self, value):
        """
        测试 client hints full-version-list
        """
        # 如果是小于等于 93 的浏览器版本，则跳过
        chromium_version = get_chromium_major_version()
        if chromium_version is not None and int(chromium_version) <= 93:
            assert True
            return
        settings = FPBrowserSettings()

        clientHints = ClientHints() \
            .set_viewport_width(900) \
            .set_viewport_height(900) \
            .set_prefers_color(PrefersColor.DARK) \
            .set_platform_version("10.0.0") \
            .set_architecture("set_architecture") \
            .set_bitness("set_bitness") \
            .set_wow64(True) \
            .set_model('SM-G9600') \
            .set_disable(False)

        settings.add_module(clientHints)

        basic = Basic() \
            .set_product_name(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = get_file_script_context('./script/client_hints.js')
        value = self.driver.execute_script(script).get('fullVersionList')

        product_name = self.config.get("version-info.product-name")

        # 如果设置了 product name 就表示有 3 个单元
        if product_name:
            size = 3
        else:
            size = 2

        print("测试 client hints full-version-list:", value)
        assert len(value) == size

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ["Google Chrome", None])
    def test_brands(self, value):
        """
        测试 client hints brands
        """
        settings = FPBrowserSettings()

        clientHints = ClientHints() \
            .set_viewport_width(900) \
            .set_viewport_height(900) \
            .set_prefers_color(PrefersColor.DARK) \
            .set_platform_version("10.0.0") \
            .set_architecture("set_architecture") \
            .set_bitness("set_bitness") \
            .set_wow64(True) \
            .set_model('SM-G9600') \
            .set_disable(False)

        settings.add_module(clientHints)

        basic = Basic() \
            .set_product_name(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = get_file_script_context('./script/client_hints.js')
        value = self.driver.execute_script(script).get('brands')

        product_name = self.config.get("version-info.product-name")

        # 如果设置了 product name 就表示有 3 个单元
        if product_name:
            size = 3
        else:
            size = 2

        print("测试 client hints brands:", value)
        assert len(value) == size

        script = '''
                               function func() {
                                   return navigator.userAgentData.brands;
                               }

                               const value = func()
                               return value
                          '''
        user_agent_data_value = self.driver.execute_script(script)
        print("测试 client hints brands 两种方式是否获取一样:", value, user_agent_data_value)
        # 还需要判断 navigator.userAgentData.platform 和 navigator.userAgentData.getHighEntropyValues 获取的是否一致
        assert value == user_agent_data_value

        self.driver.close()
        self.driver.quit()
