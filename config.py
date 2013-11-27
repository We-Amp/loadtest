def loadtest_config():
    config = {
        "tests": 
        [
            {
                "name": "No PageSpeed",
                "url":"http://127.0.0.1/mod_pagespeed_example/?PageSpeed=off",
                "seconds": "1",
                "concurrencies": [1,10,100],
                "popen_args": ["siege", "-b", "@url@", "-c @concurrency@", "--time=@seconds@s"],
                "re_parse": r'(?P<key>[a-z\ ]*)[:][^0-9]*(?P<val>[0-9.]*) ?[a-z/%]*$',
             },
            {
                "name": "PageSpeed",
                "url":"http://127.0.0.1/mod_pagespeed_example/?PageSpeed=on",
                "seconds": "1",
                "concurrencies": [1,10,100],
                "popen_args": ["siege", "-b", "@url@", "-c @concurrency@", "--time=@seconds@s"],
                "re_parse": r'(?P<key>[a-z\ ]*)[:][^0-9]*(?P<val>[0-9.]*) ?[a-z/%]*$',
             },
            ]
        }
    return config
