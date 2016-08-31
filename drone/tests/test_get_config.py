from unittest import TestCase
from drone.utils.config_loader import get_config
import settings

class TestGet_config(TestCase):
    def test_get_config(self):
        result = get_config(settings.remote_jobs_config, settings.remote_jobs_config_schema)
        expected_result = {u'jobs': [{u'delay_minutes': u'',
            u'dependencies': [{u'job_completed': {u'id': u'test_remote_action',
                                                  u'last_schedule_time_interval_minutes': u'1440'}}],
            u'id': u'test_remote_action',
            u'interval_minutes': u'1440',
            u'remote_action': {u'args': [u'dummy_arg', u'dummy_arg'],
                               u'script': u'/tmp/dummy.sh'},
            u'remote_server_id': u'example',
            u'retry': u'3',
            u'start_time': u'2015-10-05T00:00:00',
            u'type': u'ssh'}]}

        self.assertEqual(result, expected_result)