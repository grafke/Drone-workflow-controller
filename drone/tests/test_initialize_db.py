import os
from pprint import pprint
from unittest import TestCase
from drone.metadata.metadata import initialize_db, insert_dummy_job, read_all_jobs
import settings

__author__ = 'pauliusklyvis'


class TestInitialize_db(TestCase):
    def test_initialize_db(self):
        os.unlink(settings.metadata)
        initialize_db(db_name=settings.metadata)
        job_id, schedule_time, execution_time, status, runs, uid = u'dummy_job', u'2015-09-12T00:00:00', u'', 0, 0, u'0'
        expected_result = [job_id, schedule_time, execution_time, status, runs, uid]
        insert_dummy_job(job_id, schedule_time, execution_time, status, runs, uid, db_name=settings.metadata)
        result = list(read_all_jobs(db_name=settings.metadata)[0])
        os.unlink(settings.metadata)

        self.assertEqual(result, expected_result)

