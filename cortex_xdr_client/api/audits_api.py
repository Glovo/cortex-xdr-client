from enum import Enum
from typing import List, Optional, Tuple

from cortex_xdr_client.api.authentication import Authentication
from cortex_xdr_client.api.base_api import BaseAPI
from cortex_xdr_client.api.models.audits import (
    GetAuditManagementLogsResponse
)
from cortex_xdr_client.api.models.filters import (
    new_request_data, request_gte_lte_filter, request_filter
)


class AuditsAPI(BaseAPI):
    def __init__(self, auth: Authentication, fqdn: str, timeout: Tuple[int, int]) -> None:
        super(AuditsAPI, self).__init__(auth, fqdn, "audits", timeout)

    # https://cortex-panw.stoplight.io/docs/cortex-xdr/091d0d8b7d283-get-audit-management-log
    def get_audit_management_logs(self,
                                  search_from: int = None,
                                  search_to: int = None,
                                  timestamp: int = None,
                                  ) -> Optional[GetAuditManagementLogsResponse]:
        """

        """
        filters = []
        if timestamp is not None:
            filters.append(request_gte_lte_filter("timestamp", timestamp, True))
        request_data = new_request_data(filters=filters, search_from=search_from, search_to=search_to)

        response = self._call(call_name="management_logs",
                              json_value=request_data)
        return GetAuditManagementLogsResponse.parse_obj(response.json())
