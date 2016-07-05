import logging

from falcon.request import Request
from falcon.response import Response


class OffsetPaginationHook(object):
    """
    Falcon Hook to extract pagination informations from request.

    This hook handle offset based pagination

    The extracted informations are set in the request context dict
    under the "pagination" key.
    """

    def __init__(self, default_limit=20, max_limit=100, offset_key='offset', limit_key='limit'):
        """
        :param default_limit: Limit to apply if none is provided
        :type default_limit: int
        :param max_limit: Maximum allowed limit
        :type max_limit: int
        :param offset_key: name of the key holding the offset value in the url
        :type offset_key: str
        :param limit_key: Name of the key holding the limit value in the url
        :type limit_key: str
        """
        self._logger = logging.getLogger(__name__)
        self._default_limit = default_limit
        self._max_limit = max_limit
        self._offset_key = offset_key
        self._limit_key = limit_key

    def __call__(self, request, response, resource, params):
        """
        Actual hook operation that extract the pagination values from the request URL

        :param request: Falcon Request
        :type request: Request
        :param response: Falcon response
        :type response: Response
        :param resource: Reference to the resource class instance associated with the request
        :type resource: object
        :param params: dict of URI Template field names
        :type params: dict
        """
        request.context['pagination'] = dict()
        self._set_page_limit(request)
        self._set_page_offset(request)

    def _set_page_offset(self, request):
        """
        Extract the offset from the request and set it in the context dict.

        The offset will be located under context['pagination']['offset']

        :param request: The Falcon request
        :type request: Request
        """
        if self._offset_key not in request.params.keys():
            request.context['pagination']['offset'] = 0
            return
        request.context['pagination']['offset'] = int(request.params[self._offset_key])

    def _set_page_limit(self, request):
        """
        Extract the limit from the request and set it in the context dict.

        The offset will be located under context['pagination']['limit']

        :param request: The Falcon request
        :type request: Request
        """
        if self._limit_key not in request.params.keys():
            self._logger.info("No pagination limit in request, setting it to %d", self._default_limit)
            request.context['pagination']['limit'] = self._default_limit
            return
        limit = int(request.params[self._limit_key])
        if limit > self._max_limit or limit <= 0:
            self._logger.info("Pagination limit out of bound, setting it to %d", self._default_limit)
            request.context['pagination']['limit'] = self._default_limit
            return
        request.context['pagination']['limit'] = limit
