from unittest import TestCase
from drone.actions.emr_launcher import launch_emr_task
from drone.config import settings
from drone.utils.config_loader import get_config


class TestLaunch_emr_task(TestCase):
    def test_launch_emr_task(self):

        config = get_config(settings.aws_jobs_config, settings.aws_jobs_config_schema)
        for job_config in config.get('jobs', []):
            result = launch_emr_task(job_config, 2, settings)
            print(result)