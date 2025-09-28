from typing import Annotated,Optional
from typing_extensions import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from google.generativeai import configure, GenerativeModel
from google.generativeai.types import GenerationConfig
from utils.logger import logger
from config import get_settings,Settings
from langgraph.graph import StateGraph, START, END
from PIL import Image
from io import BytesIO
from huggingface_hub import InferenceClient
import os


ENV_VAL=get_settings()
configure(api_key=ENV_VAL.gemini_api_key)
# img_client = genai.Client(api_key=ENV_VAL.gemini_api_key)
text_prompt_improviser_model=ChatGoogleGenerativeAI(model="gemini-2.5-flash",api_key=ENV_VAL.gemini_api_key)

image_gen_client = InferenceClient(
    provider="auto",
    api_key=ENV_VAL.HF_TOKEN,
)

# output is a PIL.Image object



class ImgGenDict(TypedDict):
    title:str
    job_id:str
    prompt:str
    llm_improvise:str|None
    style:str
    result_bytes:Optional[bytes]
    image_bytes:Optional[bytes]

def refine_prompt(state:ImgGenDict)->ImgGenDict:
    if state["prompt"]:

        human_message=HumanMessage(content=f"Create catchy thumbnail for prompt for user where title is {state["title"]} and user description is {state["prompt"]}")

        try:
            resp=text_prompt_improviser_model.invoke([human_message])
            refine_prompt=resp.content    
            logger.info(f"refine_prompt()-------------->{resp}")
            state["llm_improvise"]=refine_prompt
        except Exception as e:

            logger.info(f"refine+_prompt------------->{str(e)}")
            state["llm_improvise"]=None

        return state
        
def gen_img(state:ImgGenDict)->ImgGenDict:
    prompt=state.get("llm_improvise") or state["prompt"]
    path=os.path.join("C:/Users/Rushikesh Kadam/OneDrive/Documents/code_space/NeuroThumb/backend/app","store")
    try:
         

        resp_img=image_gen_client.text_to_image(
                    "Astronaut riding a horse",
                    model="Qwen/Qwen-Image",
                )
        
       
        if resp_img:
            buffer=BytesIO()
            resp_img.save(buffer,format="JPEG")
            resp_bytes=buffer.getvalue()
            logger.info(f"Successfully generated image, bytes length: {len(resp_bytes)}")
            state["result_bytes"] = resp_bytes
        else:
            logger.error("Image generation failed, no candidates returned.")
            state["result_bytes"] = None

    except Exception as e:
        logger.info(str(e))
        state["result_bytes"] = None
    
    return state


graph_node=StateGraph(ImgGenDict)

graph_node.add_node("refine_prompt",refine_prompt)
graph_node.add_node("gen_img",gen_img)

graph_node.set_entry_point("refine_prompt")
graph_node.add_edge("refine_prompt","gen_img")
graph_node.add_edge("gen_img",END)

app_graph=graph_node.compile()
