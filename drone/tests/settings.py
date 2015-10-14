import logging
import os

application_name = 'Workflow manager'

aws_jobs_config = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config/aws_jobs_config.json')
aws_jobs_config_schema = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config/aws_jobs_config_schema.json')

remote_jobs_config = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config/remote_jobs_config.json')
remote_jobs_config_schema = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config/remote_jobs_config_schema.json')

# Metadata
metadata = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'dev-metadata.db')
metadata_history_days = 7
metadata_future_days = 7

# Logging
log_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'logs/application.log')
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(log_file)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Scheduler
schedule_interval_seconds = 1

supported_dependencies = ['job_completed']
supported_job_types = ['ssh', 'emr']