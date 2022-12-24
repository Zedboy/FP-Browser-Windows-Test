async function get_ips(callback) {
    var ip_dups = {};

    //compatibility for firefox and chrome
    var RTCPeerConnection = window.RTCPeerConnection
        || window.mozRTCPeerConnection
        || window.webkitRTCPeerConnection;
    var useWebKit = !!window.webkitRTCPeerConnection;

    //bypass naive webrtc blocking using an iframe
    if (!RTCPeerConnection) {
        //NOTE: you need to have an iframe in the page right above the script tag
        //
        //<iframe id="iframe" sandbox="allow-same-origin" style="display: none"></iframe>
        //<script>...getIPs called in here...
        //
        var win = window.iframe.contentWindow;
        RTCPeerConnection = win.RTCPeerConnection
            || win.mozRTCPeerConnection
            || win.webkitRTCPeerConnection;
        useWebKit = !!win.webkitRTCPeerConnection;
    }

    //minimal requirements for data connection
    var mediaConstraints = {
        optional: [{RtpDataChannels: true}]
    };

    var servers = {
        iceServers: [{
            urls: [
                "stun:stun.l.google.com:19302?transport=udp",
                "stun:stun.l.google.com:19302",
                "stun:stun2.l.google.com:19302",
                "stun:stun.services.mozilla.com",
            ]
        }]
    };

    //construct a new RTCPeerConnection
    var pc = new RTCPeerConnection(servers, mediaConstraints);

    const is_privite_ip = (ip) => {
        // https://stackoverflow.com/questions/30674845/regex-how-to-match-ip-address-in-rfc1918-private-ipv4-address-ranges-in-python
        const ip_regex = /^(?:10|127|172\.(?:1[6-9]|2[0-9]|3[01])|192\.168)\..*/g
        const result = ip_regex.exec(ip);

        return Array.isArray(result) && result.length > 0;
    }

    const result = {
        privite_ip_addr: null,
        public_ip_addr: null,
    };

    function handleCandidate(candidate) {
        try {
            //match just the IP address
            var ip_regex = /([0-9]{1,3}(\.[0-9]{1,3}){3}|[a-f0-9]{1,4}(:[a-f0-9]{1,4}){7})/
            const exec_result = ip_regex.exec(candidate);
            if (!exec_result || exec_result.length <= 0) {
                return;
            }
            var ip_addr = exec_result[1];
            const is_privite = is_privite_ip(ip_addr);

            if (is_privite) {
                result.privite_ip_addr = ip_addr;
            } else {
                result.public_ip_addr = ip_addr;
            }

            //remove duplicates
            if (ip_dups[ip_addr] === undefined)
                callback(result);

            ip_dups[ip_addr] = true;
        } catch (e) {

        }
    }

    //listen for candidate events
    pc.onicecandidate = function (ice) {

        //skip non-candidate events
        if (ice.candidate) {
            handleCandidate(ice.candidate.candidate);
        }
    };

    //create a bogus data channel
    pc.createDataChannel("");

    //create an offer sdp
    pc.createOffer(function (result) {
        //trigger the stun server request
        pc.setLocalDescription(result, function () {
        }, function () {
        });

    }, function () {
    });

    await new Promise(resolve => setTimeout(resolve, 3000));

    //read candidate info from local description
    var lines = pc.localDescription.sdp.split('\n');
    lines.forEach(function (line) {
        if (line.indexOf('a=candidate:') === 0)
            handleCandidate(line);
    });
}

function tryCatchExecute(fun, arg) {
    try {
        return fun && fun.apply(window, arg || []) || '';
    } catch (e) {
        {
            console.info('error function: ', fun.toString(), '\ndebug error: ', e);
        }

        return '';
    }
}


async function func() {
    let result;
    await get_ips((res) => {
        result = res
    });
    return result;
}

const value = await func()
return value