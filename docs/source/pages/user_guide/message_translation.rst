Diagnostic Messages Translation
===============================
Translation implementation is located in :mod:`uds.translator` sub-package.


Translator
----------
:class:`~uds.translator.translator.Translator` is the high level interface that can be used to build
:ref:`diagnostic messages <knowledge-base-diagnostic-message>` and decode information carries by them.

- Configuration:

  Translators are configured upon :class:`~uds.translator.translator.Translator` class object creation.
  All you have to do is provide collection of :class:`~uds.translator.service.service.Service` class objects that
  contain translation logic for each :ref:`diagnostic service <knowledge-base-diagnostic-service>`.

  **Example code:**

  .. code-block::  python

    from uds.translator import Translator, Service

    # let's assume we have some services already defined
    my_services = {
        # define your services here
        Service(...),
        Service(...),
        ...
    }

    # configure translator
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


- Configuration:

  Services are configured upon :class:`~uds.translator.service.service.Service` class object creation.
  You must provide :ref:`Service Identifier (SID) <knowledge-base-sid>` value, request and response message structure.
  Optionally, you might also provide NRC codes that are supported by this service.

  **Example code:**

  .. code-block::  python

    from uds.translator import Service, AbstractDataRecord
    from uds.message import NRC

    # let's assume that we have `sub_function_data_record` and `session_parameter_data_record` Data Records defined
    sub_function_data_record: AbstractDataRecord
    session_parameter_data_record: AbstractDataRecord

    # configure example diagnostic service
    diagnostic_session_control = Service(request_sid=RequestSID.DiagnosticSessionControl,
                                         request_structure=[sub_function_data_record],
                                         response_structure=[sub_function_data_record, session_parameter_data_record],
                                         supported_nrc={NRC.SubFunctionNotSupported,
                                                        NRC.IncorrectMessageLengthOrInvalidFormat,
                                                        NRC.BusyRepeatRequest,
                                                        NRC.ConditionsNotCorrect})

- Diagnostic Messages payload building (encoding):

  Services might be used directly (or through :class:`~uds.translator.translator.Translator`) to build payload of
  diagnostic messages. This feature is provided by multiple methods:

     - :meth:`~uds.translator.service.service.Service.encode` - supports all messages types (request, positive
       and negative responses)
     - :meth:`~uds.translator.service.service.Service.encode_request` - for request messages only
     - :meth:`~uds.translator.service.service.Service.encode_positive_response` - for positive response messages only
     - :meth:`~uds.translator.service.service.Service.encode_negative_response` - for negative response messages only

  **Example code:**

  .. code-block::  python

    from uds.translator import Service, AbstractDataRecord
    from uds.message import NRC, RequestSID, ResponseSID

    # let's assume that we have `diagnostic_session_control` Service defined
    diagnostic_session_control: Service

    # build payload of example request message for Diagnostic Session Control service
    request_payload = diagnostic_session_control.encode(sid=RequestSID.DiagnosticSessionControl,
                                                        data_records_values={"subFunction": {
                                                                                 "SPRMIB": 1,
                                                                                 "diagnosticSessionType": 3}})
    request_payload = diagnostic_session_control.encode_request(data_records_values={"subFunction": {
                                                                                         "SPRMIB": 1,
                                                                                         "diagnosticSessionType": 3}})

    # build payload of example positive response message for Diagnostic Session Control service
    positive_response_payload = diagnostic_session_control.encode(rsid=ResponseSID.DiagnosticSessionControl,
                                                                  data_records_values={"subFunction": 3,
                                                                                       "sessionParameterRecord": {
                                                                                           "P2Server_max": 0x1234,
                                                                                           "P2*Server_max": 0x5678}})
    positive_response_payload = diagnostic_session_control.encode_positive_response(data_records_values={
                                                                                        "subFunction": 3,
                                                                                        "sessionParameterRecord": {
                                                                                            "P2Server_max": 0x1234,
                                                                                            "P2*Server_max": 0x5678}})

    # build payload of example negative response message for Diagnostic Session Control service
    negative_response_payload = diagnostic_session_control.encode(rsid=ResponseSID.NegativeResponse,
                                                                  sid=RequestSID.DiagnosticSessionControl,
                                                                  data_records_values={
                                                                      "NRC": NRC.SubFunctionNotSupported})
    negative_response_payload = diagnostic_session_control.encode_negative_response(nrc=NRC.SubFunctionNotSupported)

