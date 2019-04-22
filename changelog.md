irflow-sdk-python changelog

* v1.0.5 -  Initial Release  
* v1.0.6 -  Add option to pass in config_args in addition to specifiying a path to api.conf 
* v1.0.7 -  Parenthesis and helper text fix
* v1.1.1 -  Added support for IR-Flow 4.1 (api changes), Python 3 compatibility
* v1.1.2 -  Fixed module import to work better dynamically
* v1.1.4 -  Improved python3 compatibility
* v1.1.5 -  Move to a universal wheel module
* v1.1.6 -  Fix __init.py__
* v1.1.8 -  Add create object method
* v1.1.9 -  Fix requirements.txt build issue
* v1.1.10 - Fix MANIFEST.in
* v1.1.12 - Fix method attach_alert_to_incident (was the inverse)
* v1.2.0
    * Add docstrings to irflow_client for RTD build 
    * Bump version to align with IR-Flow Version. 
    * Added get_version endpoint
    * added requirements.txt freeze,
    * created readthedocs site
    * moved dev requirements to requirements-dev.
* v1.2.1 Add testing
* v1.2.2 Add requirements-dev.txt to MANIFEST
* v1.2.3 Move dump settings to debug, remove pprint, since it's supplied in json.dumps and requests.json()
* v1.2.4 Updated ignore ssl warning based on requests changes
* v1.5.0 Added session timeout values, and dynamic version based user-agent string
* v1.5.1 Fix requirements typos
* v1.5.2 Readme.md updates for Py2 and Py3 examples
* v1.5.3 Fix User Agent typo
* v1.5.4 remove sys.exit()
    * Fix CI workflow
    * detect http 503 (IR-Flow Offline)
    * fix debug logging 
    * Fix update_incident function to added owner and group IDs
    * Converted to Apache 2.0 license
* v1.5.5 Test build
* v1.5.6 Release under Apache2.0 License
    * Update requests==2.20.0 to patch CVE-2018-18074
* v1.5.7 Update .gitignore, bump requirements.txt
* v1.5.8 Fix python_requires for pip 18.0+
* v1.5.9 Update URLLib for https://nvd.nist.gov/vuln/detail/CVE-2019-11324
* v1.5.10 Fix py2 compatibility
