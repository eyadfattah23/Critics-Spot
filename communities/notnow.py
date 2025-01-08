"""Tests for the communities app models."""
from django.test import TestCase
from .models import Post, Like, Comment, Group, GroupMember
from django.contrib.auth import get_user_model

User = get_user_model()


class PostModelTest(TestCase):
    """Tests for the Post model."""

    def test_post_creation(self):
        """Test the creation of a post."""
        post = Post.objects.create(
            content='Test content'
        )
        self.assertEqual(post.content, 'Test content')


class LikeModelTest(TestCase):
    """Tests for the Like model."""

    def test_like_creation(self):
        """Test the creation of a like."""
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
    """Tests for the Comment model."""

    def test_comment_creation(self):
        """Test the creation of a comment."""
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
    """Tests for the Community model."""

    def test_group_creation(self):
        """Test the creation of a community."""
        group = Group.objects.create(
            name="Sample Group",
            description="This is a sample group."
        )
        self.assertEqual(group.name, "Sample Group")
        self.assertEqual(group.description, "This is a sample group.")


class GroupMemberModelTest(TestCase):
    """Tests for the Community members."""

    def test_group_member_creation(self):
        """Test the addition of a member to a community."""
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
