from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from setfit import SetFitModel
from typing import List
import logging

# Initializing the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Setting up the logger to write logs to a file
file_handler = logging.FileHandler("application.log")
file_handler.setLevel(logging.INFO)

# Creating a formatter to define the log message format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# Adding the file handler to the logger
logger.addHandler(file_handler)

#initializing fastAPI app
app = FastAPI()

#initializing the baseModel to compare the data that will come from clientSide
class AnalysisRequest(BaseModel):
    text: List[str]

#initializing the baseModel to compare the date that will be returned as response
class AnalysisResult(BaseModel):
    sentiment: List[str]

#for initial start up
#below json will be returned upon visiting the webserver
@app.get("/")
def root():
    return {"server status":"The server has started successfully"}


#decorating the endpoint and giving AnalysisResult as response_model parameter to compare
@app.post("/analyze", response_model=AnalysisResult)
async def analyze(request: AnalysisRequest):
    #getting the text that was sent to the server
    texts = request.text

    # Log the incoming request
    logger.info(f"Incoming request: {texts}")

    #initializing the setFit model as testModel
    testModel = SetFitModel.from_pretrained("StatsGary/setfit-ft-sentinent-eval")

    #if no texts came through request than raises an expecption 
    for string in texts:
        if string == "":
            logger.error("Text cannot be empty and sentences with words is expected")
            raise HTTPException(status_code=400, detail="Text cannot be empty and sentences with words is expected")

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

    # Log the sentiment analysis results
        logger.info(f"Sentiment analysis results: {temp}")

    #if any error raises inside try then an exception will be raised
    except Exception as e:
        # Log the error
        logger.exception("An error occurred during sentiment analysis.")
        raise HTTPException(status_code=500, detail="An error occurred during sentiment analysis.") from e

    #return the AnalysisResult baseModel where sentiment is temp
    return AnalysisResult(sentiment=temp)