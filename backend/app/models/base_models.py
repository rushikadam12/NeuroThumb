from pydantic import BaseModel

class ImageGenReq(BaseModel):
    prompt:str


class ImageGenResp(BaseModel):
    image:str
    content:list
    prompt:str
    ai_response:str|None
