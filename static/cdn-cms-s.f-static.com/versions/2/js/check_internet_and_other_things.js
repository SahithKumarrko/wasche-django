"use strict";
var received_pushes = []
  , count_messages_received = 0
  , offline_cache = null;
caches.open("offline").then(function(a) {
    offline_cache = a
}),
self.addEventListener("fetch", on_fetch),
self.addEventListener("install", on_install),
self.addEventListener("activate", on_activate),
self.addEventListener("message", on_message),
self.addEventListener("push", on_push),
self.addEventListener("notificationclick", on_notification_click);
function on_fetch(a) {
    var b = a.request;
    if ("navigate" === a.request.mode) {
        new URL(self.location);
        !1 === navigator.onLine ? a.respondWith(fetch(b).catch(function() {
            return get_offline_page("offline_page")
        })) : a.respondWith(fetch(b).catch(function() {
            return getVarFromDB("v", "countryID").then(function(a) {
                return self.countryID = a,
                get_offline_page("network_error_page")
            })
        }))
    }
}
function on_install(a) {
    self.skipWaiting(),
    a.waitUntil(check_offline_page(["offline_page", "network_error_page"])),
    createDB()
}
function on_activate(a) {
    a.waitUntil(self.clients.claim().then(function() {
        call_countryID()
    }))
}
function get_offline_page(a) {
    return offline_cache ? offline_cache.match("/api/ajax/general/?action=" + a) : Promise.resolve()
}
function check_offline_page(a) {
    var b = !0
      , c = !1
      , d = void 0;
    try {
        for (var e, f = function() {
            var a = e.value;
            get_offline_page(a).then(function(b) {
                b || cache_offline_page(a)
            })
        }, g = a[Symbol.iterator](); !(b = (e = g.next()).done); b = !0)
            f()
    } catch (a) {
        c = !0,
        d = a
    } finally {
        try {
            b || null == g.return || g.return()
        } finally {
            if (c)
                throw d
        }
    }
}
function cache_offline_page(a) {
    var b = new Request("/api/ajax/general/?action=" + a);
    fetch(b).then(function(a) {
        return offline_cache.put(b, a)
    })
}
function on_message(a) {
    if (a.data.countryID) {
        var b = a.data.countryID;
        putDB(b, "countryID"),
        self.countryID = a.data.countryID
    }
    a.data.offline_cache_version && getVarFromDB("v", "offline_cache_version").then(function(b) {
        var c = a.data.offline_cache_version
          , d = "offline_cache_version";
        if (b < c) {
            ["offline_page", "network_error_page"].forEach(function(a) {
                cache_offline_page(a)
            }),
            putDB(c, d),
            self.offline_cache_version = a.data.offline_cache_version
        } else
            void 0 === b && (putDB(c, d),
            self.offline_cache_version = a.data.offline_cache_version)
    }).catch(function() {
        putDB(offline_cache_version, key),
        self.offline_cache_version = a.data.offline_cache_version
    });
    var c = {};
    switch (a.data) {
    case "get_new_pushes":
        a.ports[0].postMessage(JSON.stringify(received_pushes));
        break;
    case "count_received":
        a.ports[0].postMessage(count_messages_received),
        count_messages_received = 0;
        break;
    case "trigger_countryID_change":
        return c = {
            event: a,
            success: navigate
        },
        network_error_handler(c);
        break;
    case "trigger_countryID_change_hint":
        return c = {
            event: a,
            success: broadcastNetworkErrorHint
        },
        network_error_handler(c);
    }
}
function navigate(a, b) {
    b.postMessage({
        action: "window.location.replace",
        url: a
    })
}
function network_error_handler(a) {
    a.event.waitUntil(self.clients.claim().then(function() {
        return self.clients.matchAll({
            type: "window"
        })
    }).then(function(b) {
        return b.map(function(b) {
            return getVarFromDB("v", "country_list_requested").then(function(c) {
                return c = c || 0,
                c < Date.now() - 18e5 ? (putDB(Date.now(), "country_list_requested"),
                try_get_to_country_domain().then(function(c) {
                    return a.success(c, b)
                }).catch(function() {
                    return navigate(self.location.origin, b)
                })) : navigate(self.location.origin, b)
            })
        })
    }))
}
function multiple_notification_summary(a) {
    var b = "";
    return a.body ? ("Locanto" !== a.title && (b += a.title + ": "),
    b += a.body + "\n",
    a.close(),
    b) : b
}
self.addEventListener("error", function() {});
function on_push(a) {
    count_messages_received++;
    self.Notification && "granted" === self.Notification.permission && a.waitUntil(self.clients.matchAll({
        includeUncontrolled: !0
    }).then(function() {
        return self.registration.getNotifications().then(function(b) {
            return handle_notifications(a, b)
        })
    }))
}
function handle_notifications(a, b) {
    var c = Math.round;
    if (a && a.data) {
        var d = a.data.json()
          , e = null
          , f = null;
        if (!d.body && !d.image)
            return;
        b && 0 < b.length && (f = "Locanto",
        e = d.title + ": " + d.body + "\n" + b.map(multiple_notification_summary)),
        100 <= received_pushes.length && received_pushes.shift(),
        received_pushes.push({
            title: d.title,
            message: d.body,
            tracking_type: d.tracking_type,
            additionalData: {
                unix: c(new Date().getTime() / 1e3),
                image: d.icon || null,
                url: d.url
            }
        });
        var g = [];
        d.action_label_1 && d.action_key_1 && g.push({
            action: d.action_key_1,
            title: d.action_label_1
        }),
        d.action_label_2 && d.action_key_2 && g.push({
            action: d.action_key_2,
            title: d.action_label_2
        });
        var h = {
            body: e || d.body || "",
            data: {
                url: d.url,
                tracking_type: d.tracking_type
            },
            actions: g
        };
        return d.icon && (h.icon = d.icon),
        d.image && (h.image = d.image),
        d.badge && (h.badge = d.badge),
        self.registration.showNotification(f || d.title, h)
    }
}
function on_notification_click(a) {
    a.notification.close();
    var b = a.notification.data.url
      , c = a.notification.data.tracking_type ? a.notification.data.tracking_type : "webpush-mc"
      , d = 0 < b.indexOf("?") ? "&" : "?";
    b += d + "track_push_click=" + c,
    a.waitUntil(clients.matchAll({
        type: "window"
    }).then(function(a) {
        for (var c, d = 0; d < a.length; d++)
            if (c = a[d],
            0 < c.url.indexOf("show=inbox") && "focus"in c)
                return void c.focus();
        clients.openWindow ? clients.openWindow(b) : c && c.focus()
    }))
}
function try_get_to_country_domain() {
    return new Promise(function(a, b) {
        function c() {
            var d = self.country_list_tdls[g];
            g < self.country_list_tdls.length ? fetch_country_domain("https://" + f + ".locanto." + d + e + "/").then(function(b) {
                a(b)
            }).catch(function(a) {
                "no_change" === a.message ? b() : (++g,
                c())
            }) : b()
        }
        var d = new URL(self.location)
          , e = "" === d.port ? d.port : ":" + d.port
          , f = self.location.hostname.startsWith("m.locanto") ? "m" : "www"
          , g = 0;
        self.country_list_tdls = ["com", "es", "co.kr", "mu", "co.nz"],
        c()
    }
    )
}
function fetch_country_domain(a) {
    return new Promise(function(b, c) {
        var d = new Headers({
            "Content-Type": "application/json"
        });
        fetch(a + "api/ajax/general/?action=country_domain", {
            method: "OPTIONS",
            headers: d,
            cache: "no-cache"
        }).then(function(a) {
            return a.json()
        }).then(function(a) {
            var c = new URL(self.location)
              , d = c.origin + "/";
            return getVarFromDB("v", "countryID").then(function(c) {
                self.countryID = c;
                var e = a[self.countryID].base_url;
                if (d !== e)
                    b(e);
                else
                    throw new Error("no_change");
                if (200 !== a.status && void 0 !== a.status)
                    throw new Error(a.status)
            }),
            !1
        }).catch(function(a) {
            c(a)
        })
    }
    )
}
function broadcastNetworkErrorHint(a) {
    self.clients.matchAll().then(function(b) {
        b.forEach(function(b) {
            b.postMessage({
                action: "showErrorHint",
                url: a
            })
        })
    })
}
function call_countryID() {
    self.clients.matchAll().then(function(a) {
        a.forEach(function(a) {
            a.postMessage({
                action: "send_countryID"
            })
        })
    })
}
function createDB() {
    return new Promise(function() {
        var a = indexedDB.open("yalwa", 1);
        a.onupgradeneeded = function() {
            var b = a.result;
            b.createObjectStore("v", {
                autoIncrement: !0
            })
        }
        ,
        a.onsuccess = function() {}
    }
    )
}
function putDB(a, b) {
    var c = indexedDB.open("yalwa", 1);
    c.onupgradeneeded = function() {
        var a = c.result;
        a.createObjectStore("v", {
            autoIncrement: !0
        })
    }
    ,
    c.onsuccess = function() {
        var d = c.result
          , e = d.transaction("v", "readwrite")
          , f = e.objectStore("v");
        f.put(a, b),
        e.oncomplete = function() {
            d.close()
        }
    }
}
function getVarFromDB(a, b) {
    return new Promise(function(c, d) {
        var e = indexedDB.open("yalwa", 1);
        e.onsuccess = function() {
            var f = e.result
              , g = f.transaction(a, "readonly")
              , h = g.objectStore(a)
              , i = h.get(b);
            i.onsuccess = function(a) {
                c(a.target.result)
            }
            ,
            i.onerror = function(a) {
                d(a)
            }
            ,
            f.close()
        }
        ,
        e.onerror = function(a) {
            d(a)
        }
    }
    )
}

//# sourceMappingURL=sw.js.map
