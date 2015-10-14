# Drone

Drone is a platform to schedule and monitor workflows.
Workflows are defined in JSON.

Use Drone to create workflows as directed acyclic graphs (DAGs) of jobs.
The Drone scheduler executes your jobs on a remote resource (on EMR, EC2, or a remote host via SSH).

Design Principles
----------------
* **Simple**: based on JSON
* **Extensible**: component-based approach
* **Transparent**: state stored in a SQLite database
* **Reliable**: stateless components
* **Feature-rich**: auto-retries, runtime alternations

TO-DO
----------------
* Per-job emails

Quick start
----------------

    git clone https://github.com/grafke/Drone-workflow-controller
    cd Drone-workflow-controller

Drone uses SQLite as persistent storage. 

Running Drone is super easy:
    
    python bin/drone_app.py

Configure Drone
----------------

All configuration files are stored in drone/config.

settings.py - main configuration file. There are a few parameters to configure. For example:

    schedule_interval_seconds - defines how often Drone checks the status of jobs.
    metadata_history_days - defines how long to keep job history in the database 

supported_remote_hosts.py - this configuration file stores information about remote hosts.

    remote_servers = {
        'test_server_A': {
            'ssh_details': {
                'username': 'username',
                'password': 'password',
                'ssh_key': 'id_rsa file path',
                'host': ''
            },
            'logging': {
                'stdout_log_dir': '/var/log/drone/',
                'stderr_log_dir': '/var/log/drone/',
                'pid_file_dir': '/var/run/drone/'
            }
        },
        ...
    }
    
supported_emr_clusters.py -  this configuration file stores information about supported EMR clusters.
    
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

aws_jobs_config.json - this file stores the configuration of your EMR jobs.

remote_jobs_config - this file stores the configuration of you remote jobs.

------------------------------------------------
# Drone-web

Drone-web is a web-ui to monitor and manage Drone jobs.

![img] (http://i.imgur.com/X5BYvBx.png)


## Features
- ** Change job status to SUCCEEDED, READY, NOT_READY, or FAILED
- ** Report number of runs for each job (number displayed in a cell)
- ** Filter job list (Search field)
- ** Sort the output by any column

## TO-DO
- ** Allow to change a job status for several jobs (mini batches)
- ** Report running time for running jobs
- ** Report execution time for finished, and failed jobs.
