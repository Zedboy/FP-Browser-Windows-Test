import pytest
from helper.util import get_driver, sleep
from fp_browser_sdk.ext.basic import Basic
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings


class TestBasic(object):

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [True, False])
    def test_disable_settings(self, value):
        """
        否禁用 window.chrome「1：true; 0：false」
        """
        settings = FPBrowserSettings()
        setting_timezone = 'Asia/Kabul'
        basic = Basic() \
            .set_time_zone(setting_timezone) \
            .set_global_disable_settings(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
                       function func(el)
                       {
                         return window.Intl.DateTimeFormat().resolvedOptions().timeZone;
                       }
                       return func();
                   '''
        value = self.driver.execute_script(script)

        if int(self.config.get('global.disable-settings')) == 1:
            timezone = 'Asia/Shanghai'
        else:
            timezone = setting_timezone
        print("否禁用 window.chrome「1：true; 0：false」:", value, timezone)
        assert value == timezone

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ['Asia/Kabul', 'America/Chicago', 'Asia/Shanghai'])
    def test_timezone(self, value):
        """
        时区
        """
        settings = FPBrowserSettings()

        basic = Basic() \
            .set_time_zone(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                 return window.Intl.DateTimeFormat().resolvedOptions().timeZone;
               }
               return func();
           '''
        value = self.driver.execute_script(script)

        script = '''
            // 对Date的扩展，将 Date 转化为指定格式的String
            // 月(M)、日(d)、小时(h)、分(m)、秒(s)、季度(q) 可以用 1-2 个占位符，
            // 年(y)可以用 1-4 个占位符，毫秒(S)只能用 1 个占位符(是 1-3 位的数字)
            // 例子：
            // (new Date()).Format("yyyy-MM-dd hh:mm:ss.S") ==> 2006-07-02 08:09:04.423
            // (new Date()).Format("yyyy-M-d h:m:s.S") ==> 2006-7-2 8:9:4.18
            
            Date.prototype.Format = function (fmt) { // author: meizz
                var o = {
                    "M+": this.getMonth() + 1, // 月份
                    "d+": this.getDate(), // 日
                    "h+": this.getHours(), // 小时
                    "m+": this.getMinutes(), // 分
                    "s+": this.getSeconds(), // 秒
                    "q+": Math.floor((this.getMonth() + 3) / 3), // 季度
                    "S": this.getMilliseconds() // 毫秒
                };
                if (/(y+)/.test(fmt))
                    fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
                for (var k in o)
                    if (new RegExp("(" + k + ")").test(fmt)) fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
                        return fmt;
            }
            
            return new Date().Format("yyyy-MM-dd hh:mm:ss"); 
        '''
        time = self.driver.execute_script(script)

        script = '''
                      function func(el)
                      {
                        return new Date().getTimezoneOffset();
                      }
                      return func();
                  '''
        timezone = self.driver.execute_script(script)
        setting_value = self.config.get('basic.timezone')
        print("时间:", time)
        print("时区:", value, timezone, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    @pytest.mark.skip()
    def test_hour_cycle(self):
        """
        小时制
        """
        script = '''
               function func(el)
               {
                 return new Intl.DateTimeFormat(undefined, { hour: "numeric" }).resolvedOptions().hourCycle;
               }
               return func();
           '''
        value = self.driver.execute_script(script)

        setting_value = self.config.get('basic-hour-cycle')
        print("小时制:", value, setting_value)
        assert value == setting_value

    # @pytest.mark.skip()
    @pytest.mark.parametrize('init_length', [100, -100, 98, 2, 1, 0])
    def test_history_length(self, init_length: int):
        """
        初始化的历史记录数量
        """
        settings = FPBrowserSettings()

        basic = Basic() \
            .set_init_history_length(init_length)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                 return window.history.length;
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('basic.init-history-length')

        print("初始化的历史记录数量:", value, setting_value)
        # 因为是初始化的数量，所以这个值需要大于设置的值

        if init_length < 0:
            assert value == 1
        else:
            assert value == int(setting_value) + 2

        self.driver.close()
        self.driver.quit()
