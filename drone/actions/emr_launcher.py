import boto3
from botocore.exceptions import ClientError
from drone.utils.helpers import parse_schedule_time


def launch_emr_task(job_config, schedule_time, settings):
    settings.logger.info('Creating EMR client')
    emr_client = boto3.client('emr')
    settings.logger.info('EMR client created')

    #ugly hack
    steps_from_json = job_config.get('Steps', [])
    for step_config in steps_from_json:
        for arg_id in range(len(step_config.get('HadoopJarStep').get('Args'))):
            step_config['HadoopJarStep']['Args'][arg_id] = parse_schedule_time(
                step_config['HadoopJarStep']['Args'][arg_id], schedule_time)

    try:
        aws_response = emr_client.run_job_flow(
            Name='_'.join([job_config.get('id'), schedule_time]),
            LogUri=job_config.get('LogUri', ''),
            AmiVersion=job_config.get('AmiVersion', ''),
            Instances=job_config.get('Instances'),
            Steps=steps_from_json,
            BootstrapActions=job_config.get('BootstrapActions', []),
            SupportedProducts=job_config.get('SupportedProducts', []),
            NewSupportedProducts=job_config.get('NewSupportedProducts', []),
            Applications=job_config.get('Applications', []),
            Configurations=job_config.get('Configurations', []),
            VisibleToAllUsers=True if job_config.get('VisibleToAllUsers') == "True" else False,
            JobFlowRole=job_config.get('JobFlowRole', settings.job_flow_role),
            ServiceRole=job_config.get('ServiceRole', settings.service_role)
        )
    except ClientError:
        settings.logger.info('Invalid AWS response for %s' % job_config)
        return False, None

    settings.logger.info('AWS response\n%s' % aws_response)

    success = aws_response.get('ResponseMetadata').get('HTTPStatusCode') == 200
    cluster_id = aws_response.get('JobFlowId')
    return success, cluster_id
