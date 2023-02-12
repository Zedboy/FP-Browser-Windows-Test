from exception.config_error_exception import ConfigErrorException
import argparse
import time
from urllib.parse import urlparse
import os
from helper.driver import Driver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException


def parse_params(argparse):
    """
    解析参数
    """
    parser = argparse.ArgumentParser()

    parser.add_argument("-driver_version", "--driver_version", help="Chrome 驱动的版本号", default='102.0.5005.125')
    parser.add_argument("-chrome_port", "--chrome_port", help="chrome 端口 (默认为 0 则表示会自动找一个空闲的端口)", default='0')
    parser.add_argument("-chrome_version", "--chrome_version", help="chrome 版本号", default='102.0.5005.125')
    parser.add_argument("-url", "--url", help="访问的目标链接", default='https://tyua07.github.io/FP-Browser-Detect/')
    parser.add_argument("-chrome_binary_location", "--chrome_binary_location", help="chrome文件位置", default='')
    parser.add_argument("-config", "--config", help="配置信息文件名", default='vivo')

    args = parser.parse_args()
    driver_version = args.driver_version
    chrome_port = int(args.chrome_port)
    chrome_version = args.chrome_version
    url = args.url
    config_name = args.config
    chrome_binary_location = args.chrome_binary_location

    return url, config_name, chrome_port, chrome_version, driver_version, chrome_binary_location


def get_chromium_version():
    """
    获得 chromium 版本号
    """
    url, config_name, chrome_port, chrome_version, driver_version, chrome_binary_location = parse_params(argparse)

    return chrome_version


def get_force_chrome_binary_location():
    """
    获得 chromium 文件
    """
    url, config_name, chrome_port, chrome_version, driver_version, chrome_binary_location = parse_params(argparse)

    return chrome_binary_location


def get_chromium_major_version():
    """
    获得 chromium 主版本号
    """
    url, config_name, chrome_port, chrome_version, driver_version, chrome_binary_location = parse_params(argparse)

    return int(parse_version_number(chrome_version)[0])


def get_config(file):
    """
    获得配置信息
    """
    path = './config/{}.py'.format(file)

    if not os.path.exists(path):
        raise ConfigErrorException()

    module_name = "config.{}".format(file)
    return getattr(__import__(module_name, fromlist=True), "get_config")()
    pass


def get_driver(custom_config: dict = None, custom_url=None, only_custom_config=False, encrypt=True):
    """
    获得驱动
    """
    # 解析参数
    url, config_name, chrome_port, chrome_version, driver_version, chrome_binary_location = parse_params(argparse)

    # 访问目标链接
    if custom_url:
        url = custom_url

    config = get_config(config_name)

    if custom_config:
        if only_custom_config:
            config = custom_config
        else:
            config = merge_dict(config, custom_config)
        config = merge_dict(config, {"url": url})

    driver = Driver.handle(
        driver_version=driver_version,
        chrome_version=chrome_version,
        config=config,
        chrome_port=chrome_port,
        encrypt=encrypt,
        force_chrome_binary_location=chrome_binary_location
    )

    wait_timeout = 60 * 60 * 24
    driver.set_page_load_timeout(wait_timeout)
    driver.implicitly_wait(wait_timeout)

    driver.get(url)

    return driver, config


def merge_dict(dict1, dict2):
    res = {**dict1, **dict2}
    return res


def sleep(seconds: int):
    """
    sleep
    """
    time.sleep(seconds)
    print("sleep:{} seconds".format(str(seconds)))


def format_url(url):
    """
    如果链接后面没有 path，则自动添加一个 /
    """
    if not url:
        return url

    if not urlparse(url).path:
        url += "/"

    return url


def split_cookie(cookie):
    """
    组合 cookie
    """
    result = {}

    if not cookie:
        return result

    cookie = cookie.strip().split(';')

    if cookie and len(cookie) > 0:
        for item in cookie:
            data = item.strip().split('=')

            if data and len(data) == 2:
                result[data[0]] = data[1]

    return result


