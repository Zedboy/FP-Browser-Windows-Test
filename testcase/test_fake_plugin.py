import pytest
from helper.util import get_driver, sleep, get_chromium_major_version, stop_browser_app
import json
from fp_browser_sdk.ext.navigator import Navigator
from fp_browser_sdk.ext.plugin import Plugin, MimeType
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings
from fp_browser_sdk.ext.browser_enum import BaseEnum, TLSVersion, Platform, PrefersColor, \
    CompatMode, MatchType, SpeechSynthesisVoiceAppendMode, PerformanceNavigationType, DoNotTrackType, MaxTouchPoint, \
    ScreenColorDepth, ScreenOrientationType, MediaKind, WebEffectiveConnectionType, WebConnectionType


class TestFakePlugin(object):
    def setup_method(self):
        stop_browser_app()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [False])
    def test_plugin(self, value):
        """
        测试 关闭插件
        """
        settings = FPBrowserSettings()

        basic = Navigator() \
            .set_enable_plugin(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
                       function func()
                       {
                          return Array.from(navigator.plugins).map(item => {
                              return {
                                  "name": item["name"],
                                  "filename": item["filename"],
                                  "description": item["description"],
                              }
                          });
                       }
                       return func();
                   '''
        value = self.driver.execute_script(script)
        setting_value = int(self.config.get('navigator.enable-fake-plugin')) == 1

        print("设置 关闭插件:", value, setting_value)
        assert len(value) == 0

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [True])
    def test_fake_plugin(self, value):
        """
        测试 fake 插件
        """
        # 如果是小于等于 93 的浏览器版本，则跳过
        chromium_version = get_chromium_major_version()
        if chromium_version is not None and int(chromium_version) <= 93:
            assert True
            return
        settings = FPBrowserSettings()

        basic = Navigator() \
            .set_enable_plugin(True) \
            .set_enable_fake_plugin(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
                       function func()
                       {
                          return Array.from(navigator.plugins).map(item => {
                              return {
                                  "name": item["name"],
                                  "filename": item["filename"],
                                  "description": item["description"],
                              }
                          });
                       }
                       return func();
                   '''
        value = self.driver.execute_script(script)
        setting_value = int(self.config.get('navigator.enable-fake-plugin')) == 1

        print("设置 fake 插件:", value, setting_value)
        if setting_value:
            assert len(value) == 5
        else:
            assert len(value) == 0

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    def test_custom_plugin(self):
        """
        测试 自定义插件
        """
        settings = FPBrowserSettings()

        basic = Navigator() \
            .set_enable_plugin(True) \
            .append_plugin(Plugin().set_name('测试 name').set_filename("测试 filename").set_description(
            "测试 pdf description").append_mime_types(
            MimeType().set_name("测试 pdf/types").set_description("测试 pdf description").append_extensions(
                "测试 pdf1").append_extensions("测试 pdf2")
        )) \
            .append_plugin(Plugin().set_name('测试 name2').set_filename("测试 filename2").set_description(
            "测试 pdf description2").append_mime_types(
            MimeType().set_name("测试2 pdf/types").set_description("测试2 pdf description").append_extensions(
                "测试2 pdf1").append_extensions("测试2 pdf2")
        )) \
            .set_enable_fake_plugin(False)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
                       function func()
                       {
                          return Array.from(navigator.plugins).map(item => {
                              return {
                                  "name": item["name"],
                                  "filename": item["filename"],
                                  "description": item["description"],
                              }
                          });
                       }
                       return func();
                   '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('navigator.plugin-json')

        print("设置 自定义插件:", value, setting_value)
        assert len(value) == len(setting_value)

        # 对比插件
        for (key, item) in enumerate(value):
            assert item['name'] == setting_value[key]['name']
            assert item['filename'] == setting_value[key]['filename']
            assert item['description'] == setting_value[key]['description']

        script = '''
                               function func()
                               {
                                  return Array.from(navigator.mimeTypes).map(item => {
                                      return {
                                          "name": item["type"],
                                          "extensions": item["suffixes"],
                                          "description": item["description"],
                                      }
                                  });
                               }
                               return func();
                           '''
        value = self.driver.execute_script(script)
        print("设置 自定义 mime_types:", value, setting_value)

        # 对比 mime types
        # 如果是小于等于 93 的浏览器版本，则跳过
        chromium_version = get_chromium_major_version()
        if chromium_version is not None and int(chromium_version) <= 93:
            assert True
            return

        for plugin in setting_value:
            for (key, item) in enumerate(plugin['mime_types']):
                assert item["name"] == value[key]['name']
                assert item["description"] == value[key]['description']
                assert ','.join(item["extensions"]) == value[key]['extensions']

        self.driver.close()
        self.driver.quit()
