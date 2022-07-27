[![Tests](https://github.com/open-data/ckanext-gcnotify/workflows/Tests/badge.svg?branch=main)](https://github.com/open-data/ckanext-gcnotify/actions)

# ckanext-gcnotify

CKAN Extentsion for GC Notify itegration


## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.6 and earlier | No    |
| 2.7             | No    |
| 2.8             | No    |
| 2.9             | Yes    |

| Python version    | Compatible?   |
| --------------- | ------------- |
| 3.5 and earlier | No    |
| 3.6 and later             | Yes    |

## Installation

To install ckanext-gcnotify:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    git clone https://github.com/open-data/ckanext-gcnotify.git
    cd ckanext-gcnotify
    pip install -e .
	pip install -r requirements.txt

3. Add `gcnotify` to the `ckan.plugins` setting in your CKAN
   config file

4. Add `ckanext.gcnotify.api_key` setting in your CKAN config file with the value of your GC Notify API key

5. Add `ckanext.gcnotify.base_url` setting in your CKAN config file with the value of your GC Notify base URI

6. Restart CKAN

## Config settings

```
# GC Notify API key
# (required, default: None).
ckanext.gcnotify.api_key = my_api_key
```
```
# GC Notify base URI
# (required, default: None).
ckanext.gcnotify.base_url = my_base_uri
```

## Developer installation

To install ckanext-gcnotify for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/open-data/ckanext-gcnotify.git
    cd ckanext-gcnotify
    python setup.py develop
    pip install -r dev-requirements.txt

## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini

## Releasing a new version of ckanext-gcnotify

If ckanext-gcnotify should be available on PyPI you can follow these steps to publish a new version:

1. Update the version number in the `setup.py` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:

    pip install --upgrade setuptools wheel twine

3. Create a source and binary distributions of the new version:

       python setup.py sdist bdist_wheel && twine check dist/*

   Fix any errors you get.

4. Upload the source distribution to PyPI:

       twine upload dist/*

5. Commit any outstanding changes:

       git commit -a
       git push

6. Tag the new release of the project on GitHub with the version number from
   the `setup.py` file. For example if the version number in `setup.py` is
   0.0.1 then do:

       git tag 0.0.1
       git push --tags

## License

[MIT](https://raw.githubusercontent.com/open-data/ckanext-gcnotify/master/LICENSE)
