import subprocess

from drone.metadata.metadata import set_succeeded, set_failed
from drone.config.supported_remote_hosts import remote_servers


def check_ssh_task_status(job_config, schedule_time, pid_file, settings):
    job_id = job_config.get('id')

    remote_server_id = job_config.get('remote_server_id')
    remote_server_config = remote_servers.get(remote_server_id)
    remote_server_ssh_key = remote_server_config.get('ssh_details').get('ssh_key')
    remote_server_username = remote_server_config.get('ssh_details').get('username')
    remote_server_host = remote_server_config.get('ssh_details').get('host')

    get_pid_id_cmd = ['ssh', '-i', remote_server_ssh_key, '@'.join([remote_server_username, remote_server_host]), 'cat',
                      pid_file]

    get_pid_id_proc = subprocess.Popen(get_pid_id_cmd, stdout=subprocess.PIPE)
    pid_id = get_pid_id_proc.communicate()[0].strip()
    exit_code = get_pid_id_proc.returncode

    if exit_code != 0:
        set_succeeded(job_id, schedule_time, db_name=settings.metadata)
        settings.logger.info('%s %s has succeeded' % (job_id, schedule_time))
        return
    else:
        check_running_process_cmd = ['ssh', '-i', remote_server_ssh_key,
                                     '@'.join([remote_server_username, remote_server_host]), 'ps', '-p',
                                     pid_id]

        check_if_process_still_running = subprocess.Popen(check_running_process_cmd)
        ps_output = check_if_process_still_running.communicate()
        process_running = check_if_process_still_running.returncode

        if process_running == 0:
            return
        else:
            set_failed(job_id, schedule_time, db_name=settings.metadata)
            settings.logger.warning('%s %s has failed' % (job_id, schedule_time))
            return


def check_emr_task(job_config, schedule_time, uid, settings):
    return NotImplemented


task_checker = {'ssh': check_ssh_task_status,
                'emr': check_emr_task}


def check_running_job_progress(job_config, schedule_time, uid, settings):
    job_type = job_config.get('type')
    task_checker.get(job_type)(job_config, schedule_time, uid, settings)
