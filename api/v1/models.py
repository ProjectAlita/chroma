from flask import request
from pydantic.v1 import ValidationError
from tools import api_tools

from ...models.integration_pd import IntegrationModel


class ProjectAPI(api_tools.APIModeHandler):
    ...


class AdminAPI(api_tools.APIModeHandler):
    ...


class API(api_tools.APIBase):
    url_params = [
        '<string:mode>/<int:project_id>',
        '<int:project_id>'
    ]

    mode_handlers = {
        'default': ProjectAPI,
        'administration': AdminAPI,
    }

    def post(self, **kwargs):
        try:
            settings = IntegrationModel.parse_obj(request.json)
        except ValidationError as e:
            return e.errors(), 400

        check_connection_response = settings.check_connection(None)
        if check_connection_response is not True:
            return [{'loc': ['check_connection'], 'msg': 'Path already exists'}], 400

        return {}, 200
