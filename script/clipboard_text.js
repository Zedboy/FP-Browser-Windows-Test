async function func() {
    let text;
    await navigator.permissions.query({name: "clipboard-read"}).then(async (result) => {
        if (result.state == "granted" || result.state == "prompt") {
            text = await navigator.clipboard.readText();
        }
    });

    return text;
}

const value = await func()

return value