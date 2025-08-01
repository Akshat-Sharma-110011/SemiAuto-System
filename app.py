from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse, Response  # Changed
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import httpx
import os

app = FastAPI(title="SemiAuto Main System", version="1.0")

# Templates
templates = Jinja2Templates(directory="templates")

# Microservice URLs
MICROSERVICES = {
    "regression": "http://semiauto-regression:8030",
    "classification": "http://semiauto-classification:8020",
    "clustering": "http://semiauto-clustering:8010"
}

# Global variable to store selected service
selected_service = None

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/select-service")
async def select_service(request: Request):
    global selected_service
    form_data = await request.form()
    service_type = form_data.get("service_type")

    if service_type not in MICROSERVICES:
        raise HTTPException(status_code=400, detail="Invalid service type")

    selected_service = service_type
    return RedirectResponse(url="/service-home", status_code=303)

@app.get("/service-home")
async def service_home(request: Request):
    global selected_service  # Add this line
    if not selected_service:
        return RedirectResponse(url="/")
    # Pass selected_service as the third argument
    return await proxy_request(request, "", selected_service)

# New catch-all route for all other endpoints
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def catch_all(request: Request, path: str):
    if not selected_service:
        return RedirectResponse(url="/")
    return await proxy_request(request, path, selected_service)


# Add this ABOVE your existing catch-all route
@app.api_route("/{service_name}-static/{file_path:path}", methods=["GET"])
async def static_proxy(request: Request, service_name: str, file_path: str):
    # Identify service
    service = None
    if service_name == "regression":
        service = "regression"
    elif service_name == "classification":
        service = "classification"
    elif service_name == "clustering":
        service = "clustering"

    if not service:
        raise HTTPException(status_code=404, detail="Static path not recognized")

    return await proxy_request(request, f"{service_name}-static/{file_path}", service)


async def proxy_request(request: Request, path: str, service: str):
    target_url = f"{MICROSERVICES[service]}/{path}"
    # Ensure we don't create double slashes
    target_url = target_url.replace("//", "/").replace(":/", "://")
    timeout = httpx.Timeout(300.0, connect=60.0)

    async with httpx.AsyncClient(timeout=timeout) as client:
        client_request = client.build_request(
            method=request.method,
            url=target_url,
            headers={k: v for k, v in request.headers.items()
                     if k.lower() not in ["host", "content-length"]},
            params=request.query_params,
            content=await request.body()
        )

        try:
            response = await client.send(client_request)
        except httpx.ConnectError:
            raise HTTPException(
                status_code=503,
                detail=f"{service.capitalize()} microservice unavailable"
            )

        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers)
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)