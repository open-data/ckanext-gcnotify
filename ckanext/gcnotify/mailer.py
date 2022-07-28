import ckan.lib.mailer as mailer
from ckan.common import _, config
from ckan.lib.base import render_jinja2

from ckanext.gcnotify.notification import GcnotifyAPI


class MailerOverride:

  gcnotify_api = GcnotifyAPI()
  
  def send_reset_link(self,
                      user):
    # type: (ckan.model.User) -> None

    mailer.create_reset_key(user)
    body = mailer.get_reset_link_body(user)
    extra_vars = {
        'site_title': config.get('ckan.site_title')
    }
    subject = render_jinja2('emails/reset_password_subject.txt', extra_vars)

    # Make sure we only use the first line
    subject = subject.split('\n')[0]

    if (user.email is None) or not len(user.email):
          raise mailer.MailerException(_("No recipient email address available!"))

    self.gcnotify_api.send_email(
      recipient=user.email,
      subject=subject,
      body=body
    )

  def send_invite(self,
                  user,
                  group_dict=None,
                  role=None):
    # type: (ckan.model.User, dict|None, str|None) -> None

    mailer.create_reset_key(user)
    body = mailer.get_invite_body(user, group_dict, role)
    extra_vars = {
        'site_title': config.get('ckan.site_title')
    }
    subject = render_jinja2('emails/invite_user_subject.txt', extra_vars)

    # Make sure we only use the first line
    subject = subject.split('\n')[0]

    if (user.email is None) or not len(user.email):
          raise mailer.MailerException(_("No recipient email address available!"))

    self.gcnotify_api.send_email(
      recipient=user.email,
      subject=subject,
      body=body
    )
