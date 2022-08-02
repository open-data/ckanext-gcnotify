import ckan.lib.mailer as mailer
from ckanext.gcnotify.notification import GcnotifyAPI
from ckan.common import _, config
from ckan.lib.helpers import roles_translated
import json
import logging


class MailerOverride:

  gcnotify_api = GcnotifyAPI()
  templateIDs = config.get('ckanext.gcnotify.template_ids') # type: dict|None
  log = logging.getLogger(__name__) # type: logging.Logger

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

    try:

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

    except mailer.MailerException as exception:

      self.log.error(exception.message)


  def send_invite(self,
                  user,
                  group_dict=None,
                  role=None):
    # type: (ckan.model.User,dict|None,str|None) -> None

    try:

      if (user.email is None) or not len(user.email):
        raise mailer.MailerException(_("No recipient email address available!"))

      # use user ID, use user fullname if it is set
      userName = user.name
      if user.fullname is not None:
        userName = user.fullname

      # generate a user reset key, then get it
      mailer.create_reset_key(user)
      resetLink = mailer.get_reset_link(user)

      # get group type and name
      group_type = "N/A"
      group_title = "N/A"
      if group_dict:
        group_type = (_('organization') if group_dict['is_organization']
                      else _('group'))
        group_title = group_dict.get('title')

      # get role name
      role_name = "N/A"
      if role:
        role_name = roles_translated().get(role, _(role))
      
      self.gcnotify_api.send_email(
        recipient=user.email,
        templateID=self.get_template_id(self.send_invite.__name__),
        personalisation={
          "user_name": userName,
          "group_type": group_type,
          "group_title": group_title,
          "role_name": role_name,
          "reset_link": resetLink
        }
      )

    except mailer.MailerException as exception:

      self.log.error(exception.message)


  def notify_ckan_user_create(self,
                              email,
                              fullname,
                              username,
                              phoneno,
                              dept):
    # type: (str, str, str, str, str) -> None

    ###
    # send email to canada.notification_new_user_email config if it exists
    ###
    try:

      if 'canada.notification_new_user_email' in config:

        recipientName = config.get(
            'canada.notification_new_user_name',
            config['canada.notification_new_user_email']
        )

        recipientAddress = config['canada.notification_new_user_email']

        self.gcnotify_api.send_email(
          recipient=recipientAddress,
          templateID=self.get_template_id(self.notify_ckan_user_create.__name__),
          personalisation={
            "user_name": recipientName
          }
        )

    except mailer.MailerException as exception:

      self.log.error(exception.message)

    ###
    # send email to form post values
    ###
    try:

      self.gcnotify_api.send_email(
        recipient=email,
        templateID=self.get_template_id(self.notify_ckan_user_create.__name__),
        personalisation={
          "user_name": fullname or email
        }
      )

    except mailer.MailerException as exception:

      self.log.error(exception.message)

