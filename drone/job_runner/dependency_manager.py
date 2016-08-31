from datetime import timedelta, datetime

from drone.metadata.metadata import check_job_succeeded
from drone.config.settings import supported_dependencies
from drone.utils.helpers import string_to_iso_datetime


def check_job_dependency(dependency, job_schedule_time, settings):
    dependency_type = dependency.keys()[0]
    dependency_job_id = dependency.get(dependency_type).get('id')
    dependency_job_schedule_time_lag = dependency.get(dependency_type).get(
        'last_schedule_time_interval_minutes')
    dependency_job_schedule_time = (string_to_iso_datetime(job_schedule_time) - timedelta(
        minutes=int(dependency_job_schedule_time_lag))).isoformat()
    if check_job_succeeded(dependency_job_id, dependency_job_schedule_time, db_name=settings.metadata):
        return True
    else:
        return False


dependency_is_met = {'job_completed': check_job_dependency}


def dependencies_are_met(job_config, schedule_time, settings):
    delay_minutes = int(job_config.get('delay_minutes') or 1440)
    if string_to_iso_datetime(schedule_time) + timedelta(minutes=delay_minutes) >= datetime.now():
        return False

    for dependency in job_config.get('dependencies', []):
        dependency_type = dependency.keys()[0]
        if dependency_type not in supported_dependencies:
            settings.logger.error('Unsupported dependency type "%s"') % dependency_type
            return False
        else:
            if dependency_is_met.get(dependency_type)(dependency, schedule_time, settings):
                continue
            else:
                return False

    return True
