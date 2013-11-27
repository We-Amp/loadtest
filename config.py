def loadtest_config():
    config = {
        "tests": 
        [
            {
                "name": "No PageSpeed",
                "url":"http://127.0.0.1/mod_pagespeed_example/?PageSpeed=off",
                "seconds": "10",
                "concurrencies": [1,10,50,100,250],
                "popen_args": ["siege", "-b", "@url@", "-c @concurrency@", "--time=@seconds@s"],
                "re_parse": r'(?P<key>[a-z\ ]*)[:][^0-9]*(?P<val>[0-9.]*) ?[a-z/%]*$',
             },
            {
                "name": "PageSpeed",
                "url":"http://127.0.0.1/mod_pagespeed_example/?PageSpeed=on",
                "seconds": "10",
                "concurrencies": [1,10,50,100,250],
                "popen_args": ["siege", "-b", "@url@", "-c @concurrency@", "--time=@seconds@s"],
                "re_parse": r'(?P<key>[a-z\ ]*)[:][^0-9]*(?P<val>[0-9.]*) ?[a-z/%]*$',
             },
            ]
        }
    return config
