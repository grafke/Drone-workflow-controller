emr_clusters = [
    {
        "id": "test_cluster",
        "aws_credentials":
            {
                "access_key": "",
                "secret_key": "",
                "region": ""
            },
        "ec2_key_name": "",
        "ami_version": "",
        "hadoop_version": "",
        "hive_version": "",
        "log_uri": "",
        "debug": "",
        "instance_groups":
            {
                "master":
                    {
                        "type": "",
                        "count": "",
                        "bid_price": ""
                    },
                "core":
                    {
                        "type": "",
                        "count": "",
                        "bid_price": ""
                    },
                "task":
                    {
                        "type": "",
                        "count": "",
                        "bid_price": ""
                    }
            },
        "bootstrap_steps":
            [
                {
                    "script": "",
                    "args": []
                }
            ],
        "hive_args":
            [
                {
                    "name": "",
                    "value": ""
                }
            ]
    }
]
