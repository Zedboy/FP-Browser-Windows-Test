import pytest
from helper.util import get_driver, sleep, get_file_script_context, get_chromium_major_version, stop_browser_app
import json
from fp_browser_sdk.ext.basic import Basic
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings
from fp_browser_sdk.ext.browser_enum import BaseEnum, TLSVersion, Platform, PrefersColor, \
    CompatMode, MatchType, SpeechSynthesisVoiceAppendMode, PerformanceNavigationType, DoNotTrackType, MaxTouchPoint, \
    ScreenColorDepth, ScreenOrientationType, MediaKind, WebEffectiveConnectionType, WebConnectionType
from fp_browser_sdk.ext.geo import Geo
from fp_browser_sdk.ext.permission_types.util import get_permission_type
from fp_browser_sdk.ext.permission_types.permission_type import PermissionType


class TestGeo(object):

    def setup_class(self):
        stop_browser_app()
        # 花都广场
        # {
        #     "coords": {
        #         "accuracy": 3.749000072479248,
        #         "altitude": 5,
        #         "altitudeAccuracy": null,
        #         "heading": 0,
        #         "latitude": 37.4219983,
        #         "longitude": -122.084,
        #         "speed": 0
        #     },
        #     "timestamp": 1657251769930
        # }
        # url = 'https://map.baidu.com/mobile/webapp/index/index/foo=bar/vt=map'
        url = 'https://m.amap.com/'
        # url = 'https://browserleaks.com/geo'

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

        driver, config = get_driver(custom_url=url, custom_config=settings.parse(),
                                    only_custom_config=True)
        self.driver = driver
        self.config = config

    def teardown_class(self):
        sleep(10)
        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    def test_longitude(self):
        """
        测试 经度
        """
        script = get_file_script_context('./script/geo.js')
        value = self.driver.execute_script(script)
        print(value)
        value = value.get("coords").get("longitude")
        setting_value = self.config.get('geo.longitude')

        print("设置 经度:", value, setting_value)
        assert float(value) == float(setting_value)

    # @pytest.mark.skip()
    def test_latitude(self):
        """
        测试 纬度
        """
        script = get_file_script_context('./script/geo.js')
        value = self.driver.execute_script(script).get("coords").get("latitude")
        setting_value = self.config.get('geo.latitude')

        print("设置 纬度:", value, setting_value)
        assert float(value) == float(setting_value)

    # @pytest.mark.skip()
    def test_accuracy(self):
        """
        测试 经度精确值
        """
        script = get_file_script_context('./script/geo.js')
        value = self.driver.execute_script(script).get("coords").get("accuracy")
        setting_value = self.config.get('geo.accuracy')

        print("设置 经度精确值:", value, setting_value)
        assert float(value) == float(setting_value)

    # @pytest.mark.skip()
    def test_altitude(self):
        """
        测试 海平面高度（无法提供时为 null）
        """
        script = get_file_script_context('./script/geo.js')
        value = self.driver.execute_script(script).get("coords").get("altitude")
        setting_value = self.config.get('geo.altitude')

        print("设置 海平面高度（无法提供时为 null）:", value, setting_value)

        if setting_value == "null":
            assert value is None
        else:
            assert float(value) == float(setting_value)

    # @pytest.mark.skip()
    def test_altitude_accuracy(self):
        """
        测试 高度精确值（无法提供时为 null）
        """
        script = get_file_script_context('./script/geo.js')
        value = self.driver.execute_script(script).get("coords").get("altitudeAccuracy")
        setting_value = self.config.get('geo.altitude-accuracy')

        print("设置 高度精确值（无法提供时为 null）:", value, setting_value)

        if setting_value == "null":
            assert value is None
        else:
            assert float(value) == float(setting_value)

    # @pytest.mark.skip()
    def test_heading(self):
        """
        测试 前进方向（无法提供时为 null）
        """
        script = get_file_script_context('./script/geo.js')
        value = self.driver.execute_script(script).get("coords").get("heading")
        setting_value = self.config.get('geo.heading')

        print("设置 前进方向（无法提供时为 null）:", value, setting_value)

        if setting_value == "null":
            assert value is None
        else:
            assert float(value) == float(setting_value)

    # @pytest.mark.skip()
    def test_speed(self):
        """
        测试 速度（无法提供时为 null）
        """
        script = get_file_script_context('./script/geo.js')
        value = self.driver.execute_script(script).get("coords").get("speed")
        setting_value = self.config.get('geo.speed')

        print("设置 速度（无法提供时为 null）:", value, setting_value)

        if setting_value == "null":
            assert value is None
        else:
            assert float(value) == float(setting_value)
