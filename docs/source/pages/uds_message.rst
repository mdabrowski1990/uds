UDS Message
===========

.. role:: python(code)
    :language: python

Diagnostic messages (both requests and responses) are the only information that are exchanged by servers and clients
during UDS communication. To handle UDS messages ``UDS package`` defines:

- :python:`UDSMessage` - common implementation of all diagnostic messages (both requests and responses)
- :python:`UDSRequest` - implementation of diagnostic request messages that are transmitted by servers and received by clients
- :python:`UDSResponse` - implementation of diagnostic response message that are transmitted by clients and received by servers
