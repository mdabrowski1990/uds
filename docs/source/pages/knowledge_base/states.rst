.. _knowledge-base-states:

States
======
In UDS, the behavior of a server (ECU) depends on its current operating state. Many diagnostic services are
only available when specific conditions are satisfied. For example, a service may only be supported in
Extended Diagnostic Session, require an unlocked security level (to protect from unwanted access),
or be available only when the engine is stopped from safety reasons.

The current state of the ECU therefore determines whether a diagnostic request is accepted or rejected.

Typical diagnostic states include:

* `Diagnostic Session`_
* `Security Access`_
* `Authentication`_

In addition to these diagnostic states, many ECUs also consider vehicle-specific conditions, such as:

* whether the ignition (KL15) is ON
* whether the engine is running
* vehicle speed
* battery voltage
* gear selector position
* parking brake status

Manufacturers may define additional ECU-specific states depending on the functionality being protected.


Diagnostic Session
------------------
The Diagnostic Session defines the current operating mode of the ECU. It is controlled through the
:ref:`DiagnosticSessionControl <knowledge-base-service-diagnostic-session-control>` service.

Only one diagnostic session can be active at any given time.
After an ECU reset or power-up, the server enters the **Default Session**.
A client may request a different session, such as Programming Session or Extended Diagnostic Session,
to gain access to additional diagnostic features.


Security Access
---------------
Security Access protects diagnostic functionality that should not be available to every client.
It is controlled through the :ref:`SecurityAccess <knowledge-base-service-security-access>` service.

The server starts in a **locked** state. A client may unlock one or more security levels by
successfully completing the Security Access sequence (`requestSeed` → `sendKey`).

The unlocked security level shall be cleared whenever the diagnostic session changes or the ECU is reset.


Authentication
--------------
Authentication provides an identity-based mechanism for authorizing diagnostic communication.
It is controlled through the :ref:`Authentication <knowledge-base-service-authentication>` service.

Unlike `Security Access`_, which is based on a challenge-response algorithm using a seed and key,
Authentication establishes the identity of the communicating parties, typically using cryptographic credentials.

Authentication may be performed in either direction.
Depending on the ECU implementation and requested SubFunction, the client may authenticate the server,
the server may authenticate the client, or both parties may authenticate each other (bi-directional authentication).

Some diagnostic services may only be available after successful authentication.
