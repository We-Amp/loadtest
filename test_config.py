def get_config():
    config = {
        "result_dir": "result/",
        "seconds": "10",
        "popen_args": ["siege", "-b", "@url@", "-c @concurrency@", "--time=@seconds@s"],
        "concurrencies": [1,10,100,200],
        "re_parse": r'(?P<key>[a-z\ ]*)[:][^0-9]*(?P<val>[0-9\.]*) ?[ a-z/\%\(\)\[\]\#]*$',
        "x_axis_caption": "Concurrency",
        "y_axis_caption": "#",
        # TODO
        "type": "linechart", 
        "host": "127.0.0.1",
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
       ],
       "graphs": [
            {
                "name": "AB Time taken",
                "tests": ["abtest"],
                "stats": ["Time taken for tests"],
                "y_axis_caption": "Seconds",
                },
            {
                "name": "AB Total transferred",
                "tests": ["abtest"],
                "stats": ["Total transferred"],
                "y_axis_caption": "Bytes",
                },
            {
                "name": "Requests per second",
                "tests": ["abtest"],
                "stats": ["Requests per second"],
                "y_axis_caption": "QPS",
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
