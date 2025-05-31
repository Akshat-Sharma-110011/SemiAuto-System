from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import httpx
import os

app = FastAPI(title="SemiAuto Main System", version="1.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates
templates = Jinja2Templates(directory="templates")

# Microservice URLs (adjust ports as needed)
MICROSERVICES = {
    "regression": "http://localhost:8030",
    "classification": "http://localhost:8020",
    "clustering": "http://localhost:8010"
}

# Global variable to store selected service
selected_service = None


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Main entry point with service selection"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/select-service")
async def select_service(request: Request):
    """Set the selected service type"""
    global selected_service
    form_data = await request.form()
    service_type = form_data.get("service_type")

    if service_type not in MICROSERVICES:
        raise HTTPException(status_code=400, detail="Invalid service type")

    selected_service = service_type
    return RedirectResponse(url="/service-home", status_code=303)


@app.get("/service-home", response_class=HTMLResponse)
async def service_home(request: Request):
    """Home page for the selected service"""
    if not selected_service:
        return RedirectResponse(url="/")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{MICROSERVICES[selected_service]}/")
        return HTMLResponse(content=response.text)
    except httpx.ConnectError:
        raise HTTPException(
            status_code=503,
            detail=f"{selected_service.capitalize()} microservice is unavailable"
        )


@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_request(request: Request, path: str):
    """Proxy all requests to the appropriate microservice"""
    if not selected_service:
        return RedirectResponse(url="/")

    # Get target URL
    target_url = f"{MICROSERVICES[selected_service]}/{path}"

    # Forward the request
    async with httpx.AsyncClient() as client:
        # Prepare request
        client_request = client.build_request(
            method=request.method,
            url=target_url,
            headers=dict(request.headers),
            params=dict(request.query_params),
        )

        # Handle form data
        if request.method in ["POST", "PUT"]:
            form_data = await request.form()
            client_request = client.build_request(
                method=request.method,
                url=target_url,
                data=dict(form_data),
                headers=dict(request.headers),
                params=dict(request.query_params),
            )

        # Send request
        response = await client.send(client_request)

        # Return response
        return HTMLResponse(
            content=response.content,
            status_code=response.status_code,
            headers=dict(response.headers)
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)