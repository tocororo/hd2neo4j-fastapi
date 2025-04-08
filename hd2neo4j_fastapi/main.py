from fastapi import FastAPI, File
import logging
import uvicorn
from typing import Annotated
from hd2neo4j_fastapi.service_register import ServiceRegistry


logging.basicConfig(filename="logfile.log", level=logging.INFO)
logger = logging.getLogger(__name__)


app = FastAPI(title="hd2neo4j standalone tool", version="0.9.0")


@app.get("/")
def get_graph(): 
    response = ServiceRegistry().get_repository_service().get_graph()
    return response.records


@app.get("/query")
def execute_query(query: str):
    return ServiceRegistry().get_repository_service().execute_external_query(query)


@app.post("/start")
def start_mapping(
    configFile: Annotated[bytes, File()],
    dataFile: Annotated[bytes, File()],
):
    controller = ServiceRegistry().get_mapper_service(mapping_config=configFile, data_to_map=dataFile)
    controller.start_mapping()


@app.delete("")
def drop_db():
    ServiceRegistry().get_repository_service().clean_graph_db()



def start():
    """Launched with `poetry run start` at root level"""
    uvicorn.run("hd2neo4j_fastapi.main:app", host="0.0.0.0", port=8000, reload=True)
