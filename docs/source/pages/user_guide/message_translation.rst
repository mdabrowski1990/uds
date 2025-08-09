Diagnostic Messages Translation
===============================
Translation implementation is located in :mod:`uds.translator` sub-package.


Translator
----------
:class:`~uds.translator.translator.Translator` is the high level interface that can be used to build
:ref:`diagnostic messages <knowledge-base-diagnostic-message>` and decode information carries by them.

- Configuration of the translator:

  Translators are configured upon :class:`~uds.translator.translator.Translator` class object creation.
  All you have to do is provide collection of :class:`~uds.translator.service.service.Service` class objects that
  contain translation logic for each :ref:`diagnostic service <knowledge-base-diagnostic-service>`.

  **Example code:**

    .. code-block::  python

      from uds.translator import Translator, Service

      my_services = {
          # define your services here
          Service(...),
          Service(...),
          ...
      }

      my_translator = Translator(my_services)


- Diagnostic Messages payload building (encoding):

  Translators might be used to build payload of diagnostic messages.
  This feature is provided by :meth:`~uds.translator.translator.Translator.encode` method.
  You might use it to build all diagnostic messages types (request, positive and negative responses).

  **Example code:**

  .. code-block::  python

    from uds.message import RequestSID, ResponseSID, NRC

    # let's assume that we have `my_translator` already configured with Diagnostic Session Control service
    # Diagnostic Session Control service structure must match `data_records_values` parameters
    my_translator: Translator

    # build payload of example request message for Diagnostic Session Control service
    request_payload = my_translator.encode(sid=RequestSID.DiagnosticSessionControl,
                                           data_records_values={"subFunction": {"SPRMIB": 1,
                                                                                "diagnosticSessionType": 3}})

    # build payload of example positive response message for Diagnostic Session Control service
    positive_response_payload = my_translator.encode(rsid=ResponseSID.DiagnosticSessionControl,
                                                     data_records_values={"subFunction": 3,
                                                                          "sessionParameterRecord": {
                                                                              "P2Server_max": 0x1234,
                                                                              "P2*Server_max": 0x5678}})

    # build payload of example negative response message for Diagnostic Session Control service
    negative_response_payload = my_translator.encode(rsid=ResponseSID.NegativeResponse,
                                                     sid=RequestSID.DiagnosticSessionControl,
                                                     data_records_values={"NRC": NRC.SubFunctionNotSupported})


- Extracting information carried by Diagnostic Messages (decoding):

  Translators might be used to extract comprehensive information carried by diagnostic messages.
  This functionality is provided by :meth:`~uds.translator.translator.Translator.decode` method.
  You might use it with all diagnostic messages types (request, positive and negative responses).

  **Example code:**

  .. code-block::  python

    from uds.message import UdsMessage, UdsMessageRecord

    # let's assume that we have `my_translator` already configured and some messages defined
    my_translator: Translator
    some_message: UdsMessage
    some_message_record: UdsMessageRecord

    # decode information
    decoded_message_information = my_translator.decode(some_message)
    decoded_message_record_information = my_translator.decode(some_message_record)


Service
-------
Each object of :class:`~uds.translator.service.service.Service` class defines a translation logic for one specific
:ref:`diagnostic service <knowledge-base-diagnostic-service>`.

:class:`~uds.translator.service.service.Service` provides



Data Records
------------
