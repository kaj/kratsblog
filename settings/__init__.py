# Collect actual settings

from .defaults import *
from .local import *

if PROD:
    # Set a bunch of security headers
    SESSION_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 3600 # TODO maybe 31536000 when confirmed
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # Allow h2o proxying
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
