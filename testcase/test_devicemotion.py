import pytest
from helper.util import get_driver, sleep, wait_el, get_title, get_file_script_context, get_chromium_version
from fp_browser_sdk.ext.basic import Basic
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings
from fp_browser_sdk.ext.media import Media
from fp_browser_sdk.ext.browser_enum import  BaseEnum, TLSVersion, Platform, PrefersColor, \
    CompatMode, MatchType, SpeechSynthesisVoiceAppendMode, PerformanceNavigationType, DoNotTrackType, MaxTouchPoint, \
    ScreenColorDepth, ScreenOrientationType, MediaKind, WebEffectiveConnectionType, WebConnectionType
from fp_browser_sdk import ConfigConvertSetting

class TestDevicemotion(object):
    def setup_class(self):
        custom_config = ConfigConvertSetting( config_path='./config/sm-g9600.json',
                                             browser_version=get_chromium_version()).handle(
            cookie=[],
            real_ip="8.8.8.8",
            connection_type=WebConnectionType.CELLULAR,
            effective_type=WebEffectiveConnectionType.kType4G
        )

        driver, config = get_driver(custom_config=custom_config, only_custom_config=True)
        self.driver = driver
        self.config = config

    def teardown_class(self):
        sleep(10)
        self.driver.close()
        self.driver.quit()

    def test_alpha(self):
        """
        测试-alpha 它会在加速度传感器检测到设备在方向上发生变化时触发。
        """
        sleep(10000)

        # todo 需要手动测试
        # 运行当前用例
        # 在 inspect 执行当前 js
        '''
            (async () => {
                let result;
            
                function listen_function(e) {
                    console.log(e)
                    let acceleration = e.accelerationIncludingGravity;
            
                    let x2 = acceleration.x || 0;
                    let y2 = acceleration.y || 0;
                    let z2 = acceleration.z || 0;
            
                    acceleration = e.acceleration;
            
                    let x1 = acceleration.x || 0;
                    let y1 = acceleration.y || 0;
                    let z1 = acceleration.z || 0;
            
                    let rotationRate = e.rotationRate;
            
                    let alpha = rotationRate.alpha || 0;
                    let beta = rotationRate.beta || 0;
                    let gamma = rotationRate.gamma || 0;
            
                    let interval = e.interval;
            
                    result = {
                        x1,
                        y1,
                        z1,
                        x2,
                        y2,
                        z2,
                        alpha,
                        beta,
                        gamma,
                        interval
                    }
            
                    console.log(result)
                    // 触发一次后就停止收集
                    window.removeEventListener('devicemotion', listen_function);
                }
            
                window.addEventListener('devicemotion', listen_function);
            })()
        '''

        '''
        (async () => {
            function get_deviceorientation() {
                let gamma;
                let beta;
                let alpha;
                let absolute;

                window.addEventListener('deviceorientation', function (event) {
                    console.log(event)
                    beta = event.beta || 0;
                    gamma = event.gamma || 0;
                    alpha = event.alpha || 0;
                    absolute = event.absolute;
                })
            }
            get_deviceorientation();
        })()

        '''


"""
"device-motion.x1": "0.1",
"device-motion.y1": "0.1",
"device-motion.z1": "-1.1",
"device-motion.x2": "3",
"device-motion.y2": "6.9",
"device-motion.z2": "5",
"device-motion.alpha": "31.4",
"device-motion.beta": "74",
"device-motion.gamma": "12.1",

alpha: 31.4
beta: 74
gamma: 12.1
interval: 16
x1: 0.1
x2: 3
y1: 0.1
y2: 6.9
z1: -1.1
z2: 5


"device-orientation.alpha": "166.6",
"device-orientation.beta": "45.7",
"device-orientation.gamma": "-25.3",
"device-orientation.absolute": "0",


isTrusted: true
absolute: false
alpha: 166.6
beta: 45.7
bubbles: false
cancelBubble: false
cancelable: false
composed: false
currentTarget: Window {window: Window, self: Window, document: document, name: '', location: Location, …}
defaultPrevented: false
eventPhase: 0
gamma: -25.3
path: [Window]
returnValue: true
srcElement: Window {window: Window, self: Window, document: document, name: '', location: Location, …}
target: Window {window: Window, self: Window, document: document, name: '', location: Location, …}
timeStamp: 70085.79999998212
type: "deviceorientation"
"""