"""Implmentation of translator configurable through typical diagnostic parameters."""

__all__ = ["ConfigurableTranslator"]

from .translator import Translator
from .translator_definitions import BASE_TRANSLATOR
from .data_record import MessageStructureAlias


class ConfigurableTranslator(Translator):
    """
    Simplified translator for UDS messages that assumes typical messages structures.

    Features:
     - configuration with diagnostic parameters and messages structures
     - building diagnostic messages (requests, positive and negative responses)
     - extracting meaningful information from diagnostic messages payload

    .. note:: It contains core features but in advances cases (where message structure has to be adapted)
        :class:`~uds.translator.translator.Translator` shall be directly used instead.
    """

    def __init__(self,
                 base: Translator = BASE_TRANSLATOR,
                 *,
                 diagnostic_session_type_mapping: None | dict[int, str] = None,
                 reset_type_mapping: None | dict[int, str] = None,
                 report_type_mapping: None | dict[int, str] = None,
                 security_access_type_mapping: None | dict[int, str] = None,
                 control_type_type_mapping: None | dict[int, str] = None,
                 authentication_task_mapping: None | dict[int, str] = None,
                 definition_type_mapping: None | dict[int, str] = None,
                 routine_control_type_mapping: None | dict[int, str] = None,
                 zero_subfunction_mapping: None | dict[int, str] = None,
                 timing_parameter_access_type_mapping: None | dict[int, str] = None,
                 dtc_setting_type_mapping: None | dict[int, str] = None,
                 event_type_mapping: None | dict[int, str] = None,
                 link_control_type_mapping: None | dict[int, str] = None,
                 rid_mapping: None | dict[int, str] = None,
                 did_mapping: None | dict[int, str] = None,
                 did_structure_mapping: None | dict[int, MessageStructureAlias]) -> None:
        services = BASE_TRANSLATOR.services  # TODO: deepcopy
        # TODO: adapt SubFunctions values mapping
        # TODO: adapt DID names
        # TODO: adapt structure of DIDs
        # TODO: propagate DIDs data records to multiple services:
        #  - ReadDTCInformation
        #  - DefineDataIdentifier
        #  - ResponseOnEvent
        #  - ReadDataByIdentifier
        #  - WriteDataByIdentifier
        super().__init__(services=services)
