import logging
from azure.devops.connection import Connection # type: ignore
from msrest.authentication import BasicAuthentication # type: ignore
from app_logger import get_logger
import os

logger = get_logger(__name__)

organization_url = os.getenv('AZURE_DEVOPS_ORG_URL')
personal_access_token = os.getenv('AZURE_DEVOPS_TOKEN')
project_name = os.getenv('PROJECT_NAME')
    
if not organization_url:
    raise EnvironmentError("The 'AZURE_DEVOPS_ORG_URL' environment variable is not set.")
if not personal_access_token:
    raise EnvironmentError("The 'AZURE_DEVOPS_TOKEN' environment variable is not set.")
if not project_name:
    raise EnvironmentError("The 'PROJECT_NAME' environment variable is not set.")

# Method to trigger Azure DevOps pipeline
def trigger_azure_pipeline(pipeline_id: int):
    logger.info(f"Triggering Azure DevOps pipeline with ID: {pipeline_id}")
    credentials = BasicAuthentication('', personal_access_token)
    connection = Connection(base_url=organization_url, creds=credentials)
    
    pipelines_client = connection.clients.get_pipelines_client()

    # Run the pipeline
    try:
        run_parameters = {
            "resources": {
                "repositories": {
                    "self": {
                        "refName": "refs/heads/main"  # Default to the main branch
                    }
                }
            }
        }

        # Trigger the pipeline
        pipeline_run = pipelines_client.run_pipeline(project=project_name, pipeline_id=pipeline_id, run_parameters=run_parameters)
        
        logger.info(f"Pipeline {pipeline_id} triggered successfully with Run ID: {pipeline_run}")
        return f"Pipeline {pipeline_id} triggered successfully!"
    except Exception as e:
        logger.error(f"Failed to trigger pipeline {pipeline_id}: {e}")
        return f"Failed to trigger pipeline: {str(e)}"

# Method to check the status of the Azure DevOps pipeline
def check_azure_pipeline_status(pipeline_id: int):
    # Create a connection to the organization
    credentials = BasicAuthentication('', personal_access_token)
    connection = Connection(base_url=organization_url, creds=credentials)

    # Get a client to interact with the Build service
    build_client = connection.clients.get_build_client()

    # Get the latest build (pipeline run) for the specified pipeline ID
    builds = build_client.get_builds(project=project_name, definitions=[pipeline_id], top=1)

    # If builds are found, return the build details
    if builds and len(builds) > 0:
        build = builds[0]
        return {
                "pipeline_id": build.definition.id,
                "build_number": build.build_number,
                "status": build.status,
                "result": build.result,
                "queue_time": build.queue_time.isoformat() if build.queue_time else None,
                "start_time": build.start_time.isoformat() if build.start_time else None,
                "finish_time": build.finish_time.isoformat() if build.finish_time else None
            }
    else:
        return {"message": f"No builds found for pipeline ID: {pipeline_id}"}