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

------------------------------------------------
# Drone-web

Drone-web is a web-ui to monitor and manage [Drone](https://github.com/grafke/Drone) jobs.

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
