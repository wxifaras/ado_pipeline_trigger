# Azure DevOps Pipeline Trigger Functions

This project provides Azure Functions that allow you to trigger Azure DevOps pipelines via HTTP requests. The environment is configured using a `.env` file and functions are designed to handle specific pipelines based on the provided pipeline IDs.

## Environment Variables

This project uses a `.env` file to manage sensitive configuration for Azure DevOps. To set up your local environment:

1. Copy the `.env.example` file and rename it to `.env`:
    ```bash
    cp .env.example .env
    ```

2. Open the `.env` file and update the values with your own credentials and configuration:

    - `AZURE_DEVOPS_ORG_URL`: Your Azure DevOps organization URL (e.g., `https://dev.azure.com/your-org-name`)
    - `AZURE_DEVOPS_TOKEN`: Your Azure DevOps personal access token (PAT)
    - `PIPELINE_IDS`: A comma-separated list of pipeline IDs you want to monitor (e.g., `1,2,3`)
    - `PROJECT_NAME`: The name of your project

    Example `.env` file:
    ```bash
    AZURE_DEVOPS_ORG_URL=https://dev.azure.com/my-org
    AZURE_DEVOPS_TOKEN=my-secret-token
    PIPELINE_IDS=1,2,3
    PROJECT_NAME=my-project
    APP_INSIGHTS_INSTRUMENTATION_KEY=<your app insights instrumentation key>
    ```

3. Do **not** commit your `.env` file to version control. The `.env` file is included in `.gitignore` for security reasons.

## Azure Function HTTP Triggers

This project includes an Azure Function HTTP trigger that interact with Azure DevOps pipelines. The trigger uses environment variables and handle pipeline authorization based on the IDs defined in the `PIPELINE_IDS` environment variable.

### `pipeline_trigger`

This function is an HTTP trigger that allows triggering a single Azure DevOps pipeline based on the `pipeline_id` provided in the request.

- **Route:** `pipeline_trigger`
- **Method:** `POST`
- **Query Parameters:**
    - `pipeline_id`: (Required) The ID of the pipeline to trigger.

- **Example Request (POST):**

  ```http
  POST /pipeline_trigger?pipeline_id=1
  ```
 ### `check_pipeline_status_trigger`

 This function is an HTTP trigger that will check the status of an Azure DevOps pipeline based on the `pipeline_id` provided in the request.

 - **Route:** `check_pipeline_status_trigger`
 - **Method:** `GET`
 - **Query Parameters:**
    - `pipeline_id`: (Required) The ID of the pipeline to check.

- **Example Request (GET):**

  ```http
  GET /check_pipeline_status_trigger?pipeline_id=1
  ```
 
