import ckan.plugins as plugins

import ckan.lib.mailer as mailer

from ckanext.gcnotify.mailer import MailerOverride

class GcnotifyPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    mailer_override = MailerOverride()

    # IConfigurer

    def update_config(self, config):
        # type: (object) -> None

        mailer.send_reset_link = self.mailer_override.send_reset_link
