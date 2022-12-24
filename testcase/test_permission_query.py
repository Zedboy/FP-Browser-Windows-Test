import pytest
from helper.util import get_driver, sleep, get_file_script_context, get_permission_query_name, \
    stop_browser_app, get_chromium_major_version
import json
from fp_browser_sdk.ext.basic import Basic
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings
from fp_browser_sdk.ext.browser_enum import BaseEnum, TLSVersion, Platform, PrefersColor, \
    CompatMode, MatchType, SpeechSynthesisVoiceAppendMode, PerformanceNavigationType, DoNotTrackType, MaxTouchPoint, \
    ScreenColorDepth, ScreenOrientationType, MediaKind, WebEffectiveConnectionType, WebConnectionType
from fp_browser_sdk.ext.permission_types.util import get_permission_type
from fp_browser_sdk.ext.permission_types.permission_type import PermissionType


class TestPermissionQuery(object):
    def setup_method(self):
        stop_browser_app()

    def _get_query_script(self):
        """
        获得查询权限的 js 脚本
        """
        script = '''    
            const permission_name_list = JSON.parse(arguments[0]);
            async function func() {
                let result = {};
                const queryPromises = permission_name_list.map(
                  name => navigator.permissions.query({ name })
                );
                for await (const status of queryPromises) {
                    result[status.name] = status.state;
                }

                return result;
            }

            const value = await func()
            return value
        '''

        # 如果是小于等于 93 的浏览器版本是没有 name 的，所以需要自己去组合
        chromium_version = get_chromium_major_version()
        if chromium_version is not None and int(chromium_version) <= 93:
            script = '''    
                const permission_name_list = JSON.parse(arguments[0]);
                async function func() {
                    let result = {};
                    const queryPromises = permission_name_list.map(
                      name => navigator.permissions.query({ name })
                    );
                    let i = 0;
                    for await (const status of queryPromises) {
                        result[permission_name_list[i]] = status.state;
                        i ++;
                    }

                    return result;
                }

                const value = await func()
                return value
                '''

        return script

    # @pytest.mark.skip()
    def test_allow(self):
        """
        测试 允许的权限
        """
        settings = FPBrowserSettings()

        basic = Basic() \
            .append_allow_permission(
            get_permission_type(permission_type=PermissionType.GEOLOCATION, version=get_chromium_major_version())) \
            .append_allow_permission(
            get_permission_type(permission_type=PermissionType.NOTIFICATIONS, version=get_chromium_major_version()))

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        setting_value = self.config.get('basic.allow-permissions')
        if setting_value:
            setting_value = setting_value
        else:
            setting_value = []

        permission_name_list = []
        for item in setting_value:
            permission_name_list.append(get_permission_query_name(item).lower())

        print(permission_name_list)
        script = self._get_query_script()

        value = self.driver.execute_script(script, json.dumps(permission_name_list))

        print("设置 允许的权限:", value, permission_name_list, setting_value)
        for item in permission_name_list:
            item = item.replace('-', "_")
            assert value[item] == 'granted'

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    def test_reject(self):
        """
        测试 拒绝的权限
        """
        settings = FPBrowserSettings()

        basic = Basic() \
            .append_allow_permission(
            get_permission_type(permission_type=PermissionType.GEOLOCATION, version=get_chromium_major_version())) \
            .append_reject_permission(
            get_permission_type(permission_type=PermissionType.NOTIFICATIONS, version=get_chromium_major_version()))

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        setting_value = self.config.get('basic.reject-permissions')
        if setting_value:
            setting_value = setting_value
        else:
            setting_value = []

        permission_name_list = []
        for item in setting_value:
            permission_name_list.append(get_permission_query_name(item).lower())

        print(permission_name_list)
        script = self._get_query_script()
        value = self.driver.execute_script(script, json.dumps(permission_name_list))

        print("设置 拒绝的权限:", value, permission_name_list, setting_value)
        for item in permission_name_list:
            assert value[item] == 'denied'

        self.driver.close()
        self.driver.quit()