def get_md5_func():
    """
    获得 md5 js 内容
    """
    md5 = """
            /**
     * [js-md5]{@link https://github.com/emn178/js-md5}
     *
     * @namespace md5
     * @version 0.7.3
     * @author Chen, Yi-Cyuan [emn178@gmail.com]
     * @copyright Chen, Yi-Cyuan 2014-2017
     * @license MIT
     */
    !function(){"use strict";function t(t){if(t)d[0]=d[16]=d[1]=d[2]=d[3]=d[4]=d[5]=d[6]=d[7]=d[8]=d[9]=d[10]=d[11]=d[12]=d[13]=d[14]=d[15]=0,this.blocks=d,this.buffer8=l;else if(a){var r=new ArrayBuffer(68);this.buffer8=new Uint8Array(r),this.blocks=new Uint32Array(r)}else this.blocks=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0];this.h0=this.h1=this.h2=this.h3=this.start=this.bytes=this.hBytes=0,this.finalized=this.hashed=!1,this.first=!0}var r="input is invalid type",e="object"==typeof window,i=e?window:{};i.JS_MD5_NO_WINDOW&&(e=!1);var s=!e&&"object"==typeof self,h=!i.JS_MD5_NO_NODE_JS&&"object"==typeof process&&process.versions&&process.versions.node;h?i=global:s&&(i=self);var f=!i.JS_MD5_NO_COMMON_JS&&"object"==typeof module&&module.exports,o="function"==typeof define&&define.amd,a=!i.JS_MD5_NO_ARRAY_BUFFER&&"undefined"!=typeof ArrayBuffer,n="0123456789abcdef".split(""),u=[128,32768,8388608,-2147483648],y=[0,8,16,24],c=["hex","array","digest","buffer","arrayBuffer","base64"],p="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/".split(""),d=[],l;if(a){var A=new ArrayBuffer(68);l=new Uint8Array(A),d=new Uint32Array(A)}!i.JS_MD5_NO_NODE_JS&&Array.isArray||(Array.isArray=function(t){return"[object Array]"===Object.prototype.toString.call(t)}),!a||!i.JS_MD5_NO_ARRAY_BUFFER_IS_VIEW&&ArrayBuffer.isView||(ArrayBuffer.isView=function(t){return"object"==typeof t&&t.buffer&&t.buffer.constructor===ArrayBuffer});var b=function(r){return function(e){return new t(!0).update(e)[r]()}},v=function(){var r=b("hex");h&&(r=w(r)),r.create=function(){return new t},r.update=function(t){return r.create().update(t)};for(var e=0;e<c.length;++e){var i=c[e];r[i]=b(i)}return r},w=function(t){var e=eval("require('crypto')"),i=eval("require('buffer').Buffer"),s=function(s){if("string"==typeof s)return e.createHash("md5").update(s,"utf8").digest("hex");if(null===s||void 0===s)throw r;return s.constructor===ArrayBuffer&&(s=new Uint8Array(s)),Array.isArray(s)||ArrayBuffer.isView(s)||s.constructor===i?e.createHash("md5").update(new i(s)).digest("hex"):t(s)};return s};t.prototype.update=function(t){if(!this.finalized){var e,i=typeof t;if("string"!==i){if("object"!==i)throw r;if(null===t)throw r;if(a&&t.constructor===ArrayBuffer)t=new Uint8Array(t);else if(!(Array.isArray(t)||a&&ArrayBuffer.isView(t)))throw r;e=!0}for(var s,h,f=0,o=t.length,n=this.blocks,u=this.buffer8;f<o;){if(this.hashed&&(this.hashed=!1,n[0]=n[16],n[16]=n[1]=n[2]=n[3]=n[4]=n[5]=n[6]=n[7]=n[8]=n[9]=n[10]=n[11]=n[12]=n[13]=n[14]=n[15]=0),e)if(a)for(h=this.start;f<o&&h<64;++f)u[h++]=t[f];else for(h=this.start;f<o&&h<64;++f)n[h>>2]|=t[f]<<y[3&h++];else if(a)for(h=this.start;f<o&&h<64;++f)(s=t.charCodeAt(f))<128?u[h++]=s:s<2048?(u[h++]=192|s>>6,u[h++]=128|63&s):s<55296||s>=57344?(u[h++]=224|s>>12,u[h++]=128|s>>6&63,u[h++]=128|63&s):(s=65536+((1023&s)<<10|1023&t.charCodeAt(++f)),u[h++]=240|s>>18,u[h++]=128|s>>12&63,u[h++]=128|s>>6&63,u[h++]=128|63&s);else for(h=this.start;f<o&&h<64;++f)(s=t.charCodeAt(f))<128?n[h>>2]|=s<<y[3&h++]:s<2048?(n[h>>2]|=(192|s>>6)<<y[3&h++],n[h>>2]|=(128|63&s)<<y[3&h++]):s<55296||s>=57344?(n[h>>2]|=(224|s>>12)<<y[3&h++],n[h>>2]|=(128|s>>6&63)<<y[3&h++],n[h>>2]|=(128|63&s)<<y[3&h++]):(s=65536+((1023&s)<<10|1023&t.charCodeAt(++f)),n[h>>2]|=(240|s>>18)<<y[3&h++],n[h>>2]|=(128|s>>12&63)<<y[3&h++],n[h>>2]|=(128|s>>6&63)<<y[3&h++],n[h>>2]|=(128|63&s)<<y[3&h++]);this.lastByteIndex=h,this.bytes+=h-this.start,h>=64?(this.start=h-64,this.hash(),this.hashed=!0):this.start=h}return this.bytes>4294967295&&(this.hBytes+=this.bytes/4294967296<<0,this.bytes=this.bytes%4294967296),this}},t.prototype.finalize=function(){if(!this.finalized){this.finalized=!0;var t=this.blocks,r=this.lastByteIndex;t[r>>2]|=u[3&r],r>=56&&(this.hashed||this.hash(),t[0]=t[16],t[16]=t[1]=t[2]=t[3]=t[4]=t[5]=t[6]=t[7]=t[8]=t[9]=t[10]=t[11]=t[12]=t[13]=t[14]=t[15]=0),t[14]=this.bytes<<3,t[15]=this.hBytes<<3|this.bytes>>>29,this.hash()}},t.prototype.hash=function(){var t,r,e,i,s,h,f=this.blocks;this.first?r=((r=((t=((t=f[0]-680876937)<<7|t>>>25)-271733879<<0)^(e=((e=(-271733879^(i=((i=(-1732584194^2004318071&t)+f[1]-117830708)<<12|i>>>20)+t<<0)&(-271733879^t))+f[2]-1126478375)<<17|e>>>15)+i<<0)&(i^t))+f[3]-1316259209)<<22|r>>>10)+e<<0:(t=this.h0,r=this.h1,e=this.h2,r=((r+=((t=((t+=((i=this.h3)^r&(e^i))+f[0]-680876936)<<7|t>>>25)+r<<0)^(e=((e+=(r^(i=((i+=(e^t&(r^e))+f[1]-389564586)<<12|i>>>20)+t<<0)&(t^r))+f[2]+606105819)<<17|e>>>15)+i<<0)&(i^t))+f[3]-1044525330)<<22|r>>>10)+e<<0),r=((r+=((t=((t+=(i^r&(e^i))+f[4]-176418897)<<7|t>>>25)+r<<0)^(e=((e+=(r^(i=((i+=(e^t&(r^e))+f[5]+1200080426)<<12|i>>>20)+t<<0)&(t^r))+f[6]-1473231341)<<17|e>>>15)+i<<0)&(i^t))+f[7]-45705983)<<22|r>>>10)+e<<0,r=((r+=((t=((t+=(i^r&(e^i))+f[8]+1770035416)<<7|t>>>25)+r<<0)^(e=((e+=(r^(i=((i+=(e^t&(r^e))+f[9]-1958414417)<<12|i>>>20)+t<<0)&(t^r))+f[10]-42063)<<17|e>>>15)+i<<0)&(i^t))+f[11]-1990404162)<<22|r>>>10)+e<<0,r=((r+=((t=((t+=(i^r&(e^i))+f[12]+1804603682)<<7|t>>>25)+r<<0)^(e=((e+=(r^(i=((i+=(e^t&(r^e))+f[13]-40341101)<<12|i>>>20)+t<<0)&(t^r))+f[14]-1502002290)<<17|e>>>15)+i<<0)&(i^t))+f[15]+1236535329)<<22|r>>>10)+e<<0,r=((r+=((i=((i+=(r^e&((t=((t+=(e^i&(r^e))+f[1]-165796510)<<5|t>>>27)+r<<0)^r))+f[6]-1069501632)<<9|i>>>23)+t<<0)^t&((e=((e+=(t^r&(i^t))+f[11]+643717713)<<14|e>>>18)+i<<0)^i))+f[0]-373897302)<<20|r>>>12)+e<<0,r=((r+=((i=((i+=(r^e&((t=((t+=(e^i&(r^e))+f[5]-701558691)<<5|t>>>27)+r<<0)^r))+f[10]+38016083)<<9|i>>>23)+t<<0)^t&((e=((e+=(t^r&(i^t))+f[15]-660478335)<<14|e>>>18)+i<<0)^i))+f[4]-405537848)<<20|r>>>12)+e<<0,r=((r+=((i=((i+=(r^e&((t=((t+=(e^i&(r^e))+f[9]+568446438)<<5|t>>>27)+r<<0)^r))+f[14]-1019803690)<<9|i>>>23)+t<<0)^t&((e=((e+=(t^r&(i^t))+f[3]-187363961)<<14|e>>>18)+i<<0)^i))+f[8]+1163531501)<<20|r>>>12)+e<<0,r=((r+=((i=((i+=(r^e&((t=((t+=(e^i&(r^e))+f[13]-1444681467)<<5|t>>>27)+r<<0)^r))+f[2]-51403784)<<9|i>>>23)+t<<0)^t&((e=((e+=(t^r&(i^t))+f[7]+1735328473)<<14|e>>>18)+i<<0)^i))+f[12]-1926607734)<<20|r>>>12)+e<<0,r=((r+=((h=(i=((i+=((s=r^e)^(t=((t+=(s^i)+f[5]-378558)<<4|t>>>28)+r<<0))+f[8]-2022574463)<<11|i>>>21)+t<<0)^t)^(e=((e+=(h^r)+f[11]+1839030562)<<16|e>>>16)+i<<0))+f[14]-35309556)<<23|r>>>9)+e<<0,r=((r+=((h=(i=((i+=((s=r^e)^(t=((t+=(s^i)+f[1]-1530992060)<<4|t>>>28)+r<<0))+f[4]+1272893353)<<11|i>>>21)+t<<0)^t)^(e=((e+=(h^r)+f[7]-155497632)<<16|e>>>16)+i<<0))+f[10]-1094730640)<<23|r>>>9)+e<<0,r=((r+=((h=(i=((i+=((s=r^e)^(t=((t+=(s^i)+f[13]+681279174)<<4|t>>>28)+r<<0))+f[0]-358537222)<<11|i>>>21)+t<<0)^t)^(e=((e+=(h^r)+f[3]-722521979)<<16|e>>>16)+i<<0))+f[6]+76029189)<<23|r>>>9)+e<<0,r=((r+=((h=(i=((i+=((s=r^e)^(t=((t+=(s^i)+f[9]-640364487)<<4|t>>>28)+r<<0))+f[12]-421815835)<<11|i>>>21)+t<<0)^t)^(e=((e+=(h^r)+f[15]+530742520)<<16|e>>>16)+i<<0))+f[2]-995338651)<<23|r>>>9)+e<<0,r=((r+=((i=((i+=(r^((t=((t+=(e^(r|~i))+f[0]-198630844)<<6|t>>>26)+r<<0)|~e))+f[7]+1126891415)<<10|i>>>22)+t<<0)^((e=((e+=(t^(i|~r))+f[14]-1416354905)<<15|e>>>17)+i<<0)|~t))+f[5]-57434055)<<21|r>>>11)+e<<0,r=((r+=((i=((i+=(r^((t=((t+=(e^(r|~i))+f[12]+1700485571)<<6|t>>>26)+r<<0)|~e))+f[3]-1894986606)<<10|i>>>22)+t<<0)^((e=((e+=(t^(i|~r))+f[10]-1051523)<<15|e>>>17)+i<<0)|~t))+f[1]-2054922799)<<21|r>>>11)+e<<0,r=((r+=((i=((i+=(r^((t=((t+=(e^(r|~i))+f[8]+1873313359)<<6|t>>>26)+r<<0)|~e))+f[15]-30611744)<<10|i>>>22)+t<<0)^((e=((e+=(t^(i|~r))+f[6]-1560198380)<<15|e>>>17)+i<<0)|~t))+f[13]+1309151649)<<21|r>>>11)+e<<0,r=((r+=((i=((i+=(r^((t=((t+=(e^(r|~i))+f[4]-145523070)<<6|t>>>26)+r<<0)|~e))+f[11]-1120210379)<<10|i>>>22)+t<<0)^((e=((e+=(t^(i|~r))+f[2]+718787259)<<15|e>>>17)+i<<0)|~t))+f[9]-343485551)<<21|r>>>11)+e<<0,this.first?(this.h0=t+1732584193<<0,this.h1=r-271733879<<0,this.h2=e-1732584194<<0,this.h3=i+271733878<<0,this.first=!1):(this.h0=this.h0+t<<0,this.h1=this.h1+r<<0,this.h2=this.h2+e<<0,this.h3=this.h3+i<<0)},t.prototype.hex=function(){this.finalize();var t=this.h0,r=this.h1,e=this.h2,i=this.h3;return n[t>>4&15]+n[15&t]+n[t>>12&15]+n[t>>8&15]+n[t>>20&15]+n[t>>16&15]+n[t>>28&15]+n[t>>24&15]+n[r>>4&15]+n[15&r]+n[r>>12&15]+n[r>>8&15]+n[r>>20&15]+n[r>>16&15]+n[r>>28&15]+n[r>>24&15]+n[e>>4&15]+n[15&e]+n[e>>12&15]+n[e>>8&15]+n[e>>20&15]+n[e>>16&15]+n[e>>28&15]+n[e>>24&15]+n[i>>4&15]+n[15&i]+n[i>>12&15]+n[i>>8&15]+n[i>>20&15]+n[i>>16&15]+n[i>>28&15]+n[i>>24&15]},t.prototype.toString=t.prototype.hex,t.prototype.digest=function(){this.finalize();var t=this.h0,r=this.h1,e=this.h2,i=this.h3;return[255&t,t>>8&255,t>>16&255,t>>24&255,255&r,r>>8&255,r>>16&255,r>>24&255,255&e,e>>8&255,e>>16&255,e>>24&255,255&i,i>>8&255,i>>16&255,i>>24&255]},t.prototype.array=t.prototype.digest,t.prototype.arrayBuffer=function(){this.finalize();var t=new ArrayBuffer(16),r=new Uint32Array(t);return r[0]=this.h0,r[1]=this.h1,r[2]=this.h2,r[3]=this.h3,t},t.prototype.buffer=t.prototype.arrayBuffer,t.prototype.base64=function(){for(var t,r,e,i="",s=this.array(),h=0;h<15;)t=s[h++],r=s[h++],e=s[h++],i+=p[t>>>2]+p[63&(t<<4|r>>>4)]+p[63&(r<<2|e>>>6)]+p[63&e];return t=s[h],i+=p[t>>>2]+p[t<<4&63]+"=="};var _=v();f?module.exports=_:(i.md5=_,o&&define(function(){return _}))}();
            """
    return md5