- Extracting information carried by Diagnostic Messages (decoding):

  Services might be used directly (or though :class:`~uds.translator.translator.Translator`) to extract
  comprehensive information carried by diagnostic messages.
  This feature is provided by multiple methods:

    - :meth:`~uds.translator.service.service.Service.decode` - supports all messages types (request, positive
      and negative responses)
    - :meth:`~uds.translator.service.service.Service.decode_request` - for request messages only
    - :meth:`~uds.translator.service.service.Service.decode_positive_response` - for positive response messages only
    - :meth:`~uds.translator.service.service.Service.decode_negative_response` - for negative response messages only

  **Example code:**

  .. code-block::  python

    from uds.message import UdsMessage, UdsMessageRecord

    # let's assume that we have `diagnostic_session_control` Service and messages for this service defined
    diagnostic_session_control: Service
    diagnostic_session_control_message: UdsMessage
    diagnostic_session_control_message_record: UdsMessageRecord

    # decode information
    decoded_message_information = diagnostic_session_control.decode(diagnostic_session_control_message)
    decoded_message_record_information = diagnostic_session_control.decode(diagnostic_session_control_message_record)

    # decode request messages
    decoded_request_message_information = diagnostic_session_control.decode_request(diagnostic_session_control_message)
    decoded_request_message_record_information = diagnostic_session_control.decode_request(diagnostic_session_control_message_record)

    # decode positive response messages
    decoded_positive_response_message_information = diagnostic_session_control.decode_positive_response(diagnostic_session_control_message)
    decoded_positive_response_message_record_information = diagnostic_session_control.decode_positive_response(diagnostic_session_control_message_record)

    # decode negative response messages
    decoded_negative_response_message_information = diagnostic_session_control.decode_negative_response(diagnostic_session_control_message)
    decoded_negative_response_message_record_information = diagnostic_session_control.decode_negative_response(diagnostic_session_control_message_record)


Data Records
------------
Data Records are parts of diagnostic messages and they are used to define diagnostic messages structures used by
:class:`~uds.translator.service.service.Service` class.
All Data Records implementation can be found in :mod:`~uds.translator.data_record`.


Abstract Data Record
````````````````````
:class:`~uds.translator.data_record.abstract_data_record.AbstractDataRecord` class defines common functionality for
almost all Data Records (except `Conditional Data Record`_).

Abstract Data Record features:
 - common configuration (name, bit length, children, min and max number of occurrences, unit)
 - common attributes definition (e.g.
   :attr:`~uds.translator.data_record.abstract_data_record.AbstractDataRecord.is_reoccurring`,
   :attr:`~uds.translator.data_record.abstract_data_record.AbstractDataRecord.fixed_total_length`)
 - children management

.. warning:: A **user shall not use**
    :class:`~uds.translator.data_record.abstract_data_record.AbstractDataRecord` **directly**,
    but one is able (and encouraged) to use
    :class:`~uds.translator.data_record.abstract_data_record.AbstractDataRecord`
    implementation on any of its children classes.

.. note:: Attribute :attr:`~uds.translator.data_record.abstract_data_record.AbstractDataRecord.length` contains
    number of **bits** (not bytes) that are used to present **a single Data Record occurrence**
    (not necessarily total length).


Raw Data Record
```````````````
:class:`~uds.translator.data_record.raw_data_record.RawDataRecord` class is used to define an entries
in diagnostic messages that cannot be translated (due to various reasons) to any meaningful information.
That means that physical and raw values for all Raw Data Records are the same.

**Example code:**

.. code-block::  python

  from uds.translator import RawDataRecord

  # define example Raw Data Records
  sub_function = RawDataRecord(name="subFunction",
                               length=8,
                               min_occurrences=1,
                               max_occurrences=1)
  message_filler = RawDataRecord(name="Filler for message with unknown structure",
                                 length=8,
                                 min_occurrences=0,
                                 max_occurrences=None)

  # get_raw_value
  sub_function.get_raw_value(0)  # 0
  sub_function.get_raw_value(255)  # 255
  message_filler.get_raw_value(0)  # 0
  message_filler.get_raw_value(255)  # 255

  # get_physical_value
  sub_function.get_physical_value(0)  # 0
  sub_function.get_physical_value(255)  # 255
  message_filler.get_physical_value(0)  # 0
  message_filler.get_physical_value(255)  # 255

  # get_physical_values
  message_filler.get_physical_values(0, 255)  # (0, 255)
  message_filler.get_physical_values(0, 1, 2, 3, 4, 5, 6, 7)  # (0, 1, 2, 3, 4, 5, 6, 7)


Mapping Data Record
```````````````````
:class:`~uds.translator.data_record.mapping_data_record.MappingDataRecord` class is used to define an entries
in diagnostic messages that can be translated to labels due to some known mapping.
That means that physical value would usually be str type. If *user provides raw value for which no mapping is defined*
though, then a warning would be reported.

.. note:: Raw values for which mapping is not defined are handled the same way as per
  :class:`~uds.translator.data_record.raw_data_record.RawDataRecord`.
  Same goes for int type physical values.
  This is fallback mechanism for Mapping Data Records with labels defined only for some raw values.

**Example code:**

.. code-block::  python

  from uds.translator import MappingDataRecord

  # define example Mapping Data Records
  sprmib = MappingDataRecord(name="Suppress Positive Response Message Indication Bit",
                             length=1,
                             values_mapping={0: "no", 1: "yes"},
                             min_occurrences=1,
                             max_occurrences=1)
  diagnostic_session = MappingDataRecord(name="diagnosticSessionType",
                                         length=7,
                                         values_mapping={1: "Default",
                                                         2: "Programming",
                                                         3: "Extended"},
                                         min_occurrences=1,
                                         max_occurrences=1)

  # get_raw_value
  sprmib.get_raw_value("no")  # 0
  sprmib.get_raw_value("yes")  # 1
  diagnostic_session.get_raw_value("Default")  # 1
  diagnostic_session.get_raw_value(4)  # 4 and warning

  # get_physical_value
  sprmib.get_physical_value(0)  # "no"
  sprmib.get_physical_value(1)  # "yes"
  diagnostic_session.get_physical_value(1)  # "Default"
  diagnostic_session.get_physical_value(4)  # 4 and warning


