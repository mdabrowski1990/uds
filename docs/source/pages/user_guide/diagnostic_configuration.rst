.. _implementation-ecu-diagnostic-configuration:

Diagnostic Configuration
========================
The Diagnostic Configuration module provides a mechanism for describing the conditions under which an ECU supports
diagnostic messages. It allows applications to model ECU operating states and define the availability of
diagnostic functions depending on the current state.

The implementation is located in the :mod:`uds.diagnostic_configuration` package and consists of
the following components:

- `State`_
- `States Definitions`_
- `ECU Diagnostic Configuration`_


State
-----
The :class:`~uds.diagnostic_configuration.state.State` class represents a single
:ref:`ECU state <knowledge-base-states>` that may affect the availability of diagnostic functions.
A state has a name, a predefined set of allowed values, and a current value representing the ECU's current operating
condition.

Attributes:

- :attr:`~uds.diagnostic_configuration.state.State.name` - name of a state
- :attr:`~uds.diagnostic_configuration.state.State.possible_values` - collection of all values the state can assume
- :attr:`~uds.diagnostic_configuration.state.State.current_value` - current value of the state

**Example code:**

  .. code-block::  python

    import uds

    # create an example state describing the active diagnostic session
    session = uds.diagnostic_configuration.State(name="Diagnostic Session",
                                                 possible_values={"Default", "Programming", "Extended"})

    # change the current session
    session.current_value = "Default"

    # mark the current session as undefined
    session.current_value = None


States Definitions
------------------
The :mod:`uds.diagnostic_configuration.state_definitions` module provides predefined
:class:`~uds.diagnostic_configuration.state.State` objects representing the most common ECU states used in
UDS diagnostic communication. These definitions can be used directly or serve as a starting point for creating custom
diagnostic configurations.

The following state definitions are provided:

- :obj:`~uds.diagnostic_configuration.state_definitions.DEFAULT_DIAGNOSTIC_SESSION_STATE`
  - current diagnostic session.
- :obj:`~uds.diagnostic_configuration.state_definitions.DEFAULT_SECURITY_ACCESS_STATE`
  - currently unlocked security access level.
- :obj:`~uds.diagnostic_configuration.state_definitions.DEFAULT_AUTHENTICATION_STATE`
  - current authentication state.
- :obj:`~uds.diagnostic_configuration.state_definitions.DEFAULT_SECURED_TRANSMISSION_STATE`
  – indicates whether secured data transmission is active.
- :obj:`~uds.diagnostic_configuration.state_definitions.DEFAULT_ENGINE_STATE`
  - current engine state.
- :obj:`~uds.diagnostic_configuration.state_definitions.DEFAULT_ADDRESSING_TYPE_STATE`
  – current addressing type (physical or functional).


ECU Diagnostic Configuration
----------------------------
The :class:`~uds.diagnostic_configuration.ecu_configuration.EcuDiagnosticConfiguration` class is the central
component of the Diagnostic Configuration module. It stores the ECU states relevant for diagnostic communication
together with the restrictions that determine when diagnostic services, sub-functions, DID and RID are available.

Restrictions can be defined at multiple levels of specificity:

- Service Identifier (SID)
- Sub-function (for a given SID)
- Data Identifier (DID, for a given SID)
- Routine Identifier (RID, for a given SID)

More specific restrictions complement or override the restrictions defined at higher levels.

Attributes:

- :attr:`~uds.diagnostic_configuration.ecu_configuration.EcuDiagnosticConfiguration.states`
  - configured ECU states
- :attr:`~uds.diagnostic_configuration.ecu_configuration.EcuDiagnosticConfiguration.states_names`
  - names of all configured states
- :attr:`~uds.diagnostic_configuration.ecu_configuration.EcuDiagnosticConfiguration.states_mapping`
  - mapping from state name to :class:`~uds.diagnostic_configuration.state.State` object
- :attr:`~uds.diagnostic_configuration.ecu_configuration.EcuDiagnosticConfiguration.sid_restrictions`
  - restrictions defined for diagnostic services (SIDs)
- :attr:`~uds.diagnostic_configuration.ecu_configuration.EcuDiagnosticConfiguration.subfunction_restrictions`
  - restrictions defined for service sub-functions
- :attr:`~uds.diagnostic_configuration.ecu_configuration.EcuDiagnosticConfiguration.did_restrictions`
  - restrictions defined for Data Identifiers (DIDs)
- :attr:`~uds.diagnostic_configuration.ecu_configuration.EcuDiagnosticConfiguration.rid_restrictions`
  - restrictions defined for Routine Identifiers (RIDs)

Methods:

- :attr:`~uds.diagnostic_configuration.ecu_configuration.EcuDiagnosticConfiguration.combine_restrictions`
  - combines multiple restriction definitions into a single effective restriction
- :attr:`~uds.diagnostic_configuration.ecu_configuration.EcuDiagnosticConfiguration.get_restrictions`
  - returns the effective restrictions for a diagnostic message


**Example code:**

  .. code-block::  python

    import uds

    # create an example (simplified) ECU Configuration
    ecu_config = uds.diagnostic_configuration.EcuDiagnosticConfiguration(
        states=(uds.diagnostic_configuration.DEFAULT_DIAGNOSTIC_SESSION_STATE,
                uds.diagnostic_configuration.DEFAULT_SECURITY_ACCESS_STATE,
                uds.diagnostic_configuration.DEFAULT_ADDRESSING_TYPE_STATE),
        sid_restrictions={
            0x22: {
                "Session": {0x03},
                }},
        did_restrictions={
            0x22: {
                0xF190: {
                    "Session": {0x03},
                    "SecurityAccess": {0x01},
                    "AddressingType": {uds.addressing.AddressingType.PHYSICAL}}
                    }},
        rid_restrictions={},
        subfunction_restrictions={})

    # Restrictions for ReadDataByIdentifier (0x22)
    ecu_config.sid_restrictions[0x22]

    # Restrictions for 22 (ReadDataByIdentifier) F1 90 (DID 0xF190) message
    ecu_config.get_restrictions([0x22, 0xF1, 0x90])
