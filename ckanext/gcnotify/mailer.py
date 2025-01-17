from typing import Dict, Any, Optional, List
from ckan.model import User

from ckan.lib.helpers import ckan_version, roles_translated

from ckan.common import _, config, request
import ckan.lib.mailer as mailer

import requests
import json

import traceback
import logging


def get_template_id(action: str) -> str:
    template_ids = config.get('ckanext.gcnotify.template_ids', '')
    if not template_ids:
        template_ids = {}
    else:
        template_ids = json.loads(template_ids)

    if action not in template_ids:
        raise mailer.MailerException(_("No GC Notify template ID is set!"))

    template_id = template_ids.get(action)
    if not isinstance(template_id, str):
        raise mailer.MailerException(_("No GC Notify template ID is set!"))

    return template_id


def send_reset_link(user: 'User'):
    if not user.email:
        raise mailer.MailerException(_("No recipient email address available!"))

    # use user ID, use user fullname if it is set
    user_name = user.name
    if user.fullname:
        user_name = "%s (%s)" % (user.fullname, user.name)

    # generate a user reset key, then get it
    mailer.create_reset_key(user)
    reset_link = mailer.get_reset_link(user)

    send_email(recipient=user.email,
               template_id=get_template_id("send_reset_link"),
               personalisation={"user_name": user_name,
                                "reset_link": reset_link})


def send_username_recovery(email: str,
                           username_list: List[str]):
    if not email:
        raise mailer.MailerException(_("No recipient email address available!"))

    send_email(recipient=email,
               template_id=get_template_id("send_username_recovery"),
               personalisation={"username_list": '\n'.join(username_list)})


def send_invite(user: 'User',
                group_dict: Optional[Dict[str, Any]] = None,
                role: Optional[str] = None):
    if not user.email:
        raise mailer.MailerException(_("No recipient email address available!"))

    # use user ID, use user fullname if it is set
    user_name = user.name
    if user.fullname:
        user_name = "%s (%s)" % (user.fullname, user.name)

    # generate a user reset key, then get it
    mailer.create_reset_key(user)
    reset_link = mailer.get_reset_link(user)

    # get group type and name
    group_type = "N/A"
    group_title = "N/A"
    if group_dict:
        group_type = (_('organization') if
                      group_dict['is_organization'] else _('group'))
        group_title = group_dict.get('title')

    # get role name
    role_name = "N/A"
    if role:
        role_name = roles_translated().get(role, _(role))

    send_email(recipient=user.email,
               template_id=get_template_id("send_invite"),
               personalisation={"user_name": user_name,
                                "group_type": group_type,
                                "group_title": group_title,
                                "role_name": role_name,
                                "reset_link": reset_link})


def notify_ckan_user_create(email: str,
                            fullname: str,
                            username: str,
                            phoneno: str,
                            dept: str):
    """
    Send email to canada.notification_new_user_email config if it exists
    """
    if 'canada.notification_new_user_email' in config:

        recipient_name = config.get(
            'canada.notification_new_user_name',
            config['canada.notification_new_user_email']
        )

        recipient_address = config['canada.notification_new_user_email']

        # use user ID, use user fullname if it is set
        user_name = username
        if fullname:
            user_name = "%s (%s)" % (fullname, username)

        send_email(recipient=recipient_address,
                   template_id=get_template_id("new_user_admin_note"),
                   personalisation={"admin_name": recipient_name,
                                    "user_name": user_name,
                                    "email_address": email,
                                    "phone_number": phoneno or "N/A",
                                    "department": dept})

        # send email to form post values
        send_email(recipient=email,
                   template_id=get_template_id("new_user_note"),
                   personalisation={"user_name": user_name})


def notify_lockout(user: 'User', lockout_timeout: int):
    if not user.email:
        raise mailer.MailerException(_("No recipient email address available!"))

    send_email(recipient=user.email,
               template_id=get_template_id("notify_lockout"),
               personalisation={"timeout": int(lockout_timeout / 60)})


def get_request_headers(headers: Dict[str, Any]) -> Dict[str, Any]:
    secret_key = config.get('ckanext.gcnotify.secret_key')

    headers['Authorization'] = 'ApiKey-v1 {}'.format(secret_key)
    headers['Content-Type'] = 'application/json'
    headers['User-agent'] = 'CKAN/{}'.format(ckan_version())

    return headers


def get_api_endpoint(endpoint: str) -> str:
    base_uri = config.get('ckanext.gcnotify.base_url')

    if not endpoint:
        raise mailer.MailerException(_("No GC Notify API endpoint is set!"))

    return base_uri + endpoint


def get_request_body(recipient: str,
                     template_id: str,
                     personalisation: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'email_address': recipient,
        'template_id': template_id,
        'personalisation': personalisation,
        'reference': request.url if request else config.get('ckan.site_id', 'N/A'),
    }


def send_email(recipient: str,
               template_id: str,
               personalisation: Optional[Dict[str, Any]] = None,
               headers: Optional[Dict[str, Any]] = None,
               attachments: Optional[Dict[str, Any]] = None):
    if not personalisation:
        personalisation = {}
    if not headers:
        headers = {}
    method = 'POST'
    body_content = get_request_body(recipient, template_id, personalisation)
    header_content = get_request_headers(headers)
    endpoint = get_api_endpoint('/v2/notifications/email')

    response = requests.request(method=method,
                                url=endpoint,
                                json=body_content,
                                headers=header_content,
                                verify=False)

    try:
      response.raise_for_status()
    except Exception as e:
      logging.error(traceback.format_exc())
