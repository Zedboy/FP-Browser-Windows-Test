import json
from fp_browser_sdk.ext.basic import Basic
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings
import pytest
from helper.util import get_driver, sleep, stop_browser_app
from fp_browser_sdk.ext.screen import Screen

match_script = """
            const doesMatch = (attr, val) => {
                return matchMedia('(' + attr + ':' + val + ')').matches;
            }

        """


class TestMediaMatch(object):
    def setup_method(self):
        stop_browser_app()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ["rec2020", 'p3', "srgb"])
    def test_color_gamut(self, value):
        """
        测试  color-gamut 匹配
        """
        settings = FPBrowserSettings()

        screen = Screen() \
            .append_media_matchs("color-gamut", value)

        settings.add_module(screen)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = match_script + '''
                      function func(el)
                      {
                            const arr = ["rec2020", 'p3', "srgb"];
                            for(let attr of arr) {
                                if (doesMatch('color-gamut', attr)) {
                                    return attr;
                                }
                            }
                        
                            return '无';
                      }
                      return func();
                  '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('media.matchs-json')

        for item in setting_value:
            if item.find('color-gamut') >= 0:
                setting_value = item.split(':')[1]

        print("设置 color-gamut 匹配:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ["active", 'none'])
    def test_forced_colors(self, value):
        """
        测试  forced-colors 匹配
        """
        settings = FPBrowserSettings()

        screen = Screen() \
            .append_media_matchs("forced-colors", value)

        settings.add_module(screen)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = match_script + '''
                      function func(el)
                      {
                            const arr = ["active", 'none'];
                            for(let attr of arr) {
                                if (doesMatch('forced-colors', attr)) {
                                    return attr;
                                }
                            }

                            return '无';
                      }
                      return func();
                  '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('media.matchs-json')

        for item in setting_value:
            if item.find('forced-colors') >= 0:
                setting_value = item.split(':')[1]

        print("设置 forced-colors 匹配:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ["high", 'standard'])
    def test_dynamic_range(self, value):
        """
        测试  dynamic-range 匹配
        """
        settings = FPBrowserSettings()

        screen = Screen() \
            .append_media_matchs("dynamic-range", value)

        settings.add_module(screen)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = match_script + '''
                      function func(el)
                      {
                            const arr = ["high", 'standard'];
                            for(let attr of arr) {
                                if (doesMatch('dynamic-range', attr)) {
                                    return attr;
                                }
                            }

                            return '无';
                      }
                      return func();
                  '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('media.matchs-json')

        for item in setting_value:
            if item.find('dynamic-range') >= 0:
                setting_value = item.split(':')[1]

        print("设置 dynamic-range 匹配:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ["no-preference", 'high', 'more', 'low', 'less', 'forced'])
    def test_prefers_contrast(self, value):
        """
        测试  prefers-contrast 匹配
        """
        settings = FPBrowserSettings()

        screen = Screen() \
            .append_media_matchs("prefers-contrast", value)

        settings.add_module(screen)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = match_script + '''
                      function func(el)
                      {
                             const arr = ["no-preference", 'high', 'more', 'low', 'less', 'forced'];
                            for(let attr of arr) {
                                if (doesMatch('prefers-contrast', attr)) {
                                    return attr;
                                }
                            }

                            return '无';
                      }
                      return func();
                  '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('media.matchs-json')

        for item in setting_value:
            if item.find('prefers-contrast') >= 0:
                setting_value = item.split(':')[1]

        print("设置 prefers-contrast 匹配:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ["inverted", 'none'])
    def test_inverted_colors(self, value):
        """
        测试  inverted-colors 匹配
        """
        settings = FPBrowserSettings()

        screen = Screen() \
            .append_media_matchs("inverted-colors", value)

        settings.add_module(screen)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = match_script + '''
                      function func(el)
                      {
                            const arr = ["inverted", 'none'];
                            for(let attr of arr) {
                                if (doesMatch('inverted-colors', attr)) {
                                    return attr;
                                }
                            }

                            return '无';
                      }
                      return func();
                  '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('media.matchs-json')

        for item in setting_value:
            if item.find('inverted-colors') >= 0:
                setting_value = item.split(':')[1]

        print("设置 inverted-colors 匹配:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()
