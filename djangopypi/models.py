import os
from django.db import models
from django.utils.translation import ugettext_lazy as _

OS_NAMES = (
        ("aix", "AIX"),
        ("beos", "BeOS"),
        ("debian", "Debian Linux"),
        ("dos", "DOS"),
        ("freebsd", "FreeBSD"),
        ("hpux", "HP/UX"),
        ("mac", "Mac System x."),
        ("macos", "MacOS X"),
        ("mandrake", "Mandrake Linux"),
        ("netbsd", "NetBSD"),
        ("openbsd", "OpenBSD"),
        ("qnx", "QNX"),
        ("redhat", "RedHat Linux"),
        ("solaris", "SUN Solaris"),
        ("suse", "SuSE Linux"),
        ("yellowdog", "Yellow Dog Linux"),
)

ARCHITECTURES = (
    ("alpha", "Alpha"),
    ("hppa", "HPPA"),
    ("ix86", "Intel"),
    ("powerpc", "PowerPC"),
    ("sparc", "Sparc"),
    ("ultrasparc", "UltraSparc"),
)

class Classifier(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = _(u"classifier")
        verbose_name_plural = _(u"classifiers")

    def __unicode__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=255, unique=True)
    license = models.CharField(max_length=255, blank=True)
    metadata_version = models.CharField(max_length=64, default=1.0)
    author = models.CharField(max_length=128, blank=True)
    home_page = models.URLField(verify_exists=False, blank=True, null=True)
    download_url = models.URLField(verify_exists=False, blank=True, null=True)
    summary = models.TextField(blank=True)
    description = models.TextField(blank=True)
    author_email = models.CharField(max_length=255, blank=True)
    classifiers = models.ManyToManyField(Classifier)

    class Meta:
        verbose_name = _(u"project")
        verbose_name_plural = _(u"projects")

    def __unicode__(self):
        return self.name

class Release(models.Model):
    version = models.CharField(max_length=128)
    distribution = models.FileField(upload_to="dists")
    dist_md5sum = models.CharField(max_length=255, blank=True)
    platform = models.CharField(max_length=255, blank=True)
    signature = models.CharField(max_length=128, blank=True)
    project = models.ForeignKey(Project, related_name="releases")

    class Meta:
        unique_together = ('version', 'platform')
        verbose_name = _(u"release")
        verbose_name_plural = _(u"releases")

    def __unicode__(self):
        return self.version

    @property
    def filename(self):
        return os.path.basename(self.distribution.name)

    @property
    def path(self):
        return self.distribution.name

