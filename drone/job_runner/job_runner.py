import sys
from drone.actions.emr_launcher import launch_emr_task
from drone.actions.ssh_launcher import launch_ssh_task
from drone.job_runner.dependency_manager import dependencies_are_met
from drone.job_runner.job_progress_checker import check_running_job_progress
from drone.metadata.metadata import get_job_info, job_status, set_ready, set_running, set_failed

task_launcher = {'ssh': launch_ssh_task,
                 'emr': launch_emr_task}


def process(job_config, settings):
    for job_id, schedule_time, execution_time, status, runs, uid in get_job_info(job_config.get('id'),
                                                                                 db_name=settings.metadata):

        if status == job_status.get('failed'):
            if (int(job_config.get('retry')) if job_config.get('retry') else 0) > int(runs):
                if dependencies_are_met(job_config, schedule_time, settings):
                    set_ready(job_config.get('id'), schedule_time, db_name=settings.metadata)
                    settings.logger.info('Job "%s" "%s" set as ready' % (job_config.get('id'), schedule_time))
                    run(job_config, schedule_time, settings)
                    continue
                else:
                    continue
            else:
                continue
        elif status == job_status.get('running'):
            check_running_job_progress(job_config, schedule_time, uid, settings)
            continue
        elif status == job_status.get('ready'):
            run(job_config, schedule_time, settings)
        elif status == job_status.get('succeeded'):
            continue
        elif status == job_status.get('not_ready'):
            if dependencies_are_met(job_config, schedule_time, settings):
                set_ready(job_config.get('id'), schedule_time, db_name=settings.metadata)
                settings.logger.info('Job "%s" "%s" set as ready' % (job_config.get('id'), schedule_time))
                run(job_config, schedule_time, settings)
            else:
                continue
        else:
            settings.logger.error('Unknown job status "%s"' % status)
            sys.exit(1)


def run(job_config, schedule_time, settings):
    settings.logger.info('Starting job "%s" "%s"' % (job_config.get('id'), schedule_time))
    job_type = job_config.get('type')
    try:
        assert job_type in settings.supported_job_types
    except:
        settings.logger.warning(
            'Unsupported job type %s. Valid types are %s' % (job_type, str(settings.supported_job_types)))

    task_lauched_successfully, uid = task_launcher.get(job_type)(job_config, schedule_time, settings)

    if task_lauched_successfully:
        set_running(job_config.get('id'), schedule_time, uid, db_name=settings.metadata)
        settings.logger.info('Started job "%s" "%s"' % (job_config.get('id'), schedule_time))
    else:
        set_failed(job_config.get('id'), schedule_time, db_name=settings.metadata)
        settings.logger.warning('Failed to start job "%s" "%s"' % (job_config.get('id'), schedule_time))

