import pytest
from helper.util import get_driver, sleep, format_url, get_match_item, get_all_headers, stop_browser_app
import json
import time
from urllib.parse import urlparse
from fp_browser_sdk.ext.basic import Basic
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings
from fp_browser_sdk.ext.browser_enum import  BaseEnum, TLSVersion, Platform, PrefersColor, \
    CompatMode, MatchType, SpeechSynthesisVoiceAppendMode, PerformanceNavigationType, DoNotTrackType, MaxTouchPoint, \
    ScreenColorDepth, ScreenOrientationType, MediaKind, WebEffectiveConnectionType, WebConnectionType
from fp_browser_sdk.ext.document import Document, VideoSupport, DocumetMatch
from requests.utils import requote_uri


class TestDocumentTargetMatch(object):
    def setup_method(self):
        stop_browser_app()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [
        ("https://ly.so.com/", 0),
        ("https://ly.so.com/?src=m_home", 1),
        ('https://3g.163.com/sports/article/H3CC1DJ300058781.html', 2),
        ('https://3g.163.com/sports/article/HEMRKJBI00058781.html?clickfrom=index2018_sports_newslist#offset=1', 3),
    ])
    def test_title(self, value):
        """
        测试 强制修改标题
        """
        (custom_url, index) = value
        settings = FPBrowserSettings()

        document = Document() \
            .append_match_list(DocumetMatch()
                               .set_target_url("https://ly.so.com/") \
                               .set_match_break(True) \
                               .set_current_url("https://2g.163.com/") \
                               .set_document_referrer("https://m.baidu.com/1234") \
                               .set_header_referrer("https://m.baidu.com/1234") \
                               .set_title("love you") \
                               .set_match_type(MatchType.PATH)
                               ) \
            .append_match_list(DocumetMatch()
                               .set_target_url("https://ly.so.com/?src=m_home") \
                               .set_match_break(True) \
                               .set_current_url("https://3g.163.com/") \
                               .set_document_referrer("https://m.baidu.com/2345") \
                               .set_header_referrer("https://m.baidu.com/2345") \
                               .set_title("fuck you") \
                               .set_match_type(MatchType.FULL)
                               ) \
            .append_match_list(DocumetMatch()
                               .set_target_url("https://3g.163.com/sports/article/(\\S+)") \
                               .set_match_break(True) \
                               .set_current_url("https://3g.163.com/static") \
                               .set_document_referrer("https://m.baidu.com/static") \
                               .set_header_referrer("https://m.baidu.com/static") \
                               .set_title("fuck you") \
                               .set_match_type(MatchType.RE)
                               ) \
            .append_match_list(DocumetMatch()
                               .set_target_url(
            "https://3g.163.com/sports/article/HEMRKJBI00058781.html?clickfrom=index2018_sports_newslist#offset=1") \
                               .set_match_break(True) \
                               .set_current_url("https://3g.163.com/sta") \
                               .set_document_referrer("https://m.baidu.com/sta") \
                               .set_header_referrer("https://m.baidu.com/sta") \
                               .set_title("fuck you") \
                               .set_match_type(MatchType.FULL)
                               ) \
            .set_compat_mode(CompatMode.CSS1COMPAT)

        settings.add_module(document)

        driver, config = get_driver(custom_url=custom_url, custom_config=settings.parse(),
                                    only_custom_config=True)
        self.driver = driver
        self.config = config
        self.current = self.config.get("document.match-json")[index]

        script = '''
               function func(el)
               {
                  return [
                    document.title,
                    document.querySelector('title').text,
                    document.querySelector('title').innerText,
                    document.querySelector('title').innerHTML
                  ]
               }
               return func();
           '''
        items = self.driver.execute_script(script)
        setting_value = self.current.get('title')

        print("设置 强制修改标题:", items, setting_value)

        for item in items:
            assert setting_value == item

        script = '''
                       function func(el)
                       {
                          return [
                            document.URL,
                            document.baseURI,
                            document.documentURI,
                            document.location.href,
                            window.location.href
                          ]
                       }
                       return func();
                   '''
        items = self.driver.execute_script(script)
        setting_value = self.current.get('current_url')

        print("设置 强制修改后的链接:", json.dumps(items), setting_value)

        for item in items:
            assert setting_value == item

        script = '''
                       function func(el)
                       {
                          return document.referrer;
                       }
                       return func();
                   '''
        value = self.driver.execute_script(script)
        setting_value = self.current.get('document_referrer')

        print("设置 referrer:", value, setting_value)
        assert value == format_url(setting_value)

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [
        ("https://1024tools.com/header", 0)
    ])
    def test_referrer(self, value):
        """
        测试 强制修改标题
        """
        (custom_url, index) = value
        settings = FPBrowserSettings()

        document = Document() \
            .append_match_list(DocumetMatch()
                               .set_target_url("https://1024tools.com/header") \
                               .set_match_break(True) \
                               .set_current_url("https://2g.163.com/") \
                               .set_document_referrer("https://m.baidu.com/1234") \
                               .set_header_referrer("https://m.baidu.com/1234") \
                               .set_title("love you") \
                               .set_match_type(MatchType.PATH)
                               ) \
            .set_compat_mode(CompatMode.CSS1COMPAT)

        settings.add_module(document)

        driver, config = get_driver(custom_url=custom_url, custom_config=settings.parse(),
                                    only_custom_config=True)
        self.driver = driver
        self.config = config
        self.current = self.config.get("document.match-json")[index]

        # 获得全部 header
        result = get_all_headers(driver=self.driver)
        value = result.get('referer')
        setting_value = self.current.get('header_referrer')

        print(result)
        print("referrer 的值:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()
