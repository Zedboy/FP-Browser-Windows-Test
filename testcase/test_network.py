import pytest
import time
from helper.util import get_driver, sleep, stop_browser_app
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings
from fp_browser_sdk.ext.network import Network
from fp_browser_sdk.ext.browser_enum import BaseEnum, TLSVersion, Platform, PrefersColor, \
    CompatMode, MatchType, SpeechSynthesisVoiceAppendMode, PerformanceNavigationType, DoNotTrackType, MaxTouchPoint, \
    ScreenColorDepth, ScreenOrientationType, MediaKind, WebEffectiveConnectionType, WebConnectionType, Floatinfinity


class TestNetwork(object):
    def setup_method(self):
        stop_browser_app()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [
        WebEffectiveConnectionType.kTypeUnknown,
        WebEffectiveConnectionType.kTypeOffline,
        WebEffectiveConnectionType.kTypeSlow2G,
        WebEffectiveConnectionType.kType2G,
        WebEffectiveConnectionType.kType3G,
        WebEffectiveConnectionType.kType4G,
    ])
    def test_effective_type(self, value):
        """
        测试 网络有效类型
        """
        settings = FPBrowserSettings()

        network = Network() \
            .set_effective_type(value)

        settings.add_module(network)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
           function func(el)
           {
              return navigator.connection.effectiveType;
           }
           return func();
       '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('connection.effective-type')

        print("设置 网络有效类型:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [
        Floatinfinity.INFINITY.value,
        100,
        200,
        200.2,
    ])
    def test_downlink(self, value):
        """
        测试 网络下行速度
        """
        settings = FPBrowserSettings()

        network = Network() \
            .set_downlink(value)

        settings.add_module(network)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
           function func(el)
           {
              return navigator.connection.downlink;
           }
           return func();
       '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('connection.downlink')

        print("设置 网络下行速度:", value, setting_value)
        if setting_value == Floatinfinity.INFINITY.value:
            assert value is None
        else:
            assert value == float(setting_value)

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [50, 100])
    def test_rtt(self, value):
        """
        测试 估算的往返时间
        """
        settings = FPBrowserSettings()

        network = Network() \
            .set_rtt(value)

        settings.add_module(network)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
           function func(el)
           {
              return navigator.connection.rtt;
           }
           return func();
       '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('connection.rtt')

        print("设置 估算的往返时间:", value, setting_value)
        assert value == int(setting_value)

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [True, False])
    def test_save_data(self, value):
        """
        测试 打开/请求数据保护模式「1：true; 0：false」
        """
        settings = FPBrowserSettings()

        network = Network() \
            .set_save_data(value)

        settings.add_module(network)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
           function func(el)
           {
              return navigator.connection.saveData;
           }
           return func();
       '''
        value = self.driver.execute_script(script)
        setting_value = int(self.config.get('connection.save-data')) == 1

        print("设置 打开/请求数据保护模式「1：true; 0：false」:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()
