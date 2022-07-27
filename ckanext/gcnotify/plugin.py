import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit

import ckan.model as model

import ckan.lib.mailer as mailer

from ckan.lib.mailer import MailerException, Attachment
from typing import Any, Iterable, Optional
from ckan.common import _, config

from notifications_python_client.notifications import NotificationsAPIClient


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
              attachments: Optional[Iterable[Attachment]] = None) -> None:

        if (recipient.email is None) or not len(recipient.email):
            raise MailerException(_("No recipient email address available!"))

        if (self.apiKey is None) or not len(self.apiKey):
            raise MailerException(_("No GC Notify API key is set!"))

        if (self.baseURI is None) or not len(self.baseURI):
            raise MailerException(_("No GC Notify base URI is set!"))

        if (self.templateID is None) or not len(self.templateID):
            raise MailerException(_("No GC Notify template ID is set!"))

        if body_html is not None:
            body = body_html

        if (body is None) or not len(body):
            raise MailerException(_("No email body is set!"))

        notificactions_client = NotificationsAPIClient(self.apiKey)

        if attachments is not None:
            #TODO: hanled attachments.
            attachments = attachments

        notificactions_client.send_email_notification(
            email_address=recipient.email,
            template_id=self.templateID,
            personalisation={
                'subject': subject,
                'rendered_body': body,
            }
        )

    
