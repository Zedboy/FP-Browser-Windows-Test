function getPosition() {
    try {
        return new Promise((res, rej) => {
            navigator.geolocation.getCurrentPosition(res, rej, {});
        });
    } catch (e) {
        return false;
    }
}

async function func() {
    try {
        const position = await getPosition();
        return position
    } catch (e) {
        return false;
    }
}

const value = await func()
return value