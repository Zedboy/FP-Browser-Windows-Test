async function func() {
    let text;

    await navigator.permissions.query({name: "clipboard-read"}).then(async (result) => {
        if (result.state == "granted" || result.state == "prompt") {
            await navigator.clipboard.read().then(data => {
                text = data;
                // console.log(data)
                // for (let i = 0; i < data.items.length; i++) {
                //     if (data.items[i].type != "text/plain") {
                //         alert("Clipboard contains non-text data. Unable to access it.");
                //     } else {
                //         text = data.items[i].getAs("text/plain");
                //     }
                // }
            });
        }
    });

    return text;
}

const value = await func()

return value