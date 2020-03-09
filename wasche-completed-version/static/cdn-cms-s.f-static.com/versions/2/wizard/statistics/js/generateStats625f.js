/**
 * Website Statistics Plugin
 */
S123.websiteStatistics = new (function() {

    // Set the global object instance
    var ws = this;

    // Timestamp value
    var timestamp = '';

    /**
     * Initialize Statistics
     */
    this.init = function() {
        // tracking data
        ws.data = {};
        // timestamp value
        timestamp = +new Date();
        // Initialize the time tracker
        ws.trackTimeSpentInit();
        // store the request object
        var req = window.location;
        // get webpage path
        var path = req.pathname + req.search;
        // Missing path
        if ( !path ) {
            path = '/';
        }
        // get webpage hostname
        var hostname = req.protocol + '//' + req.hostname;
        // set the unique tracking id
        ws.data.id = ws.randomString(20);
        // hostname
        ws.data.hn = hostname;
        // path
        ws.data.pt = path;
        // title
        ws.data.t = document.title;
        // websiteID
        ws.data.wID = $('#websiteID').val();
        // timestamp
        ws.data.tm = timestamp;
        // referrer only set referrer if not internal
        ws.data.rf = document.referrer;
        // captures module type number
        ws.data.mNUM = '';
        // get moduleType
        if ( $('#moduleTypeNUM').length !== 0 ) {
            ws.data.mNUM = $('#moduleTypeNUM').val();
        }
        // get the user device type
        ws.data.dv = ws.getUserDevice();
        // get the screen resolution
        ws.data.screenRes = screen.width + 'X' + screen.height;
        // fetch data from cookies
        var data = ws.getData();
        // check if user is a unique user
        ws.data.uq = data.pagesViewed.indexOf(path) == -1 ? 1 : 0;
        //check if user is a new visitor
        ws.data.nvs = data.isNewVisitor ? 1 : 0;
        // check if it is a new session
        ws.data.ns = data.isNewSession ? 1 : 0;
        // get the previous page view id
        ws.data.pid = data.previousPageviewId || '';
        // get session id
        ws.data.sid = data.sid;
        // set the default action to save
        ws.action = 'save';
        // save the statistics
        ws.saveStatistics(data, 'save');
    };

    /**
     * Initialize events to tracks the amount of time users spends on a page
     */
    this.trackTimeSpentInit = function() {
        // start the timer
        var start = new Date();
        // when the pjax request begins
        $(document).off('s123.pjax.send').on('s123.pjax.send', function( event ) {
            // tracks the amount of time users spends on a page
            ws.trackTimeSpent(start);
        });
        // before leaving the page
        window.onbeforeunload = function() {
           // tracks the amount of time users spends on a page
            ws.trackTimeSpent(start);
        };
    };

    /**
     * Tracks the amount of time users spends on a page
     * and updates the each tracking id
     */
    this.trackTimeSpent = function( start ) {
        var end = new Date();
        // get the time difference between the start time and the end time.
        ws.data.time_spent = Math.floor(
            (end.getTime() - start.getTime()) / 1000
        );

        // update the stats to be finished
        ws.data.is_finished = 1;
        
        // update statistics with the set timestamp and set to be finished
        ws.saveStatistics(null, 'update');
    };

    /**
     * Sends an ajax request to save and update the statistics
     *
     * @param array data statistics data with all the necessary parameter from the cookies
     * @param string action specify the action to perform on the data, either save or update
     */
    this.saveStatistics = function( data, action ) {
        $.ajax({
            type: 'GET',
            url:'https://analytics.site123.io/versions/2/wizard/statistics/classes/Router.php?action=save',
            data: ws.data,
            async: action === 'update' ? false : true,
            success: function( response ) {
                if ( data ) {
                    // get the current time
                    let now = new Date();
                    // get the current time + 24 hours
                    let expiresStats = new Date(now.getTime() + (24 * 60 * 60 * 1000));
                    // set the previousPageviewId for the next tracking object to be the current tracking id.
                    data.previousPageviewId = ws.data.id;
                    data.isNewVisitor = false;
                    data.isNewSession = false;
                    data.timestamp = timestamp;
                    // set the cookies to expire after 24 hours.
                    ws.setCookie('_website_stats', JSON.stringify(data), {
                        expires: expiresStats,
                        path: '/',
                    });
                }
            },
        });
    };

    /**
     * Converts object to query string
     *
     * @param {object} obj Object to be stringified
     * @returns {string} stringified value
     */
    this.stringifyObject = function(obj) {
        var keys = Object.keys(obj);
        return (
            '?' +
            keys
                .map(function(k) {
                    return (
                        encodeURIComponent(k) + '=' + encodeURIComponent(obj[k])
                    );
                })
                .join('&')
        );
    };

    /**
     * Generates random string for n length
     *
     * @param {string} n the length of the string
     * @returns {string} the random string
     */
    this.randomString = function(n) {
        var s = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
        return Array(n)
            .join()
            .split(',')
            .map(function() {
                return s.charAt(Math.floor(Math.random() * s.length));
            })
            .join('');
    };

    /**
     * Gets the cookie value for a particular name
     *
     * @param {string} name the name of the cookie
     * @returns {string} the cookie value
     */
    this.getCookie = function(name) {
        // split the cookies value
        var cookies = document.cookie ? document.cookie.split('; ') : [];
        //
        for (var i = 0; i < cookies.length; i++) {
            var parts = cookies[i].split('=');
            if ( decodeURIComponent(parts[0]) !== name ) continue;
            var cookie = parts.slice(1).join('=');
            return decodeURIComponent(cookie);
        }
        return '';
    };

    /**
     * Sets the cookie for a particular name
     *
     * @param {string} name the name of the cookie
     * @param {string} data the cookie value
     * @returns void
     */
    this.setCookie = function(name, data, args) {
        //
        name = encodeURIComponent(name);
        //
        data = encodeURIComponent(String(data));
        //
        var str = name + '=' + data;
        //
        if ( args.path ) {
            str += ';path=' + args.path;
        }
        //
        if ( args.expires ) {
            str += ';expires=' + args.expires;
        }
        //
        document.cookie = str;
    };

    /**
     * Creates a new visitor object for tracking
     *
     * @returns {object} the new visitor's object
     */
    this.newVisitorData = function() {
        return {
            isNewVisitor: true,
            isNewSession: true,
            pagesViewed: [],
            previousPageviewId: '',
            timestamp: timestamp,
            sid: ws.uniqid('st-')
        };
    };

    /**
     * The function Generate a unique ID.
     * Documentation : http://phpjs.org/functions/uniqid/
     */
    this.uniqid = function(prefix, more_entropy) {
        if (typeof prefix === 'undefined') prefix = '';
        var retId;
        var formatSeed = function (seed, reqWidth) {
            seed = parseInt(seed, 10).toString(16);
            if (reqWidth < seed.length) {
                return seed.slice(seed.length - reqWidth);
            }
            if (reqWidth > seed.length) {
                return Array(1 + (reqWidth - seed.length)).join('0') + seed;
            }
            return seed;
        };
        if (!this.php_js) {
            this.php_js = {};
        }
        if (!this.php_js.uniqidSeed) {
            this.php_js.uniqidSeed = Math.floor(Math.random() * 0x75bcd15);
        }
        this.php_js.uniqidSeed++;
        retId = prefix;
        retId += formatSeed(parseInt(new Date().getTime() / 1000, 10), 8);
        retId += formatSeed(this.php_js.uniqidSeed, 5);
        if (more_entropy) {
            retId += (Math.random() * 10).toFixed(8).toString();
        }
        return retId;
    }

    /**
     * Gets the data for either existing visitor or new visitor
     *
     * @returns {object} the tracking object
     */
    this.getData = function() {
        let thirtyMinsAgo = new Date();
        thirtyMinsAgo.setMinutes(thirtyMinsAgo.getMinutes() - 30);

        // get user data valid cookie
        let data = ws.getCookie('_website_stats');
        // if user does not have a cookie set, then the user is a new visitor
        if ( !data ) {
            data = ws.newVisitorData();
        }
        //
        try {
            data = JSON.parse(data);
        } catch (e) {
            data = ws.newVisitorData();
        }
        // if the data was created in less than 30 mins ago the it's a new session
        if ( data.timestamp < +thirtyMinsAgo ) {
            data.isNewSession = true;
        }
        //
        return data;
    };

    /**
     * Gets the user current device
     *
     * @returns {string} the user device type
     */
    this.getUserDevice = function() {
        //
        var userAgent = navigator.userAgent;
        //
        if (userAgent.match(/Android/i)) {
            return 'Mobile';
        }
        if (userAgent.match(/BlackBerry/i)) {
            return 'Mobile';
        }
        if (userAgent.match(/iPhone/i)) {
            return 'Mobile';
        }
        if (userAgent.match(/iPad/i)) {
            return 'Tablet';
        }
        if (userAgent.match(/iPod/i)) {
            return 'Mobile';
        }
        if (userAgent.match(/Opera Mini/i)) {
            return 'Mobile';
        }
        if (userAgent.match(/IEMobile/i)) {
            return 'Mobile';
        }
        if (userAgent.match(/Macintosh/i)) {
            return 'Desktop';
        }
        if (userAgent.match(/Windows/i)) {
            return 'Desktop';
        }
        return 'Unknown Device';
    };
})();

// Run when the page ready (before images and other resource)
jQuery(function($) {
    // website statistics initialize
    S123.websiteStatistics.init();
    // when the pjax request complete
    $(document).on('s123.pjax.complete', function(event) {
        // website statistics initialize
        S123.websiteStatistics.init();
    });
});
