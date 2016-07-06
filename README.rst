falcon-pagination-hook
======================

A small falcon hook to parse pagination elements from the request.

For now it parses an Offset based pagination.

Usage
-----

Basic usage
^^^^^^^^^^^

The easiest way to use this hook is the following:

.. code:: python

    @falcon.before(PaginationFromRequestHook())
    def on_get(self, req, resp, user):
        # Here req['context']['pagination'] is set
        # with 2 keys: 'offset' and 'limit'

The Hook will look in the query parameters for 2 keys:

* offset: The pagination offset
* limit: The pagination limit

It will create a pagination dict into the request context accessible at :code:`req.context['pagination']`.
This pagination dict will contain 2 values:

* offset: The offset from the request or 0 if it doesn't exists
* limit: The limit to apply. If no limit is found the default one is applied (20). If the value is bigger than the max value (100) then the default limit is also applied.
