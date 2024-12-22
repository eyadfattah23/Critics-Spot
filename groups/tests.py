from django.test import TestCase
from users.models import CustomUser
from .models import Post, Comment, Like, Group
import datetime


class PostTestCase(TestCase):
    """ Test the post model. """
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='testuser', password='testpassword')
        self.post = Post.objects.create(content="This is a post", user=self.user, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())

    def test_post_creation(self):
        self.assertEqual(self.post.content, "This is a post")
        self.assertEqual(self.post.user, self.user)
        self.assertIsNotNone(self.post.created_at)
        self.assertIsNotNone(self.post.updated_at)

    def test_post_update(self):
        self.post.content = "This is an updated post"
        self.post.save()
        self.assertEqual(self.post.content, "This is an updated post")
        self.assertIsNotNone(self.post.updated_at)

    def tearDown(self):
        self.user.delete()
        self.post.delete()

class LikePostTestCase(TestCase):
    """ Test the like model. """
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='testuser', password='testpassword')
        self.post = Post.objects.create(content="This is a post", user=self.user, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())
        self.like = Like.objects.create(user=self.user, post=self.post, created_at=datetime.datetime.now())

    def test_like_creation(self):
        self.assertEqual(self.like.user, self.user)
        self.assertEqual(self.like.post, self.post)
        self.assertIsNotNone(self.like.created_at)

    def tearDown(self):
        self.user.delete()
        self.post.delete()
        self.like.delete()


class CommentPostTestCase(TestCase):
    """ Test the comment model. """
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='testuser', password='testpassword')
        self.post = Post.objects.create(content="This is a post", user=self.user, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())
        self.comment = Comment.objects.create(post=self.post, user=self.user, content="This is a comment", created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())

    def test_comment_creation(self):
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.post, self.post)
        self.assertEqual(self.comment.content, "This is a comment")
        self.assertIsNotNone(self.comment.created_at)
        self.assertIsNotNone(self.comment.updated_at)
    

    def test_comment_update(self):
        self.comment.content = "This is an updated comment"
        self.comment.save()
        self.assertEqual(self.comment.content, "This is an updated comment")
        self.assertIsNotNone(self.comment.updated_at)
    
    def tearDown(self):
        self.user.delete()
        self.post.delete()
        self.comment.delete()

class GroupTestCase(TestCase):
    """ Test the group model. """
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", email="testemail", password="testpassword")
        self.post1 = Post.objects.create(content="This is a post", user=self.user, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())
        self.post2 = Post.objects.create(content="This is another post", user=self.user, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())
        self.group = Group.objects.create(name="test Group", description="This a test group", user=self.user, date_added=datetime.datetime.now())
        self.group.posts.add(self.post1)
        self.group.posts.add(self.post2)
    
    def test_group_creation(self):
        self.assertEqual(self.group.name, "test Group")
        self.assertEqual(self.group.description, "This a test group")
        self.assertEqual(self.group.user, self.user)
        self.assertIsNotNone(self.group.date_added)
        self.assertEqual(self.group.posts.all()[0], self.post1)
        self.assertEqual(self.group.posts.all()[1], self.post2)
    
    def test_group_add_post(self):
        self.assertEqual(self.group.posts.count(), 2)

    def tearDown(self):
        self.user.delete()
        self.post1.delete()
        self.post2.delete()
        self.group.delete()
