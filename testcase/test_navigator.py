import pytest
from helper.util import get_driver, sleep, get_chromium_version, stop_browser_app, get_chromium_major_version
from fp_browser_sdk.ext.navigator import Navigator
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings
from fp_browser_sdk.ext.browser_enum import BaseEnum, TLSVersion, Platform, PrefersColor, \
    CompatMode, MatchType, SpeechSynthesisVoiceAppendMode, PerformanceNavigationType, DoNotTrackType, MaxTouchPoint, \
    ScreenColorDepth, ScreenOrientationType, MediaKind, WebEffectiveConnectionType, WebConnectionType


class TestNavigator(object):
    def setup_method(self):
        stop_browser_app()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ["zh-CN", 'en-US'])
    def test_locale(self, value):
        """
        测试 用户语言环境
        """
        settings = FPBrowserSettings()

        basic = Navigator() \
            .set_locale(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return Intl.DateTimeFormat().resolvedOptions().locale;
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('navigator.locale')

        print("用户语言环境:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [True, False])
    def test_bluetooth_availability(self, value):
        """
        测试 蓝牙可用性
        """
        settings = FPBrowserSettings()

        basic = Navigator() \
            .set_bluetooth_availability(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               async function func(el)
               {
                  const availability = await navigator.bluetooth.getAvailability();
                  return !!availability;
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = int(self.config.get('navigator.bluetooth-availability')) == 1
        print("设置  蓝牙可用性 状态「1：true; 0：false」:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [True, False])
    def test_webdriver(self, value):
        """
        测试 webdriver 状态
        """
        settings = FPBrowserSettings()

        basic = Navigator() \
            .set_webdriver_status(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return window.navigator.webdriver;
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = int(self.config.get('navigator.webdriver-status')) == 1
        print("设置  webdriver 状态「1：true; 0：false」:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [
        Platform.LINUX_ARMV8L,
        Platform.LINUX_X86_64,
        Platform.WIN64,
        Platform.IPHONE,
    ])
    def test_platform(self, value):
        """
        测试 平台
        """
        settings = FPBrowserSettings()

        basic = Navigator() \
            .set_platform(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return window.navigator.platform;
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('navigator.platform')

        print("平台:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ['Apple Computer, Inc.', 'Google Inc.'])
    def test_vendor(self, value):
        """
        测试 浏览器供应商
        """
        settings = FPBrowserSettings()

        basic = Navigator() \
            .set_vendor(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return window.navigator.vendor;
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('navigator.vendor')

        print("浏览器供应商:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [MaxTouchPoint.MOBILE, MaxTouchPoint.PC])
    def test_max_touch_points(self, value):
        """
        测试 设备能够支持的最大同时触摸的点数「移动端：5; PC:1」
        """
        settings = FPBrowserSettings()

        basic = Navigator() \
            .set_max_touch_points(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return navigator.maxTouchPoints;
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('navigator.max-touch-points')

        print("设备能够支持的最大同时触摸的点数「移动端：5; PC:1」:", value, setting_value)
        assert value == int(setting_value)

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [2, 4, 6, 8, 9, 10])
    def test_hardware_concurrency(self, value):
        """
        测试 处理器数量
        """
        settings = FPBrowserSettings()

        basic = Navigator() \
            .set_hardware_concurrency(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return navigator.hardwareConcurrency;
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('navigator.hardware-concurrency')

        print("处理器数量:", value, setting_value)
        assert value == int(setting_value)

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [2, 4, 6, 8, 9, 10])
    def test_device_memory(self, value):
        """
        测试 设备内存数
        """
        settings = FPBrowserSettings()

        basic = Navigator() \
            .set_device_memory(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return navigator.deviceMemory;
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('navigator.device-memory')

        print("设备内存数:", value, setting_value)
        assert value == int(setting_value)

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [DoNotTrackType.OFF, DoNotTrackType.ON, DoNotTrackType.UNSPECIFIED, ])
    def test_do_not_track(self, value):
        """
        测试 设置 Do Not Track（如果强制不追踪就设置为 “1”，否则请不要设置该值。）
        """
        settings = FPBrowserSettings()

        basic = Navigator() \
            .set_do_not_track(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return navigator.doNotTrack;
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('navigator.do-not-track')

        print("设置 Do Not Track（如果强制不追踪就设置为 “1”，否则请不要设置该值。）:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [True, False])
    def test_online(self, value):
        """
        测试 是否在线「1：true; 0：false」（注意：建议强烈设置成 1）
        """
        settings = FPBrowserSettings()

        basic = Navigator() \
            .set_online(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return navigator.onLine;
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = int(self.config.get('navigator.online')) == 1

        print("是否在线「1：true; 0：false」（注意：建议强烈设置成 1）:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [True, False])
    def test_java_enabled(self, value):
        """
        测试 javaEnabled「1：true; 0：false」(注意：建议设置成对应机型的值)
        """
        settings = FPBrowserSettings()

        basic = Navigator() \
            .set_java_enabled(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return navigator.javaEnabled();
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = int(self.config.get('navigator.java-enabled')) == 1

        print("	javaEnabled「1：true; 0：false」(注意：建议设置成对应机型的值):", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [True, False])
    def test_pdf_viewer_enabled(self, value):
        """
        测试 pdfViewerEnabled「1：true; 0：false」(注意：建议设置成对应机型的值)
        """
        # 如果是小于等于 93 的浏览器版本，则跳过
        chromium_version = get_chromium_major_version()
        if chromium_version is not None and int(chromium_version) <= 93:
            assert True
            return

        settings = FPBrowserSettings()

        basic = Navigator() \
            .set_pdf_viewer_enabled(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return navigator.pdfViewerEnabled;
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = int(self.config.get('navigator.pdf-viewer-enabled')) == 1

        print("pdfViewerEnabled「1：true; 0：false」(注意：建议设置成对应机型的值):", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ["en-US,zh-CN,zh", 'cn,zh'])
    def test_languages(self, value):
        """
        测试 浏览器支持语言（多个请用","符号连接）
        """
        settings = FPBrowserSettings()

        basic = Navigator() \
            .set_languages(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return navigator.languages.join(',');
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('navigator.languages')

        print("浏览器支持语言（多个请用", "符号连接）:", value, setting_value)
        assert value == setting_value

        script = '''
                       function func(el)
                       {
                          return navigator.language;
                       }
                       return func();
                   '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('navigator.languages').split(',')[0]

        print("用户偏好语言:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()