Formula Data Record
```````````````````
There are two types of Formula Data Records:
 - :class:`~uds.translator.data_record.formula_data_record.LinearFormulaDataRecord`
 - :class:`~uds.translator.data_record.formula_data_record.CustomFormulaDataRecord`

Both classes are used define an entries in diagnostic messages that can be translated to numeric values
(physical values must be either int or float type) using special formula.

:class:`~uds.translator.data_record.formula_data_record.LinearFormulaDataRecord` class can only handle linear
conversions, but has better error handling and is easier to define. **Users are encouraged to use**
:class:`~uds.translator.data_record.formula_data_record.LinearFormulaDataRecord` **over**
:class:`~uds.translator.data_record.formula_data_record.CustomFormulaDataRecord` **whenever possible.**

**Example code:**

.. code-block::  python

  from uds.translator import LinearFormulaDataRecord

  # define example Linear Formula Data Records
  engine_temp = LinearFormulaDataRecord(name="Engine Temperature",
                                        length=16,
                                        factor=0.01,
                                        offset=-100,
                                        unit="Celsius degrees")

  # get_raw_value
  engine_temp.get_raw_value(0)  # 10000
  engine_temp.get_raw_value(61.25)  # 16125

  # get_physical_value
  engine_temp.get_physical_value(0)  # - 100.0 [Celsius degrees]
  engine_temp.get_physical_value(12345)    # 23.45 [Celsius degrees]

:class:`~uds.translator.data_record.formula_data_record.CustomFormulaDataRecord` class is more flexible and can handle
any (also non-linear) conversion, but it requires properly implemented encoding and decoding functions.

.. warning:: There is almost no error handling and no crosschecks. If a user provides encoding and decoding formulas
    that are inconsistent (e.g. encoding does not correctly reverse decoding), it will not be detected and
    might lead to extremely confusing results.

**Example code:**

.. code-block::  python

  from typing import Union
  from uds.translator import CustomFormulaDataRecord

  # define a Custom Formula Data Record with example encoding and decoding formulas
  def decode_pressure(raw_value: int) -> int:
      return raw_value*raw_value
  def encode_pressure(physical_value: Union[int, float]) -> int:
      return int(round(physical_value**0.5,0))
  pressure = CustomFormulaDataRecord(name="Pressure",
                                     length=16,
                                     encoding_formula=encode_pressure,
                                     decoding_formula=decode_pressure,
                                     unit="Pascal",
                                     min_occurrences=4,
                                     max_occurrences=4)

  # get_raw_value
  pressure.get_raw_value(100)  # 10
  pressure.get_raw_value(654321)  # 809 - the closest value

  # get_physical_value
  pressure.get_physical_value(809)  # 654481 [Pascals]
  pressure.get_physical_value(4000)  # 16000000 [Pascals]

  # get_physical_values
  pressure.get_physical_values(0, 100, 250, 6789)  # (0, 10000, 62500, 46090521)


Text Data Record
````````````````
:class:`~uds.translator.data_record.text_data_record.TextDataRecord` class is used to define an entries
in diagnostic messages that can be translated to text using known text encoding format.
All supported encoding formats are defined in :class:`~uds.translator.data_record.text_data_record.TextEncoding` enum.
Physical values produces by :class:`~uds.translator.data_record.text_data_record.TextDataRecord` are str type, even
the output of :meth:`~uds.translator.data_record.text_data_record.TextDataRecord.get_physical_values` method is
str type.

**Example code:**

.. code-block::  python

  from uds.translator import TextDataRecord, TextEncoding

  # define example Text Data Records
  software_version = TextDataRecord(name="Software Version",
                                    encoding=TextEncoding.BCD,
                                    min_occurrences=4,
                                    max_occurrences=4)
  spare_part_number = TextDataRecord(name="Spare Part Number",
                                     encoding=TextEncoding.ASCII,
                                     min_occurrences=8,
                                     max_occurrences=None)

  # get_raw_value
  software_version.get_raw_value("1")  # 1
  software_version.get_raw_value("9")  # 9
  spare_part_number.get_raw_value("A")  # 0x41
  spare_part_number.get_raw_value("1")  # 0x31

  # get_physical_value
  software_version.get_physical_value(1)  # "1"
  spare_part_number.get_physical_value(0x41)  # "A"

  # get_physical_values
  software_version.get_physical_values(9, 0, 1, 8)  # "9018"
  spare_part_number.get_physical_values(0x41, 0x42, 0x43, 0x2D, 0x31, 0x32, 0x33, 0x34)  # "ABC-1234"


Conditional Data Record
```````````````````````
