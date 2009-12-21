from django.conf import settings


_PREFICES = ("PYPI", "DJANGOPYPI")

def get_setting(name, default=None):
    for prefix in _PREFICES:
        fq = "_".join([prefix, name])
        if hasattr(settings, fq):
            return getattr(settings, fq)
    return default

ROLES = get_setting("ROLES", {"default": ()})
DEFAULT_ROLE = get_setting("DEFAULT_ROLE", "default")
RELEASE_UPLOAD_TO = get_setting("RELEASE_UPLOAD_TO", "dists")
ALLOW_VERSION_OVERWRITE = get_setting("ALLOW_VERSION_OVERWRITE", False)
