const get_support_font = () => {
    var t = [],
        n = document.body;
    if (!n) return [];
    var r = ["monospace", "sans-serif", "serif"],
        o = ["sans-serif-thin", "ARNO PRO", "Agency FB", "Arabic Typesetting",
            "Arial Unicode MS", "AvantGarde Bk BT", "BankGothic Md BT", "Batang",
            "Bitstream Vera Sans Mono", "Calibri", "Century", "Century Gothic", "Clarendon",
            "EUROSTILE", "Franklin Gothic", "Futura Bk BT", "Futura Md BT", "GOTHAM",
            "Gill Sans", "HELV", "Haettenschweiler", "Helvetica Neue", "Humanst521 BT",
            "Leelawadee", "Letter Gothic", "Levenim MT", "Lucida Bright", "Lucida Sans",
            "Menlo", "MS Mincho", "MS Outlook", "MS Reference Specialty", "MS UI Gothic",
            "MT Extra", "MYRIAD PRO", "Marlett", "Meiryo UI", "Microsoft Uighur", "Minion Pro",
            "Monotype Corsiva", "PMingLiU", "Pristina", "SCRIPTINA", "Segoe UI Light", "Serifa",
            "SimHei", "Small Fonts", "Staccato222 BT", "TRAJAN PRO", "Univers CE 55 Medium",
            "Vrinda", "ZWAdobeF", 'Academy Engraved LET', 'Adobe Garamond', '微软雅黑'],
        e = document.createElement("div"),
        i = {},
        a = {},
        u = function (t) {
            var n = document.createElement("span"),
                i = ["position: absolute", "left: -9999px", "font-size: 72px",
                    "font-style: normal", "font-weight : normal", "letter-spacing : normal",
                    "line-break : auto", "line-height : normal", "text-transform : none",
                    "text-align : left", "text-decoration : none", "text-shadow : none",
                    "white-space : normal", "word-break : normal", "word-spacing : normal"].join(
                    ";");
            return n.style.cssText = i, n.style.fontFamily = t, n.textContent = "mmMwWLliI0O&1",
                e.appendChild(n), n
        },
        c = function (t) {
            for (var n = 0; n < r.length; n++)
                if (t[n].offsetWidth !== i[r[n]] || t[n].offsetHeight !== a[r[n]]) return !0;
            return !1
        },
        s = function () {
            for (var t = [], n = 0; n < r.length; n++) t.push(u(r[n]));
            return t
        }(),
        f = function () {
            for (var t = {}, n = 0; n < o.length; n++) {
                var i = o[n];
                t[i] = [];
                for (var e = 0; e < r.length; e++) t[i].push(u('"' + i + '",' + r[e]))
            }
            return t
        }();
    n.appendChild(e);
    for (var d = 0; d < r.length; d++) {
        i[r[d]] = s[d].offsetWidth;
        a[r[d]] = s[d].offsetHeight;
    }
    for (var h = 0; h < o.length; h++) {
        if (c(f[o[h]])) {
            t.push(o[h])
        }
    }
    return t
}