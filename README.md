# Drone

Drone is a platform to schedule and monitor workflows.
Workflows are defined in JSON.

Use Drone to create workflows as directed acyclic graphs (DAGs) of jobs.
The Drone scheduler executes your jobs on a remote resource (on EMR, EC2, or a remote host via SSH).

# Design Principles

* **Simple**: based on JSON
* **Extensible**: component-based approach
* **Transparent**: state stored in a SQLite database
* **Reliable**: stateless components
* **Feature-rich**: auto-retries, runtime alternations

# TO-DO

* Per-job emails

# Quick start


    git clone https://github.com/grafke/Drone-workflow-controller
    cd Drone-workflow-controller

Drone uses SQLite as persistent storage. 

Running Drone is super easy:
    
    python bin/drone_app.py

# Configure Drone


All configuration files are stored in drone/config.

settings.py - main configuration file. There are a few parameters to configure. For example:

    schedule_interval_seconds - defines how often Drone checks the status of jobs and re-reads job configuration files.
    metadata_history_days - defines how long to keep job history in the database 
    
    host_ip - ip address for Drone API
    port - port for Drone API

Drone does not require a restart after new job configuration files are deployed. 
Jobs configuration files are parsed every __schedule_interval_seconds__ seconds. 
Restart is required only after changes are made in settings.py, supported_remote_hosts.py, or supported_emr_clusters.py.

# Job configuration

Job environment
----------------

supported_remote_hosts.py - this configuration file stores information about remote hosts. Drone uses SSH to
connect to a remote host.

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

    stdout_log_dir, stderr_log_dir, and pid_file_dir have to be writable. Drone writes the pid of a remote process in 
    the pid file. Drone uses the remote pid file to check the status of the remote job. If it's missing, Drone marks the
     job as succeeded. If it's present, but the process of that pid is not running, Drone marks the
     job as failed. If the remote pid directory is not writable, Drone will not be able to read a pid file and will mark 
      the remote job as succeeded. Drone does not validate remote environment configuration.
    
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

Job definition
----------------

remote_jobs_config.py - this file stores the configuration of you remote jobs.

    {
      "jobs": [
        {
          "id": "test_remote_action",
          "type": "ssh",
          "remote_server_id": "test_server",
          "start_time": "2015-10-05T00:00:00",
          "delay_minutes": "0",
          "interval_minutes": "1440",
          "retry": "3",
          "dependencies": [
            {
              "job_completed": {
                "id": "test_remote_action",
                "last_schedule_time_interval_minutes": "1440"
              }
            }
          ],
          "remote_action": {
            "script": "/home/leos/script.sh",
            "args": [
              "dummy_arg", "dummy_arg_2"
            ]
          }
        }
      ]
    }
    
    

aws_jobs_config.json - this file stores the configuration of your EMR jobs.

    empty

------------------------------------------------

# Drone-web

Drone-web is a web-ui to monitor and manage Drone jobs.

![img] (http://i.imgur.com/X5BYvBx.png)

Drone-web can be served from a different server than Drone.

# Configuration

Drone-web needs a URL for Drone API.

    var host = 'http://127.0.0.1:8080';
    
# Job status

Not ready - grey
Ready - round blue
Running - blue
Succeeded - green
Failed - red

# Features
- ** Change job status to SUCCEEDED, READY, NOT_READY, or FAILED
- ** Report number of runs for each job (number displayed in a cell)
- ** Filter job list (Search field)
- ** Sort the output by any column

# TO-DO
- ** Allow to change a job status for several jobs (mini batches)
- ** Report running time for running jobs
- ** Report execution time for finished, and failed jobs.
