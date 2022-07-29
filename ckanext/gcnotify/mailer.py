import ckan.lib.mailer as mailer
from ckanext.gcnotify.notification import GcnotifyAPI
from ckan.common import _, config
import json


class MailerOverride:

  gcnotify_api = GcnotifyAPI()
  templateIDs = config.get('ckanext.gcnotify.template_ids') # type: dict|None

  def __init__(self):
    # type: () -> None

    if (self.templateIDs is None) or not len(self.templateIDs):
      self.templateIDs = {}
    else:
      self.templateIDs = json.loads(self.templateIDs)


  def get_template_id(self,
                      action):
    # type: (str) -> str|None

    if action not in self.templateIDs:
      raise mailer.MailerException(_("No GC Notify template ID is set!"))

    return self.templateIDs.get(action)


  def send_reset_link(self,
                      user):
    # type: (ckan.model.User) -> None

    if (user.email is None) or not len(user.email):
        raise mailer.MailerException(_("No recipient email address available!"))

    # use user ID, use user fullname if it is set
    userName = user.name
    if user.fullname is not None:
      userName = user.fullname

    # generate a user reset key, then get it
    mailer.create_reset_key(user)
    resetLink = mailer.get_reset_link(user)
    
    self.gcnotify_api.send_email(
      recipient=user.email,
      templateID=self.get_template_id(self.send_reset_link.__name__),
      personalisation={
        "user_name": userName,
        "reset_link": resetLink
      }
    )
