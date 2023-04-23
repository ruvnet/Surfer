#              - chatgpt-huggingface-plugin 
#     /\__/\   - main.py 
#    ( o.o  )  - v0.0.1
#      >^<     - by @rUv

import httpx
import json
import logging
import mimetypes
import os
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, validator
from typing import List, Optional


app = FastAPI()

HUGGINGFACE_API_KEY = os.environ["HUGGINGFACE_API_KEY"]
HUGGINGFACE_BASE_URL = "https://huggingface.co"
# HUGGINGFACE_BASE_URL = "https://api.endpoints.huggingface.cloud"
logging.basicConfig(level=logging.DEBUG)

@app.get("/api/models/{repo_id}", description="Get all information for a specific model.")
async def model_info(repo_id: str):
    api_url = f"{HUGGINGFACE_BASE_URL}/api/models/{repo_id}"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

@app.get("/api/models/{repo_id}/revision/{revision}", description="Get information for a specific model revision.")
async def model_info_revision(repo_id: str, revision: str):
    api_url = f"{HUGGINGFACE_BASE_URL}/api/models/{repo_id}/revision/{revision}"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

@app.get("/api/datasets-tags-by-type", description="Gets all the available dataset tags hosted in the Hub")
async def get_dataset_tags():
    api_url = f"{HUGGINGFACE_BASE_URL}/api/datasets-tags-by-type"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

@app.get("/api/spaces", description="Get information from all Spaces in the Hub.")
async def list_spaces(
    search: Optional[str] = None,
    author: Optional[str] = None,
    filter: Optional[str] = None,
    sort: Optional[str] = None,
    direction: Optional[str] = None,
    limit: Optional[int] = 10,
    full: Optional[bool] = None,
    config: Optional[bool] = None,
):
    params = {
        "search": search,
        "author": author,
        "filter": filter,
        "sort": sort,
        "direction": direction,
        "limit": limit,
        "full": full,
        "config": config,
    }
    params = {k: v for k, v in params.items() if v is not None}
    
    api_url = f"{HUGGINGFACE_BASE_URL}/api/spaces"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, headers=headers, params=params)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

@app.get("/api/spaces/{repo_id}", description="Get all information for a specific space.")
@app.get("/api/spaces/{repo_id}/revision/{revision}", description="Get all information for a specific space at a specific revision.")
async def space_info(repo_id: str, revision: Optional[str] = None):
    api_url = f"{HUGGINGFACE_BASE_URL}/api/spaces/{repo_id}"
    if revision:
        api_url += f"/revision/{revision}"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

@app.get("/api/metrics", description="Get information from all metrics in the Hub.")
async def list_metrics():
    api_url = f"{HUGGINGFACE_BASE_URL}/api/metrics"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

class CreateRepoRequest(BaseModel):
    type: Optional[str] = None
    name: str
    organization: Optional[str] = None
    private: Optional[bool] = False

class DeleteRepoRequest(BaseModel):
    type: str
    # repo_id: str
    name: str  # Add the "name" field to the request model


class UpdateRepoVisibilityRequest(BaseModel):
    private: bool

class MoveRepoRequest(BaseModel):
    fromRepo: str
    toRepo: str

class CreateSpaceRequest(BaseModel):
    type: str
    name: str
    private: bool
    sdk: str

@app.post("/api/repos/create", description="Create a new space in the Hugging Face Model Hub. The 'sdk' field must be one of ['streamlit', 'gradio', 'docker', 'static'].")
async def create_space(create_space_request: CreateSpaceRequest):
    try:
        # Construct the URL for the endpoint
        api_url = f"{HUGGINGFACE_BASE_URL}/api/repos/create"
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        # Convert the request payload to a dictionary
        data = create_space_request.dict()
        async with httpx.AsyncClient() as client:
            response = await client.post(api_url, headers=headers, json=data)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        return response.json()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/repos/delete/{name}", description="Delete a repository in the Hugging Face Model Hub.")
async def delete_repo(name: str, request: DeleteRepoRequest):
    try:
        # Construct the URL for the endpoint
        api_url = f"{HUGGINGFACE_BASE_URL}/api/repos/delete/{name}"
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method="DELETE", url=api_url, headers=headers, json=request.dict()
            )

        if response.status_code != 200:
            logging.error(f"Error response from Hugging Face API: {response.text}")
            return JSONResponse(status_code=response.status_code, content=response.text)

        return response.json()

    except Exception as e:
        logging.exception("An error occurred while processing the request")
        return JSONResponse(status_code=500, content={"detail": str(e)})


@app.put("/api/repos/{type}/{repo_id}/settings", description="Update repo visibility.")
async def update_repo_visibility(type: str, repo_id: str, request: UpdateRepoVisibilityRequest):
    api_url = f"{HUGGINGFACE_BASE_URL}/api/repos/{type}/{repo_id}/settings"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

    async with httpx.AsyncClient() as client:
        response = await client.put(api_url, headers=headers, json=request.dict())

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

@app.post("/api/repos/move", description="Move a repository (rename within same namespace or transfer from user to organization).")
async def move_repo(request: MoveRepoRequest):
    api_url = f"{HUGGINGFACE_BASE_URL}/api/repos/move"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

    async with httpx.AsyncClient() as client:
        response = await client.post(api_url, headers=headers, json=request.dict())

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

from fastapi import UploadFile, File

