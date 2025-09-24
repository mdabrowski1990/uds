Client
======
This section provides usage examples for :ref:`Client implementation <implementation-client>`.

.. seealso:: https://github.com/mdabrowski1990/uds/tree/main/examples/client


Sending Requests and Receiving Responses
----------------------------------------
Example of sending a single request message and collecting all responses until receiving the final one.

.. include:: ../../../../examples/client/send_request_get_responses.py
  :code: python


Managing Tester Present
-----------------------
Example of periodic :ref:`TesterPresent <knowledge-base-service-tester-present>` messages sending.

.. include:: ../../../../examples/client/periodic_tester_present.py
  :code: python


Using Background Receiving
--------------------------
Example of collecting response messages without sending a request.

.. include:: ../../../../examples/client/background_receiving.py
  :code: python
