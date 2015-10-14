import os
import subprocess

from drone.config.supported_remote_hosts import remote_servers
from drone.utils.helpers import job_id_generator


def ssh_task_cmd_generator(remote_action_script, remote_action_script_args, remote_server_config, unique_job_id,
                           settings):
    remote_server_host = remote_server_config.get('ssh_details').get('host')
    remote_server_username = remote_server_config.get('ssh_details').get('username')
    remote_server_password = remote_server_config.get('ssh_details').get('password')
    remote_server_ssh_key = remote_server_config.get('ssh_details').get('ssh_key')
    remote_server_stdout_file = os.path.join(remote_server_config.get('logging').get('stdout_log_dir'),
                                             unique_job_id + '.stdout.log')
    remote_server_stderr_file = os.path.join(remote_server_config.get('logging').get('stderr_log_dir'),
                                             unique_job_id + '.stderr.log')
    remote_server_pid_file = os.path.join(remote_server_config.get('logging').get('pid_file_dir'),
                                          unique_job_id + '.pid')

    if remote_server_ssh_key:
        return [os.path.join(os.path.dirname(os.path.realpath(__file__)), 'remote_action_launcher.sh'),
                remote_server_ssh_key, remote_server_username,
                remote_server_host, remote_action_script, remote_server_stdout_file,
                remote_server_stderr_file, remote_server_pid_file] + remote_action_script_args, remote_server_pid_file
    else:
        settings.logger.warning('Please provide a SSH key. Direct login is not supported yet.')
        return None, None


def launch_ssh_task(job_config, schedule_time, settings):
    unique_job_id = job_id_generator(job_config.get('id'), schedule_time)

    remote_server_id = job_config.get('remote_server_id')
    remote_server_config = remote_servers.get(remote_server_id)

    remote_action_script = job_config.get('remote_action').get('script')
    remote_action_script_args = job_config.get('remote_action').get('args')

    local_action_cmd, uid = ssh_task_cmd_generator(remote_action_script, remote_action_script_args,
                                                   remote_server_config, unique_job_id, settings)

    subprocess.Popen(local_action_cmd)

    if local_action_cmd:
        return True, uid
    else:
        return False, None
