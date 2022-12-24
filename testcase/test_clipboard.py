import pytest
from helper.util import get_driver, sleep, get_file_script_context, get_chromium_major_version, stop_browser_app
from selenium.common.exceptions import TimeoutException, JavascriptException
from fp_browser_sdk.ext.basic import Basic
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings
from fp_browser_sdk.ext.browser_enum import BaseEnum, TLSVersion, Platform, PrefersColor, \
    CompatMode, MatchType, SpeechSynthesisVoiceAppendMode, PerformanceNavigationType, DoNotTrackType, MaxTouchPoint, \
    ScreenColorDepth, ScreenOrientationType, MediaKind, WebEffectiveConnectionType, WebConnectionType
from fp_browser_sdk import ConfigConvertSetting
from fp_browser_sdk.ext.permission_types.util import get_permission_type
from fp_browser_sdk.ext.permission_types.permission_type import PermissionType


class TestClipBoard(object):
    def setup_method(self):
        stop_browser_app()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ["sasa", "鞍山市科技安徽省；1123！！sakjsa", 1212121])
    def test_get_text(self, value):
        """
        测试 剪切板文字
        """
        settings = FPBrowserSettings()

        basic = Basic() \
            .append_allow_permission(
            get_permission_type(permission_type=PermissionType.CLIPBOARD_READ_WRITE, version=get_chromium_major_version())) \
            .set_clipboard_text(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = get_file_script_context('./script/clipboard_text.js')
        value = self.driver.execute_script(script)
        setting_value = self.config.get('clipboard.text')

        print("剪切板文字:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    def test_empty_permission(self):
        """
        测试 剪切板未授权
        """
        settings = FPBrowserSettings()

        basic = Basic()

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config
        try:
            script = get_file_script_context('./script/clipboard_text.js')
            value = self.driver.execute_script(script)
            print(value)
            assert False
        except (TimeoutException, JavascriptException):
            assert True

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    def test_empty_text(self):
        """
        测试 空内容
        """
        settings = FPBrowserSettings()

        basic = Basic() \
            .append_allow_permission(
            get_permission_type(permission_type=PermissionType.CLIPBOARD_READ_WRITE, version=get_chromium_major_version())) \
            .set_clipboard_text("")

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = get_file_script_context('./script/clipboard_text.js')
        value = self.driver.execute_script(script)
        setting_value = self.config.get('clipboard.text')

        print("空内容:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ["sasa"])
    def test_reject_permission(self, value):
        """
        测试 拒绝权限
        """
        settings = FPBrowserSettings()

        basic = Basic() \
            .append_reject_permission(
            get_permission_type(permission_type=PermissionType.CLIPBOARD_READ_WRITE, version=get_chromium_major_version())) \
            .set_clipboard_text(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = get_file_script_context('./script/clipboard_text.js')
        value = self.driver.execute_script(script)
        setting_value = self.config.get('clipboard.text')

        print("拒绝权限:", value, setting_value)
        assert value is None or value is False

        self.driver.close()
        self.driver.quit()
