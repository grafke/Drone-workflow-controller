import boto3


def launch_emr_task(job_config, schedule_time, settings):

    emr_client = boto3.client('emr')

    aws_response = emr_client.run_job_flow(
        Name=job_config.get('id'),
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
        JobFlowRole=job_config.get('JobFlowRole', 'AmazonElasticMapReduceRole'),
        ServiceRole=job_config.get('ServiceRole', 'EMR_EC2_DefaultRole')
    )

    success = aws_response.get('ResponseMetadata').get('HTTPStatusCode') == 200
    cluster_id = aws_response.get('JobFlowId')
    return success, cluster_id
