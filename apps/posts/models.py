from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.contrib.postgres.fields import ArrayField

from allauth.socialaccount.fields import JSONField

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

    PENDING, SENT = (0, 1)

    STATUS = (
        (PENDING, 'pending'),
        (SENT, 'sent')
    )


    publish_date = models.DateTimeField(
        _('date published'),
        null=False,
        blank=False,
        help_text=_("The date which the post was posted to social.")
    )

    status = models.PositiveSmallIntegerField(
        _("status"),
        choices=STATUS,
        null=False,
        blank=False,
        default=PENDING,
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

class Pages(models.Model):

    uid = models.PositiveIntegerField(
        help_text=_("id from facebook"),
        default =5
        )

    ME, PAGE = (0, 1)

    TYPE = (
        (ME, "me"),
        (PAGE, "page"),

    )

    name = models.CharField(
        max_length=50
    )

    avatar = models.URLField(
        _("url"),
        max_length=200,
        blank=True,
        null=True,
        help_text=_(
            "The url of the user avatar" )
    )

    provider = models.CharField(
        max_length=25
    )

    type = models.PositiveSmallIntegerField(
        _("type"),
        choices=TYPE,
        null=False,
        blank=False,
    )
    extra_data = models.TextField(
        verbose_name=_('extra data'), 
        default=dict
    ) 

class PagePost(models.Model):
    page = models.ForeignKey(
        'Pages',
        on_delete=models.CASCADE,
        related_name="post_page",
        unique=False,
        null=False,
        blank=False,
        help_text=_("The page has post or posts")
    )

    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        related_name="page_post",
        unique=False,
        null=False,
        blank=False,
        help_text=_("The post belongs to page or pages")
    )
    
    is_published = models.BooleanField()

class PageUser(models.Model):
    user = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name="page_user",
        unique=False,
        null=False,
        blank=False,
        help_text=_("The user has page or pages")
    )

    page = models.ForeignKey(
        'Pages',
        on_delete=models.CASCADE,
        related_name="user_page",
        unique=False,
        null=False,
        blank=False,
        help_text=_("The page belongs to user or users")
    )