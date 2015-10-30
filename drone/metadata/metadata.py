import sqlite3
import datetime

job_status = {'failed': 4,
              'not_ready': 0,
              'ready': 1,
              'running': 2,
              'succeeded': 3}


def execute_db(msg):
    def wrap(f):
        def wrapped_f(*args, **kwargs):
            query = f(*args, **kwargs)
            conn = sqlite3.connect(kwargs.get('db_name'))
            c = conn.cursor()
            c.execute(query)
            conn.commit()
            result = c.fetchall()
            conn.close()
            return result

        return wrapped_f

    return wrap


@execute_db('Initializing...')
def initialize_db(db_name=None):
    return '''CREATE TABLE IF NOT EXISTS job_status
                 (job_id text, schedule_time date, execution_time date, status integer, runs integer, uid text)'''


@execute_db('Reading data...')
def read_all_jobs(db_name=None):
    return 'SELECT * FROM job_status;'


@execute_db('Removing old entries...')
def remove_old_data(days, db_name=None):
    date_time = (datetime.datetime.now().date() - datetime.timedelta(days=days)).isoformat()
    return '''DELETE FROM job_status WHERE schedule_time < "%s";''' % date_time


@execute_db('Updating job status...')
def set_failed(job_id, schedule_time, db_name=None):
    return 'UPDATE job_status SET status = %s WHERE job_id = "%s" AND schedule_time = "%s"' % (
        job_status.get('failed'), job_id, schedule_time)


@execute_db('Updating job status...')
def set_succeeded(job_id, schedule_time, db_name=None):
    return 'UPDATE job_status SET status = %s WHERE job_id = "%s" AND schedule_time = "%s"' % (
        job_status.get('succeeded'), job_id, schedule_time)


@execute_db('Updating job status...')
def set_not_ready(job_id, schedule_time, db_name=None):
    return 'UPDATE job_status SET status = %s WHERE job_id = "%s" AND schedule_time = "%s"' % (
        job_status.get('not_ready'), job_id, schedule_time)


@execute_db('Updating job status...')
def set_ready(job_id, schedule_time, db_name=None):
    return 'UPDATE job_status SET status = %s WHERE job_id = "%s" AND schedule_time = "%s"' % (
        job_status.get('ready'), job_id, schedule_time)


@execute_db('Updating job status...')
def set_running(job_id, schedule_time, uid, db_name=None):
    return 'UPDATE job_status SET status = %s, runs = runs + 1, uid = "%s", execution_time = "%s" WHERE job_id = "%s" AND schedule_time = "%s"' % (
        job_status.get('running'), uid, datetime.datetime.now().isoformat(), job_id, schedule_time)


@execute_db("List all jobs...")
def get_all_job_ids(db_name=None):
    return 'SELECT DISTINCT job_id from job_status;'


@execute_db('Adding a new entry...')
def add_new_job(job_id, schedule_time, db_name=None):
    return 'INSERT INTO job_status VALUES ("%s", "%s", "", 0, 0, "");' % (job_id, schedule_time)


@execute_db('test')
def insert_dummy_job(job_id, schedule_time, execution_time, status, runs, uid, db_name=None):
    return 'insert into job_status values ("%s", "%s", "%s", %s, %s, %s);' % (
        job_id, schedule_time, execution_time, status, runs, uid,)


@execute_db('Getting job info...')
def get_job_info(job_id, db_name=None):
    return 'SELECT * FROM job_status WHERE job_id = "%s"' % job_id


@execute_db('Getting job schedule status...')
def get_job_schedule_status(job_id, schedule_time, db_name=None):
    return 'SELECT * FROM job_status WHERE job_id = "%s" and schedule_time = "%s";' % (job_id, schedule_time)


@execute_db('Getting job schedule status...')
def check_job_succeeded(job_id, schedule_time, db_name=None):
    return 'SELECT * FROM job_status WHERE job_id = "%s" and schedule_time = "%s" and status = %s;' % (
        job_id, schedule_time, job_status.get('succeeded'))


@execute_db('Reset all jobs...')
def reset_all_jobs(db_name=None):
    return 'UPDATE job_status SET status=%s WHERE 1=1;' % job_status.get('not_ready')


update_job_status = {'ready': set_ready,
                     'not_ready': set_not_ready,
                     'failed': set_failed,
                     'succeeded': set_succeeded}


