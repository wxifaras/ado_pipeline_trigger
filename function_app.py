import json
import os
import azure.functions as func # type: ignore
from azure_devops_trigger import check_azure_pipeline_status, trigger_azure_pipeline  # No cross-imports from init
from opencensus.ext.azure.log_exporter import AzureLogHandler
from app_logger import get_logger

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# Get the logger for this module (example.py)
logger = get_logger(__name__)

# List of allowed pipeline IDs from environment
allowed_pipeline_ids = list(map(int, os.getenv('PIPELINE_IDS', '').split(',')))

@app.route(route="pipeline_trigger")
def pipeline_trigger(req: func.HttpRequest) -> func.HttpResponse:
    pipeline_id = req.params.get('pipeline_id')
    logger.info(f'Azure HTTP trigger function pipeline_trigger processed a request. Pipeline ID: {pipeline_id}.')
        
    if not pipeline_id:
        logger.error("Invalid request. No valid pipeline_id found.")

    if pipeline_id:
        try:
            pipeline_id = int(pipeline_id)
        except ValueError:
            logger.error(f"Invalid pipeline_id {pipeline_id} is not an integer.")
            return func.HttpResponse(
                "Invalid pipeline_id. It must be an integer.",
                status_code=400
            )
        
        if pipeline_id not in allowed_pipeline_ids:
            logger.warning(f"Unauthorized pipeline_id: {pipeline_id}")
            return func.HttpResponse(
                f"Unauthorized pipeline_id: {pipeline_id}. You are not allowed to trigger this pipeline.",
                status_code=403
            )
        
        response_message = trigger_azure_pipeline(pipeline_id)
        logger.info(f"Response from trigger_azure_pipeline: {response_message}")
        return func.HttpResponse(response_message)
    else:
        logger.warning("No pipeline_id provided.")
        return func.HttpResponse(
            "This HTTP triggered function executed successfully, but no pipeline_id was provided.",
            status_code=200
        )

@app.route(route="check_pipeline_status_trigger")
def check_pipeline_status_trigger(req: func.HttpRequest) -> func.HttpResponse:
    pipeline_id = req.params.get('pipeline_id')
    logger.info(f'Azure HTTP trigger function check_pipeline_status_trigger processed a request. Pipeline ID: {pipeline_id}.')

    if not pipeline_id:
        logger.error("Invalid request. No valid pipeline_id found.")

    if pipeline_id:
        try:
            pipeline_id = int(pipeline_id)
        except ValueError:
            logger.error(f"Invalid pipeline_id {pipeline_id} is not an integer.")
            return func.HttpResponse(
                "Invalid pipeline_id. It must be an integer.",
                status_code=400
            )
        
        if pipeline_id not in allowed_pipeline_ids:
            logger.warning(f"Unauthorized pipeline_id: {pipeline_id}")
            return func.HttpResponse(
                f"Unauthorized pipeline_id: {pipeline_id}. You are not allowed to trigger this pipeline.",
                status_code=403
            )
        
        pipeline_status = check_azure_pipeline_status(pipeline_id)
        response_message = json.dumps(pipeline_status)

        logger.info(f"Response from check_pipeline_status: {response_message}")
        return func.HttpResponse(response_message)
    else:
        logger.warning("No pipeline_id provided.")
        return func.HttpResponse(
            "This HTTP triggered function executed successfully, but no pipeline_id was provided.",
            status_code=200
        )

@app.route(route="trigger_all_pipelines")
def trigger_all_pipelines(req: func.HttpRequest) -> func.HttpResponse:
    logger.info('Azure HTTP trigger function for all pipelines started.')

    results = []
    for pipeline_id in allowed_pipeline_ids:
        logger.info(f"Triggering pipeline with ID: {pipeline_id}")
        response_message = trigger_azure_pipeline(pipeline_id)
        results.append(f"Pipeline {pipeline_id}: {response_message}")
    
    return func.HttpResponse("\n".join(results), status_code=200)