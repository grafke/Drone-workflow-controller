import os
from time import sleep
from unittest import TestCase
from drone.bin.initialize import sync_jobs
from drone.job_runner.job_runner import process
from drone.metadata.metadata import initialize_db, read_all_jobs, set_ready, execute_db
import settings


class TestProcess(TestCase):

    def _init(self):
        try:
            os.unlink(settings.metadata)
        except OSError:
            pass
        initialize_db(db_name=settings.metadata)
        self.jobs_config = sync_jobs(settings)

    def test_process_init(self):

        self._init()
        preprocess_status = read_all_jobs(db_name=settings.metadata)

        for job_config in self.jobs_config:
            process(job_config, settings)

        postrocess_status = read_all_jobs(db_name=settings.metadata)

        self.assertEqual(preprocess_status, postrocess_status)

    def test_process_after_ready(self):
        return True
        self._init()
        job_config = self.jobs_config[0]

        dummy_command = '#!/bin/bash\nsleep 5\nexit 0'
        dummy_script = job_config.get('remote_action').get('script')

        with open(dummy_script, 'w') as f:
            f.write(dummy_command)

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

        sleep(8)

        process(job_config, settings)

        finished_jobs = list_finished_jobs(db_name=settings.metadata)

        self.assertEqual(len(finished_jobs), 1)

        new_running_jobs = list_running_jobs(db_name=settings.metadata)

        self.assertEqual(len(new_running_jobs), 1)

        os.unlink(settings.metadata)
        os.unlink(dummy_script)