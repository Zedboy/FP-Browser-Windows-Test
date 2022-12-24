import pytest
from helper.util import get_driver, sleep, get_all_headers, get_chromium_major_version, stop_browser_app
import json
from fp_browser_sdk.ext.basic import Basic
from fp_browser_sdk.ext.navigator import Navigator
from fp_browser_sdk.ext.client_hints import ClientHints
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings
from fp_browser_sdk.ext.screen import Screen
from fp_browser_sdk.ext.browser_enum import BaseEnum, TLSVersion, Platform, PrefersColor, \
    CompatMode, MatchType, SpeechSynthesisVoiceAppendMode, PerformanceNavigationType, DoNotTrackType, MaxTouchPoint, \
    ScreenColorDepth, ScreenOrientationType, MediaKind, WebEffectiveConnectionType, WebConnectionType
from fp_browser_sdk import ConfigConvertSetting
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings
from fp_browser_sdk.ext.network import Network
from fp_browser_sdk.ext.browser_enum import BaseEnum, TLSVersion, Platform, PrefersColor, \
    CompatMode, MatchType, SpeechSynthesisVoiceAppendMode, PerformanceNavigationType, DoNotTrackType, MaxTouchPoint, \
    ScreenColorDepth, ScreenOrientationType, MediaKind, WebEffectiveConnectionType, WebConnectionType, Floatinfinity, \
    WebClientHintsType
from fp_browser_sdk.ext.client_hints import ClientHints


