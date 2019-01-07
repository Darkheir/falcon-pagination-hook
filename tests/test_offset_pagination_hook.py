from falcon_pagination.offset_pagination_hook import OffsetPaginationHook


def test_empty_request_pagination_set(request_obj, mocker):
    hook = OffsetPaginationHook()
    hook(request_obj, mocker.Mock(), None, dict())

    assert isinstance(request_obj.context.get("pagination"), dict)


def test_empty_request_offset_0(request_obj, mocker):
    hook = OffsetPaginationHook()
    hook(request_obj, mocker.Mock(), None, dict())

    assert request_obj.context["pagination"]["offset"] == 0


def test_empty_request_limit_default(request_obj, mocker):
    hook = OffsetPaginationHook()
    hook(request_obj, mocker.Mock(), None, dict())

    assert request_obj.context["pagination"]["limit"] == hook.default_limit


def test_request_with_limit(request_obj, mocker):
    request_obj.params["limit"] = 30
    hook = OffsetPaginationHook()
    hook(request_obj, mocker.Mock(), None, dict())

    assert request_obj.context["pagination"]["limit"] == 30


def test_request_with_offset(request_obj, mocker):
    request_obj.params["offset"] = 30
    hook = OffsetPaginationHook()
    hook(request_obj, mocker.Mock(), None, dict())

    assert request_obj.context["pagination"]["offset"] == 30


def test_request_with_limit_too_big(request_obj, mocker):
    request_obj.params["limit"] = 1000
    hook = OffsetPaginationHook()
    hook(request_obj, mocker.Mock(), None, dict())

    assert request_obj.context["pagination"]["limit"] == hook.default_limit


def test_request_with_negative_limit(request_obj, mocker):
    request_obj.params["limit"] = -5
    hook = OffsetPaginationHook()
    hook(request_obj, mocker.Mock(), None, dict())

    assert request_obj.context["pagination"]["limit"] == hook.default_limit


def test_request_with_other_offset_key(request_obj, mocker):
    request_obj.params["new_offset"] = 30
    hook = OffsetPaginationHook(offset_key="new_offset")
    hook(request_obj, mocker.Mock(), None, dict())

    assert request_obj.context["pagination"]["offset"] == 30


def test_request_with_invalid_offset(request_obj, mocker):
    request_obj.params["offset"] = "error"
    hook = OffsetPaginationHook()
    hook(request_obj, mocker.Mock(), None, dict())

    assert request_obj.context["pagination"]["offset"] == 0


def test_request_with_other_limit_key(request_obj, mocker):
    request_obj.params["new_limit"] = 30
    hook = OffsetPaginationHook(limit_key="new_limit")
    hook(request_obj, mocker.Mock(), None, dict())

    assert request_obj.context["pagination"]["limit"] == 30


def test_request_with_other_default_limit(request_obj, mocker):
    hook = OffsetPaginationHook(default_limit=65)
    hook(request_obj, mocker.Mock(), None, dict())

    assert request_obj.context["pagination"]["limit"] == 65


def test_request_with_other_max_limit(request_obj, mocker):
    request_obj.params["limit"] = 666
    hook = OffsetPaginationHook(max_limit=1000)
    hook(request_obj, mocker.Mock(), None, dict())

    assert request_obj.context["pagination"]["limit"] == 666


def test_request_with_invalid_limit(request_obj, mocker):
    request_obj.params["limit"] = "error"
    hook = OffsetPaginationHook()
    hook(request_obj, mocker.Mock(), None, dict())

    assert request_obj.context["pagination"]["limit"] == hook.default_limit
