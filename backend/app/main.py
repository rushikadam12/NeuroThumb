from fastapi import FastAPI,Form
from fastapi import Response
from models.base_models import ImageGenReq
from worker.bg_task import run_workflow
from utils.logger import logger
import uvicorn

app=FastAPI()


@app.get("/")
def home():
    return {"message":"server alive"}


@app.post("/image_generator")
def image_gen_func(    
    title: str = Form(...),
    prompt: str = Form(""),
    style: str = Form("default")
    ):
    try:
        logger.info(prompt)        
        result=run_workflow(prompt=prompt,title=title,style=style)
        return {"result":result,"status":200}
    except Exception as e:
        return {"error":str(e),"status":500}


if __name__=="__main__":
    uvicorn.run("main:app",host="0.0.0.0",port=5000,reload=True)
