import logging
from azure.devops.connection import Connection # type: ignore
from msrest.authentication import BasicAuthentication # type: ignore
import os

# Method to trigger Azure DevOps pipeline
def trigger_azure_pipeline(pipeline_id: int):
    # Azure DevOps organization URL and personal access token (PAT)
    organization_url = os.getenv('AZURE_DEVOPS_ORG_URL')  # Set as environment variable
    personal_access_token = os.getenv('AZURE_DEVOPS_TOKEN')  # Set as environment variable
    project_name = os.getenv('PROJECT_NAME')  # Set as environment variable
    
    logging.info(f"Triggering Azure DevOps pipeline with ID: {pipeline_id}")

    # Authenticate with Azure DevOps
    credentials = BasicAuthentication('', personal_access_token)
    connection = Connection(base_url=organization_url, creds=credentials)
    
    # Get the pipeline client
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
        
        logging.info(f"Pipeline {pipeline_id} triggered successfully with Run ID: {pipeline_run.id}")
        return f"Pipeline {pipeline_id} triggered successfully!"
    except Exception as e:
        logging.error(f"Failed to trigger pipeline: {e}")
        return f"Failed to trigger pipeline: {str(e)}"