from ckan.lib.helpers import roles_translated
from ckan.model import User

from notifications_python_client.notifications import NotificationsAPIClient
from notifications_python_client.utils import DOCUMENT_UPLOAD_SIZE_LIMIT

import base64
import json
from typing import Any, Iterable, Optional, cast

from ckan.common import _, config
import ckan.lib.mailer as mailer


def get_template_id(action: str) -> str:

    template_ids = config.get('ckanext.gcnotify.template_ids') # type: dict|None
    if not template_ids:
      template_ids = {}
    else:
      template_ids = json.loads(template_ids)

    if action not in template_ids:
      raise mailer.MailerException(_("No GC Notify template ID is set!"))

    return template_ids.get(action)


def send_reset_link(user: User) -> None:

    if not user.email:
      raise mailer.MailerException(_("No recipient email address available!"))

    # use user ID, use user fullname if it is set
    user_name = user.name
    if user.fullname:
      user_name = user.fullname

    # generate a user reset key, then get it
    mailer.create_reset_key(user)
    reset_link = mailer.get_reset_link(user)
    
    send_email(
      recipient=user.email,
      template_id=get_template_id("send_reset_link"),
      personalisation={
        "user_name": user_name,
        "reset_link": reset_link
      }
    )


def send_invite(user: User,
                group_dict: Optional[dict] = None,
                role: Optional[str] = None) -> None:

    if not user.email:
      raise mailer.MailerException(_("No recipient email address available!"))

    # use user ID, use user fullname if it is set
    user_name = user.name
    if user.fullname:
      user_name = user.fullname

    # generate a user reset key, then get it
    mailer.create_reset_key(user)
    reset_link = mailer.get_reset_link(user)

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
    
    send_email(
      recipient=user.email,
      template_id=get_template_id("send_invite"),
      personalisation={
        "user_name": user_name,
        "group_type": group_type,
        "group_title": group_title,
        "role_name": role_name,
        "reset_link": reset_link
      }
    )


def notify_ckan_user_create(email: str,
                            fullname: str,
                            username: str,
                            phoneno: str,
                            dept: str) -> None:

  ###
  # send email to canada.notification_new_user_email config if it exists
  ###
  if 'canada.notification_new_user_email' in config:

    recipient_name = config.get(
        'canada.notification_new_user_name',
        config['canada.notification_new_user_email']
    )

    recipient_address = config['canada.notification_new_user_email']

    send_email(
      recipient=recipient_address,
      template_id=get_template_id("new_user_admin_note"),
      personalisation={
        "admin_name": recipient_name,
        "user_name": username,
        "email_address": email,
        "phone_number": phoneno or "N/A",
        "department": dept
      }
    )

  ###
  # send email to form post values
  ###
  send_email(
    recipient=email,
    template_id=get_template_id("new_user_note"),
    personalisation={
      "user_name": fullname or email
    }
  )


def get_attachments(attachments: dict,
                    personalisation: dict) -> dict:
    
    if attachments is None:
        return personalisation

    for index, attachment in attachments:
        if len(attachment) == 3:
            name, _file, media_type = cast(mailer.AttachmentWithType, attachment)
        else:
            name, _file = cast(mailer.AttachmentWithoutType, attachment)
            media_type = None

        contents = _file.read()
        sendingMethod = 'attach'

        if len(contents) > DOCUMENT_UPLOAD_SIZE_LIMIT:
            sendingMethod = 'link'

        personalisation[f"file_{index}"] = {
            'file': base64.b64encode(contents).decode('ascii'),
            'filename': name,
            'sending_method': sendingMethod
        }
    return personalisation


def send_email(recipient: str,
              template_id: str,
              personalisation: Optional[dict] = {},
              headers: Optional[dict] = {},
              attachments: Optional[Iterable[mailer.Attachment]] = None) -> None:

    personalisation = get_attachments(attachments, personalisation)

    notificactions_client = NotificationsAPIClient(config.get("ckanext.gcnotify.api_key"))   

    notificactions_client.send_email_notification(
        email_address=recipient,
        template_id=template_id,
        personalisation=personalisation
    )
