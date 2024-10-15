import os
import azure.functions as func # type: ignore
import logging
from azure_devops_trigger import trigger_azure_pipeline  # No cross-imports from init

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

# List of allowed pipeline IDs from environment
allowed_pipeline_ids = list(map(int, os.getenv('PIPELINE_IDS', '').split(',')))

@app.route(route="ado_pipeline_http_trigger")
def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Azure HTTP trigger function processed a request.')

    pipeline_id = req.params.get('pipeline_id')
    if not pipeline_id:
        try:
            req_body = req.get_json()
        except ValueError:
            logging.error("Invalid request. No valid pipeline_id found.")
            return func.HttpResponse(
                "Invalid request. Please pass pipeline_id in the query string or request body.",
                status_code=400
            )
        else:
            pipeline_id = req_body.get('pipeline_id')

    if pipeline_id:
        try:
            pipeline_id = int(pipeline_id)
        except ValueError:
            logging.error(f"Invalid pipeline_id {pipeline_id} is not an integer.")
            return func.HttpResponse(
                "Invalid pipeline_id. It must be an integer.",
                status_code=400
            )
        
        if pipeline_id not in allowed_pipeline_ids:
            logging.warning(f"Unauthorized pipeline_id: {pipeline_id}")
            return func.HttpResponse(
                f"Unauthorized pipeline_id: {pipeline_id}. You are not allowed to trigger this pipeline.",
                status_code=403
            )
        
        response_message = trigger_azure_pipeline(pipeline_id)
        logging.info(f"Response from pipeline trigger: {response_message}")
        return func.HttpResponse(response_message)
    else:
        logging.warning("No pipeline_id provided.")
        return func.HttpResponse(
            "This HTTP triggered function executed successfully, but no pipeline_id was provided.",
            status_code=200
        )

@app.route(route="trigger_all_pipelines")
def trigger_all_pipelines(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Azure HTTP trigger function for all pipelines started.')

    results = []
    for pipeline_id in allowed_pipeline_ids:
        logging.info(f"Triggering pipeline with ID: {pipeline_id}")
        response_message = trigger_azure_pipeline(pipeline_id)
        results.append(f"Pipeline {pipeline_id}: {response_message}")
    
    return func.HttpResponse("\n".join(results), status_code=200)