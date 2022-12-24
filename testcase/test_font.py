import pytest
from helper.util import get_driver, sleep, get_file_script_context
import json
import numpy
from fp_browser_sdk.ext.basic import Basic
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings


class TestFont(object):
    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [
        "Marlett",
        "Academy Engraved LET",
        "Adobe Garamond",
        "微软雅黑",
    ])
    def test_font_list(self, value):
        """
        测试字体列表
        """
        settings = FPBrowserSettings()

        basic = Basic() \
            .append_font(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = get_file_script_context('./script/font.js') + '''
           function func()
           {
              return get_support_font();
           }
           return func();
        '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('font.list-json')

        print("注入字体:", value, setting_value)

        # 获得的字体：['sans-serif-thin', 'Marlett', 'Academy Engraved LET', 'Adobe Garamond']
        # 注入的字体：['Marlett', 'Academy Engraved LET', 'Adobe Garamond']
        # 在众多检测字体中 'sans-serif-thin' 是本来就存在的，然后本来存在+注入的字体，就得到了 ['sans-serif-thin', 'Marlett', 'Academy Engraved LET', 'Adobe Garamond']
        for item in setting_value:
            assert item in value

        self.driver.close()
        self.driver.quit()
