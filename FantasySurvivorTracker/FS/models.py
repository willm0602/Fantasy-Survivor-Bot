from postgrest import SyncRequestBuilder, SyncSelectRequestBuilder
from supabase.client import Client as SupabaseClient




class Model:

    table_name: str | None = None
    supabase_fields_to_class_fields = {}

    class Manager:
        request_builder: SyncRequestBuilder
        _type: 'Model'

        def __init__(
            self,
            request_builder: SyncRequestBuilder,
            _type: 'Model'
        ):
            self.request_builder = request_builder
            self._type = _type

        def get(self, **kwargs) -> _type | None:
            select_req: SyncSelectRequestBuilder = self.request_builder.f('*')
            for key, val in kwargs.items():
                select_req = select_req.eq(key, val)
            select_req: SyncSelectRequestBuilder


    def objects(
        kls,
        supabase_client: SupabaseClient
    ) -> SyncRequestBuilder:
        table_name = kls.table_name
        if table_name is None:
            raise ValueError(f'{type(kls)} needs a table name provided')
        return kls.Manager(supabase_client.table(table_name))