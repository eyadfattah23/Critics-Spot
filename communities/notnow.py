from django.test import TestCase
from .models import Post, Like, Comment, Group, GroupMember
from django.contrib.auth import get_user_model

User = get_user_model()


class PostModelTest(TestCase):
    """ Test Post model. """
    def test_post_creation(self):
        """ Test creating a new post. """
        post = Post.objects.create(
            content='Test content'
        )
        self.assertEqual(post.content, 'Test content')


class LikeModelTest(TestCase):
    """ Test Like model. """
    def test_like_creation(self):
        """ Test creating a new like. """
        user = User.objects.create_user(
            username="sampleuser",
            password="samplepassword"
        )
        post = Post.objects.create(
            content='Test content'
        )
        like = Like.objects.create(
            user=user,
            post=post
        )
        self.assertEqual(like.user.username, "sampleuser")
        self.assertEqual(like.post.content, "Test content")


class CommentModelTest(TestCase):
    """ Test Comment model. """
    def test_comment_creation(self):
        """ Test creating a new comment. """
        user = User.objects.create_user(
            username="sampleuser",
            password="samplepassword"
        )
        post = Post.objects.create(
            content='Test content'
        )
        comment = Comment.objects.create(
            user=user,
            post=post,
            content='Test comment'
        )
        self.assertEqual(comment.user.username, "sampleuser")
        self.assertEqual(comment.post.content, "Test content")
        self.assertEqual(comment.content, "Test comment")


class GroupModelTest(TestCase):
    """ Class for testing group models. """
    def test_group_creation(self):
        group = Group.objects.create(
            name="Sample Group",
            description="This is a sample group."
        )
        self.assertEqual(group.name, "Sample Group")
        self.assertEqual(group.description, "This is a sample group.")


class GroupMemberModelTest(TestCase):
    """ Class for testing group member models. """
    def test_group_member_creation(self):
        user = User.objects.create_user(
            username="sampleuser",
            password="samplepassword"
        )
        group = Group.objects.create(
            name="Sample Group",
            description="This is a sample group."
        )
        group_member = GroupMember.objects.create(
            user=user,
            group=group
        )
        self.assertEqual(group_member.user.username, "sampleuser")
        self.assertEqual(group_member.group.name, "Sample Group")
