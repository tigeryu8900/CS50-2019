var proxiedLocation = document.createElement('a');
proxiedLocation.href = window.location.pathname.replace("/proxy/", "");
Object.defineProperty(proxiedLocation, 'noPortOrigin', {
    get() {
        return this.protocol + "//" + this.hostname;
    }
});
xhook.before(function(request) {
    if (-1 == request.url.indexOf("/proxy/")) {
        var origUrl = request.url;

        if (request.url.startsWith("http://") || request.url.startsWith("https://")) {
            // do nothing with the url
        } else if (request.url.startsWith("//")) {
            request.url = proxiedLocation.protocol + request.url;
        } else if (request.url.startsWith("/")) {
            request.url = proxiedLocation.noPortOrigin + request.url;
        } else if (request.url.startsWith(".")) {
            request.url = proxiedLocation.noPortOrigin + request.url.replace("./", "/");
        } else {
            request.url = proxiedLocation.origin + "/" + request.url;
        }

        var sanitizedUrl = request.url;

        request.url = "/proxy/" + request.url;

        console.log("Proxy: XHR request '" + origUrl + "' was sanitized '" + sanitizedUrl + "' and proxied '" + request.url + "'");
    } else {
        console.log("Proxy: XHR no action needed: '" + request.url + "'");
    }
});

