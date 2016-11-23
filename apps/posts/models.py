from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

# for custom user model
# from django.contrib.auth import get_user_model
# User = get_user_model()


class Post(models.Model):

    REPOST, IMAGE, TEXT = range(3)

    TYPE = (
        (REPOST, "repost"),
        (IMAGE, "image"),
        (TEXT, "text"),

    )

    date_created = models.DateTimeField(
        _('date created'),
        default=timezone.now,
        editable=False,
        help_text=_("The date which the post was created.")
    )

    owner = models.ForeignKey(
        'auth.User',
        related_name="posts",
        unique=False,
        null=True,
        blank=True,
        help_text=_("The ownder of the post")
    )

    type = models.PositiveSmallIntegerField(
        _("type"),
        choices=TYPE,
        null=True,
        blank=True,
    )

    content = models.TextField(
        _("code"),
        blank=True,
        null=True,
        help_text=_("The content of the post")
    )

    themes = ArrayField(
        models.CharField(max_length=100),
        default=list,
        help_text=_("The themes of the post")
    )

    keywords = ArrayField(
        models.CharField(max_length=50),
        default=list,
        help_text=_("The keywords of the post")
    )

    url = models.URLField(
        _("url"),
        max_length=200,
        blank=True,
        null=True,
        help_text=_(
            "The url of the original article, used by REPOST type only")
    )

    # objects = models.Manager()

    # TODO: enable image upload
    # ref: http://stackoverflow.com/questions/20473572/django-rest-framework-file-upload
    # images = ArrayField(
    #     models.ImageField(),
    # )

    class Meta:
        ordering = ['date_created']
