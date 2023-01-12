## 联系我
微信: @tyua07

![wechat](https://github.com/tyua07/FP-Browser-Detect/raw/master/docs/wechat.jpg)

## 项目介绍

指纹浏览器（For Windows）全部选项的测试用例

>注意：该项目已经完成全部测试，免费的 Windows 指纹浏览器项目请访问 [FP-Browser-Windows-Public 指纹浏览器（For Windows）免费公开项目](https://github.com/tyua07/FP-Browser-Windows-Public) 。

## 相关开源项目
* [FP-Browser-Public 浏览器底层动态注入](https://github.com/tyua07/FP-Browser-Public) 
* [FP-Browser-Detect 浏览器属性检测](https://github.com/tyua07/FP-Browser-Detect)
* [FP-Browser-SDK 浏览器属性注入参数 SDK](https://github.com/tyua07/FP-Browser-SDK)
* [FP-Browser-Test 指纹浏览器（For Android）全部选项的测试用例](https://github.com/tyua07/FP-Browser-Test)
* [FP-Browser-Windows-Test 指纹浏览器（For Windows）全部选项的测试用例](https://github.com/tyua07/FP-Browser-Windows-Test)
* [FP-Browser-Windows-Public 指纹浏览器（For Windows）免费公开项目](https://github.com/tyua07/FP-Browser-Windows-Public)
## 测试用例列表

```python
from helper.util import get_driver, sleep
import pytest
import warnings

if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=DeprecationWarning)
    # 测试 chrome driver
    pytest.main(["-s", "-v", "--report=chrome_driver.html", '--template=2', "testcase/test_chrome_driver.py"])

    # 测试 basic
    pytest.main(["-s", "-v", "--report=basic.html", '--template=2', "testcase/test_basic.py"])

    # # 测试字体
    pytest.main(["-s", "-v", "--report=font.html", '--template=2', "testcase/test_font.py"])

    # 测试注入 js
    pytest.main(["-s", "-v", "--report=inject_js.html", '--template=2', "testcase/test_inject_js.py"])

    # 测试电量
    pytest.main(["-s", "-v", "--report=battery.html", '--template=2', "testcase/test_battery.py"])

    # 测试 navigation
    pytest.main(["-s", "-v", "--report=navigator.html", '--template=2', "testcase/test_navigator.py"])

    # 测试性能
    pytest.main(["-s", "-v", "--report=performance.html", '--template=2', "testcase/test_performance.py"])

    # 测试剪切板
    pytest.main(["-s", "-v", "--report=clipboard.html", '--template=2', "testcase/test_clipboard.py"])

    # 测试语音合成
    pytest.main(["-s", "-v", "--report=speech_synthesis_voice.html", '--template=2', "testcase/test_speech_synthesis_voice.py"])

    # 测试 navigator userAgent data
    pytest.main(["-s", "-v", "--report=navigator_user_agent_data.html", '--template=2', "testcase/test_navigator_user_agent_data.py"])

    # 测试 浏览器插件
    pytest.main(["-s", "-v", "--report=fake_plugin.html", '--template=2', "testcase/test_fake_plugin.py"])

    # 测试内存
    pytest.main(["-s", "-v", "--report=memoryinfo.html", '--template=2', "testcase/test_memoryinfo.py"])

    # 测试 screen
    pytest.main(["-s", "-v", "--report=screen.html", '--template=2', "testcase/test_screen.py"])

    # 测试 rect
    pytest.main(["-s", "-v", "--report=rect.html", '--template=2', "testcase/test_rect.py"])
    #
    # 测试 document test_document
    pytest.main(["-s", "-v", "--report=document.html", '--template=2', "testcase/test_document.py"])

    # 测试多重匹配
    pytest.main(["-s", "-v", "--report=document_target_match_json.html", '--template=2', "testcase/test_document_target_match_json.py"])

    # 测试 header
    pytest.main(["-s", "-v", "--report=header.html", '--template=2', "testcase/test_header.py"])

    # 测试 client hints
    pytest.main(["-s", "-v", "--report=client_hints.html", '--template=2', "testcase/test_client_hints.py"])

    # 测试 cookie
    pytest.main(["-s", "-v", "--report=cookie.html", '--template=2', "testcase/test_cookie.py"])

    # 测试网络
    pytest.main(["-s", "-v", "--report=network.html", '--template=2', "testcase/test_network.py"])

    # 测试 webrtc
    pytest.main(["-s", "-v", "--report=webrtc.html", '--template=2', "testcase/test_webrtc.py"])

    # 测试 media match
    pytest.main(["-s", "-v", "--report=media_match.html", '--template=2', "testcase/test_media_match.py"])

    # 测试 media 设备信息
    pytest.main(["-s", "-v", "--report=media_device.html", '--template=2', "testcase/test_media_device.py"])

    # 测试 frame
    pytest.main(["-s", "-v", "--report=frame.html", '--template=2', "testcase/test_frame.py"])

    # 测试权限查询
    pytest.main(["-s", "-v", "--report=permission_query.html", '--template=2', "testcase/test_permission_query.py"])

    # 测试权限
    pytest.main(["-s", "-v", "--report=permission.html", '--template=2', "testcase/test_permission.py"])

    # 测试 geo 坐标拾取器 https://lbs.amap.com/tools/picker
    pytest.main(["-s", "-v", "--report=geo.html", '--template=2', "testcase/test_geo.py"])

    # 测试指纹
    pytest.main(["-s", "-v", "--report=fingerprint.html", '--template=2', "testcase/test_fingerprint.py"])

    # 测试 webgl 指纹
    pytest.main(["-s", "-v", "--report=webgl_fingerprint.html", '--template=2', "testcase/test_webgl_fingerprint.py"])

    # 测试 ja3
    pytest.main(["-s", "-v", "--report=ssl.html", '--template=2', "testcase/test_ssl.py"])

    # 测试 document iframe 里的 referer
    pytest.main(["-s", "-v", "--report=document.html", '--template=2', "testcase/test_document_iframe.py"])

    # 测试 rect
    pytest.main(["-s", "-v", "--report=rect.html", '--template=2', "testcase/test_rect.py"])
#
```