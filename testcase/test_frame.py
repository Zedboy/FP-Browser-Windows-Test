import pytest
from helper.util import get_driver, sleep, wait_el, get_title, stop_browser_app
from selenium.common.exceptions import UnexpectedAlertPresentException
from fp_browser_sdk.ext.basic import Basic
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings


class TestFrame(object):
    def setup_method(self):
        stop_browser_app()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [True, False])
    def test_alert(self, value):
        """
        测试 alert 状态
        """
        settings = FPBrowserSettings()

        basic = Basic() \
            .set_disable_alert(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_url="https://tyua07.github.io/FP-Browser-Test/check_alert.html",
                                    custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        sleep(3)

        try:
            # 如果有弹框，调用 page_source 会抛出 UnexpectedAlertPresentException 异常，所以直接这么判断就行了
            self.driver.page_source
        except UnexpectedAlertPresentException:
            if value:
                assert True
        else:
            if value is False:
                assert True

        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [True, False])
    def test_confirm(self, value):
        """
        测试 confirm 状态
        """
        settings = FPBrowserSettings()

        basic = Basic() \
            .set_confirm(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
           function func(el)
           {
                const status = window.confirm("Confirm 弹出信息");
                return status;
           }
           return func();
       '''
        value = self.driver.execute_script(script)
        setting_value = int(self.config.get('frame.confirm')) == 1

        print("设置 confirm 状态:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [True, False])
    def test_open(self, value):
        """
        测试 open 状态
        """
        settings = FPBrowserSettings()

        basic = Basic() \
            .set_disable_window_open(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        old_title = get_title(driver=self.driver)
        old_url = self.driver.current_url

        script = '''
                   function func(el)
                   {
                        window.open('https://myip.ipip.net', '_self')
                   }
                   return func();
               '''
        self.driver.execute_script(script)

        current_title = get_title(driver=self.driver)
        current_url = self.driver.current_url

        print("设置 window.open 状态:", old_title, current_title)
        print("设置 window.open 状态:", old_url, current_url)

        if int(self.config.get('frame.disable-window-open')) == 0:
            assert old_url != current_url
        else:
            assert old_url == current_url

        self.driver.close()
        self.driver.quit()
