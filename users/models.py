from django.db import models


class users(models.Model):
    """ Class representing users. """
    name = models.CharField(max_length=255)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(max_length=255)
    image = models.ImageField(upload_to='profile_pictures/', default='default_user_image.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes = [
            models.Index(fields=['name'])
        ]
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.name


class groups(models.Model):
    """ Class representing groups. """
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    users = models.ManyToManyField(users)
    admins = models.ManyToManyField(users, related_name='group_admins')
    members = models.ManyToManyField(users, related_name='group_members')
    posts = models.ManyToManyField('posts', related_name='group_posts')
    files = models.ManyToManyField('files', related_name='group_files')
    events = models.ManyToManyField('events', related_name='group_events')
    notifications = models.ManyToManyField('notifications', related_name='group_notifications')
    messages = models.ManyToManyField('messages', related_name='group_messages')

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = "group"
        verbose_name_plural = "groups"

    def __str__(self):
        return self.name


class posts(models.Model):
    """ Class representing posts. """
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(users, on_delete=models.CASCADE)
    group = models.ForeignKey(groups, on_delete=models.CASCADE)
    comments = models.ManyToManyField('comments', related_name='post_comments')
    likes = models.ManyToManyField(users, related_name='post_likes')
    shares = models.ManyToManyField('posts', related_name='post_shares')
    notifications = models.ManyToManyField('notifications', related_name='post_notifications')
    files = models.ManyToManyField('files', related_name='post_files')

    class Meta:
        indexes = [
            models.Index(fields=['content']),
        ]
        ordering = ['-created_at']
        verbose_name = "post"
        verbose_name_plural = "posts"

    def __str__(self):
        return f"Post #{self.pk}: {self.content[:50]}..."


class comments(models.Model):
    """ Class representing comments. """
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(users, on_delete=models.CASCADE)
    post = models.ForeignKey(posts, on_delete=models.CASCADE)
    replies = models.ManyToManyField('comments', related_name='comment_replies')
    likes = models.ManyToManyField(users, related_name='comment_likes')
    notifications = models.ManyToManyField('notifications', related_name='comment_notifications')
    files = models.ManyToManyField('files', related_name='comment_files')

    class Meta:
        indexes = [
            models.Index(fields=['content']),
        ]
        ordering = ['-created_at']
        verbose_name = "comment"
        verbose_name_plural = "comments"

    def __str__(self):
        return f"Comment #{self.pk}: {self.content[:50]}..."


class files(models.Model):
    """ Class representing files. """
    file = models.FileField(upload_to='files/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(users, on_delete=models.CASCADE)
    post = models.ForeignKey(posts, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(comments, on_delete=models.CASCADE, null=True)
    notifications = models.ManyToManyField('notifications', related_name='file_notifications')
    groups = models.ManyToManyField(groups, related_name='file_groups')
    users = models.ManyToManyField(users, related_name='file_users')
    messages = models.ManyToManyField('messages', related_name='file_messages')

    class Meta:
        verbose_name = "file"
        verbose_name_plural = "files"

    def __str__(self):
        return f"File #{self.pk}: {self.file.name[:50]}..."


class events(models.Model):
    """ Class representing events. """
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(users, on_delete=models.CASCADE)
    group = models.ForeignKey(groups, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(users, related_name='event_attendees')
    notifications = models.ManyToManyField('notifications', related_name='event_notifications')

    class Meta:
        indexes = [
            models.Index(fields=['title']),
        ]
        ordering = ['-start_date']
        verbose_name = "event"
        verbose_name_plural = "events"

    def __str__(self):
        return f"Event #{self.pk}: {self.title[:50]}..."


class likes(models.Model):
    """ Class representing likes. """
    user = models.ForeignKey(users, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'post'), ('user', 'comment'), ('user', 'file'), ('user', 'event'))
        verbose_name = "like"
        verbose_name_plural = "likes"

    def __str__(self):
        return f"Like #{self.pk}"


class shares(models.Model):
    """ Class representing shares. """
    user = models.ForeignKey(users, on_delete=models.CASCADE)
    post = models.ForeignKey(posts, on_delete=models.CASCADE)
    comment = models.ForeignKey(comments, on_delete=models.CASCADE, null=True)
    file = models.ForeignKey(files, on_delete=models.CASCADE, null=True)
    event = models.ForeignKey(events, on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = (('user', 'post'), ('user', 'comment'), ('user', 'file'), ('user', 'event'))
        verbose_name = "share"
        verbose_name_plural = "shares"

    def __str__(self):
        return f"Share #{self.pk}"


class notifications(models.Model):
    """ Class representing notifications. """
    user = models.ForeignKey(users, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'post'), ('user', 'comment'), ('user', 'file'), ('user', 'event'))
        verbose_name = "notification"
        verbose_name_plural = "notifications"

    def __str__(self):
        return f"Notification #{self.pk}"


class messages(models.Model):
    """ Class representing messages. """
    sender = models.ForeignKey(users, on_delete=models.CASCADE, related_name='sender_messages')
    recipient = models.ForeignKey(users, on_delete=models.CASCADE, related_name='recipient_messages')
    content = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)
    group = models.ForeignKey(groups, on_delete=models.CASCADE, null=True)
    notifications = models.ManyToManyField('notifications', related_name='message_notifications')

    class Meta:
        indexes = [
            models.Index(fields=['content']),
        ]
        ordering = ['-created_at']
        verbose_name = "message"
        verbose_name_plural = "messages"

    def __str__(self):
        return f"Message #{self.pk}: {self.content[:50]}..."
