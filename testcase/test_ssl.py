import pytest
from helper.util import get_driver, sleep, stop_browser_app


class TestSsl(object):
    def setup_class(self):
        driver, config = get_driver(custom_url="https://browserleaks.com/ssl")
        self.driver = driver
        self.config = config

    def teardown_class(self):
        sleep(100)
        self.driver.close()
        self.driver.quit()

    def setup_method(self):
        stop_browser_app()

    def test_window_chrome(self):
        """
        否禁用 window.chrome「1：true; 0：false」
        """
        script = '''
               function func(el)
               {
                  return !!window.chrome;
               }
               return func();
           '''
        value = self.driver.execute_script(script)

        if int(self.config.get('basic-disable-window-chrome')) == 1:
            setting_value = False
        else:
            setting_value = True
        print("否禁用 window.chrome「1：true; 0：false」:", value, setting_value)
        assert value == setting_value
