async function func() {
    try {
        const status = await Notification.requestPermission();
        return status
    } catch (e) {
        return false;
    }
}

const value = await func()
return value