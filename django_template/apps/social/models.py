from django.db import models
from core.models import Thing
from django.utils import timezone
from django.contrib.auth import get_user_model
from polymorphic.models import PolymorphicModel 
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Profile(PolymorphicModel, Thing):
    TYPE_CHOICES = [
        ('public', _('Public')),
        ('private', _('Private')),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='public', verbose_name=_('Type'), db_comment=_('Public profiles are visible to everyone, private profiles are only visible to profiles following.'))
    followers = models.ManyToManyField('self', related_name='profile_fk_followers', symmetrical=False, blank=True, verbose_name=_('Followers'))
    following = models.ManyToManyField('self', related_name='profile_fk_following', symmetrical=False, blank=True, verbose_name=_('Following'))
    blocked = models.ManyToManyField('self', related_name='profile_fk_blocked', symmetrical=False, blank=True, verbose_name=_('Blocked'))

    def __str__(self):
        return f'{self.type} - {self.polymorphic_ctype}'

    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('Profiles')
        ordering = ['-created_at', 'type', 'is_active']

class CommonProfile(Profile):
    user = models.OneToOneField('users.User', on_delete=models.CASCADE, related_name='commonprofile_fk_user', verbose_name=_('User'))
    person = models.OneToOneField('persons.Person', on_delete=models.CASCADE, related_name='commonprofile_fk_person', verbose_name=_('Person'), null=True, blank=True)

    def __str__(self):
        return f'{self.type} - {self.user.username}'

    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')
        ordering = ['user', '-created_at', 'type', 'is_active']
        unique_together = ['user', 'person'] 

class Post(Thing):
    TYPE_CHOICES = [
        ('public', _('Public')),
        ('private', _('Private')),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='public', verbose_name=_('Type'))
    author = models.ForeignKey('social.Profile', on_delete=models.CASCADE, related_name='post_fk_author', verbose_name=_('Profile'))
    content = models.TextField(null=False, blank=False, max_length=512, verbose_name=_('Content'))
    likes = models.ManyToManyField('social.Profile', related_name='liked_posts', blank=True, verbose_name=_('Likes'))
    views = models.PositiveIntegerField(default=0, verbose_name=_('Views'))
    shares = models.PositiveIntegerField(default=0, verbose_name=_('Shares'))
    enable_comments = models.BooleanField(default=True, verbose_name=_('Enable Comments'))
    description = None

    def __str__(self):
        return f'{self.author} - {self.content[:30]}'

    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        ordering = ['is_active', 'views', 'author', '-created_at']

class Comment(Thing):
    parent_comment = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies', verbose_name=_("Parent Comment"))
    profile = models.ForeignKey('social.Profile', on_delete=models.CASCADE, related_name='comment_fk_profile', verbose_name=_('Profile'))
    post = models.ForeignKey('social.Post', on_delete=models.CASCADE, related_name='comment_fk_post', verbose_name=_('Post'))
    content = models.TextField(verbose_name=_('Content'))

    def __str__(self):
        return f'{self.profile} - {self.content[:30]}'

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['-created_at', 'profile', 'post']

class Chat(models.Model):
    participants = models.ManyToManyField('social.Profile', related_name='chats')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))

    def __str__(self):
        return f'Chat between {", ".join([str(participant) for participant in self.participants.all()])}'

    class Meta:
        verbose_name = _('Chat')
        verbose_name_plural = _('Chats')
        ordering = ['-created_at']

class Message(Thing):
    STATUS_CHOICES = [
        ('created', _('Created')),
        ('sent', _('Sent')),
        ('received', _('Received')),
        ('read', _('Read')),
        ('deleted', _('Deleted')),
    ]
    sender = models.ForeignKey('social.Profile', on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey('social.Profile', on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField(verbose_name=_('Content'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created', verbose_name=_('Status'))

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver}'

    class Meta:
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
        ordering = ['-created_at', 'sender', 'receiver', 'status']

class Notification(Thing):
    profile = models.ForeignKey('social.Profile', on_delete=models.CASCADE, related_name='notifications')
    content = models.TextField(verbose_name=_('Content'))
    status = models.CharField(max_length=20, choices=Message.STATUS_CHOICES, default='created', verbose_name=_('Status'))

    def __str__(self):
        return f'Notification for {self.profile}'

    class Meta:
        verbose_name = _('Notification')
        verbose_name_plural = _('Notifications')
        ordering = ['-created_at', 'profile', 'status']
