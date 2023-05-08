import os
from fastapi import FastAPI, Form, Request, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
from import_doc import main as doc_main, get_internship_template
from starlette.responses import FileResponse
from jinja2 import Environment, FileSystemLoader
from fastapi.responses import JSONResponse

from pydantic import BaseSettings

# Create a Jinja2 environment with the path to your templates directory
env = Environment(loader=FileSystemLoader("templates"))


class Settings(BaseSettings):
    openapi_url: str = "/api/v1/openapi.json"


settings = Settings()


description = """
Cover Letter Generator helps us to genartor cover letter for . 🚀
"""


app = FastAPI(
    title="Cover Letter Generator",
    description=description,
    # version="0.0.1",
    terms_of_service="http://example.com/terms/",
    # contact={
    #     "name": "Deadpoolio the Amazing",
    #     "url": "http://x-force.example.com/contact/",
    #     "email": "dp@x-force.example.com",
    # },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    docs_url="/documentation",
    redoc_url=None,
    openapi_url=settings.openapi_url,
)

app = FastAPI()


# Custom Middleware
# To create a middleware you use the decorator @app.middleware("http") on top of a function
@app.middleware("http")
async def verify_user_agent(request: Request, call_next):
    if request.headers["User-Agent"].find("Mobile") == -1:
        # function 'call_next' that will receive the 'request' as a parameter
        response = await call_next(request)
        return response
    else:
        return JSONResponse(
            content={"message": "We do not allow mobiles"}, status_code=401
        )


def delete_file(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        raise RuntimeError(f"File at path {file_path} does not exist.")


@app.post("/download")
async def download_file(
    job_title: str = Form(),
    company_name: str = Form(),
    your_name: str = Form(),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    try:
        name = str(your_name).capitalize()
        _job_title = str(job_title).capitalize()
        company = str(company_name).capitalize()
        import_data = doc_main(name, _job_title, company)

        background_tasks.add_task(delete_file, import_data["file_location"])

        return FileResponse(
            path=import_data["file_location"],
            media_type="application/octet-stream",
            filename=import_data["file_name"],
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error",
        )


@app.post("/download/internship")
async def download_file(
    your_name: str = Form(),
    company_name: str = Form(),
    status: str = Form(),
    study_field: str = Form(),
    university_name: str = Form(),
):
    data: dict = {
        "name": str(your_name),
        "company": str(company_name),
        "status": str(status),
        "study_field": str(study_field),
        "university_name": str(university_name),
    }
    file_contents = get_internship_template(data)

    # Render the template with the dynamic data and message variable
    template = env.get_template("mail_templates.html")
    html_content = template.render(message=file_contents)

    # Return the rendered HTML content
    return HTMLResponse(content=html_content, status_code=200)


@app.get("/")
async def main():
    return HTMLResponse(content=open("templates/form.html").read(), status_code=200)


@app.get("/internship")
async def main():
    return HTMLResponse(
        content=open("templates/internship.html").read(), status_code=200
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=9000, reload=True)
