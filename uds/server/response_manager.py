"""Module with automatic responses to UDS requests."""

__all__ = ["ResponseManager", "ResponseRule"]


class ResponseRule:
    """A single response rule for ResponseManager."""

    def __init__(self) -> None:  # TODO: params, annotation
        """
        Create a single rule for creating response messages to request messages.
        """

    def is_rule_for_this_request(self, request) -> bool:  # TODO: annotation
        """
        Check if this rule is obeys the provided request.

        :param request: Request messages to be checked.

        :return: True if this rule obeys this request, False otherwise.
        """

    def spawn_response(self, request):  # TODO: annotation
        """
        Create response messages to the provided request according to the rule configuration.

        :param request: Request messages for which response to be generated.

        :return: Generated response messages to the provided request messages.
        """


class ResponseManager:
    """
    Unit that creates UDS response messages to any UDS request according to previously configured set of rules.

    It is used to generate response messages for UDS server when its simulation is on.
    """

    def __init__(self) -> None:  # TODO: params, annotation
        """
        Create new response manager and define default rules.

        TODO: :param default_nrc: NRC to be used in Negative Response Message that would be returned by ResponseManager
            if all other known rules can not be applied.
        """

    def insert_rule(self,
                    rule: ResponseRule,
                    index: int = 0) -> None:  # TODO: annotation
        """
        Add new rule in given position.

        :param rule: Response messages creation rule to add.
        :param index: Index (position in list) where the rule should be put in the rules queue.
            By default new rules are added in position 0 (the first one to be processed).
        """

    def pop_rule(self, index: int) -> ResponseRule:  # TODO: annotation
        """
        Pop already know rule from the rules queue.

        :param index: Index (position in list) from which a rule to be removed.

        :return: The rule that was removed from the the rules queue.
        """

    def dump_rules(self, rules_format):  # TODO: annotation
        """
        Dump all known rules to given format.

        :param rules_format: Any of supported rules format.

        :return: Dump with all known rules in given format.
        """

    def import_rules(self, rules, rules_format) -> None:  # TODO: annotation
        """
        Import set of rules and use them instead of these currently configured.

        :param rules: Rules to be imported by the manager.
        :param rules_format: Format in which rules are provided.
        """