def get_file_script_context(file):
    """
    读取 js 内容
    """
    with open(file, encoding="utf8") as f:
        context = f.read()
        f.close()
        return context


def format_media_kind(kind):
    """
    格式化设备媒体的类型
    """
    if kind == 'audioinput':
        return "0"

    if kind == 'audiooutput':
        return "1"

    if kind == 'videoinput':
        return "2"

    return None


def get_title(driver):
    """
    获得 title
    """
    script = '''
                               function func(el)
                               {
                                    return document.title
                               }
                               return func();
                           '''
    return driver.execute_script(script)


def get_permission_query_name(permission_type):
    """
    把枚举类型转换成字符串(针对 query 的 name)
    """
    permission_type = int(permission_type)
    if permission_type == 4:
        return "geolocation"
    elif permission_type == 5:
        return "notifications"
    elif permission_type == 5:
        return "push"
    elif permission_type == 27:
        return "midi"
    elif permission_type == 9:
        return "camera"
    elif permission_type == 8:
        return "microphone"
    elif permission_type == 36:
        return "background-fetch"
    elif permission_type == 21:
        return "background-sync"
    elif permission_type == 18:
        return "persistent-storage"
    elif permission_type == 32:
        # 都属于传感器系列
        return "ambient-light-sensor"
    elif permission_type == 32:
        # 都属于传感器系列
        return "accelerometer"
    elif permission_type == 32:
        # 都属于传感器系列
        return "gyroscope"
    elif permission_type == 32:
        # 都属于传感器系列
        return "magnetometer"
    elif permission_type == 46:
        return "screen-wake-lock"
    elif permission_type == 51:
        return "nfc"
    elif permission_type == 66:
        return "display-capture"
    elif permission_type == 33:
        return "accessibility-events"
    elif permission_type == 53:
        return "clipboard-read"
    elif permission_type == 53:
        return "clipboard-write"
    elif permission_type == 34:
        return "payment-handler"
    elif permission_type == 38:
        return "idle-detection"
    elif permission_type == 42:
        return "periodic-background-sync"
    elif permission_type == 47:
        return "system-wake-lock"
    elif permission_type == 59:
        return "storage-access"
    elif permission_type == 61:
        return "window-placement"
    elif permission_type == 63:
        return "local-fonts"
    else:
        return ""


