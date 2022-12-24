import pytest
from helper.util import get_driver, sleep, get_md5_func, stop_browser_app
from fp_browser_sdk.ext.basic import Basic
from fp_browser_sdk.fp_browser_settings import FPBrowserSettings
from fp_browser_sdk.ext.fingerprint_offset import FingerprintOffset
from fp_browser_sdk.ext.browser_enum import  BaseEnum, TLSVersion, Platform, PrefersColor, \
    CompatMode, MatchType, SpeechSynthesisVoiceAppendMode, PerformanceNavigationType, DoNotTrackType, MaxTouchPoint, \
    ScreenColorDepth, ScreenOrientationType, MediaKind, WebEffectiveConnectionType, WebConnectionType


class TestFingerprint(object):
    def setup_method(self):
        stop_browser_app()

    # @pytest.mark.skip("")
    @pytest.mark.parametrize('offset',
                             [0.919,
                              0.919,
                              0.819,
                              99.819,
                              99.819,
                              19.819,
                              19.818,
                              0.002,
                              0.002,
                              0.001])
    def test_audio(self, offset):
        """
        测试 音频指纹偏移量
        """
        settings = FPBrowserSettings()

        fingerprint_offset = FingerprintOffset() \
            .set_audio_offset(offset) \
            .auto_canvas_offset() \
            .auto_webgl_offset()

        settings.add_module(fingerprint_offset)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        audio_script = """
    /**
     * hash
     * @param arr
     * @returns {number}
     */
    const hash_func = (arr) => {
        let result = "";

        for (let i = 0; i < arr.length; ++i) {
            result += arr[i];
        }

        return md5(result);
    }

    const get_audio_fingerprint = async (callback) => {
        try {
            const audio_ctx = window.OfflineAudioContext || window.webkitOfflineAudioContext;

            if (!audio_ctx) {
                return callback(false);
            }

            const offline_ctx = new audio_ctx(1, 5000, 44100);
            const oscillator = offline_ctx.createOscillator();

            oscillator.type = "triangle";
            oscillator.frequency.value = 10000;

            const compressor = offline_ctx.createDynamicsCompressor();
            compressor.threshold.value = -50;
            compressor.knee.value = 40;
            compressor.ratio.value = 12;
            compressor.attack.value = 0;
            compressor.release.value = 0.25;

            oscillator.connect(compressor);
            compressor.connect(offline_ctx.destination);
            oscillator.start(0);
            //render_audio(offline_ctx, callback);
            offline_ctx.startRendering();
            let result;

            offline_ctx.oncomplete = function (offline_ctx) {
                const buffer = offline_ctx.renderedBuffer;
                result = hash_func(buffer.getChannelData(0).subarray(4500));
            };

            await new Promise(resolve => setTimeout(resolve, 3000));

            return callback(result);
        } catch (e) {
            // console.log(e)
        }
        return callback(false);
    }
        """
        script = get_md5_func() + audio_script + '''
                             async function func() {
                                const result = await get_audio_fingerprint((result) => {
                                    return result
                                })
                        
                                return result;
                            }
                        
                            const hash = await func();
                            return hash;
                          '''

        value = self.driver.execute_script(script)
        setting_value = self.config.get('fingerprint.audio-rand-value')

        print("设置 audio 指纹偏移量,只需要偏移量不一样，对应的指纹不一样就行:", value, setting_value)
        assert value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip("")
    @pytest.mark.parametrize('offset',
                             [0.919,
                              0.919,
                              0.819,
                              99.819,
                              99.819,
                              19.819,
                              19.818,
                              0.002,
                              0.002,
                              0.001])
    def test_canvas(self, offset):
        """
        测试 Canvas 指纹偏移量
        """
        settings = FPBrowserSettings()

        fingerprint_offset = FingerprintOffset() \
            .auto_audio_offset() \
            .set_canvas_offset(offset) \
            .auto_webgl_offset()

        settings.add_module(fingerprint_offset)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = get_md5_func() + '''
                       function func(el)
                       {
                            const canvas = document.createElement("canvas");
                            const ctx = canvas.getContext("2d");

                            ctx.fillStyle = "rgb(255,0,255)";
                            ctx.beginPath();
                            ctx.rect(20, 20, 150, 100);
                            ctx.fill();
                            ctx.stroke();
                            ctx.closePath();
                            ctx.beginPath();
                            ctx.fillStyle = "rgb(0,255,255)";
                            ctx.arc(50, 50, 50, 0, Math.PI * 2, true);
                            ctx.fill();
                            ctx.stroke();
                            ctx.closePath();

                            const txt = 'abz190#$%^@£éú';
                            ctx.textBaseline = "top";
                            ctx.font = '17px "Arial 17"';
                            ctx.textBaseline = "alphabetic";
                            ctx.fillStyle = "rgb(255,5,5)";
                            ctx.rotate(.03);
                            ctx.fillText(txt, 4, 17);
                            ctx.fillStyle = "rgb(155,255,5)";
                            ctx.shadowBlur = 8;
                            ctx.shadowColor = "red";
                            ctx.fillRect(20, 12, 100, 5);

                            // hashing function
                            const src = canvas.toDataURL();
                            return md5(src)
                       }
                       return func();
                   '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('fingerprint.canvas-rand-value')

        print("设置 Canvas 指纹偏移量,只需要偏移量不一样，对应的指纹不一样就行:", value, setting_value)
        assert value

        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip("")
    @pytest.mark.parametrize('value', ['Qualcomm', 'ARM'])
    def test_webgl_vendor(self, value):
        """
        测试 显卡供应商
        """
        settings = FPBrowserSettings()

        basic = Basic() \
            .set_webgl_vendor(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
           function func(el)
           {
              try {
                const canvas = document.createElement("canvas");
                const gl = canvas.getContext('webgl');

                const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
                const vendor = gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL);
                const renderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
                return vendor
            } catch (e) {

            }

            return ''
           }
           return func();
       '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('webgl.vendor')

        print("设置 显卡供应商:", value, setting_value)
        assert value == setting_value
        self.driver.close()
        self.driver.quit()

    # @pytest.mark.skip("")
    @pytest.mark.parametrize('value', ['Mali-G57 MC4', 'Adreno (TM) 640', 'Adreno (TM) 660'])
    def test_webgl_renderer(self, value):
        """
        测试 显卡型号
        """
        settings = FPBrowserSettings()

        basic = Basic() \
            .set_webgl_renderer(value)

        settings.add_module(basic)

        driver, config = get_driver(custom_config=settings.parse(), only_custom_config=True)
        self.driver = driver
        self.config = config

        script = '''
           function func(el)
           {
              try {
                const canvas = document.createElement("canvas");
                const gl = canvas.getContext('webgl');

                const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
                const vendor = gl.getParameter(debugInfo.UNMASKED_VENDOR_WEBGL);
                const renderer = gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
                return renderer
            } catch (e) {

            }

            return ''
           }
           return func();
       '''
        value = self.driver.execute_script(script)
        setting_value = self.config.get('webgl.renderer')

        print("设置 显卡型号:", value, setting_value)
        assert value == setting_value
        self.driver.close()
        self.driver.quit()
