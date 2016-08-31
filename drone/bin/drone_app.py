from time import sleep
from concurrent import futures
from drone.api.api import api_app
from drone.bin.initialize import sync_jobs
from drone.config import settings
from drone.job_runner.job_runner import process
from drone.metadata.metadata import initialize_db


def drone_runner():
    while True:
        jobs_config = sync_jobs(settings)
        for job_config in jobs_config:
            process(job_config, settings)
        sleep(settings.schedule_interval_seconds)


def web_runner(app=api_app):
    app.run(debug=settings.debug,
            use_reloader=settings.use_reloader,
            host=settings.host_ip,
            port=settings.port,
            threaded=True,
            processes=1)


if __name__ == "__main__":
    try:
        initialize_db(db_name=settings.metadata)

        with futures.ProcessPoolExecutor(max_workers=2) as executors:
            executors.submit(web_runner)
            executors.submit(drone_runner)

    except KeyboardInterrupt:
        exit()
    except:
        raise
