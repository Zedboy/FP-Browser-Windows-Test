import pytest
from helper.util import get_driver, sleep
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings
from fp_browser_sdk.ext.battery import Battery
from fp_browser_sdk.ext.browser_enum import BaseEnum, TLSVersion, Platform, PrefersColor, \
    CompatMode, MatchType, SpeechSynthesisVoiceAppendMode, PerformanceNavigationType, DoNotTrackType, MaxTouchPoint, \
    ScreenColorDepth, ScreenOrientationType, MediaKind, WebEffectiveConnectionType, WebConnectionType, Floatinfinity


class TestBattery(object):

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [True, False])
    def test_charging(self, value):
        """
        测试 是否正在充电「1：true; 0：false」
        """
        settings = FPBrowserSettings()

        battery = Battery() \
            .set_charging(value)

        settings.add_module(battery)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
                        async function func() {
                            const battery = await window.navigator.getBattery()
                    
                            return battery.charging;
                        }
                    
                        const value = await func()
                        return value
                   '''
        value = self.driver.execute_script(script)
        setting_value = int(self.config.get('battery-manager.charging')) == 1

        print("设置 是否正在充电「1：true; 0：false」:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [100, 1, 0, Floatinfinity.INFINITY.value])
    def test_charging_time(self, value):
        """
        测试 距离充电完毕还需多少秒，如果为0则充电完毕
        """
        settings = FPBrowserSettings()

        battery = Battery() \
            .set_charging_time(value)

        settings.add_module(battery)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
                                async function func() {
                                    const battery = await window.navigator.getBattery()

                                    return battery.chargingTime;
                                }

                                const value = await func()
                                return value
                           '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('battery-manager.charging-time')

        if setting_value == Floatinfinity.INFINITY.value:
            setting_value = None
        else:
            setting_value = float(setting_value)

        print("设置 距离充电完毕还需多少秒，如果为0则充电完毕:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [100, 1, 0])
    def test_discharging_time(self, value):
        """
        测试 距离电池耗电至空且挂起需要多少秒
        """
        settings = FPBrowserSettings()

        battery = Battery() \
            .set_discharging_time(value)

        settings.add_module(battery)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
                                        async function func() {
                                            const battery = await window.navigator.getBattery()

                                            return battery.dischargingTime;
                                        }

                                        const value = await func()
                                        return value
                                   '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('battery-manager.discharging-time')

        if setting_value == Floatinfinity.INFINITY.value:
            setting_value = None
        else:
            setting_value = float(setting_value)

        print("设置 距离电池耗电至空且挂起需要多少秒:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip()
    @pytest.mark.parametrize('value', [100, 0, 78])
    def test_level(self, value):
        """
        测试 电量（单位是两位小数。例如：0.28 代表百分之 28 的电量。最大为 1，代表百分之百电量。）
        """
        settings = FPBrowserSettings()

        battery = Battery() \
            .set_level(value)

        settings.add_module(battery)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
                                                async function func() {
                                                    const battery = await window.navigator.getBattery()

                                                    return battery.level;
                                                }

                                                const value = await func()
                                                return value
                                           '''
        value = self.driver.execute_script(script)
        setting_value = float(self.config.get('battery-manager.level'))

        print("设置 电量（单位是两位小数。例如：0.28 代表百分之 28 的电量。最大为 1，代表百分之百电量。）:", value, setting_value)
        assert value == setting_value

        self.driver.close()
        self.driver.quit()
