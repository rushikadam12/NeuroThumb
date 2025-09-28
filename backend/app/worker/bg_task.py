from workflows.laggraph_workflow import app_graph
import uuid,os


def run_workflow(title:str,prompt:str,style:str):
    job_id=str(uuid.uuid4())

    state_graph_params={
        "job_id": job_id,
        "title": title,
        "prompt": prompt,
        "style": style,
        "result_bytes": None
    }
    result=app_graph.invoke(state_graph_params)

    return job_id,result