var constraints = {audio: true, video: {width: 1280, height: 720}};
// var constraints = {audio: true};
// var constraints = {video: {width: 1280, height: 720}};

async function func() {
    let result;
    try {
        await navigator.mediaDevices.getUserMedia(constraints)
            .then(function (mediaStream) {
                result = mediaStream;
            })
        return result;
    } catch (e) {
        return false;
    }
}

const value = await func()
return value