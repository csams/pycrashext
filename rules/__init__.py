from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

STANDARD_PASS = "No error detected."
STANDARD_FAIL = """
Title  : {{title}}
Message: {{msg}}

KCS Title: {{kcs_title}}
KCS URL: {{kcs_url}}
Resolution: {{resolution}}
"""
