import pytest
from helper.util import get_driver, sleep, get_chromium_major_version, stop_browser_app
from fp_browser_sdk.ext.basic import Basic
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings
from fp_browser_sdk.ext.screen import Screen
from fp_browser_sdk.ext.browser_enum import BaseEnum, TLSVersion, Platform, PrefersColor, \
    CompatMode, MatchType, SpeechSynthesisVoiceAppendMode, PerformanceNavigationType, DoNotTrackType, MaxTouchPoint, \
    ScreenColorDepth, ScreenOrientationType, MediaKind, WebEffectiveConnectionType, WebConnectionType
from fp_browser_sdk import ConfigConvertSetting


class TestScreen(object):
    def setup_method(self):
        stop_browser_app()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [ScreenColorDepth.ColorDepth_30, ScreenColorDepth.ColorDepth_24])
    def test_color_depth(self, value):
        """
        测试 colorDepth（屏幕的色彩深度）
        """
        settings = FPBrowserSettings()

        screen = Screen() \
            .set_color_depth(value)

        settings.add_module(screen)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return [window.screen.colorDepth, window.screen.pixelDepth];
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('screen.color-depth')

        print("设置 colorDepth（屏幕的色彩深度）:", value, setting_value)
        for item in value:
            assert item == int(setting_value)

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ['./config/sm-g9600.json', './config/redmi_6a.json'])
    def test_width(self, value):
        """
        测试 屏幕宽度（单位：px）
        """
        custom_config = ConfigConvertSetting(config_path=value,
                                             browser_version=get_chromium_major_version()).handle(
            cookie=[],
            real_ip="8.8.8.8",
            connection_type=WebConnectionType.CELLULAR,
            effective_type=WebEffectiveConnectionType.kType4G
        )

        driver, config = get_driver(custom_config=custom_config, only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return window.screen.width
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('screen.width')

        print("设置 屏幕宽度（单位：px）:", value, setting_value)
        assert value == int(setting_value)

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ['./config/sm-g9600.json', './config/redmi_6a.json'])
    def test_height(self, value):
        """
        测试 屏幕高度（单位：px）
        """
        custom_config = ConfigConvertSetting(config_path=value,
                                             browser_version=get_chromium_major_version()).handle(
            cookie=[],
            real_ip="8.8.8.8",
            connection_type=WebConnectionType.CELLULAR,
            effective_type=WebEffectiveConnectionType.kType4G
        )

        driver, config = get_driver(custom_config=custom_config, only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return window.screen.height
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('screen.height')

        print("设置 屏幕高度（单位：px）:", value, setting_value)
        assert value == int(setting_value)

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ['./config/sm-g9600.json', './config/redmi_6a.json'])
    def test_avail_width(self, value):
        """
        测试 可用空间的屏幕宽度（单位：px）
        """
        custom_config = ConfigConvertSetting(config_path=value,
                                             browser_version=get_chromium_major_version()).handle(
            cookie=[],
            real_ip="8.8.8.8",
            connection_type=WebConnectionType.CELLULAR,
            effective_type=WebEffectiveConnectionType.kType4G
        )

        driver, config = get_driver(custom_config=custom_config, only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return window.screen.availWidth
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('screen.avail-width')

        print("设置 可用空间的屏幕宽度（单位：px）:", value, setting_value)
        assert value == int(setting_value)

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ['./config/sm-g9600.json', './config/redmi_6a.json'])
    def test_avail_height(self, value):
        """
        测试 可用空间的屏幕高度（单位：px）
        """
        custom_config = ConfigConvertSetting(config_path=value,
                                             browser_version=get_chromium_major_version()).handle(
            cookie=[],
            real_ip="8.8.8.8",
            connection_type=WebConnectionType.CELLULAR,
            effective_type=WebEffectiveConnectionType.kType4G
        )

        driver, config = get_driver(custom_config=custom_config, only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return window.screen.availHeight
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('screen.avail-height')

        print("设置 可用空间的屏幕高度（单位：px）:", value, setting_value)
        assert value == int(setting_value)

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ['./config/sm-g9600.json', './config/redmi_6a.json'])
    def test_avail_top(self, value):
        """
        测试 可用空间的左边边界的第一个像素点
        """
        custom_config = ConfigConvertSetting( config_path=value,
                                             browser_version=get_chromium_major_version()).handle(
            cookie=[],
            real_ip="8.8.8.8",
            connection_type=WebConnectionType.CELLULAR,
            effective_type=WebEffectiveConnectionType.kType4G
        )

        driver, config = get_driver(custom_config=custom_config, only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return window.screen.availTop
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('screen.avail-top')

        print("设置 可用空间的左边边界的第一个像素点:", value, setting_value)
        assert value == int(setting_value)

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ['./config/sm-g9600.json', './config/redmi_6a.json'])
    def test_avail_left(self, value):
        """
        测试 可用空间的顶部边界的第一个像素点
        """
        custom_config = ConfigConvertSetting( config_path=value,
                                             browser_version=get_chromium_major_version()).handle(
            cookie=[],
            real_ip="8.8.8.8",
            connection_type=WebConnectionType.CELLULAR,
            effective_type=WebEffectiveConnectionType.kType4G
        )

        driver, config = get_driver(custom_config=custom_config, only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return window.screen.availLeft
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('screen.avail-left')

        print("设置 可用空间的顶部边界的第一个像素点:", value, setting_value)
        assert value == int(setting_value)

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value',
                             [ScreenOrientationType.LANDSCAPE_SECONDARY, ScreenOrientationType.LANDSCAPE_PRIMARY,
                              ScreenOrientationType.PORTRAIT_PRIMARY])
    def test_orientation(self, value):
        """
        测试 屏幕方向「0、90、180、270」，注意：请配合 “ScreenOrientationType” 搭配使用。
        """
        settings = FPBrowserSettings()

        screen = Screen() \
            .set_orientation(value)

        settings.add_module(screen)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return [window.screen.orientation.type, window.screen.orientation.angle]
               }
               return func();
           '''
        value = self.driver.execute_script(script)

        setting_value = self.config.get('screen.orientation-type')
        print("设置 屏幕方向「0、90、180、270」，注意：请配合 “ScreenOrientationType” 搭配使用。:", value, setting_value)
        assert value[0] == setting_value

        setting_value = self.config.get('screen.orientation-angle')
        print("设置 屏幕方向「0、90、180、270」，注意：请配合 “ScreenOrientationType” 搭配使用。:", value, setting_value)
        assert value[1] == int(setting_value)

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [2.75, 3])
    def test_device_pixel_ratio(self, value):
        """
        测试 设备像素比
        """
        settings = FPBrowserSettings()

        screen = Screen() \
            .set_device_pixel_ratio(value)

        settings.add_module(screen)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return window.devicePixelRatio;
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('screen.device-pixel-ratio')

        print('设置 设备像素比:', value, setting_value)
        assert value == float(setting_value)

        self.driver.close()
        self.driver.quit()