class TestClientHints(object):
    def setup_method(self):
        stop_browser_app()

    def _get_header_value(self, key):
        """
        获得指定 header 的值
        """
        script = '''
                   function func(el)
                   {
                       const all_header = JSON.parse(document.querySelector('.header').innerText);
                        for (let key in all_header) {
                            if (key.toLowerCase() === '{key}') {
                                return all_header[key][0]
                            }
                        }

                        return null;
                   }
                   return func();
               '''
        return self.driver.execute_script(script.replace("{key}", key))

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ["zh,cn", 'cn,zh'])
    def test_language(self, value):
        """
        测试 设置语言的值
        """
        # 如果是小于等于 93 的浏览器版本，则跳过
        chromium_version = get_chromium_major_version()
        if chromium_version is not None and int(chromium_version) > 93:
            assert True
            return

        settings = FPBrowserSettings()

        basic = Navigator() \
            .set_languages(value)

        settings.add_module(basic)

        client_hints = ClientHints().set_disable(False)
        settings.add_module(client_hints)

        driver, config = get_driver(custom_url="https://1024tools.com/header",
                                    custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        # 获得全部 header
        result = get_all_headers(driver=self.driver)
        value = result.get('sec-ch-lang')

        # 格式化一下
        # 把 '"zh", "cn"' 格式化成 'zh,cn'
        value = ",".join([item.replace('"', '').replace(' ', '') for item in value.split(',')])

        setting_value = self.config.get('navigator.languages')

        print(result)
        print("设置 client hints height 的值:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('disable_field', [True, False])
    def test_disable_json(self, disable_field):
        """
        测试 设置 dpr 的值
        """
        settings = FPBrowserSettings()

        clientHints = ClientHints() \
            .set_prefers_color(PrefersColor.DARK) \
            .set_disable(False)

        if disable_field:
            clientHints.append_disable_field(WebClientHintsType.kPrefersColorScheme)

        settings.add_module(clientHints)

        driver, config = get_driver(custom_url="https://1024tools.com/header", custom_config=settings.parse(),
                                    only_custom_config=True)
        self.driver = driver
        self.config = config

        # 获得全部 header
        result = get_all_headers(driver=self.driver)
        value = result.get('sec-ch-prefers-color-scheme')

        setting_value = self.config.get('client-hints.prefers-color')

        print(result)
        print("设置 client hints client-hints-prefers-color 的值:", value, setting_value)
        if disable_field:
            assert value is None
        else:
            assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ['./config/sm-g9600.json', './config/redmi_6a.json'])
    def test_memory(self, value):
        """
        测试 设置 memory 的值
        """
        custom_config = ConfigConvertSetting( config_path=value,
                                             browser_version=get_chromium_major_version()).handle(
            cookie=[],
            real_ip="8.8.8.8",
            connection_type=WebConnectionType.CELLULAR,
            effective_type=WebEffectiveConnectionType.kType4G,
            disable_client_hints=False
        )

        driver, config = get_driver(custom_url="https://1024tools.com/header",
                                    custom_config=custom_config, only_custom_config=True)
        self.driver = driver
        self.config = config

        # 获得全部 header
        result = get_all_headers(driver=self.driver)
        value = result.get('device-memory')
        value2 = result.get('sec-ch-device-memory')

        setting_value = int(self.config.get('navigator.device-memory'))

        print("设置 client hints memory 的值:", value, value2, setting_value)
        assert int(value) == setting_value

        # 如果是小于等于 93 的浏览器版本，则跳过
        chromium_version = get_chromium_major_version()
        if chromium_version is not None and int(chromium_version) <= 93:
            pass
        else:
            assert int(value2) == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ['./config/sm-g9600.json', './config/redmi_6a.json'])
    def test_dpr(self, value):
        """
        测试 设置 dpr 的值
        """
        custom_config = ConfigConvertSetting( config_path=value,
                                             browser_version=get_chromium_major_version()).handle(
            cookie=[],
            real_ip="8.8.8.8",
            connection_type=WebConnectionType.CELLULAR,
            effective_type=WebEffectiveConnectionType.kType4G,
            disable_client_hints=False
        )

        driver, config = get_driver(custom_url="https://1024tools.com/header",
                                    custom_config=custom_config, only_custom_config=True)
        self.driver = driver
        self.config = config

        # 获得全部 header
        result = get_all_headers(driver=self.driver)
        value = result.get('dpr')
        value2 = result.get('sec-ch-dpr')

        setting_value = float(self.config.get('screen.device-pixel-ratio'))

        print(result)
        print("设置 client hints dpr 的值:", value, value2, setting_value)
        assert float(value) == setting_value

        # 如果是小于等于 93 的浏览器版本，则跳过
        chromium_version = get_chromium_major_version()
        if chromium_version is not None and int(chromium_version) <= 93:
            pass
        else:
            assert float(value2) == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ['./config/sm-g9600.json', './config/redmi_6a.json'])
    def test_width(self, value):
        """
        测试 设置 width 的值
        """
        custom_config = ConfigConvertSetting( config_path=value,
                                             browser_version=get_chromium_major_version()).handle(
            cookie=[],
            real_ip="8.8.8.8",
            connection_type=WebConnectionType.CELLULAR,
            effective_type=WebEffectiveConnectionType.kType4G,
            disable_client_hints=False
        )

        driver, config = get_driver(custom_url="https://1024tools.com/header",
                                    custom_config=custom_config, only_custom_config=True)
        self.driver = driver
        self.config = config

        # 获得全部 header
        result = get_all_headers(driver=self.driver)
        value = result.get('viewport-width')
        value2 = result.get('sec-ch-viewport-width')

        setting_value = int(self.config.get('client-hints.viewport-width'))

        print(result)
        print("设置 client hints width 的值:", value, value2, setting_value)
        assert int(value) == setting_value

        # 如果是小于等于 93 的浏览器版本，则跳过
        chromium_version = get_chromium_major_version()
        if chromium_version is not None and int(chromium_version) <= 93:
            pass
        else:
            assert int(value2) == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', ['./config/sm-g9600.json', './config/redmi_6a.json'])
    def test_height(self, value):
        """
        测试 设置 height 的值
        """
        # 如果是小于等于 93 的浏览器版本，则跳过
        chromium_version = get_chromium_major_version()
        if chromium_version is not None and int(chromium_version) <= 93:
            assert True
            return

        custom_config = ConfigConvertSetting( config_path=value,
                                             browser_version=get_chromium_major_version()).handle(
            cookie=[],
            real_ip="8.8.8.8",
            connection_type=WebConnectionType.CELLULAR,
            effective_type=WebEffectiveConnectionType.kType4G,
            disable_client_hints=False
        )

        driver, config = get_driver(custom_url="https://1024tools.com/header",
                                    custom_config=custom_config, only_custom_config=True)
        self.driver = driver
        self.config = config

        # 获得全部 header
        result = get_all_headers(driver=self.driver)
        value = result.get('sec-ch-viewport-height')

        setting_value = int(self.config.get('client-hints.viewport-height'))

        print(result)
        print("设置 client hints height 的值:", value, setting_value)
        assert int(value) == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [WebConnectionType.CELLULAR, WebConnectionType.WIFI])
    def test_rtt(self, value):
        """
        测试 设置 rtt 的值
        """
        custom_config = ConfigConvertSetting( config_path='./config/sm-g9600.json',
                                             browser_version=get_chromium_major_version()).handle(
            cookie=[],
            real_ip="8.8.8.8",
            connection_type=value,
            effective_type=WebEffectiveConnectionType.kType4G,
            disable_client_hints=False
        )

        driver, config = get_driver(custom_url="https://1024tools.com/header",
                                    custom_config=custom_config, only_custom_config=True)
        self.driver = driver
        self.config = config

        # 获得全部 header
        result = get_all_headers(driver=self.driver)
        value = result.get('rtt')

        setting_value = int(self.config.get('connection.rtt'))

        print(result)
        print("设置 client hints rtt 的值:", value, setting_value)
        assert int(value) == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [WebConnectionType.CELLULAR, WebConnectionType.WIFI])
    def test_downlink(self, value):
        """
        测试 设置 downlink 的值
        """
        custom_config = ConfigConvertSetting( config_path='./config/sm-g9600.json',
                                             browser_version=get_chromium_major_version()).handle(
            cookie=[],
            real_ip="8.8.8.8",
            connection_type=value,
            effective_type=WebEffectiveConnectionType.kType4G,
            disable_client_hints=False
        )

        driver, config = get_driver(custom_url="https://1024tools.com/header",
                                    custom_config=custom_config, only_custom_config=True)
        self.driver = driver
        self.config = config

        # 获得全部 header
        result = get_all_headers(driver=self.driver)
        value = result.get('downlink')

        setting_value = float(self.config.get('connection.downlink'))

        print(result)
        print("设置 client hints downlink 的值:", value, setting_value)
        assert float(value) == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [
        WebEffectiveConnectionType.kTypeUnknown,
        WebEffectiveConnectionType.kTypeOffline,
        WebEffectiveConnectionType.kTypeSlow2G,
        WebEffectiveConnectionType.kType2G,
        WebEffectiveConnectionType.kType3G,
        WebEffectiveConnectionType.kType4G,
    ])
    def test_ect(self, value):
        """
        测试 设置 ect 的值
        """
        custom_config = ConfigConvertSetting( config_path='./config/sm-g9600.json',
                                             browser_version=get_chromium_major_version()).handle(
            cookie=[],
            real_ip="8.8.8.8",
            connection_type=WebConnectionType.CELLULAR,
            effective_type=value,
            disable_client_hints=False
        )

        driver, config = get_driver(custom_url="https://1024tools.com/header",
                                    custom_config=custom_config, only_custom_config=True)
        self.driver = driver
        self.config = config

        # 获得全部 header
        result = get_all_headers(driver=self.driver)
        value = result.get('ect')

        setting_value = self.config.get('connection.effective-type')

        print(result)
        print("设置 client hints ect 的值:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [True, False])
    def test_save_data(self, value):
        """
        测试 设置 save_data 的值
        """
        # 如果是小于等于 93 的浏览器版本，则跳过
        chromium_version = get_chromium_major_version()
        if chromium_version is not None and int(chromium_version) <= 93:
            assert True
            return

        settings = FPBrowserSettings()

        network = Network() \
            .set_save_data(value)

        settings.add_module(network)

        clientHints = ClientHints() \
            .set_disable(False)

        settings.add_module(clientHints)

        driver, config = get_driver(custom_url="https://1024tools.com/header", custom_config=settings.parse(),
                                    only_custom_config=True)
        self.driver = driver
        self.config = config

        # 获得全部 header
        result = get_all_headers(driver=self.driver)
        value = result.get('save-data')

        setting_value = int(self.config.get('connection.save-data'))

        print(result)
        print("设置 client hints save_data 的值:", value, setting_value)

        if setting_value == 1:
            assert value == "on"
        else:
            assert value is None

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [PrefersColor.LIGHT, PrefersColor.DARK])
    def test_prefers_color(self, value):
        """
        测试 设置 prefers color 的值
        """
        settings = FPBrowserSettings()

        clientHints = ClientHints() \
            .set_prefers_color(value) \
            .set_disable(False)

        settings.add_module(clientHints)

        driver, config = get_driver(custom_url="https://1024tools.com/header", custom_config=settings.parse(),
                                    only_custom_config=True)
        self.driver = driver
        self.config = config

        # 获得全部 header
        result = get_all_headers(driver=self.driver)
        value = result.get('sec-ch-prefers-color-scheme')

        setting_value = self.config.get('client-hints.prefers-color')

        print(result)
        print("设置 client hints client-hints-prefers-color 的值:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()
