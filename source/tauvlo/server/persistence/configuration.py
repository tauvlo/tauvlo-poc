import os
import json

from tauvlo.server import ROOT_DIR


CONFIG_FILE = os.path.join(ROOT_DIR, "..", "..", "config.json")


class Config:

    def __init__(self, config_file):
        self.config_file = config_file

        # All configuration defaults go here
        self.debug_ws_host = "0.0.0.0"
        self.debug_ws_port = 8080

        self.dev_access_key = "tauvlo2024"
        self.dev_admin_key = "PLACEHOLDER_REPLACE_ME"  # put listing key here

        self.frontend_static_dir = os.path.join(ROOT_DIR, "..", "..", "frontend_placeholder")
        self.db_connection_string = ""

        self.stellar_horizon_url = "https://horizon-testnet.stellar.org"
        self.stellar_use_mainnet = False
        self.stellar_issuer_public_key = "GDBC2X3OZP4KU5WIM5GJ5P5PNMWK77CL2YRORXAFIWE2UD5WRCT7XTZS"
        self.stellar_usdc_issuer_public_key = "GBBD47IF6LWK7P7MDEVSCWR7DPUWV3NY3DTQEVFL4NAT4AQH3ZLLFLA5"
        self.stellar_issuer_private_key = os.getenv("STELLAR_ISSUER_PRIVATE_KEY")
        self.stellar_default_base_fee = 100
        self.stellar_default_trn_timeout_sec = 90

        self._load_from_json()

    def _load_from_json(self):
        data = None
        print(f"Loading config file: {os.path.abspath(self.config_file)}")
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as file:
                    data = json.load(file)
            except Exception as err:
                print("Config loading exception:")
                print(err)
                raise err
        else:
            print("Config file not found, using defaults")

        if data is None:
            return
        if not isinstance(data, dict):
            print("Error: Invalid type of configuration object, expected dict, got %s", type(data))
            return
        for key, value in data.items():
            self.__setattr__(key, value)


CONFIG = Config(CONFIG_FILE)
