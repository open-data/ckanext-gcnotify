import ckan.plugins as plugins

import ckan.lib.mailer as mailer
import ckanext.gcnotify.mailer as mailer_overrider
from ckan.common import config


class GcnotifyPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    assert config["ckanext.gcnotify.secret_key"]
    assert config["ckanext.gcnotify.base_url"]
    assert config["ckanext.gcnotify.template_ids"]

    # IConfigurer

    def update_config(self, config):
        # type: (object) -> None

        mailer.send_reset_link = mailer_overrider.send_reset_link
        mailer.send_invite = mailer_overrider.send_invite
        mailer.notify_ckan_user_create = mailer_overrider.notify_ckan_user_create
        mailer.notify_lockout = mailer_overrider.notify_lockout

