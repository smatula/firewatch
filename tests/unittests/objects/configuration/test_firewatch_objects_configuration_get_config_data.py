import os
import tempfile
from unittest.mock import patch

from cli.objects.configuration import Configuration
from tests.unittests.objects.configuration.configuration_base_test import (
    ConfigurationBaseTest,
)


@patch.dict(os.environ, {"FIREWATCH_DEFAULT_JIRA_PROJECT": "TEST"})
class TestGetConfigData(ConfigurationBaseTest):
    def test_configuration_gets_config_data_with_valid_file_path(self):
        valid_config_data = '{"failure_rules": [{"step": "step1", "failure_type": "pod_failure", "classification": "none"}]}'
        with tempfile.TemporaryDirectory() as tmp_path:
            config_file = os.path.join(tmp_path, "config.json")
            with open(config_file, "w") as f:
                f.write(valid_config_data)
            config = Configuration(self.mock_jira, True, True, True, 10, config_file)
            assert config.config_data == {
                "failure_rules": [
                    {
                        "step": "step1",
                        "failure_type": "pod_failure",
                        "classification": "none",
                    },
                ],
            }

    def test_configuration_gets_config_data_with_invalid_file_path(self):
        with self.assertRaises(SystemExit):
            Configuration(self.mock_jira, True, True, True, 10, "/tmp/invalid.json")

    @patch.dict(
        os.environ,
        {
            "FIREWATCH_CONFIG": '{"failure_rules": [{"step": "step1", "failure_type": "pod_failure", "classification": "none"}]}',
        },
    )
    def test_configuration_gets_config_data_with_valid_env_var(self):
        config = Configuration(self.mock_jira, True, True, True, 10, None)
        assert config.config_data == {
            "failure_rules": [
                {
                    "step": "step1",
                    "failure_type": "pod_failure",
                    "classification": "none",
                },
            ],
        }

    def test_configuration_gets_config_data_with_no_env_var(self):
        if "FIREWATCH_CONFIG" in os.environ:
            del os.environ["FIREWATCH_CONFIG"]
        with self.assertRaises(SystemExit):
            Configuration(self.mock_jira, True, True, True, 10, None)
