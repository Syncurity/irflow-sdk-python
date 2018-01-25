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

