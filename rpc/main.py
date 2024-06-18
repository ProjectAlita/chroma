from typing import Optional

from pylon.core.tools import log  # pylint: disable=E0611,E0401
from pylon.core.tools import web

from tools import rpc_tools


class RPC:
    integration_name = 'chroma'

    rpc = lambda name: web.rpc(f'chroma_{name}', name)

    @web.rpc(f'embedding_config_{integration_name}')
    @rpc_tools.wrap_exceptions(RuntimeError)
    def make_dusty_config(self, context, test_params, scanner_params):
        """ Prepare config """
        result = {'code': '/tmp/code', **scanner_params}
        # result = {'connection_string'}
        return "pgvector", result

    @rpc('vector_store_details')
    def vector_store_details(self, project_id: Optional[int], integration_uid: str, datasource_version_uuid: str):
        integration = rpc_tools.RpcMixin().rpc.call.integrations_get_by_uid(
            integration_uid, project_id, check_all_projects=True
        )
        if integration is None:
            raise ValueError(f'Integration with {integration_uid=} not found')
        return {
            "vectorstore": 'chroma',
            "vectorstore_params": {
                "collection_name": datasource_version_uuid,
                "persist_directory": f"{integration.settings.get('path')}/{project_id}",
                "integration_uid": integration_uid,
            }
        }
