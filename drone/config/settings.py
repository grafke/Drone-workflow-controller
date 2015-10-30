import logging
import os

application_name = 'Drone workflow manager'

aws_jobs_config = '/etc/drone/aws_jobs_config.json'
aws_jobs_config_schema = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'aws_jobs_config_schema.json')

remote_jobs_config = '/etc/drone/remote_jobs_config.json'
remote_jobs_config_schema = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'remote_jobs_config_schema.json')

# Metadata
metadata = '/var/drone/metadata/metadata.db'
metadata_history_days = 7
metadata_future_days = 7

# Logging
log_file = '/var/drone/logs/application.log'
logging.basicConfig(filename=log_file, level=logging.DEBUG)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(log_file)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Scheduler
schedule_interval_seconds = 60

supported_dependencies = ['job_completed']
supported_job_types = ['ssh', 'emr']

# web
host_ip = '0.0.0.0'
port = 8080
use_reloader = False
debug = False

# EMR
job_flow_role = 'AmazonElasticMapReduceRole'
service_role = 'EMR_EC2_DefaultRole'