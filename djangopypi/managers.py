import operator

from django.db import models
from django.db.models.query import QuerySet, Q

from djangopypi import roles
from djangopypi import conf


def role_circuit(role):
    mro = roles.get_mro(role)
    return len(mro) > 1 and reduce(operator.or_, map(Q, mro)) or mro[0]


class RoleAwareManager(models.Manager):
    match_role_by = "role"

    def role(self, role=conf.DEFAULT_ROLE):
        return self.filter(**{self.match_role_by: role_circuit(role)})


class ProjectManager(RoleAwareManager):
    match_role_by = "role"


class ReleaseManager(RoleAwareManager):
    match_role_by = "project__role"

