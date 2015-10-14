from time import sleep
from threading import Thread
from drone.api.api import api_app
from drone.bin.initialize import sync_jobs
from drone.config import settings
from drone.job_runner.job_runner import process
from drone.metadata.metadata import initialize_db

def main(settings):
    initialize_db(db_name=settings.metadata)
    while True:
        jobs_config = sync_jobs(settings)
        for job_config in jobs_config:
            process(job_config, settings)
        sleep(settings.schedule_interval_seconds)


if __name__ == "__main__":
    api_thread = Thread(target=api_app.run,
                        kwargs={'debug': settings.debug, 'use_reloader': settings.user_reloader,
                                'host': settings.host_ip, 'port': settings.port})
    api_thread.setDaemon(True)

    main_thread = Thread(target=main, args=[settings])
    main_thread.setDaemon(False)

    main_thread.start()
    api_thread.start()
