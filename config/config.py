
import logging
import os
from pathlib import Path
import yaml
import yaml
from azure.appconfiguration import AzureAppConfigurationClient
from azure.identity import DefaultAzureCredential, ManagedIdentityCredential
from azure.keyvault.secrets import SecretClient
from setup import BASE_DIR

class Configuration():

    def __init__(self, env):
        os.environ['APP_CONFIG_CONNECTION_STRING'] = ""
        os.environ['KEY_VAULT_NAME'] = ""

        env_name = os.getenv(env)
        config_path = "config/"+env_name+".yml"
        self.__config_path = Path(f"{os.path.join(BASE_DIR, config_path)}").resolve()
        self.__config_client = AzureAppConfigurationClient.from_connection_string(
            os.getenv('APP_CONFIG_CONNECTION_STRING'))
        self.__settings = self.__get_settings()
        self.__update_settings_from_app_config()
        self.__secret_client = SecretClient(vault_url=f"https://{os.environ['KEY_VAULT_NAME']}.vault.azure.net/",
                                            # credential=ManagedIdentityCredential(
                                            #  client_id=self.__settings.managed_identity.client_id))
                                            credential=DefaultAzureCredential(exclude_environment_credential=True,
                                                                              exclude_shared_token_cache_credential=True,
                                                                              exclude_visual_studio_code_credential=True))

        self.__update_settings_from_key_vault()
        self.__logger = self.__get_logger()


    @property
    def logger(self):
        return self.__logger

    @property
    def settings(self):
        return self.__settings

    def __get_settings(self):
        return Settings(**yaml.safe_load(self.__config_path.read_text()))

    def __update_settings_from_app_config(self):
        self.__settings.managed_identity.client_id = self.__get_value_from_app_config(
            self.__settings.managed_identity.client_id)
        self.__settings.database.name = self.__get_value_from_app_config(self.__settings.database.name)
        self.__settings.database.url = self.__get_value_from_app_config(self.__settings.database.url)
        self.__settings.authentication.url = self.__get_value_from_app_config(self.__settings.authentication.url)

    def __update_settings_from_key_vault(self):
        self.__settings.database.key = self.__get_value_from_key_vault(self.__settings.database.key)
        self.__settings.azure_service_bus.dcs_platform.conn_url = self.__get_value_from_key_vault(
            self.__settings.azure_service_bus.dcs_platform.conn_url)
        self.__settings.logging["handlers"]["azure"]["instrumentation_key"] = self.__get_value_from_key_vault(
            self.__settings.logging["handlers"]["azure"]["instrumentation_key"])

    def __get_value_from_app_config(self, conf_name):
        conf_key, conf_label = conf_name.split("-")
        return self.__config_client.get_configuration_setting(conf_key, conf_label).value

    def __get_value_from_key_vault(self, secret):
        return self.__secret_client.get_secret(secret).value

    def __get_logger(self):
        logging.config.dictConfig(self.__settings.logging)
        return logging.getLogger(__name__)


app_config = Configuration()
logger = app_config.logger
settings = app_config.settings
