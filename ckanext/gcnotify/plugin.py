import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


class GcnotifyPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)

    # IConfigurer

    def update_config(self, config_):
        