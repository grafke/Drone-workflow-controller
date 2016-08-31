from unittest import TestCase

from drone.bin.initialize import sync_jobs
from drone.metadata.metadata import initialize_db, read_all_jobs
import settings


class TestSync_jobs(TestCase):
    def test_sync_jobs(self):
        initialize_db(db_name=settings.metadata)
        result = sync_jobs(settings)
        db_jobs = read_all_jobs(db_name=settings.metadata)

        self.assertEqual(len(db_jobs), len(result) * (settings.metadata_history_days + settings.metadata_future_days))