import os
from time import sleep
from unittest import TestCase

from drone.bin.initialize import sync_jobs
from drone.job_runner.job_runner import process
from drone.metadata.metadata import initialize_db, read_all_jobs, set_ready, execute_db
import settings


class TestProcess(TestCase):
    os.unlink(settings.metadata)
    initialize_db(db_name=settings.metadata)
    jobs_config = sync_jobs(settings)

    def test_process_init(self):

        preprocess_status = read_all_jobs(db_name=settings.metadata)

        for job_config in self.jobs_config:
            process(job_config, settings)

        postrocess_status = read_all_jobs(db_name=settings.metadata)

        self.assertEqual(preprocess_status, postrocess_status)

    def test_process_after_ready(self):

        job_config = self.jobs_config[0]

        job_schedule_time = read_all_jobs(db_name=settings.metadata)[0][1]

        set_ready(job_config.get('id'), job_schedule_time, db_name=settings.metadata)

        process(job_config, settings)

        @execute_db('Initializing...')
        def list_running_jobs(db_name=settings.metadata):
            return 'SELECT * FROM job_status WHERE status = 2;'

        @execute_db('Initializing...')
        def list_finished_jobs(db_name=settings.metadata):
            return 'SELECT * FROM job_status WHERE status = 3;'

        running_jobs = list_running_jobs(db_name=settings.metadata)

        self.assertEqual(len(running_jobs), 1)

        sleep(15)

        process(job_config, settings)

        finished_jobs = list_finished_jobs(db_name=settings.metadata)

        self.assertEqual(len(finished_jobs), 1)

        new_running_jobs = list_running_jobs(db_name=settings.metadata)

        self.assertEqual(len(new_running_jobs), 1)
