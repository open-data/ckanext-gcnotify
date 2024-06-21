import ckan.plugins as plugins

from ckanext.gcnotify import mailer
from ckan.common import config


class GcnotifyPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IMailer)

    assert config["ckanext.gcnotify.secret_key"]
    assert config["ckanext.gcnotify.base_url"]
    assert config["ckanext.gcnotify.template_ids"]

    # IMailer

    def send_reset_link(self, user):
        mailer.send_reset_link(user)

    def send_invite(self, user, group_dict, role):
        mailer.send_invite(user, group_dict, role)

    def notify_ckan_user_create(self, email, fullname, username, phoneno, dept):
        mailer.notify_ckan_user_create(email, fullname, username, phoneno, dept)

    def send_username_recovery(self, email, username_list):
        mailer.send_username_recovery(email, username_list)
