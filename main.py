from fastapi import FastAPI, Request, Response, UploadFile, HTTPException
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
import boto3
import json


app = FastAPI()

templates = Jinja2Templates(directory="templates")

SAGEMAKER_ENDPOINT_NAME = "isic-resnet-v2-finetune-2024-03-12-18-5-2024-04-01-22-11-35-898"
sagemaker_runtime = boto3.Session().client('sagemaker-runtime')


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('templates/favicon.ico')


@app.get("/")
async def home_page(request: Request):
    return templates.TemplateResponse(
        request=request, 
        name="home.html"
    )


@app.get("/classifier")
async def classifier_page(request: Request, prediction: str = None, confidence: float = None):   
    return templates.TemplateResponse(
        request=request,
        name="classifier.html",
        context={"prediction": prediction, "confidence": confidence}
    )


@app.post('/predict/')
async def predict_api(file: UploadFile | None = None):
    """Called when the image upload form in /classifier is submitted."""

    image_data = await file.read()

    # Redirect back to /classifier if no image was uploaded before submitting
    if not image_data:
        return Response(
            content="No image file uploaded", 
            status_code=303, 
            headers={"Location": f"/classifier"}
        )
    
    # Sagemaker predict API call
    try:
        sagemaker_response = sagemaker_runtime.invoke_endpoint(
            EndpointName=SAGEMAKER_ENDPOINT_NAME,
            ContentType='application/x-image',
            Accept='application/json;verbose',
            Body=image_data
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {e}")

    result = json.loads(sagemaker_response['Body'].read().decode())
    print(result)
    prediction = result['predicted_label']
    #TODO: this is not necessarily confidence, just class probability
    confidence = round(result['probabilities'][result['labels'].index(prediction)]*100, 1)

    # Redirect to /classify with prediction and confidence as url query parameters to update the HTML
    return Response(
        content="File uploaded successfully", 
        status_code=303, 
        headers={"Location": f"/classifier?prediction={prediction}&confidence={confidence}"}
    )