@app.post("/api/{type}/{repo_id}/upload/{revision}/{path_in_repo}", description="Upload a file to a specific repository.")
async def upload_file(type: str, repo_id: str, revision: str, path_in_repo: str, file: UploadFile = File(...)):
    api_url = f"{HUGGINGFACE_BASE_URL}/api/{type}/{repo_id}/upload/{revision}/{path_in_repo}"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

    async with httpx.AsyncClient() as client:
        response = await client.post(api_url, headers=headers, content=file.file.read())

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()

@app.get("/api/whoami-v2", description="Get username and organizations the user belongs to.")
async def whoami():
    api_url = f"{HUGGINGFACE_BASE_URL}/api/whoami-v2"
    headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()


class InferenceRequest(BaseModel):
    text: str
    model: str

class ComputeScaling(BaseModel):
    maxReplica: int
    minReplica: int

class Compute(BaseModel):
    accelerator: str
    instanceSize: str
    instanceType: str
    scaling: ComputeScaling

class Image(BaseModel):
    huggingface: dict

class Model(BaseModel):
    framework: str
    image: Image
    repository: str
    revision: str
    task: str

class Provider(BaseModel):
    region: str
    vendor: str

class EndpointInput(BaseModel):
    accountId: Optional[str] = None
    compute: Compute
    model: Model
    name: str
    provider: Provider
    type: str

class ModelImage(BaseModel):
    huggingface: dict

class ModelData(BaseModel):
    framework: str
    image: ModelImage
    repository: str
    revision: str
    task: str

class Scaling(BaseModel):
    maxReplica: int
    minReplica: int

class ComputeData(BaseModel):
    accelerator: str
    instanceSize: str
    instanceType: str
    scaling: Scaling

class UpdateEndpointPayload(BaseModel):
    compute: ComputeData
    model: ModelData

@app.put("/endpoint/{name}", description="Update an endpoint with the provided JSON payload.")
async def update_endpoint(name: str, payload: UpdateEndpointPayload):
    # Process the request and update the endpoint with the provided data.
    # Replace the following line with your actual implementation.
    response = {"message": f"Endpoint '{name}' updated successfully.", "data": payload}

    return response

@app.post("/endpoint", description="Create an endpoint with the given configuration.")
async def create_endpoint(payload: EndpointInput):
    # Process the payload and perform the required actions.
    # For now, just return the input payload as is.
    return payload

@app.delete("/endpoint/{name}", description="Delete an endpoint with the specified name.")
async def delete_endpoint(name: str):
    # Process the request and delete the endpoint with the specified name.
    # Replace the following line with your actual implementation.
    response = {"message": f"Endpoint '{name}' deleted successfully."}

    return response

@app.get("/endpoint/{endpoint_id}", description="Get information about a specific endpoint.")
async def get_endpoint(endpoint_id: str):
    api_url = f"{HUGGINGFACE_BASE_URL}/endpoint/{endpoint_id}"
    headers = {"Accept": "application/json", "Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(api_url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=response.text)

    return response.json()


@app.get("/list_models/", description="List all available models in the Hugging Face Model Hub.")
async def list_models(
    search: Optional[str] = None,
    author: Optional[str] = None,
    filter: Optional[str] = None,
    sort: Optional[str] = None,
    direction: Optional[str] = None,
    limit: Optional[int] = 10,
    full: Optional[bool] = False,
    config: Optional[bool] = False,
):
    try:
        api_url = "https://huggingface.co/api/models"
        
        query_params = {
            "search": search,
            "author": author,
            "filter": filter,
            "sort": sort,
            "direction": direction,
            "limit": limit,
            "full": full,
            "config": config,
        }
        
        query_params = {k: v for k, v in query_params.items() if v is not None}
        
        headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, headers=headers, params=query_params)

        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)

        return response.json()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/endpoint/{name}/logs", description="Get logs for the specified endpoint.")
async def get_endpoint_logs(name: str):
    # Process the request and fetch the logs for the specified endpoint.
    # Replace the following line with your actual implementation.
    response = {"message": f"Logs for endpoint '{name}'."}

    return response

@app.get("/endpoint/{name}/metrics", description="Get metrics for the specified endpoint.")
async def get_endpoint_metrics(name: str):
    # Process the request and fetch the metrics for the specified endpoint.
    # Replace the following line with your actual implementation.
    response = {"message": f"Metrics for endpoint '{name}'."}

    return response

@app.get("/provider", description="Get provider information.")
async def get_provider():
    # Process the request and fetch provider information.
    # Replace the following line with your actual implementation.
    response = {"message": "Provider information."}

    return response

@app.get("/provider/{vendor}/region", description="Get regions for the specified provider.")
async def get_provider_regions(vendor: str):
    # Process the request and fetch regions for the specified provider.
    # Replace the following line with your actual implementation.
    response = {"message": f"Regions for provider '{vendor}'."}

    return response

@app.get("/provider/{vendor}/region/{region}/compute", description="Get compute information for the specified provider and region.")
async def get_provider_region_compute(vendor: str, region: str):
    # Process the request and fetch compute information for the specified provider and region.
    # Replace the following line with your actual implementation.
    response = {"message": f"Compute information for provider '{vendor}' in region '{region}'."}

    return response

# Additional endpoints can be added here as needed...
# Define a route for serving files from the ".well-known" path
@app.get('/.well-known/{filename}')
async def download(filename: str):
    file_path = 'plugins/' + filename  # Construct the file path based on the filename
    media_type, _ = mimetypes.guess_type(file_path)  # Determine the MIME type of the file
    return FileResponse(file_path, media_type=media_type or 'text/plain')  # Serve the file

# Run the FastAPI application using the Uvicorn ASGI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
