from unittest import TestCase
from unittest.mock import Mock

from falcon_pagination.offset_pagination_hook import OffsetPaginationHook


class TestOffsetPaginationHook(TestCase):
    def setUp(self):
        self._request = Mock()
        self._request.context = dict()
        self._request.params = dict()

        self._response = Mock()
        self._resource = Mock()
        self._params = dict()

    def test_empty_request_pagination_set(self):
        hook = OffsetPaginationHook()
        hook(self._request, self._response, self._resource, self._params)

        self.assertIsInstance(self._request.context.get("pagination"), dict)

    def test_empty_request_offset_0(self):
        hook = OffsetPaginationHook()
        hook(self._request, self._response, self._resource, self._params)

        self.assertEqual(self._request.context["pagination"]["offset"], 0)

    def test_empty_request_limit_default(self):
        hook = OffsetPaginationHook()
        hook(self._request, self._response, self._resource, self._params)

        self.assertEqual(self._request.context["pagination"]["limit"], hook._default_limit)

    def test_request_with_limit(self):
        self._request.params["limit"] = 30
        hook = OffsetPaginationHook()
        hook(self._request, self._response, self._resource, self._params)

        self.assertEqual(self._request.context["pagination"]["limit"], 30)

    def test_request_with_offset(self):
        self._request.params["offset"] = 30
        hook = OffsetPaginationHook()
        hook(self._request, self._response, self._resource, self._params)

        self.assertEqual(self._request.context["pagination"]["offset"], 30)

    def test_request_with_limit_too_big(self):
        self._request.params["limit"] = 1000
        hook = OffsetPaginationHook()
        hook(self._request, self._response, self._resource, self._params)

        self.assertEqual(self._request.context["pagination"]["limit"], hook._default_limit)

    def test_request_with_negative_limit(self):
        self._request.params["limit"] = -5
        hook = OffsetPaginationHook()
        hook(self._request, self._response, self._resource, self._params)

        self.assertEqual(self._request.context["pagination"]["limit"], hook._default_limit)

    def test_request_with_other_offset_key(self):
        self._request.params["new_offset"] = 30
        hook = OffsetPaginationHook(offset_key="new_offset")
        hook(self._request, self._response, self._resource, self._params)

    def test_request_with_invalid_offset(self):
        self._request.params["offset"] = "error"
        hook = OffsetPaginationHook()
        hook(self._request, self._response, self._resource, self._params)

        self.assertEqual(self._request.context["pagination"]["offset"], 0)

    def test_request_with_other_limit_key(self):
        self._request.params["new_limit"] = 30
        hook = OffsetPaginationHook(limit_key="new_limit")
        hook(self._request, self._response, self._resource, self._params)

        self.assertEqual(self._request.context["pagination"]["limit"], 30)

    def test_request_with_other_default_limit(self):
        hook = OffsetPaginationHook(default_limit=65)
        hook(self._request, self._response, self._resource, self._params)

        self.assertEqual(self._request.context["pagination"]["limit"], 65)

    def test_request_with_other_max_limit(self):
        self._request.params["limit"] = 666
        hook = OffsetPaginationHook(max_limit=1000)
        hook(self._request, self._response, self._resource, self._params)

        self.assertEqual(self._request.context["pagination"]["limit"], 666)

    def test_request_with_invalid_limit(self):
        self._request.params["limit"] = "error"
        hook = OffsetPaginationHook()
        hook(self._request, self._response, self._resource, self._params)

        self.assertEqual(self._request.context["pagination"]["limit"], hook._default_limit)
