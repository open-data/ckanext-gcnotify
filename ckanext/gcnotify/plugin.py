import ckan.plugins as plugins

from ckanext.gcnotify import mailer
from ckan.common import config


MAPPING = {
    'request_password_reset': mailer.send_reset_link,
    'user_invited': mailer.send_invite,
    'user_created': mailer.notify_ckan_user_create,
    'request_username_recovery': mailer.send_username_recovery,
}


class GcnotifyPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.INotifier)

    assert config["ckanext.gcnotify.secret_key"]
    assert config["ckanext.gcnotify.base_url"]
    assert config["ckanext.gcnotify.template_ids"]

    # INotifier

    def notify_recipient(self, notification_sent,
            recipient_name, recipient_email, subject,
            body, body_html, headers, attachments):
        return True

    def notify_about_topic(self, topic, details):
        if topic in MAPPING:
            MAPPING.get(topic)(**details)
