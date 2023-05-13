import pytest
from helper.util import get_driver, sleep, stop_browser_app
from fp_browser_sdk.ext.performance import Performance, PerformanceMatch
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings
from fp_browser_sdk.ext.browser_enum import  BaseEnum, TLSVersion, Platform, PrefersColor, \
    CompatMode, MatchType, SpeechSynthesisVoiceAppendMode, PerformanceNavigationType, DoNotTrackType, MaxTouchPoint, \
    ScreenColorDepth, ScreenOrientationType, MediaKind, WebEffectiveConnectionType, WebConnectionType
import random


class TestPerformance(object):
    def setup_method(self):
        stop_browser_app()

    def _type_to_string(self, type):
        """
        类型转字符串
        """
        if int(type) == int(PerformanceNavigationType.NAVIGATE.value):
            return 'navigate'
        elif int(type) == int(PerformanceNavigationType.RELOAD.value):
            return 'reload'
        elif int(type) == int(PerformanceNavigationType.BACK_FORWARD.value):
            return 'back_forward'
        else:
            return 'navigate'

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [
        ("https://ly.so.com/", 0),
        ("https://ly.so.com/?src=m_home", 1),
        ('https://m.163.com/sports/article/H3CC1DJ300058781.html', 2),
        ('https://m.163.com/sports/article/HEMRKJBI00058781.html?clickfrom=index2018_sports_newslist#offset=1', 3),
    ])
    def test_performance(self, value):
        """
        测试 如何导航到该页面，详细请查看链接：https://developer.mozilla.org/en-US/docs/Web/API/PerformanceNavigation/type
        """
        (custom_url, index) = value
        settings = FPBrowserSettings()

        basic = Performance() \
            .append_match(
            PerformanceMatch()
                .set_target_url("https://ly.so.com/") \
                .set_match_break(True) \
                .set_timing_redirectStart_offset(random.randint(10, 50)) \
                .set_timing_redirectEnd_offset(random.randint(60, 100)) \
                .set_navigation_type(PerformanceNavigationType.RELOAD) \
                .set_navigation_redirect_count(random.randint(10, 100)) \
                .set_match_type(MatchType.PATH)
        ) \
            .append_match(
            PerformanceMatch()
                .set_target_url("https://ly.so.com/?src=m_home") \
                .set_match_break(True) \
                .set_navigation_type(PerformanceNavigationType.BACK_FORWARD) \
                .set_navigation_redirect_count(random.randint(10, 100)) \
                .set_match_type(MatchType.FULL)
        ) \
            .append_match(
            PerformanceMatch()
                .set_target_url("https://m.163.com/sports/article/(\\S+)") \
                .set_match_break(True) \
                .set_timing_redirectStart_offset(random.randint(10, 50)) \
                .set_timing_redirectEnd_offset(random.randint(60, 100)) \
                .set_navigation_type(PerformanceNavigationType.NAVIGATE) \
                .set_navigation_redirect_count(random.randint(10, 100)) \
                .set_match_type(MatchType.RE)
        ) \
            .append_match(
            PerformanceMatch()
                .set_target_url(
                "https://m.163.com/sports/article/HEMRKJBI00058781.html?clickfrom=index2018_sports_newslist#offset=1") \
                .set_match_break(True) \
                .set_navigation_type(PerformanceNavigationType.BACK_FORWARD) \
                .set_navigation_redirect_count(random.randint(10, 100)) \
                .set_match_type(MatchType.FULL)
        )

        settings.add_module(basic)

        driver, config = get_driver(custom_url=custom_url, custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config
        self.current = self.config.get("performance.match-json")[index]

        script = '''
            function func(el)
            {
                const performance = window.performance;
                try {
                    return performance.navigation.type.toString()
                } catch (e) {

                }

                return false;
            }
            return func();
        '''
        value = self.driver.execute_script(script)
        setting_value = self.current['navigation_type']

        print("导航类型:", value, setting_value)
        assert int(value) == int(setting_value)

        script = '''
                    function func(el)
                    {
                        const performance = window.performance;
                        try {
                            return performance.navigation.redirectCount
                        } catch (e) {

                        }

                        return false;
                    }
                    return func();
                '''
        value = self.driver.execute_script(script)
        setting_value = self.current['navigation_redirect_count']

        print("重定向次数", value, setting_value)
        assert int(value) == int(setting_value)

        script = '''
                    function func(el)
                    {
                        return window.performance.getEntriesByType("navigation")[0]['type'];
                    }
                    return func();
                '''
        value = self.driver.execute_script(script)
        setting_value = self.current['navigation_type']

        print("导航类型:", value, self._type_to_string(setting_value))
        assert value == self._type_to_string(setting_value)

        script = '''
            function func(el)
            {
                return window.performance.getEntriesByType("navigation")[0]['redirectCount'];
            }
            return func();
        '''
        value = self.driver.execute_script(script)
        setting_value = self.current['navigation_redirect_count']

        print("重定向次数", value, setting_value)
        assert int(value) == int(setting_value)

        # script = '''
        #     function func(el)
        #     {
        #         return window.performance.getEntriesByType("navigation")[0]['redirectStart'];
        #     }
        #     return func();
        # '''
        # value = self.driver.execute_script(script)
        # setting_value = self.current['timing_redirectStart_offset']
        #
        # print("重定向开始时间", value, setting_value)
        # assert int(value) == int(setting_value)
        #
        # script = '''
        #     function func(el)
        #     {
        #         return window.performance.getEntriesByType("navigation")[0]['redirectEnd'];
        #     }
        #     return func();
        # '''
        # value = self.driver.execute_script(script)
        # setting_value = self.current['timing_redirectEnd_offset']
        #
        # print("重定向结束时间", value, setting_value)
        # assert int(value) == int(setting_value)

        self.driver.close()
        self.driver.quit()
