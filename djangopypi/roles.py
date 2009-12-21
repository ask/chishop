from djangopypi import conf


def current_role(request=None):
    role = conf.DEFAULT_ROLE
    if request:
        role = getattr(request, "pypi_role", None) or role
    return role


def get_mro(role):
    return tuple([role] + list(conf.ROLES[role]))
