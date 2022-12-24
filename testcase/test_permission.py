import pytest
from helper.util import get_driver, sleep, get_file_script_context, get_chromium_major_version, stop_browser_app
import json
from fp_browser_sdk.ext.basic import Basic
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings
from fp_browser_sdk.ext.browser_enum import BaseEnum, TLSVersion, Platform, PrefersColor, \
    CompatMode, MatchType, SpeechSynthesisVoiceAppendMode, PerformanceNavigationType, DoNotTrackType, MaxTouchPoint, \
    ScreenColorDepth, ScreenOrientationType, MediaKind, WebEffectiveConnectionType, WebConnectionType
from selenium.common.exceptions import TimeoutException, JavascriptException
from fp_browser_sdk.ext.permission_types.util import get_permission_type
from fp_browser_sdk.ext.permission_types.permission_type import PermissionType
from fp_browser_sdk.ext.geo import Geo


class TestPermission(object):
    def setup_method(self):
        stop_browser_app()

    # @pytest.mark.skip("跳过")
    def test_geolocation_allow(self):
        """
        测试 允许定位的权限
        """
        settings = FPBrowserSettings()

        basic = Basic() \
            .append_allow_permission(
            get_permission_type(permission_type=PermissionType.NOTIFICATIONS, version=get_chromium_major_version())) \
            .append_allow_permission(
            get_permission_type(permission_type=PermissionType.GEOLOCATION, version=get_chromium_major_version()))

        settings.add_module(basic)

        geo = Geo() \
            .set_longitude("113.219875") \
            .set_latitude("23.401172") \
            .set_accuracy("14") \
            .set_altitude("13") \
            .set_altitude_accuracy("12") \
            .set_heading("11") \
            .set_speed(BaseEnum.NULL.value)

        settings.add_module(geo)

        driver, config = get_driver(custom_url='https://m.amap.com/', custom_config=settings.parse(),
                                    only_custom_config=True)
        self.driver = driver
        self.config = config

        script = get_file_script_context('./script/geo.js')
        value = self.driver.execute_script(script)
        print(value)

        if value is not None:
            value = value.get("coords")

        setting_value = self.config.get('basic.allow-permissions')

        print("设置 允许定位的权限:", value, setting_value)
        assert value is not None and value is not False

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip("跳过")
    def test_geolocation_reject(self):
        """
        测试 拒绝定位的权限
        """
        settings = FPBrowserSettings()

        basic = Basic() \
            .append_reject_permission(
            get_permission_type(permission_type=PermissionType.GEOLOCATION, version=get_chromium_major_version()))

        settings.add_module(basic)

        driver, config = get_driver(custom_url='https://m.amap.com/', custom_config=settings.parse(),
                                    only_custom_config=True)
        self.driver = driver
        self.config = config

        script = get_file_script_context('./script/geo.js')
        value = self.driver.execute_script(script)
        print(value)
        value = value
        setting_value = self.config.get('basic.reject-permissions')

        print("设置 拒绝定位的权限:", value, setting_value)
        assert value is False

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip("跳过")
    def test_notifiction_allow(self):
        """
        测试 允许通知的权限
        """
        settings = FPBrowserSettings()

        basic = Basic() \
            .append_allow_permission(
            get_permission_type(permission_type=PermissionType.NOTIFICATIONS, version=get_chromium_major_version()))

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(),
                                    only_custom_config=True)
        self.driver = driver
        self.config = config

        script = get_file_script_context('./script/notifycation.js')
        value = self.driver.execute_script(script)
        print(value)
        setting_value = self.config.get('basic.allow-permissions')

        print("设置 允许通知的权限:", value, setting_value)
        assert value == 'granted'

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip("跳过")
    def test_notifiction_reject(self):
        """
        测试 拒绝通知的权限
        """
        settings = FPBrowserSettings()

        basic = Basic() \
            .append_reject_permission(
            get_permission_type(permission_type=PermissionType.NOTIFICATIONS, version=get_chromium_major_version()))

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(),
                                    only_custom_config=True)
        self.driver = driver
        self.config = config

        script = get_file_script_context('./script/notifycation.js')
        value = self.driver.execute_script(script)
        print(value)
        setting_value = self.config.get('basic.reject-permissions')

        print("设置 拒绝通知的权限:", value, setting_value)
        assert value != 'granted'

        self.driver.close()
        self.driver.quit()
