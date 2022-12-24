import json
import numpy
import time
import pytest
from helper.util import get_driver, sleep, format_media_kind, get_chromium_major_version, stop_browser_app
from fp_browser_sdk.ext.basic import Basic
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings
from fp_browser_sdk.ext.media import Media
from fp_browser_sdk.ext.browser_enum import  BaseEnum, TLSVersion, Platform, PrefersColor, \
    CompatMode, MatchType, SpeechSynthesisVoiceAppendMode, PerformanceNavigationType, DoNotTrackType, MaxTouchPoint, \
    ScreenColorDepth, ScreenOrientationType, MediaKind, WebEffectiveConnectionType, WebConnectionType
from fp_browser_sdk import ConfigConvertSetting


class TestMediaDevice(object):
    def setup_method(self):
        stop_browser_app()

    # @pytest.mark.skip()
    def test_media_list(self):
        """
        测试 硬件设备信息
        """
        custom_config = ConfigConvertSetting( config_path='./config/sm-g9600.json',
                                             browser_version=get_chromium_major_version()).handle(
            cookie=[],
            real_ip="8.8.8.8",
            connection_type=WebConnectionType.CELLULAR,
            effective_type=WebEffectiveConnectionType.kType4G
        )

        driver, config = get_driver(custom_config=custom_config, only_custom_config=True)
        self.driver = driver
        self.config = config

        script = """
            async function get_device() {
                return new Promise((res, rej) => {
                    if (navigator.mediaDevices && navigator.mediaDevices.enumerateDevices) {
                        try {
                            navigator.mediaDevices.enumerateDevices().then(function (e) {
                                res(e)
                            }).catch(function (e) {
                                rej(e)
                            })
                        } catch (e) {
                            rej(e)
                        }
                    } else if (window.MediaStreamTrack && window.MediaStreamTrack.getSources) {
                        try {
                            MediaStreamTrack.getSources(function (e) {
                                res(e)
                            })
                        } catch (e) {
                            rej(e)
                        }
                    }
                })
            }
        
            async function func() {
                const mediaDevices = await get_device()
        
                return mediaDevices;
            }
        
            const value = await func()
            return value
        """
        value = self.driver.execute_script(script)
        setting_value = self.config.get('media.list-json', '[]')

        # 格式化获取的设备信息
        format_value = []
        for item in value:
            format_value.append({
                "device_id": item['deviceId'],
                "label": item['label'],
                "group_id": item['groupId'],
                "device_type": format_media_kind(item['kind']),
            })

        print('通过 js 获取的原始的值', value)
        print('格式', format_value)
        print('设置', setting_value)

        assert format_value == setting_value

        self.driver.close()
        self.driver.quit()
