def get_config():
    config = {
        "result_dir": "result/",
        "seconds": "10",
        "popen_args": ["siege", "-b", "@url@", "-c @concurrency@", "--time=@seconds@s"],
        "concurrencies": [1,10,20,30,40,50,75,100,150,200],
        "re_parse": r'(?P<key>[a-z\ ]*)[:][^0-9]*(?P<val>[0-9\.]*) ?[ a-z/\%\(\)\[\]\#]*$',
        "x_axis_caption": "concurrency",
        "y_axis_caption": "#",
        # TODO
        "type": "linechart", 
        "host": "127.0.0.1",
        "test_store_headers": ["X-Page-Speed", "Server"],
        "tests": 
        [
            {
                "name": "abtest",
                "popen_args": ["ab", "-n 1000", "-c @concurrency@", "-k", "http://@host@/mod_pagespeed_example/"],
                },
            {
                "name": "PassThrough",
                "url":"http://@host@/mod_pagespeed_example/?PageSpeed=",
             },
            {
                "name": "collapse whitespace",
                "url":"http://@host@/mod_pagespeed_example/?PageSpeedFilters=collapse_whitespace",
             },
            {
                "name": "rewrite css",
                "url":"http://@host@/mod_pagespeed_example/?PageSpeedFilters=rewrite_css",
             },
            {
                "name": "rewrite images",
                "url":"http://@host@/mod_pagespeed_example/?PageSpeedFilters=rewrite_images",
             },
            {
                "name": "rewrite js",
                "url":"http://@host@/mod_pagespeed_example/?PageSpeedFilters=rewrite_javascript",
             },
            {
                "name": "rewrite domains",
                "url":"http://@host@/mod_pagespeed_example/?PageSpeedFilters=rewrite_domains",
             },
            {
                "name": "extend cache",
                "url":"http://@host@/mod_pagespeed_example/?PageSpeedFilters=extend_cache",
             },
            {
                "name": "prioritize critical css",
                "url":"http://@host@/mod_pagespeed_example/?PageSpeedFilters=prioritize_critical_css",
             },
            {
                "name": "insert dns prefetch",
                "url":"http://@host@/mod_pagespeed_example/insert_dns_prefetch.html?PageSpeed=on&PageSpeedFilters=insert_dns_prefetch"
             }
       ],
       "graphs": [
            {
                "name": "AB Time taken",
                "tests": ["abtest"],
                "stats": ["Time taken for tests"],
                },
            {
                "name": "AB Total transferred",
                "tests": ["abtest"],
                "stats": ["Total transferred"],
                },
            {
                "name": "Requests per second",
                "tests": ["abtest"],
                "stats": ["Requests per second"],
                },

            {
                "name": "Filter performance - availability",
                "tests": ["PassThrough", "collapse whitespace", "rewrite css", "rewrite images", "rewrite domains", "rewrite js", "extend cache", "prioritize critical css", "insert dns prefetch"],
                "stats": ["Availability"],
                },
            {
                "name": "Filter performance - rate",
                "tests": ["PassThrough", "collapse whitespace", "rewrite css", "rewrite images", "rewrite domains", "rewrite js", "extend cache", "prioritize critical css", "insert dns prefetch"],
                "stats": ["Transaction rate"],
                },
            {
                "name": "Filter performance - response time",
                "tests": ["PassThrough", "collapse whitespace", "rewrite css", "rewrite images", "rewrite domains", "rewrite js", "extend cache", "prioritize critical css", "insert dns prefetch"],
                "stats": ["Response time"],
                },
            {
                "name": "Filter performance - longest transaction",
                "tests": ["PassThrough", "collapse whitespace", "rewrite css", "rewrite images", "rewrite domains", "rewrite js", "extend cache", "prioritize critical css", "insert dns prefetch"],
                "stats": ["Longest transaction"],
                },
            {
                "name": "Filter performance - throughput",
                "tests": ["PassThrough", "collapse whitespace", "rewrite css", "rewrite images", "rewrite domains", "rewrite js", "extend cache", "prioritize critical css", "insert dns prefetch"],
                "stats": ["Throughput"],
                },
            {
                "name": "Filter performance - concurrency",
                "tests": ["PassThrough", "collapse whitespace", "rewrite css", "rewrite images", "rewrite domains", "rewrite js", "extend cache", "prioritize critical css", "insert dns prefetch"],
                "stats": ["Concurrency"],
                },
            ]
    }
    return config
