(async () => {
    let result;
    let i = 0

    function listen_function(e) {
        console.log(e)
        let acceleration = e.accelerationIncludingGravity;

        let x1 = acceleration.x || 0;
        let y1 = acceleration.y || 0;
        let z1 = acceleration.z || 0;

        acceleration = e.acceleration;

        let x2 = acceleration.x || 0;
        let y2 = acceleration.y || 0;
        let z2 = acceleration.z || 0;

        let rotationRate = e.rotationRate;

        let alpha = rotationRate.alpha || 0;
        let beta = rotationRate.beta || 0;
        let gamma = rotationRate.gamma || 0;

        let interval = e.interval;

        result = {
            x1,
            y1,
            z1,
            x2,
            y2,
            z2,
            alpha,
            beta,
            gamma,
            interval
        }

        console.log(result)
        // 触发一次后就停止收集
        if (i > 2) {
            window.removeEventListener('devicemotion', listen_function);
        } else {
            i++;
        }
    }

    window.addEventListener('devicemotion', listen_function);
})()
