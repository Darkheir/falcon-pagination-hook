falcon-pagination-hook
======================

A small falcon hook to parse pagination elements from the request.

For now it parses an Offset based pagination.

Usage
-----

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

Configuration options
---------------------

A few parameters can be passed to the hook:

* default_limit : The limit to apply if none is found in the request query or if the limit is out of bound. Default to 20
* max_limit: Maximum allowed limit. Default to 100
* offset_key: Name of the request parameter holding the offset value. Default to 'offset'
* limit_key: Name of the request parameter holding the limit value. Default to 'limit'

Here's an example setting a default limit to 10, a maximum limit to 500 the offset key to 'page_offset' and the limit key to 'result_limit':

.. code:: python

    @falcon.before(PaginationFromRequestHook(
        default_limit=10,
        max_limit=500, 
        offset_key='page_offset', 
        limit_key='result_limit'
    ))
    def on_get(self, req, resp, user):
        # Get request

