from fastapi import FastAPI, Request, Response, UploadFile
from fastapi.templating import Jinja2Templates
from pathlib import Path

UPLOAD_DIR = Path() / 'tmp'
UPLOAD_DIR.mkdir(exist_ok=True)

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="home.html"
    )

@app.get("/classify")
async def classify(request: Request, filename: str = None):   
    return templates.TemplateResponse(
        request=request,
        name="classify.html",
        context={"result": filename}
    )

@app.post('/upload/')
async def create_upload_file(file: UploadFile | None):
    data = await file.read()
    save_to = UPLOAD_DIR / file.filename
    with open(save_to, 'wb') as f:
        f.write(data)

    return Response(
        content="File uploaded successfully", 
        status_code=302, 
        headers={"Location": f"/classify/?filename={file.filename}"}
    )