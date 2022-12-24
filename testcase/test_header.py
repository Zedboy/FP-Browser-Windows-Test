import pytest
from helper.util import get_driver, sleep, format_url, stop_browser_app, get_all_headers
import json
import time
import re
from fp_browser_sdk.ext.basic import Basic
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings
from fp_browser_sdk.ext.navigator import Navigator
from fp_browser_sdk.ext.browser_enum import  BaseEnum, TLSVersion, Platform, PrefersColor, \
    CompatMode, MatchType, SpeechSynthesisVoiceAppendMode, PerformanceNavigationType, DoNotTrackType, MaxTouchPoint, \
    ScreenColorDepth, ScreenOrientationType, MediaKind, WebEffectiveConnectionType, WebConnectionType
from fp_browser_sdk.ext.document import Document, VideoSupport, DocumetMatch
from fp_browser_sdk.ext.header import Cookie, Header
from fp_browser_sdk.ext.screen import Screen


class TestHeader(object):
    def setup_method(self):
        stop_browser_app()

    def _get_user_agent_version(self, ua):
        """
        获得 ua 版本号
        """
        result = re.search('(Chrome\\/)((\\d+\\.){3}\\d+)', ua)

        if result is None:
            return None

        return result.group(2)

    def _get_major_version(self, version):
        """
        获得主版本号
        """
        result = version.split('.')

        if result and len(result) > 0:
            return "{}.0.0.0".format(result[0])

        return None

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ["zh-CN,zh,en", 'zh-CN,zh'])
    def test_languages(self, value):
        """
        测试 浏览器支持语言（多个请用","符号连接）
        """
        settings = FPBrowserSettings()

        basic = Navigator() \
            .set_languages(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_url="https://1024tools.com/header",
                                    custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        setting_value = self.config.get('navigator.languages')
        # 获得全部 header
        result = get_all_headers(driver=self.driver)
        value = result.get('accept-language')

        print("浏览器支持语言（多个请用", "符号连接）:", value, setting_value)
        if setting_value == "zh-CN,zh,en":
            assert value == "zh-CN,zh;q=0.9,en;q=0.8"
        else:
            assert value == "zh-CN,zh;q=0.9"

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    def test_appVersion(self):
        """
        测试 appVersion
        """
        settings = FPBrowserSettings()

        navigator = Navigator() \
            .set_user_agent_auto_match(False)\
            .set_user_agent(
            "Mozilla/5.0 (Linux; Android 9; vivo X22A Build/PKQ1.180819.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.3440.91 Mobile Safari/537.36")

        settings.add_module(navigator)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
                      function func(el)
                      {
                         return navigator.appVersion
                      }
                      return func();
                  '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('navigator.user-agent')
        print("设置 appVersion:")
        print(value)
        print(setting_value)
        assert value == setting_value.replace('Mozilla/', '')

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    def test_user_agent(self):
        """
        测试 设置 User-Agent
        """
        settings = FPBrowserSettings()

        navigator = Navigator() \
            .set_user_agent_auto_match(False) \
            .set_user_agent(
            "Mozilla/5.0 (Linux; Android 9; vivo X22A Build/PKQ1.180819.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.3440.91 Mobile Safari/537.36")

        settings.add_module(navigator)

        driver, config = get_driver(custom_url="https://1024tools.com/header",
                                    custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
                              function func(el)
                              {
                                 return navigator.userAgent
                              }
                              return func();
                          '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('navigator.user-agent')
        print("设置 user-agent:")
        print(value)
        print(setting_value)
        assert value == setting_value

        # 获得全部 header
        result = get_all_headers(driver=self.driver)
        value = result.get('user-agent')

        setting_value = self.config.get('navigator.user-agent')

        print("设置 header 里的 user-agent:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('auto_match', [True, False])
    def test_auto_match_user_agent(self, auto_match):
        """
        测试 修改 UserAgent 里的版本号，自动对应 "version-info.number" 字段的值
        """
        settings = FPBrowserSettings()

        basic = Basic() \
            .set_info_number("42.0.2311.60")

        settings.add_module(basic)

        navigator = Navigator() \
            .set_user_agent_auto_match(auto_match) \
            .set_user_agent(
            "Mozilla/5.0 (Linux; Android 9; vivo X22A Build/PKQ1.180819.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.3440.91 Mobile Safari/537.36")

        settings.add_module(navigator)

        driver, config = get_driver(custom_url="https://1024tools.com/header",
                                    custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
                              function func(el)
                              {
                                 return navigator.userAgent
                              }
                              return func();
                          '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('version-info.number')
        print("设置 user-agent:", value, self._get_user_agent_version(value), setting_value)

        if auto_match:
            assert self._get_user_agent_version(value) == setting_value
        else:
            assert self._get_user_agent_version(value) != setting_value

        # 获得全部 header
        result = get_all_headers(driver=self.driver)
        value = result.get('user-agent')

        setting_value = self.config.get('version-info.number')
        print("设置 user-agent:", value, self._get_user_agent_version(value), setting_value)

        if auto_match:
            assert self._get_user_agent_version(value) == setting_value
        else:
            assert self._get_user_agent_version(value) != setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [
        ("100.0.4896.127", False),
        ("101.0.4951.41", True,),
        ("103.0.5060.71", True,),
        ("94.0.4606.50", False,),
        ("99.0.4844.88", True),
    ])
    def test_reduced_major_in_minor_version_number(self, value):
        """
        测试 修改 UserAgent 里的版本号，自动对应 "version-info.number" 字段的值
        """
        settings = FPBrowserSettings()

        version_number, auto_match = value

        basic = Basic() \
            .set_info_number(version_number)

        settings.add_module(basic)

        navigator = Navigator() \
            .set_user_agent_auto_match(True) \
            .set_reduced_major_in_minor_version_number(auto_match) \
            .set_user_agent(
            "Mozilla/5.0 (Linux; Android 9; vivo X22A Build/PKQ1.180819.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/88.0.3440.91 Mobile Safari/537.36")

        settings.add_module(navigator)

        driver, config = get_driver(custom_url="https://1024tools.com/header",
                                    custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
          function func(el)
          {
             return navigator.userAgent
          }
          return func();
        '''
        value = self.driver.execute_script(script)

        if auto_match is False:
            setting_value = self.config.get('version-info.number')
        else:
            setting_value = self._get_major_version(self.config.get('version-info.number'))

        print("设置 user-agent:", value, self._get_user_agent_version(value), setting_value)

        assert self._get_user_agent_version(value) == setting_value

        # 获得全部 header
        result = get_all_headers(driver=self.driver)
        value = result.get('user-agent')
        print("设置 user-agent:", value, self._get_user_agent_version(value), setting_value, auto_match)

        assert self._get_user_agent_version(value) == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('referrer', ["http://m.baidu.com", None])
    def test_referrer(self, referrer):
        """
        测试 referrer(这个是从 header 的方式获取 referer)
        """
        settings = FPBrowserSettings()

        document = Document() \
            .set_global_match_target_url('https://1024tools.com/header') \
            .set_global_match_referrer(referrer)

        settings.add_module(document)

        driver, config = get_driver(custom_url="https://1024tools.com/header",
                                    custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
                                      function func(el)
                                      {
                                         return document.referrer;
                                      }
                                      return func();
                                  '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('document.global-match-referrer')
        print("设置 referer:", value, setting_value)

        if referrer is None:
            assert value == ""
        else:
            assert value == format_url(setting_value)

        # 获得全部 header
        result = get_all_headers(driver=self.driver)
        value = result.get('referer')
        setting_value = self.config.get('document.global-match-referrer')

        print("设置 referer:", value, setting_value)
        if referrer is None:
            assert value == "" or value is None
        else:
            assert value == format_url(setting_value)

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('package', ['com.xunmeng.pinduoduo', None])
    def test_x_requested_with(self, package):
        """
        测试 设置 X-Requested-With 的值
        """
        settings = FPBrowserSettings()

        header = Header() \
            .set_x_requested_with(package)

        settings.add_module(header)

        driver, config = get_driver(custom_url="https://1024tools.com/header",
                                    custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        # 获得全部 header
        result = get_all_headers(driver=self.driver)
        value = result.get('x-requested-with')

        setting_value = self.config.get('header.x-requested-with')

        print("设置 header X-Requested-With 的值:", value, setting_value)
        if package is None:
            assert value is None
        else:
            assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('extra_json', [{"name1": "value1", "name2": "value2"}])
    def test_extra_json(self, extra_json: dict):
        """
        测试 设置 额外的 header
        """
        settings = FPBrowserSettings()

        header = Header()

        for (key, item) in extra_json.items():
            header.append_extra_json(key=key, value=item)

        settings.add_module(header)

        driver, config = get_driver(custom_url="https://1024tools.com/header",
                                    custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        # 获得全部 header
        value = get_all_headers(driver=self.driver)
        setting_value = self.config.get('header.extra-json')
        format_setting_value = {}
        for item in setting_value:
            format_setting_value[item['name']] = item['value']

        print("设置 header 设置 额外的 header:", value, format_setting_value)

        for item in format_setting_value:
            assert value[item] == format_setting_value[item]

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [DoNotTrackType.ON, DoNotTrackType.OFF, DoNotTrackType.UNSPECIFIED, ])
    def test_do_not_track(self, value):
        """
        测试 设置 Do Not Track（如果强制不追踪就设置为 “1”，否则请不要设置该值。）
        """
        settings = FPBrowserSettings()

        basic = Navigator() \
            .set_do_not_track(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_url="https://1024tools.com/header",
                                    custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        # 获得全部 header
        result = get_all_headers(driver=self.driver)
        value = result.get('dnt')
        setting_value = self.config.get('navigator.do-not-track')

        print("设置 Do Not Track（如果强制不追踪就设置为 “1”，否则请不要设置该值。）:", value, setting_value)

        if setting_value == "1":
            assert int(value) == 1
        else:
            assert value is None

        self.driver.close()
        self.driver.quit()
