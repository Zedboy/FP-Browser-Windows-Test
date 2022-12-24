import pytest
from helper.util import get_driver, sleep, format_url, get_match_item, get_all_headers
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


class TestDocumentIframe(object):
    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [
        ("https://tyua07.github.io/FP-Browser-Test/main.html", 0),
    ])
    def test_referrer(self, value):
        """
        测试 强制修改标题
        """
        (custom_url, index) = value
        settings = FPBrowserSettings()

        document = Document() \
            .append_match_list(DocumetMatch()
                               .set_target_url("https://tyua07.github.io/FP-Browser-Test/main.html") \
                               .set_match_break(True) \
                               .set_current_url("https://2g.163.com/") \
                               .set_document_referrer("https://m.baidu.com/1234") \
                               .set_header_referrer("https://m.baidu.com/1234") \
                               .set_title("love you") \
                               .set_match_type(MatchType.FULL)
                               ) \
            .set_compat_mode(CompatMode.CSS1COMPAT)

        settings.add_module(document)

        driver, config = get_driver(custom_url=custom_url, custom_config=settings.parse(),
                                    only_custom_config=True)
        self.driver = driver
        self.config = config
        self.current = self.config.get("document.match-json")[index]

        self.driver.switch_to.frame(0)

        script = '''
                          function func(el)
                          {
                             return document.body.innerHTML;
                          }
                          return func();
                      '''
        value = self.driver.execute_script(script)
        print(value)
        sleep(100000)

        self.driver.close()
        self.driver.quit()
