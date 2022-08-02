import requests
import logging

from ckan.lib.mailer import MailerException
from ckan.lib.helpers import ckan_version
from ckan.common import _, config

log = logging.getLogger(__name__)


class GcnotifyAPI:

  secretKey = config.get('ckanext.gcnotify.secret_key') # type: str
  baseURI = config.get('ckanext.gcnotify.base_url') # type: str


  def get_request_headers(self,
                          headers):
    # type: (dict, str) -> dict|None

    if (self.secretKey is None) or not len(self.secretKey):
      raise MailerException(_("No GC Notify API key is set!"))

    headers['Authorization'] = 'ApiKey-v1 {}'.format(self.secretKey)
    headers['Content-Type'] = 'application/json'
    headers['User-agent'] = 'CKAN/{}'.format(ckan_version())

    return headers


  def get_api_endpoint(self,
                  endpoint):
    # type: (str) -> str|None

    if (self.baseURI is None) or not len(self.baseURI):
      raise MailerException(_("No GC Notify base URI is set!"))

    if (endpoint is None) or not len(endpoint):
      raise MailerException(_("No GC Notify API endpoint is set!"))

    return self.baseURI + endpoint


  def get_request_body(self,
                      recipient,
                      templateID,
                      personalisation):
    # type: (str, str, dict) -> dict|None

    return {
      'email_address': recipient,
      'template_id': templateID,
      'personalisation': personalisation
    }


  def send_email(self,
                recipient,
                templateID,
                personalisation={},
                headers={},
                attachments=None):
    # type: (str, str, dict, dict, dict|None) -> None

    method = 'POST'
    bodyContent = self.get_request_body(recipient,templateID,personalisation)
    headerContent = self.get_request_headers(headers)
    endpoint = self.get_api_endpoint('/v2/notifications/email')

    try:

      response = requests.request(
        method=method,
        url=endpoint,
        json=bodyContent,
        headers=headerContent,
        verify=False
      )

      response.raise_for_status()

    except requests.exceptions.HTTPError as error:

      log.error("API {} request on {} failed with '{}'".format(
                    method,
                    endpoint,
                    error))

    finally:

      log.debug("API {} request on {} finished".format(method, endpoint))
