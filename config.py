def loadtest_config():
    config = {
        "result_dir": "result/",
        "tests": 
        [
            {
                "name": "collapse whitespace",
                "url":"http://127.0.0.1/mod_pagespeed_example/?PageSpeedFilters=collapse_whitespace",
                "seconds": "1",
                "concurrencies": [1,10,50,100,250],
                "popen_args": ["siege", "-b", "@url@", "-c @concurrency@", "--time=@seconds@s"],
                "re_parse": r'(?P<key>[a-z\ ]*)[:][^0-9]*(?P<val>[0-9.]*) ?[a-z/%]*$',
             },
            {
                "name": "rewrite css",
                "url":"http://127.0.0.1/mod_pagespeed_example/?PageSpeedFilters=rewrite_css",
                "seconds": "1",
                "concurrencies": [1,10,50,100,250],
                "popen_args": ["siege", "-b", "@url@", "-c @concurrency@", "--time=@seconds@s"],
                "re_parse": r'(?P<key>[a-z\ ]*)[:][^0-9]*(?P<val>[0-9.]*) ?[a-z/%]*$',
             },
            {
                "name": "rewrite images",
                "url":"http://127.0.0.1/mod_pagespeed_example/?PageSpeedFilters=rewrite_images",
                "seconds": "1",
                "concurrencies": [1,10,50,100,250],
                "popen_args": ["siege", "-b", "@url@", "-c @concurrency@", "--time=@seconds@s"],
                "re_parse": r'(?P<key>[a-z\ ]*)[:][^0-9]*(?P<val>[0-9.]*) ?[a-z/%]*$',
             },
            ]
        }
    return config
