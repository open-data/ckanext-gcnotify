[![Tests](https://github.com/open-data/ckanext-gcnotify/workflows/Tests/badge.svg?branch=main)](https://github.com/open-data/ckanext-gcnotify/actions)

# ckanext-gcnotify

CKAN Extentsion for GC Notify itegration


## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.6 and earlier | Not tested    |
| 2.7             | Not tested    |
| 2.8             | No    |
| 2.9             | Yes    |

| Python version    | Compatible?   |
| --------------- | ------------- |
| 2.9 and earlier | Yes    |
| 3.0 and later             | Yes    |

## Installation

To install ckanext-gcnotify:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    git clone --branch master --single-branch https://github.com/open-data/ckanext-gcnotify.git
    cd ckanext-gcnotify
    pip install -e .
    pip install -r requirements.txt

3. Add `gcnotify` to the `ckan.plugins` setting in your CKAN
   config file

4. Add `ckanext.gcnotify.secret_key` setting in your CKAN config file with the value of your GC Notify secret key (last 5 hex groups of your API key)

5. Add `ckanext.gcnotify.base_url` setting in your CKAN config file with the value of your GC Notify base URI

6. Add `ckanext.gcnotify.template_ids` setting in your CKAN config file with the values of your GC Notify template IDs in a dict (key is email action and value is template ID, ___see Config Settings for all valid key values___)

7. Restart CKAN

## Config settings

```
# GC Notify Secret key
# (required, default: None).
ckanext.gcnotify.secret_key = my_secret_key
```
```
# GC Notify base URI
# (required, default: None).
ckanext.gcnotify.base_url = my_base_uri
```
```
# GC Notify template IDs
# (required, default: None).
ckanext.gcnotify.template_ids = {
  "send_reset_link":"template_id",
  "send_invite":"template_id",
  "new_user_admin_note":"template_id",
  "new_user_note":"template_id",
  "send_username_recovery":"template_id"}
```

## License

[MIT](https://raw.githubusercontent.com/open-data/ckanext-gcnotify/master/LICENSE)
