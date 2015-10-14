from flask import Flask
from drone.metadata.metadata import read_all_jobs, update_job_status
from drone.config.settings import application_name, metadata, host_ip, port
from drone.utils.helpers import all_jobs_from_db_to_json, string_to_iso_datetime
from flask.ext.cors import CORS

api_app = Flask(application_name)
CORS(api_app)

@api_app.route('/')
def index():
    return application_name


@api_app.route('/list_jobs', methods=['GET'])
def get_task():
    return all_jobs_from_db_to_json(read_all_jobs(db_name=metadata))


@api_app.route('/set_job_status/<job_id>/<schedule_time>/<status>', methods=['GET'])
def update_task(job_id, schedule_time, status):
    try:
        schedule_time_parsed = string_to_iso_datetime(schedule_time).isoformat()
    except ValueError:
        return ('Invalid date %s. Must match ' % schedule_time + "%Y-%m-%dT%H:%M:%S"), 500
    try:
        assert status in ['failed', 'ready', 'not_ready', 'succeeded']
    except:
        return "Invalid status. Must be one of the following: %s" % 'failed, ready, not_ready, succeeded', 500
    update_job_status.get(status)(job_id, schedule_time_parsed, db_name=metadata)
    return '%s marked as %s for %s' % (job_id, status, schedule_time_parsed)


if __name__ == '__main__':
    api_app.run(debug=True, use_reloader=False, host=host_ip, port=port)
