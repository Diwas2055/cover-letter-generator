from fastapi import FastAPI, File, Form, Request
from fastapi.responses import HTMLResponse
from import_doc import main as doc_main
from starlette.responses import FileResponse
from fastapi.responses import JSONResponse

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


@app.post("/download/")
async def download_file(
    job_title: str = Form(),
    company_name: str = Form(),
    your_name: str = Form(),
):
    name = str(your_name)
    _job_title = str(job_title)
    company = str(company_name)
    import_data = doc_main(name, _job_title, company)

    return FileResponse(
        import_data["file_location"],
        media_type="application/octet-stream",
        filename=import_data["file_name"],
    )


@app.get("/")
async def main():
    return HTMLResponse(content=open("templates/form.html").read())


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", port=9000, reload=True)
