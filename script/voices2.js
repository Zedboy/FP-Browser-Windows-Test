function getVoices() {
    return new Promise(
        function (resolve, reject) {
            let synth = window.speechSynthesis;
            let id;

            id = setInterval(() => {
                if (synth.getVoices().length > 1) {
                    resolve(synth.getVoices());
                    clearInterval(id);
                }
            }, 1000);
        }
    )
}

async function func() {
    const result = getVoices();
    if (typeof speechSynthesis !== 'undefined' && speechSynthesis.onvoiceschanged !== undefined) {
        speechSynthesis.onvoiceschanged = func;
    }

    return result
}

const value = await func()
console.log(value)
return value