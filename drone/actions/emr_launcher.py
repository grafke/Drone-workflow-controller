from pprint import pprint
import boto3
import sys


def launch_emr_task(job_config, schedule_time, setting):

    client = boto3.client('emr')
    pprint(job_config)

    response = client.run_job_flow(
        Name=job_config.get('Name'),
        LogUri=job_config.get('LogUri', ''),
        AmiVersion=job_config.get('AmiVersion', ''),
        Instances= job_config.get('Instances'),
        Steps=job_config.get('Steps', []),
        BootstrapActions=job_config.get('BootstrapActions', []),
        SupportedProducts=job_config.get('SupportedProducts', []),
        NewSupportedProducts=job_config.get('NewSupportedProducts', []),
        Applications=job_config.get('Applications', []),
        Configurations=job_config.get('Configurations', []),
        VisibleToAllUsers=True if job_config.get('VisibleToAllUsers') == "True" else False,
        JobFlowRole=job_config.get('JobFlowRole', 'EMR_EC2_DefaultRole'),
        ServiceRole=job_config.get('ServiceRole', 'EMR_DefaultRole'),
        Tags=job_config.get('Tags', [])
    )

    success = False
    cluster_id = None
    #return success, cluster_id
    return response