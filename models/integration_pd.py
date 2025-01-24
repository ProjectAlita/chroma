import os

from pydantic.v1 import BaseModel


class IntegrationModel(BaseModel):
    path: str

    def check_connection(self, project_id):
        return not os.path.exists(self.path)