def parse_version_number(version_name):
    """
    解析版本号
    """
    return version_name.split('.')


def get_all_headers(driver):
    """
    获得全部 header
    """
    script = '''
                       function func(el)
                       {    
                           const text = document.querySelector('#content > div:nth-child(2) > div:nth-child(1) > textarea').innerHTML
                           return text;
                       }
                       return func();
                   '''
    value = driver.execute_script(script)
    result = {}
    if value:
        value = value.split("\n")
        if value and len(value) > 0:
            for item in value:
                item = item.split(": ")
                if item and len(item) == 2:
                    [key, val] = item
                    result[key.lower()] = val

    return result


def get_match_item(config):
    """
    获得 document 多重匹配的值
    """
    url = config.get("url")
    result = config.get("document.match-json")
    current = None

    for item in result:
        is_full = int(item["match_type"]) == 1

        if is_full:
            if item["target_url"] == url:
                current = item
                break
        else:
            url_parse = urlparse(url)
            target_domain_parse = urlparse(item["target_url"])

            if url_parse.hostname == target_domain_parse.hostname and url_parse.path == target_domain_parse.path:
                current = item
                break

    return current


def wait_el(driver, selector, timeout=3):
    try:
        wait = WebDriverWait(driver, timeout=timeout, poll_frequency=1,
                             ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException])
        element = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
        if element is not False:
            return True
    except:
        pass

    return False


def stop_browser_app():
    pass
