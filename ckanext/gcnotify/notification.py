import requests
import logging
import json

from ckan.lib.mailer import MailerException
from ckan.lib.helpers import ckan_version
from ckan.common import _, config

log = logging.getLogger(__name__)


class GcnotifyAPI:

  secretKey = config.get('ckanext.gcnotify.secret_key')
  baseURI = config.get('ckanext.gcnotify.base_url')
  templateID = config.get('ckanext.gcnotify.template_id')
  hostURL = config.get('ckan.site_url')

  def get_host_domain(self):
    # type: () -> str|None

    if (self.hostURL is None) or not len(self.hostURL):
      raise MailerException(_("No Host URL is set!"))

    return self.hostURL.replace("https://","").replace("http//","").replace("/","")

  def get_request_headers(self,
                          headers,
                          contentLength="0"):
    # type: (dict, str) -> dict|None

    if (self.secretKey is None) or not len(self.secretKey):
      raise MailerException(_("No GC Notify API key is set!"))

    headers['Authorization'] = 'ApiKey-v1 {}'.format(self.secretKey)
    headers['Content-Type'] = 'application/json'
    headers['User-agent'] = 'CKAN {}'.format(ckan_version())
    headers['Host'] = self.get_host_domain()
    headers['Content-Length'] = contentLength

    return headers


  def get_base_uri(self,
                  endpoint):
    # type: (str) -> str|None

    if (self.baseURI is None) or not len(self.baseURI):
      raise MailerException(_("No GC Notify base URI is set!"))

    if (endpoint is None) or not len(endpoint):
      raise MailerException(_("No GC Notify API endpoint is set!"))

    return self.baseURI + endpoint

  def get_template_id(self):

    if (self.templateID is None) or not len(self.templateID):
      raise MailerException(_("No GC Notify template ID is set!"))

    return self.templateID


  def get_request_body(self,
                      recipient,
                      subject,
                      body):
    # type: (str, str, str) -> dict|None

    return {
      'email_address': recipient,
      'template_id': self.get_template_id(),
      'personalisation': self.get_personalisation(subject,body)
    }


  def get_personalisation(self,
                          subject,
                          body):
    # type: (str, str) -> dict|None

    if (body is None) or not len(body):
      raise MailerException(_("No email body is set!"))

    return {
      'subject': subject,
      'rendered_body': body
    }


  def send_email(self,
                recipient,
                subject,
                body,
                headers={},
                attachments=None):
    # type: (str, str, str, dict, dict|None) -> None

    method = 'POST'
    bodyContent = self.get_request_body(recipient,subject,body)
    bodyContent = json.dumps(bodyContent)
    headerContent = self.get_request_headers(headers,str(len(bodyContent)))
    endpoint = self.get_base_uri('/v2/notifications/email')

    try:

      log.info("    ")
      log.info("DEBUG - Request Headers")
      log.info(headerContent)
      log.info("    ")

      response = requests.request(
        method=method,
        url=endpoint,
        json=bodyContent,
        headers=headerContent
      )

      response.raise_for_status()

    except requests.exceptions.HTTPError as error:

      log.info("    ")
      log.info("DEBUG - Response Headers")
      log.info(response.headers)
      log.info("    ")

      log.error("API {} request on {} failed with '{}'".format(
                    method,
                    endpoint,
                    error))

    finally:

      log.debug("API {} request on {} finished".format(method, endpoint))
