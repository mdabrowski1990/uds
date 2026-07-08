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
The :class:`~uds.diagnostic_configuration.state.State` class represents a single ECU state that may affect
the availability of diagnostic functions.
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
