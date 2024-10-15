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
    ```

3. Do **not** commit your `.env` file to version control. The `.env` file is included in `.gitignore` for security reasons.
