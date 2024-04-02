from fastapi import FastAPI, Request, Response, UploadFile
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
import boto3
import json
from PIL import Image


app = FastAPI()

templates = Jinja2Templates(directory="templates")

SAGEMAKER_ENDPOINT_NAME = "isic-resnet-v2-finetune-2024-03-12-18-5-2024-04-01-22-11-35-898"
sagemaker_runtime = boto3.Session().client('sagemaker-runtime')


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('templates/favicon.ico')


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="home.html"
    )


@app.get("/classify")
async def classify(request: Request, prediction: str = None, confidence: float = None):   
    return templates.TemplateResponse(
        request=request,
        name="classify.html",
        context={"prediction": prediction, "confidence": confidence}
    )


@app.post('/submit/')
async def submit_file(file: UploadFile | None):
    if not file:
        return Response(
            content="No image file uploaded", 
            status_code=400, 
            headers={"Location": f"/classify/"}
        )
    else:
        data = await file.read()

        print(type(data))

        result = predict(data)

        print(result)

        prediction = result['predicted_label']
        #TODO: this is not necessarily confidence, just class probability
        confidence = round(result['probabilities'][result['labels'].index(prediction)]*100, 1)

        return Response(
            content="File uploaded successfully", 
            status_code=302, 
            headers={"Location": f"/classify/?prediction={prediction}&confidence={confidence}"}
        )


def predict(image_data):
    response = sagemaker_runtime.invoke_endpoint(
        EndpointName=SAGEMAKER_ENDPOINT_NAME,
        ContentType='application/x-image',
        Accept='application/json;verbose',
        Body=image_data
    )

    result = json.loads(response['Body'].read().decode())

    return result