from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from setfit import SetFitModel
from typing import List

#initializing fastAPI app
app = FastAPI()

#initializing the baseModel to compare the data that will come from clientSide
class AnalysisRequest(BaseModel):
    text: List[str]

#initializing the baseModel to compare the date that will be returned as response
class AnalysisResult(BaseModel):
    sentiment: List[str]

#decorating the endpoint and giving AnalysisResult as response_model parameter to compare
@app.post("/analyze", response_model=AnalysisResult)
async def analyze(request: AnalysisRequest):
    #getting the text that was sent to the server
    texts = request.text
    #initializing the setFit model as testModel
    testModel = SetFitModel.from_pretrained("StatsGary/setfit-ft-sentinent-eval")

    #if no texts came through request than raises an expecption 
    if not texts:
        raise HTTPException(status_code=400, detail="Text cannot be empty.")

    #if texts was not empty then try
    try:
        #Send texts through testModel and save the predictions as preds
        preds = testModel(texts)
        #preds is a numpy array and converting it to List for convenience
        preds = preds.tolist()
        temp = []
        #converting 0 -> negative and 1 -> positive
        for _,n in enumerate(preds):
            if n == 0:
                temp.append("negative")
            else:
                temp.append("positive")
        #print(f"printing temp:{temp}")

    #if any error raises inside try then an exception will be raised
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred during sentiment analysis.") from e

    #return the AnalysisResult baseModel where sentiment is temp
    return AnalysisResult(sentiment=temp)