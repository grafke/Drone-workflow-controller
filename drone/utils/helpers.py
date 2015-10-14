from datetime import datetime
import json
from pprint import pprint
from drone.metadata.metadata import job_status


def string_to_iso_datetime(string):
    return datetime.strptime(string.split('.')[0], "%Y-%m-%dT%H:%M:%S")


def all_jobs_from_db_to_json(db_result):
    def get_status_name(status_id):
        for name, id in job_status.iteritems():
            if status_id == id:
                return name


    def format_row(row):
        return {
            'job_id': row[0],
            'schedule_time': row[1],
            'execution_time': row[2],
            'status': get_status_name(row[3]),
            'runs': row[4]
        }
    return json.dumps(map(lambda x: format_row(x), db_result), indent=4)


def job_id_generator(job_id, schedule_time):
    return '_'.join([job_id, schedule_time])
