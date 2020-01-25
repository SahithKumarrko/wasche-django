importScripts('https://cdn.onesignal.com/sdks/OneSignalSDKWorker.js');

/**
 * Copyright 2015 Google Inc. All rights reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

(function() {
    var nativeAddAll = Cache.prototype.addAll;
    var userAgent = navigator.userAgent.match(/(Firefox|Chrome)\/(\d+\.)/);
  
    // Has nice behavior of `var` which everyone hates
    if (userAgent) {
      var agent = userAgent[1];
      var version = parseInt(userAgent[2]);
    }
  
    if (
      nativeAddAll && (!userAgent ||
        (agent === 'Firefox' && version >= 46) ||
        (agent === 'Chrome'  && version >= 50)
      )
    ) {
      return;
    }
  
    Cache.prototype.addAll = function addAll(requests) {
      var cache = this;
  
      // Since DOMExceptions are not constructable:
      function NetworkError(message) {
        this.name = 'NetworkError';
        this.code = 19;
        this.message = message;
      }
  
      NetworkError.prototype = Object.create(Error.prototype);
  
      return Promise.resolve().then(function() {
        if (arguments.length < 1) throw new TypeError();
  
        // Simulate sequence<(Request or USVString)> binding:
        var sequence = [];
  
        requests = requests.map(function(request) {
          if (request instanceof Request) {
            return request;
          }
          else {
            return String(request); // may throw TypeError
          }
        });
  
        return Promise.all(
          requests.map(function(request) {
            if (typeof request === 'string') {
              request = new Request(request);
            }
  
            var scheme = new URL(request.url).protocol;
  
            if (scheme !== 'http:' && scheme !== 'https:') {
              throw new NetworkError("Invalid scheme");
            }
  
            return fetch(request.clone());
          })
        );
      }).then(function(responses) {
        // If some of the responses has not OK-eish status,
        // then whole operation should reject
        if (responses.some(function(response) {
          return !response.ok;
        })) {
          throw new NetworkError('Incorrect response status');
        }
  
        // TODO: check that requests don't overwrite one another
        // (don't think this is possible to polyfill due to opaque responses)
        return Promise.all(
          responses.map(function(response, i) {
            return cache.put(requests[i], response);
          })
        );
      }).then(function() {
        return undefined;
      });
    };
  
    Cache.prototype.add = function add(request) {
      return this.addAll([request]);
    };
  }());




self.addEventListener('install', function(e) {
 e.waitUntil(
   caches.open('wasche').then(function(cache) {
     return cache.addAll([
       
       '/gone-offline.html'
     ]);
   })
 );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
      // Try the cache
      caches.match(event.request).then(function(response) {
        // Fall back to network
        // console.log(event.request.url);
        // if(!response){
        // }
        return response || fetch(event.request);
        //     if(event.request.url.indexOf(".html")!=-1 || event.request.url.indexOf(".svg")!=-1 || event.request.url.indexOf(".jpg")!=-1 || event.request.url.indexOf(".png")!=-1 || event.request.url.indexOf(".jpeg")!=-1){
        //         if(event.request.url.indexOf("handle.svg")==-1){
        //         var u = event.request.url;
        //         u = u.split("/");
        //         var i=3;
        //         for(var j=0;j<u.length;j++){
        //             if(u[i].indexOf("localhost")!=-1 || u[i].indexOf("wasche")!=-1){
        //                 i=j;
        //             }
        //         }
        //         // console.log("i = "+i);
        //         var r = "";
        //         u.slice(i,).map(function(e){
        //             r = r+"/"+e;
        //         })
        //         caches.open("wasche").then(function(cache){
        //             cache.add(r);
        //             // console.log("added");
        //         });
                
        //         // console.log("not found  :  " + r);
        //     }
        //     }
        //     return response;
        // });
      }).catch(function() {
          console.log("error");
        // If both fail, show a generic fallback:
        return caches.match('/gone-offline.html');
        // However, in reality you'd have many different
        // fallbacks, depending on URL & headers.
        // Eg, a fallback silhouette image for avatars.
      })
    );
  });
  self.addEventListener('activate', function(event) {
    event.waitUntil(
      caches.keys().then(function(cacheNames) {
        return Promise.all(
          cacheNames.filter(function(cacheName) {
            // Return true if you want to remove this cache,
            // but remember that caches are shared across
            // the whole origin
            console.log(cacheName);
            if(cacheName=="wasche"){
                console.log("deleted");
                return true;
            }

          }).map(function(cacheName) {
              console.log("deleting "+cacheName);
            return caches.delete(cacheName);
          })
        );
      })
    );
  });
console.log("called worker");

// var perm="";
// if("Notification" in window){
//     var st = setInterval(function(){
//         var pp = Notification.permission;
//         if(pp!=perm){
//             perm = pp;
            
//             console.log("changed");clearInterval(st);
//         }})
// }
