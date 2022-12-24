async function func() {
    let result;
    try {
        await navigator.userAgentData.getHighEntropyValues(["brands", "mobile", "platform", "platformVersion", "architecture", "bitness", "wow64", "model",
            "uaFullVersion", "fullVersionList"]).then(res => {
            result = res;
        })
        return result;
    } catch (e) {
        return false;
    }
}

const value = await func()
return value