if (typeof observeDOM === 'undefined') {
    var proxyUrl = (function(origUrl) {
        if (typeof origUrl == 'undefined' || !origUrl) {
            return origUrl;
        }

        var newUrl = origUrl;
        if (
            -1 == newUrl.indexOf("/proxy/") &&
            -1 == newUrl.indexOf(window.location.origin + "/proxy/") &&  // already proxied
            -1 == newUrl.indexOf("xhook.min.js") &&
            -1 == newUrl.indexOf("request_capture.js") &&
            -1 == newUrl.indexOf("javascript:") &&
            -1 == newUrl.indexOf("data:")
            /**/
        ) {
            newUrl = newUrl.replace(window.location.origin, "");

            if (newUrl.startsWith("http://") || newUrl.startsWith("https://")) {
                // do nothing with the url
            } else if (newUrl.startsWith("//")) {
                newUrl = proxiedLocation.protocol + newUrl;
            } else if (newUrl.startsWith("/")) {
                newUrl = proxiedLocation.origin + newUrl;
            } else if (newUrl.startsWith(".")) {
                newUrl = proxiedLocation.origin + newUrl.replace("./", "/");
            } else {
                newUrl = proxiedLocation.origin + "/" + newUrl;
            }
            var sanitizedUrl = newUrl;

            newUrl = "/proxy/" + newUrl;
            console.log("Proxy: OnDOMChange unproxied url detected '" + origUrl + "' was sanitized '" + sanitizedUrl + "' and proxied '" + newUrl + "'");
        }

        return newUrl;
    });

    // object.watch
    if (!Object.prototype.watch) {
        Object.defineProperty(Object.prototype, "watch", {
            enumerable: false,
            configurable: true,
            writable: false,
            value: function (prop, handler) {
                var oldval = this[prop];
                var newval = oldval;
                if (delete this[prop]) { // can't watch constants
                    Object.defineProperty(this, prop, {
                        get() {
                            return newval;
                        },
                        set(val) {
                            oldval = newval;
                            return newval = handler.call(this, prop, oldval, val);
                        },
                        enumerable: true,
                        configurable: true
                    });
                }
            }
        });
    }
    // object.unwatch
    if (!Object.prototype.unwatch) {
        Object.defineProperty(Object.prototype, "unwatch", {
            enumerable: false,
            configurable: true,
            writable: false,
            value: function (prop) {
                var val = this[prop];
                delete this[prop]; // remove accessors
                this[prop] = val;
            }
        });
    }
    var proxyWindowLocation =  { href: "" };
    proxyWindowLocation.watch("href", function(propertyName, oldValue, newValue) {
        window.location.href = proxyUrl(newValue);
    });
    var proxyCustomReplace = function (loc) {
        window.location.replace(proxyUrl(loc));
    };

    var observeDOM = (function(){
        var MutationObserver = window.MutationObserver || window.WebKitMutationObserver,
            eventListenerSupported = window.addEventListener;

        return function(obj, callback){
            if( MutationObserver ){
                // define a new observer
                var obs = new MutationObserver(function(mutations, observer){
                    if( mutations[0].addedNodes.length || mutations[0].removedNodes.length )
                        callback();
                });
                // have the observer observe foo for changes in children
                obs.observe( obj, { childList:true, subtree:true });
            }
            else if( eventListenerSupported ){
                obj.addEventListener('DOMNodeInserted', callback, false);
                obj.addEventListener('DOMNodeRemoved', callback, false);
            }
        };
    })();

    // Observe a specific DOM element:
    observeDOM( document.getElementsByTagName("html")[0] ,function(){
        window.removeEventListener("error", window.onerror);
        var frames = document.getElementsByTagName("iframe");
        for (var frame of frames) {
            if (frame.getAttribute("src") && "about:blank" == frame.getAttribute("src")) {
                continue;
            }
            frame.parentNode.removeChild(frame);
        }
        var images = document.getElementsByTagName("img");
        for (var image of images) {
            if (image.hasAttribute("data-src")) {
                image.src = image.getAttribute("data-src");
            }
            image.removeAttribute("srcset");
            image.src = proxyUrl(image.src);
        }
        var links = document.getElementsByTagName("a");
        for (var link of links) {
            link.href = proxyUrl(link.href);
            link.onmousedown = function() {
                this.href = proxyUrl(this.href);
            };
        }
        var scripts = document.getElementsByTagName("script");
        for (var script of scripts) {
            if (typeof script.src != 'undefined' && script.src) {
                if ("ignore" == script.getAttribute("proxy")) {
                    script.ishandled = true;
                }
                if (typeof script.ishandled == 'undefined' || null == script.ishandled) {
                    var proxiedUrl = proxyUrl(script.src);

                    if (proxiedUrl == script.src) {
                        console.log("Script: is proxied with correct url '" + script.src + "'");
                        script.ishandled = true;
                    } else {
                        console.log("Script: replacing script '" + script.src + "' with new element '" + proxiedUrl + "'");
                        var newScript = document.createElement("script");
                        newScript.src = proxiedUrl;
                        newScript.setAttribute('orig-src', script.src);
                        newScript.setAttribute("type", script.getAttribute("type"));
                        newScript.ishandled = true;
                        script.parentNode.replaceChild(newScript, script);
                    }
                }
            }
        }

        var links = document.getElementsByTagName("link");
        for (var l of links) {
            if ("ignore" == l.getAttribute("proxy")) {
                continue;
            }
            if (l.href) {
                l.href = proxyUrl(l.href);
            }
        }
        var forms = document.getElementsByTagName("form");
        for (var f of forms) {
            f.action = proxyUrl(f.action);
        }
    });

    var link = document.querySelector("link[rel*='icon']");
    if (!link) {
        link = document.createElement('link');
        link.type = 'image/x-icon';
        link.rel = 'shortcut icon';
        link.href = proxyUrl('/favicon.ico');
        document.getElementsByTagName('head')[0].appendChild(link);
    }
}

var Cookies = {
    set(name, value, secondsExpires) {
        var nameEscaped = encodeURIComponent(name);
        var valueEscaped = encodeURIComponent(value || '');
        var domain = window.location.hostname.split('.').slice(-2).join('.');

        var cookieString = nameEscaped + '=' + valueEscaped;

        if (secondsExpires !== undefined) {
            var expires = (new Date(new Date().setTime(new Date().getTime() + (secondsExpires * 1000)))).toUTCString();
            cookieString += '; expires=' + expires;
        }

        cookieString += '; path=/; domain=.' + domain;

        document.cookie = cookieString;
    },
    getAll() {
        var cookies = {};

        document.cookie.split(/;\s+/).forEach(function (cookie) {
            var splitted = cookie.split('=');
            var name = decodeURIComponent(splitted[0]);
            var value = decodeURIComponent(splitted[1]);

            cookies[name] = value;
        });

        return cookies;
    },
    get(searchName) {
        var cookies = this.getAll();
        return cookies[searchName];
    }
};


console.log("setup done");
