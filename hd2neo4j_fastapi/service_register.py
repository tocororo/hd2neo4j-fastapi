from hd2neo4j.services import RepositoryService, MapperService
from hd2neo4j_fastapi.config import get_settings

class ServiceRegistry:
    _instance = None
    st= get_settings()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ServiceRegistry, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.repository_service = RepositoryService(
            neo4j_uri=self.st.neo4j_uri,
            neo4j_user=self.st.neo4j_user,
            neo4j_pass=self.st.neo4j_pass,
            neo4j_db=self.st.neo4j_db
        )
        self.mapper_service = None 
        
    def get_repository_service(self):
        return self.repository_service

    def get_mapper_service(self, mapping_config=None, data_to_map=None):
        if self.mapper_service is None and mapping_config and data_to_map:
            self.mapper_service = MapperService(
                mapping_config,
                data_to_map,
                self.repository_service
            )
        return self.mapper_service
