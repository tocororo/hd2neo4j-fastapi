from fastapi import APIRouter, File
from typing import Annotated
from hd2neo4j.services import MapperService, RepositoryService
from service_register import ServiceRegistry

rt = APIRouter(
    prefix="/mapper",
    tags=["mapper"],
)

@rt.get("")
def get_graph():
    response = ServiceRegistry().get_repository_service().get_graph()
    return response.records


@rt.get("/query")
def execute_query(query: str):
    return ServiceRegistry().get_repository_service().execute_external_query(query)


@rt.post("/start")
def start_mapping(
    configFile: Annotated[bytes, File()],
    dataFile: Annotated[bytes, File()],
):
    controller = ServiceRegistry().get_mapper_service(mapping_config=configFile, data_to_map=dataFile)
    controller.start_mapping()


@rt.delete("")
def drop_db():
    ServiceRegistry().get_repository_service().clean_graph_db()
