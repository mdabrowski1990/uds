import uds.translator.service_definitions
from uds.translator import BASE_TRANSLATOR, BASE_TRANSLATOR_2013, BASE_TRANSLATOR_2020


class TestTranslatorDefinitions:
    """Unit tests for translator definitions."""

    @staticmethod
    def _get_services_definitions_names():
        return (service_def_name
                for service_def_name in vars(uds.translator.service_definitions).keys()
                if service_def_name.isupper() and not service_def_name.startswith("_"))

    def test_services_definition(self):
        """Make sure that all services definition are used in translators."""
        for service_def_name in self._get_services_definitions_names():
            service_def = getattr(uds.translator.service_definitions, service_def_name)
            if service_def_name.endswith("2013"):
                assert service_def in BASE_TRANSLATOR_2013.services
            elif service_def_name.endswith("2020"):
                assert service_def in BASE_TRANSLATOR_2020.services
            else:
                assert service_def in BASE_TRANSLATOR_2020.services | BASE_TRANSLATOR_2013.services

    def test_default_translator(self):
        assert BASE_TRANSLATOR is BASE_TRANSLATOR_2020
