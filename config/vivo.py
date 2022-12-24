def get_config():
    config = {
        "global-disable-settings": 0,

        'basic-timezone': 'Asia/Shanghai',  # 'Asia/Shanghai',
        #  ja3
        'basic-ja3': '',
        'basic-disable-window-chrome': '0',
        # 初始化历史记录数量
        'basic-init-history-length': '100',

        # 注入 js
        'basic-inject-js': {
            "load": [
                # "(function(){"
                # "const newProto = navigator.__proto__;"
                # "delete newProto.webdriver;"
                # "navigator.__proto__ = newProto;"
                # "})()",
                # "delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;",
                # "delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;",
                # "delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;",
                # "delete document.$cdc_asdjflasutopfhvcZLmcfl_;",
                # "delete document.$chrome_asyncScriptInfo;",
            ]
        },

        # 注入 js(由系统控制，不允许客户端注入)
        'basic-inject-system-js': {
            "load": [
                # "(function(){"
                # "alert('12121');"
                # "const newProto = navigator.__proto__;"
                # "delete newProto.webdriver;"
                # "navigator.__proto__ = newProto;"
                # "})()",
                # "delete window.cdc_adoQpoasnfa76pfcZLmcfl_Array;",
                # "delete window.cdc_adoQpoasnfa76pfcZLmcfl_Promise;",
                # "delete window.cdc_adoQpoasnfa76pfcZLmcfl_Symbol;",
                # "delete document.$cdc_asdjflasutopfhvcZLmcfl_;",
                # "delete document.$chrome_asyncScriptInfo;",
            ]
        },

        # 直接允许的权限
        'basic-allow-permissions': [

        ],
        # 直接拒绝的权限
        'basic-reject-permissions': [

        ],

        # 字体相关
        'font-list-json': [
            "Marlett",
            "Academy Engraved LET",
            "Adobe Garamond",
            "ZWAdobeF",
            "微软雅黑"
        ],

        # frame 相关
        'frame-disable-alert': 0,
        'frame-confirm': 0,
        'frame-disable-window-open': 0,

        # ua
        'navigator-user-agent': 'Mozilla/5.0 (Linux; Android 11; vivo X22A Build/PKQ1.180819.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/98.0.3440.91 Mobile Safari/537.36',
        # x-requested-with
        'header-x-requested-with': 'com.xunmeng.pinduoduo',
        # 额外的 header
        'header-extra-json': [
            {
                "name": "header1",
                "value": "value1"
            },
            {
                "name": "header2",
                "value": "value2"
            }
        ],

        # media
        'media-list-json': [
            {
                "device_id": "11123",
                "label": "11234",
                "group_id": "11456",
                "device_type": "0",  # AUDIO_INPUT
            },
            {
                "device_id": "2123",
                "label": "2234",
                "group_id": "2456",
                "device_type": "1",  # AUDIO_OUTPUT
            },
            {
                "device_id": "3123",
                "label": "3234",
                "group_id": "3456",
                "device_type": "2",  # VIDEO_INPUT
            }
        ],

        # 媒体查询设置
        'media-matchs-json': [
            "color-gamut:srgb",
            "forced-colors:none",
            "dynamic-range:standard",
            "prefers-contrast:no-preference",
            "inverted-colors:inverted",
        ],

        'document-is-trusted': 1,
        'document-global-match-title': '最痛苦0-1!归化球员5分钟内乌龙+红牌 或无缘世界杯|红牌|世界杯|马里|西萨科_手机网易网',
        # 'document-global-match-target-url': '192.168.0.100',
        'document-global-match-target-url': 'so.com',
        # 'document-global-match-target-url': 'ly.so.com',
        # 'document-global-match-target-url': '小度.中国',
        # 'document-global-match-target-url': 'www.yalala.com',
        'document-global-match-current-url': 'https://3g.163.com/sports/article/H3CC1DJ300058781.html',
        'document-global-match-referrer': 'https://m.baidu.com',
        'document-global-skip-current-url-header': '0',
        # 'document-global-match-referrer': '',
        # 'document-match-json': [
        #     {
        #         "target_domain": "https://ly.so.com/?src=m_home",
        #         "is_full": "0",
        #         "current_url": "https://3g.163.com/",
        #         "referrer": "https://m.baidu.com/1234",
        #         "title": " you",
        #     },
        # ],
        'document-compat-mode': 'CSS1Compat',
        # 'document-compat-mode': 'BackCompat',
        'document-video-support-mime-types-json': [
            {
                "type": 'video/test',
                "support": "maybe",
            },
            {
                "type": 'video/ogg; codecs="theora"',
                # "type": urllib.parse.quote_plus('video/ogg'),
                "support": "maybe",
            }
        ],

        'navigator-webdriver-status': '1',
        'navigator-platform': 'Linux aarch64',  # 'Linux armv8l',
        'navigator-vendor': 'Apple Computer, Inc.',  # Apple Computer, Inc. Google Inc.
        'navigator-online': '1',
        'navigator-max-touch-points': 5,
        'navigator-hardware-concurrency': 6,
        'navigator-device-memory': 8,
        # 'navigator-do-not-track': "unspecified",
        'navigator-performance-type': 0,
        'navigator-language': 'zh-cn',
        'navigator-languages': ','.join([
            'zh-cn',
            'zh',
            'en',
        ]),
        'navigator-java-enabled': 1,
        'navigator-pdf-viewer-enabled': 1,
        'navigator-bluetooth-availability': 0,
        # 是否开启插件，如果不开启，则永远返回空
        'navigator-enable-plugin': 0,
        # 是否开启默认浏览器自带的插件（只有 enable_plugin 设置为 1，该属性才生效）
        'navigator-enable-fake-plugin': 0,
        # 注入的 插件
        'navigator-plugin-json': [
            {
                "name": "pdf",
                "filename": "pdf filename",
                "description": "pdf description",
                "mime_types": [
                    {
                        "name": "pdf/types",
                        "description": "pdf description",
                        "extensions": [
                            "pdf1",
                        ],
                    },
                    {
                        "name": "pdf2/types",
                        "description": "pdf2 description",
                        "extensions": [
                            "pdf2",
                        ],
                    }
                ],
            }
        ],

        'cookie-status': '1',
        'cookie-json': [
            {
                "port": "80",
                "domain": ".so.com",
                "name": "name2",
                "value": "aaaaa2"
            },
            {
                "port": "80",
                "domain": ".so.com",
                "name": "name3",
                "value": "aaaaa3"
            },
            {
                "port": "80",
                "domain": "192.168.0.100",
                "name": "name3",
                "value": "aaaaa3"
            },
            {
                "port": "80",
                "domain": ".yalala.com",
                "name": "yalala1",
                "value": "yalala11"
            },
            {
                "port": "80",
                "domain": ".yalala.com",
                "name": "yalala2",
                "value": "yalala22"
            },
            {
                "port": "80",
                "domain": ".sm.cn",
                "name": "从",
                "value": "哪里"
            },
        ],

        'battery-manager-charging': 1,
        'battery-manager-charging-time': "90",
        'battery-manager-discharging-time': "-infinity",
        'battery-manager-level': 0.19,

        # 4g
        'connection-effective-type': '4g',
        'connection-type': 'cellular',
        'connection-downlink': '1.67',
        'connection-downlink-max': '1',
        'connection-rtt': '99',
        'connection-save-data': '0',

        # wifi
        # 'connection-effective-type': '4g',
        # 'connection-type': 'wifi',
        # 'connection-downlink': '1.73',
        # 'connection-downlink-max': 'infinity',
        # 'connection-rtt': '99',
        # 'connection-save-data': '0',

        'webrtc-privite-ip': '192.168.0.10',
        'webrtc-public-ip': '8.8.8.9',
        'webrtc-host-name': ' you',

        'fingerprint-audio-rand-value': '0.93',
        'fingerprint-canvas-rand-value': '0.331',
        'fingerprint-webgl-rand-value': '0.991',

        'webgl-vendor': 'Qualcomm',
        'webgl-renderer': 'Adreno (TM) 618',

        'device-motion-x1': 57.18197488483892,
        'device-motion-x1-left': 0.2,
        'device-motion-x1-right': 0.5,
        'device-motion-y1': 58.221763387241076,
        'device-motion-y1-left': 0.1,
        'device-motion-y1-right': 0.2,
        'device-motion-z1': 59.19596650622097,
        'device-motion-z1-left': 0.4,
        'device-motion-z1-right': 0.8,

        'device-motion-x2': 67.18197488483892,
        'device-motion-x2-left': 0.1,
        'device-motion-x2-right': 0.2,
        'device-motion-y2': 68.221763387241076,
        'device-motion-y2-left': 0.1,
        'device-motion-y2-right': 0.2,
        'device-motion-z2': 69.19596650622097,
        'device-motion-z2-left': 0.1,
        'device-motion-z2-right': 0.2,

        'device-motion-alpha': 77.18197488483892,
        'device-motion-alpha-left': 0.1,
        'device-motion-alpha-right': 0.2,
        'device-motion-beta': 78.221763387241076,
        'device-motion-beta-left': 0.1,
        'device-motion-beta-right': 0.2,
        'device-motion-gamma': 79.19596650622097,
        'device-motion-gamma-left': 0.1,
        'device-motion-gamma-right': 0.2,

        'device-orientation-alpha': 87.18197488483892,
        'device-orientation-alpha-left': 0.1,
        'device-orientation-alpha-right': 0.2,
        'device-orientation-beta': 88.221763387241076,
        'device-orientation-beta-left': 0.1,
        'device-orientation-beta-right': 0.2,
        'device-orientation-gamma': 89.19596650622097,
        'device-orientation-gamma-left': 0.1,
        'device-orientation-gamma-right': 0.2,
        'device-orientation-absolute': 1,

        # 正常
        'rect-width': 414,
        'rect-height': 700,
        'rect-scale-factor': 2.625,  # 该值固定（手机原始获取的值，不能修改）,获取方法：window.devicePixelRatio

        # 竖屏
        'screen-width': '500',
        'screen-height': '900',
        'screen-avail-width': '500',
        'screen-avail-height': '900',
        'screen-avail-left': '0',
        'screen-avail-top': '0',
        'screen-orientation-angle': '270',
        'screen-orientation-type': 'landscape-primary',
        'screen-color-depth': '32',
        # 'screen-device-pixel-ratio': '2.625',
        'screen-device-pixel-ratio': '3.0',

        # 横屏
        # 'screen-width': '846',
        # 'screen-height': '412',
        # 'screen-avail-width': '846',
        # 'screen-avail-height': '412',
        # 'screen-avail-left': '0',
        # 'screen-avail-top': '0',
        # 'screen-orientation-angle': '90',
        # 'screen-orientation-type': 'portrait-secondary',

        'memoryinfo-total-js': 74301723,
        'memoryinfo-used-js': 83349654,
        'memoryinfo-limit-js': 4294705155,

        # {
        #     "coords": {
        #         "accuracy": 5,
        #         "altitude": 5,
        #         "altitudeAccuracy": null,
        #         "heading": 0,
        #         "latitude": 31.193964,
        #         "longitude": 121.320081,
        #         "speed": 0
        #     },
        #     "timestamp": 1657038076489
        # }
        "geo-longitude": "113.219875",
        "geo-latitude": "23.401172",
        'geo-accuracy': 14,
        "geo-altitude": 13,
        "geo-altitude-accuracy": 12,
        "geo-heading": 11,
        "geo-speed": 15,

        "version-info-number": "89.0.0.4389",
        "version-info-product-name": "Google Chrome",

        "client-hints-disable": "0",
        "client-hints-mobile": "0",
        "client-hints-platform": "test platform",
        "client-hints-platform-version": "test platform-version",
        "client-hints-architecture": "test architecture",
        "client-hints-bitness": "test bitness",
        "client-hints-wow64": "1",
        "client-hints-model": "iphone",
        # "client-hints-full-version": "103.0.5060.71",
        "client-hints-full-version": "89.0.0.4389",
        "client-hints-viewport-width": "800",
        "client-hints-viewport-height": "300",
        "client-hints-prefers-color": "dark",  # dark or light

        "clipboard-text": " 有有！！！。。。撒18289。。kii",

        "speech-synthesis-voice-force-override": 0,  # 是否覆盖老的的语音合成数据
        "speech-synthesis-voice-append-mode": 'insert',  # 追加方式：push：尾部追加；insert：顶部追加
        "speech-synthesis-voice-json": [  # 注入新的语音合成数据
            {
                "name": "name",
                "lang": "lang",
                "is_local_service": "0",  # 需要强制设置成字符串
            }
        ],

        "ja3-min-version": "tls1.2",
        "ja3-max-version": "tls1.3",
        # "JA3-CIPHER-SUITES": [
        #     "0x1301"
        # ]
    }

    return config
