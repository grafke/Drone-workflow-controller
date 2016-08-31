from datetime import datetime
import json
import re
from drone.config import settings
from drone.metadata.metadata import job_status
from drone.utils.config_loader import get_config


def string_to_iso_datetime(string):
    """
    if string == '' return today

    :param string: str
    :return: datetime.datetime
    """
    if string:
        return datetime.strptime(string.split('.')[0], "%Y-%m-%dT%H:%M:%S")
    else:
        return datetime.strptime(datetime.today().isoformat().split('T')[0], "%Y-%m-%d")


def parse_schedule_time(input_string, schedule_time):
    if re.search(r"\{schedule_time\:.*\}", str(input_string)):
        date_format = input_string.replace('{', '').replace('}', '').split(':')[1]
        iso_date = string_to_iso_datetime(schedule_time)
        formatted_date = iso_date.strftime(date_format)
        return re.sub(r"\{schedule_time\:.*\}", formatted_date, input_string)
    else:
        return input_string


def all_jobs_from_db_to_json(db_result):
    remote_jobs = get_config(settings.remote_jobs_config, settings.remote_jobs_config_schema)
    aws_jobs = get_config(settings.aws_jobs_config, settings.aws_jobs_config_schema)
    all_jobs = remote_jobs.get('jobs', []) + aws_jobs.get('jobs', [])
    active_job_ids = map(lambda x: x.get('id'), all_jobs)

    def get_status_name(status_id):
        return [name for name, id in job_status.items() if status_id == id][0]

    def format_row(row):
        return {
            'job_id': row[0],
            'schedule_time': row[1],
            'execution_time': row[2],
            'status': get_status_name(row[3]),
            'runs': row[4]
        }

    return json.dumps(filter(lambda x: x.get('job_id') in active_job_ids, map(lambda x: format_row(x), db_result)),
                      indent=4)


def job_id_generator(job_id, schedule_time):
    return '_'.join([job_id, schedule_time])
