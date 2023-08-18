import logging

from infobip_api_client.api.send_sms_api import SendSmsApi
from infobip_api_client.api_client import ApiClient, Configuration
from infobip_api_client.exceptions import ApiException
from infobip_api_client.model.sms_advanced_textual_request import SmsAdvancedTextualRequest
from infobip_api_client.model.sms_destination import SmsDestination
from infobip_api_client.model.sms_textual_message import SmsTextualMessage

from core.config import config


class InfoBipMessageBroker:
    """ Send sms message by using Infobip API. """
    SENDER = "InfoSMS"

    def __init__(self):
        self.client_config = Configuration(
            host=config.INFO_BIP_BASE_URL,
            api_key={"APIKeyHeader": config.INFO_BIP_API_KEY},
            api_key_prefix={"APIKeyHeader": "App"},
        )

        self.api_client = ApiClient(self.client_config)

    def send_message(self, recipient, text):
        sms_request = SmsAdvancedTextualRequest(
            messages=[
                SmsTextualMessage(
                    destinations=[
                        SmsDestination(
                            to=recipient,
                        ),
                    ],
                    _from=self.SENDER,
                    text=text,
                )
            ])

        api_instance = SendSmsApi(self.api_client)

        try:
            api_response = api_instance.send_sms_message(sms_advanced_textual_request=sms_request)
            logging.debug(f"InfoBip API response: {api_response}")
        except ApiException as ex:
            logging.error("Error occurred while trying to send SMS message.")

