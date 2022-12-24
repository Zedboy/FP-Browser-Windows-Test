import pytest
from helper.util import get_driver, sleep, format_url, stop_browser_app
import json
import time
from urllib.parse import urlparse
from fp_browser_sdk.ext.basic import Basic
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings
from fp_browser_sdk.ext.browser_enum import BaseEnum, TLSVersion, Platform, PrefersColor, \
    CompatMode, MatchType, SpeechSynthesisVoiceAppendMode, PerformanceNavigationType, DoNotTrackType, MaxTouchPoint, \
    ScreenColorDepth, ScreenOrientationType, MediaKind, WebEffectiveConnectionType, WebConnectionType
from fp_browser_sdk.ext.document import Document, VideoSupport, DocumetMatch
from requests.utils import requote_uri


class TestDocument(object):
    def setup_method(self):
        stop_browser_app()

    def _timestamp_to_str(self, timestamp):
        """
        时间戳转字符串
        """
        return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(int(timestamp)))

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [int(time.time()), int(time.time() - (60 * 60 * 24))])
    def test_lastModified(self, value):
        """
        测试 文档最后更新时间
        """
        settings = FPBrowserSettings()

        document = Document() \
            .set_lastModified(value)

        settings.add_module(document)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
                   function func(el)
                   {
                      return Date.parse(document.lastModified) / 1e3;
                   }
                   return func();
               '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('document.lastmodified')

        print("设置 文档最后更新时间:", value, setting_value)
        print("设置 文档最后更新时间:", self._timestamp_to_str(value), self._timestamp_to_str(setting_value))
        assert int(value) == int(setting_value)

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ['UTF-8', 'GBK'])
    def test_charset(self, value):
        """
        测试 文档编码
        """
        settings = FPBrowserSettings()

        document = Document() \
            .set_charset(value)

        settings.add_module(document)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
                   function func(el)
                   {
                      return document.characterSet;
                   }
                   return func();
               '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('document.charset')

        print("设置 文档编码:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [
        '最痛苦0-1!归化球员5分钟内乌龙+红牌 或无缘世界杯|红牌|世界杯|马里|西萨科_手机网易网',
        'sakjskajhsa',
        '12i1sa撒飒飒!!@!jsajsa'
    ])
    def test_title(self, value):
        """
        测试 强制修改标题
        """
        settings = FPBrowserSettings()

        document = Document() \
            .set_global_match_target_url("https://m.so.com") \
            .set_global_match_title(value) \
            .set_global_match_current_url('https://3g.163.com/sports/article/H3CC1DJ300058781.html') \
            .set_global_skip_current_url_header(True) \
            .set_global_match_referrer('https://m.baidu.com') \
            .append_match_list(DocumetMatch()
                               .set_target_url("https://ly.so.com/") \
                               .set_match_break(True) \
                               .set_current_url("https://2g.163.com/") \
                               .set_document_referrer("https://m.baidu.com/1234") \
                               .set_header_referrer("https://m.baidu.com/1234") \
                               .set_title("love you") \
                               .set_match_type(MatchType.PATH)
                               ) \
            .set_is_trusted(True) \
            .append_video_support_mime_types(VideoSupport().set_type('video/test')) \
            .append_video_support_mime_types(VideoSupport().set_type('video/ogg; codecs="theora"')) \
            .set_compat_mode(CompatMode.CSS1COMPAT)

        settings.add_module(document)

        driver, config = get_driver(custom_url="https://m.so.com/", custom_config=settings.parse(),
                                    only_custom_config=True)
        self.driver = driver
        self.config = config

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
        setting_value = self.config.get('document.global-match-title')

        print("设置 强制修改标题:", items, setting_value)

        for item in items:
            assert setting_value == item

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [
        'https://3g.163.com/sports/article/H3CC1DJ300058781.html',
        requote_uri('http://so.com/index.html?sajsja=你好啊'),
    ])
    def test_current_url(self, value):
        """
        测试 强制修改后的链接
        """
        settings = FPBrowserSettings()

        document = Document() \
            .set_global_match_target_url("https://m.so.com") \
            .set_global_match_title('sakjskajhsa') \
            .set_global_match_current_url(value) \
            .set_global_skip_current_url_header(True) \
            .set_global_match_referrer('https://m.baidu.com') \
            .append_match_list(DocumetMatch()
                               .set_target_url("https://ly.so.com/") \
                               .set_match_break(True) \
                               .set_current_url("https://2g.163.com/") \
                               .set_document_referrer("https://m.baidu.com/1234") \
                               .set_header_referrer("https://m.baidu.com/1234") \
                               .set_title("love you") \
                               .set_match_type(MatchType.PATH)
                               ) \
            .set_is_trusted(True) \
            .append_video_support_mime_types(VideoSupport().set_type('video/test')) \
            .append_video_support_mime_types(VideoSupport().set_type('video/ogg; codecs="theora"')) \
            .set_compat_mode(CompatMode.CSS1COMPAT)

        settings.add_module(document)

        driver, config = get_driver(custom_url="https://m.so.com/", custom_config=settings.parse(),
                                    only_custom_config=True)
        self.driver = driver
        self.config = config

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
        setting_value = self.config.get('document.global-match-current-url')

        print("设置 强制修改后的链接:", json.dumps(items), setting_value)

        for item in items:
            assert setting_value == item

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [
        'https://3g.163.com/sports/article/H3CC1DJ300058781.html',
        requote_uri('http://so.com/index.html?sajsja=你好啊'),
    ])
    def test_current_domain(self, value):
        """
        测试 强制修改后的链接
        """
        settings = FPBrowserSettings()

        document = Document() \
            .set_global_match_target_url("https://m.so.com") \
            .set_global_match_title('sakjskajhsa') \
            .set_global_match_current_url(value) \
            .set_global_skip_current_url_header(True) \
            .set_global_match_referrer('https://m.baidu.com') \
            .append_match_list(DocumetMatch()
                               .set_target_url("https://ly.so.com/") \
                               .set_match_break(True) \
                               .set_current_url("https://2g.163.com/") \
                               .set_document_referrer("https://m.baidu.com/1234") \
                               .set_header_referrer("https://m.baidu.com/1234") \
                               .set_title("love you") \
                               .set_match_type(MatchType.PATH)
                               ) \
            .set_is_trusted(True) \
            .append_video_support_mime_types(VideoSupport().set_type('video/test')) \
            .append_video_support_mime_types(VideoSupport().set_type('video/ogg; codecs="theora"')) \
            .set_compat_mode(CompatMode.CSS1COMPAT)

        settings.add_module(document)

        driver, config = get_driver(custom_url="https://m.so.com/", custom_config=settings.parse(),
                                    only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return document.domain
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = urlparse(self.config.get('document.global-match-current-url')).hostname

        print("设置 强制修改后的链接:", value, setting_value)

        assert setting_value == value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    # def test_referrer(self):
    #     """
    #     测试 referrer
    #     """
    #     script = '''
    #            function func(el)
    #            {
    #               return document.referrer;
    #            }
    #            return func();
    #        '''
    #     value = self.driver.execute_script(script)
    #     setting_value = self.config.get('document-global-match-referrer')
    #
    #     print("设置 referrer:", value, setting_value)
    #     assert value == format_url(setting_value)
    #
    #     self.driver.close()
    #     self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [True, False])
    def test_is_trusted(self, value):
        """
        测试 是否是用户执行的事件「1：true; 0：false」（注意：建议强烈设置成 1）
        """
        settings = FPBrowserSettings()

        document = Document() \
            .set_is_trusted(value)

        settings.add_module(document)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = """
            function func(el)
           {
                let isTrusted;
                const elemm = document.createElement("a");
                elemm.className = 'trigger_click_a';
                elemm.onclick = (e) => {
                    // console.log(e)
                    isTrusted = e.isTrusted
                }
                document.body.appendChild(elemm);
            
                document.querySelector('.trigger_click_a').click()
                return isTrusted
           }
               return func();
        """
        value = self.driver.execute_script(script)
        setting_value = int(self.config.get('document.is-trusted')) == 1

        print("设置 是否是用户执行的事件「1：true; 0：false」（注意：建议强烈设置成 1）:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [CompatMode.CSS1COMPAT, CompatMode.BACKCOMPAT])
    def test_compat_mode(self, value):
        """
        测试 渲染模式
        """
        settings = FPBrowserSettings()

        document = Document() \
            .set_compat_mode(value)

        settings.add_module(document)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
               function func(el)
               {
                  return document.compatMode;
               }
               return func();
           '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('document.compat-mode')

        print("设置 渲染模式:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    def test_video_support_mime_types_json(self):
        """
        测试 支持播放的视频格式（注意：type 的内容需要 base64 编码。）
        """
        settings = FPBrowserSettings()

        document = Document() \
            .append_video_support_mime_types(VideoSupport().set_type('video/test')) \
            .append_video_support_mime_types(VideoSupport().set_type('video/ogg; codecs="theora"')) \
            .append_video_support_mime_types(VideoSupport().set_type('video/mp4; codecs="avc1.42E01E"')) \
            .append_video_support_mime_types(VideoSupport().set_type('application/x-mpegURL; codecs="avc1.42E01E"')) \
            .append_video_support_mime_types(VideoSupport().set_type('video/webm; codecs="vp9"'))

        settings.add_module(document)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
                const support_video_mime_types = [
                    'video/test',
                    'video/ogg; codecs="theora"',
                    'video/mp4; codecs="avc1.42E01E"',
                    'video/webm; codecs="vp9"',
                    'application/x-mpegURL; codecs="avc1.42E01E"'
                ]
            
                function func(type) {
                    function n(t, n) {
                        console.log(t.canPlayType(n));
                        return t.canPlayType(n).replace(/^no$/, "0").replace(/^probably$/, "1").replace(/^maybe$/, "1")
                    }
            
                    const video = document.createElement('video');
                    if (!!video.canPlayType) {
                        return n(video, type) == 1;
                    }
            
                    return false;
                }
            
                const result = [];
                for (let type of support_video_mime_types) {
                    result.push(func(type));
                }
                return result;
           '''
        items = self.driver.execute_script(script)
        setting_value = self.config.get('document.video-support-mime-types-json')

        print("设置 支持播放的视频格式（注意：type 的内容需要 base64 编码。）:", items, setting_value)
        for item in items:
            assert item

        self.driver.close()
        self.driver.quit()
