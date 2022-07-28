import ckan.plugins as plugins

import ckan.lib.mailer as mailer

from ckanext.gcnotify.mailer import MailerOverride

class GcnotifyPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    # IConfigurer

    def update_config(self, config):
        # type: (object) -> None

        mailer_override = MailerOverride()

        mailer.send_reset_link = mailer_override.send_reset_link
        mailer.send_invite = mailer_override.send_invite
