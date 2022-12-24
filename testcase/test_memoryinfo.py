import pytest
from helper.util import get_driver, sleep
from fp_browser_sdk.ext.basic import Basic
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings


class TestMemoryinfo(object):
    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [10000000, 1000000])
    def test_total_js(self, value):
        """
        测试 已分配的堆体积（以字节计算）
        """
        settings = FPBrowserSettings()

        basic = Basic() \
            .set_memory_info_total_js(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return window.performance.memory ? [window.performance.memory.totalJSHeapSize , window.console.memory.totalJSHeapSize] : false
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = int(self.config.get('memoryinfo.total-js'))

        print("设置 已分配的堆体积（以字节计算）:", value, setting_value)

        for item in value:
            assert setting_value == item

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [10000000, 1000000])
    def test_used_js(self, value):
        """
        测试 已分配的堆体积（以字节计算）
        """
        settings = FPBrowserSettings()

        basic = Basic() \
            .set_memory_info_used_js(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return window.performance.memory ? [window.performance.memory.usedJSHeapSize , window.console.memory.usedJSHeapSize]: false
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = int(self.config.get('memoryinfo.used-js'))

        print("设置 当前 JS 堆活跃段（segment）的体积（以字节计算）:", value, setting_value)
        for item in value:
            assert setting_value == item

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [1136000000, 113600000])
    def test_limit_js(self, value):
        """
        测试 已分配的堆体积（以字节计算）
        """
        settings = FPBrowserSettings()

        basic = Basic() \
            .set_memory_info_limit_js(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return window.performance.memory ? [window.performance.memory.jsHeapSizeLimit , window.console.memory.jsHeapSizeLimit]: false
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = int(self.config.get('memoryinfo.limit-js'))

        print("设置 上下文内可用堆的最大体积（以字节计算）:", value, setting_value)
        for item in value:
            assert setting_value == item

        self.driver.close()
        self.driver.quit()
