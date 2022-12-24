(async () => {
    function get_deviceorientation() {
        let gamma;
        let beta;
        let alpha;
        let absolute;

        window.addEventListener('deviceorientation', function (event) {
            console.log(event)
            beta = event.beta || 0;
            gamma = event.gamma || 0;
            alpha = event.alpha || 0;
            absolute = event.absolute;
        })
    }
    get_deviceorientation();
})()
