from fastapi import FastAPI, File, Form
from fastapi.responses import HTMLResponse
from import_doc import main as doc_main
from starlette.responses import FileResponse

app = FastAPI()


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
