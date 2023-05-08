from fastapi import FastAPI, File, Form
from fastapi.responses import HTMLResponse
from import_doc import main as doc_main, get_internship_template
from starlette.responses import FileResponse
from jinja2 import Environment, FileSystemLoader


# Create a Jinja2 environment with the path to your templates directory
env = Environment(loader=FileSystemLoader("templates"))

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
            content={"message": "we do not allow mobiles"}, status_code=401
        )

@app.post("/download")
async def download_file(
    job_title: str = Form(),
    company_name: str = Form(),
    your_name: str = Form(),
):
    name = str(your_name).capitalize()
    _job_title = str(job_title).capitalize()
    company = str(company_name).capitalize()
    import_data = doc_main(name, _job_title, company)

    return FileResponse(
        import_data["file_location"],
        media_type="application/octet-stream",
        filename=import_data["file_name"],
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
