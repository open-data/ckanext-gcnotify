import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckan.model as model

import ckan.lib.mailer as mailer

import base64
from typing import Any, Iterable, Optional, cast
from ckan.common import _, config

from notifications_python_client.notifications import NotificationsAPIClient
from notifications_python_client.utils import DOCUMENT_UPLOAD_SIZE_LIMIT


class GcnotifyPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    apiKey = config.get('ckanext.gcnotify.api_key')
    baseURI = config.get('ckanext.gcnotify.base_url')
    templateID = config.get('ckanext.gcnotify.template_id')

    # IConfigurer

    def update_config(self, config):
        toolkit.mail_user = self.mail_user
        mailer.mail_user = self.mail_user

    def mail_user(self, recipient: model.User,
              subject: str,
              body: str,
              body_html: Optional[str] = None,
              headers: Optional[dict[str, Any]] = None,
              attachments: Optional[Iterable[mailer.Attachment]] = None) -> None:

        if (recipient.email is None) or not len(recipient.email):
            raise mailer.MailerException(_("No recipient email address available!"))

        if (self.apiKey is None) or not len(self.apiKey):
            raise mailer.MailerException(_("No GC Notify API key is set!"))

        if (self.baseURI is None) or not len(self.baseURI):
            raise mailer.MailerException(_("No GC Notify base URI is set!"))

        if (self.templateID is None) or not len(self.templateID):
            raise mailer.MailerException(_("No GC Notify template ID is set!"))

        if body_html is not None:
            body = body_html

        if (body is None) or not len(body):
            raise mailer.MailerException(_("No email body is set!"))

        notificactions_client = NotificationsAPIClient(self.apiKey)
        personalisationData = {
            'subject': subject,
            'rendered_body': body,
        }

        if attachments is not None:
            for index, attachment in attachments:
                if len(attachment) == 3:
                    name, _file, media_type = cast(mailer.AttachmentWithType, attachment)
                else:
                    name, _file = cast(mailer.AttachmentWithoutType, attachment)
                    media_type = None

                contents = _file.read()
                sendingMethod = 'attach'

                if len(contents) > DOCUMENT_UPLOAD_SIZE_LIMIT:
                    sendingMethod = 'link'

                personalisationData[f"file_{index}"] = {
                    'file': base64.b64encode(contents).decode('ascii'),
                    'filename': name,
                    'sending_method': sendingMethod
                }

        notificactions_client.send_email_notification(
            email_address=recipient.email,
            template_id=self.templateID,
            personalisation=personalisationData
        )

    
