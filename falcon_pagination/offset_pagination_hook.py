import logging

from falcon import Request, Response


class OffsetPaginationHook(object):
    """Falcon Hook to extract pagination information from request.

    This hook handle offset based pagination

    The extracted information are set in the request context dict
    under the "pagination" key.
    """

    def __init__(
        self,
        default_limit: int = 20,
        max_limit: int = 100,
        offset_key: str = "offset",
        limit_key: str = "limit",
    ) -> None:
        """
        :param default_limit: Limit to apply if none is provided
        :param max_limit: Maximum allowed limit
        :param offset_key: name of the key holding the offset value in the url
        :param limit_key: Name of the key holding the limit value in the url
        """
        self._logger = logging.getLogger(__name__)
        self.default_limit = default_limit
        self._max_limit = max_limit
        self._offset_key = offset_key
        self._limit_key = limit_key

    def __call__(
        self, request: Request, response: Response, resource: object, params: dict
    ) -> None:
        """Actual hook operation that extract the pagination values from the request URL

        :param request: Falcon Request
        :param response: Falcon response
        :param resource: Reference to the resource class instance associated with the request
        :param params: dict of URI Template field names
        """
        request.context.setdefault("pagination", dict())
        self._set_page_limit(request)
        self._set_page_offset(request)

    def _set_page_offset(self, request: Request) -> None:
        """Extract the offset from the request and set it in the context dict.

        The offset will be located under context['pagination']['offset']

        :param request: The Falcon request
        """
        if self._offset_key not in request.params.keys():
            request.context["pagination"]["offset"] = 0
            return

        try:
            request.context["pagination"]["offset"] = int(
                request.params[self._offset_key]
            )
        except ValueError:
            self._logger.warning(
                f"Pagination offset is not an integer, setting it to 0"
            )
            request.context["pagination"]["offset"] = 0

    def _set_page_limit(self, request: Request) -> None:
        """Extract the limit from the request and set it in the context dict.

        The offset will be located under context['pagination']['limit']

        :param request: The Falcon request
        """
        if self._limit_key not in request.params.keys():
            self._logger.info(
                f"No pagination limit in request, setting it to {self.default_limit}"
            )
            request.context["pagination"]["limit"] = self.default_limit
            return

        try:
            limit = int(request.params[self._limit_key])
        except ValueError:
            self._logger.warning(
                f"Pagination limit is not an integer, setting it to {self.default_limit}"
            )
            request.context["pagination"]["limit"] = self.default_limit
            return

        if limit > self._max_limit or limit <= 0:
            self._logger.info(
                f"Pagination limit out of bound, setting it to {self.default_limit}"
            )
            request.context["pagination"]["limit"] = self.default_limit
            return

        request.context["pagination"]["limit"] = limit
