from __future__ import division
import datetime
from drone.metadata.metadata import get_job_schedule_status, add_new_job, remove_old_data
from drone.utils.config_loader import get_config
from drone.utils.helpers import string_to_iso_datetime


def sync_job(job_config, settings):
    job_id = job_config.get('id')
    job_config_start_datetime = string_to_iso_datetime(job_config.get('start_time'))
    job_schedule_datetime_end = datetime.datetime.now() + datetime.timedelta(days=settings.metadata_future_days)

    if job_config_start_datetime <= job_schedule_datetime_end:
        job_schedule_datetime_start = string_to_iso_datetime(max(job_config_start_datetime,
                                                                 datetime.datetime.now() - datetime.timedelta(
                                                                     days=settings.metadata_history_days)).strftime('%Y-%m-%d') + 'T' +
                                                             job_config_start_datetime.strftime('%H:%M:%S'))

        delta_schedule_seconds = (job_schedule_datetime_end - job_schedule_datetime_start).days * 1440
        job_schedule_interval_minutes = int(job_config.get('interval_minutes') or 60)
        job_schedule = [
            (job_schedule_datetime_start + datetime.timedelta(
                minutes=i * job_schedule_interval_minutes)).isoformat()
            for i in range(int(delta_schedule_seconds / job_schedule_interval_minutes))]

        for schedule_time in job_schedule:
            if not job_is_present(job_id, schedule_time, db_name=settings.metadata):
                add_new_job(job_id, schedule_time, db_name=settings.metadata)
    else:
        # Ignore all jobs that will start in the future
        pass


def job_is_present(job_id, schedule_time, db_name):
    return get_job_schedule_status(job_id, schedule_time, db_name=db_name)


def sync_jobs(settings):
    remove_old_data(settings.metadata_history_days, db_name=settings.metadata)
    remote_jobs = get_config(settings.remote_jobs_config, settings.remote_jobs_config_schema)
    aws_jobs = get_config(settings.aws_jobs_config, settings.aws_jobs_config_schema)
    for remote_job_config in remote_jobs.get('jobs', {}):
        sync_job(remote_job_config, settings)
    for aws_job_config in aws_jobs.get('jobs', {}):
        sync_job(aws_job_config, settings)
    return remote_jobs.get('jobs', []) + aws_jobs.get('jobs', [])
