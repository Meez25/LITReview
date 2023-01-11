from django.utils import timezone
from django.test import TestCase
from authentication.models import User

from .models import Ticket, Review, UserFollows

from .views import get_users_viewable_tickets, get_users_viewable_reviews
# Create your tests here.


class TicketDisplayedTests(TestCase):
    """
    Class to test the display of tickets in the "flux"
    """

    def setUp(self):
        now = timezone.now()
        self.user1 = User.objects.create_user(
                username="user1", password="toto")
        self.user2 = User.objects.create_user(
                username="user2", password="toto")
        self.user3 = User.objects.create_user(
                username="user3", password="toto")

        self.ticket1 = Ticket(title="Titre 1", description="Description 1",
                              user=self.user1, time_created=now)
        self.ticket1.save()
        self.ticket2 = Ticket(title="Titre 2", description="Description 2",
                              user=self.user2,
                              time_created=now - timezone.timedelta(days=1))
        self.ticket2.save()
        self.ticket3 = Ticket(title="Titre 3", description="Description 3",
                              user=self.user3,
                              time_created=now - timezone.timedelta(days=2))
        self.ticket3.save()

    def test_get_users_viewable_tickets(self):
        """
        get_users_viewable_tickets should return the ticket I created
        """
        viewable_tickets = get_users_viewable_tickets(self.user1)
        self.assertIn(self.ticket1, viewable_tickets)
        self.assertNotIn(self.ticket2, viewable_tickets)
        self.assertNotIn(self.ticket3, viewable_tickets)
        self.assertEqual(len(viewable_tickets), 1)

    def test_see_following_user_ticket(self):
        """
        test if the current user see other's people post
        """
        self.userFollow1 = UserFollows(
                user=self.user1, followed_user=self.user2)
        self.userFollow1.save()
        self.userFollow2 = UserFollows(
                user=self.user1, followed_user=self.user3)
        self.userFollow2.save()
        viewable_tickets = get_users_viewable_tickets(self.user1)
        self.assertIn(self.ticket1, viewable_tickets)
        self.assertIn(self.ticket2, viewable_tickets)
        self.assertIn(self.ticket3, viewable_tickets)
        viewable_tickets_from_user2 = get_users_viewable_tickets(self.user2)
        self.assertNotIn(self.ticket1, viewable_tickets_from_user2)
        self.assertNotIn(self.ticket3, viewable_tickets_from_user2)

    def test_see_other_people_review_on_my_ticket(self):
        """
        Test if the current user see other's people reply on his tickets
        """
        self.userFollow1 = UserFollows(
                user=self.user1, followed_user=self.user2)
        self.userFollow1.save()
        self.userFollow2 = UserFollows(
                user=self.user1, followed_user=self.user3)
        self.userFollow2.save()
        self.review = Review(ticket=self.ticket1,
                             rating=5,
                             user=self.user2,
                             headline="headline",
                             body="body",
                             time_created=timezone.now())
        self.review.save()
        viewable_tickets = get_users_viewable_tickets(self.user1)
        viewable_reviews = get_users_viewable_reviews(self.user1)
        viewable_reviews_as_user_2 = get_users_viewable_reviews(self.user2)
        self.assertNotIn(self.ticket1, viewable_tickets)
        self.assertIn(self.review, viewable_reviews)
        self.assertNotIn(self.ticket1, viewable_reviews_as_user_2)
        self.assertIn(self.review, viewable_reviews_as_user_2)

    def test_see_reviews_on_following_user_ticket(self):
        """
        Test if the current user can see reviews on tickets from users he
        follows
        """
        self.userFollow1 = UserFollows(
                user=self.user2, followed_user=self.user1)
        self.userFollow1.save()
        self.userFollow2 = UserFollows(
                user=self.user3, followed_user=self.user2)
        self.userFollow2.save()
        self.review1 = Review(ticket=self.ticket1,
                              rating=5,
                              user=self.user2,
                              headline="headline",
                              body="body",
                              time_created=timezone.now())
        self.review1.save()
        self.review2 = Review(ticket=self.ticket2,
                              rating=5,
                              user=self.user3,
                              headline="headline",
                              body="body",
                              time_created=timezone.now())
        self.review2.save()
        viewable_reviews = get_users_viewable_reviews(self.user1)
        self.assertIn(self.review1, viewable_reviews)
        self.assertNotIn(self.review2, viewable_reviews)
        viewable_reviews_as_user_2 = get_users_viewable_reviews(self.user2)
        self.assertIn(self.review1, viewable_reviews_as_user_2)
        self.assertIn(self.review2, viewable_reviews_as_user_2)
        viewable_reviews_as_user_3 = get_users_viewable_reviews(self.user3)
        self.assertIn(self.review1, viewable_reviews_as_user_3)
        self.assertIn(self.review2, viewable_reviews_as_user_3)

    def test_dont_see_reviews_on_other_tickets(self):
        """
        Test if the current user cannot see reviews on
        tickets he doesn't have access to
        """
        self.userFollow1 = UserFollows(
                user=self.user2, followed_user=self.user1)
        self.userFollow1.save()
        self.userFollow2 = UserFollows(
                user=self.user3, followed_user=self.user2)
        self.userFollow2.save()
        self.review1 = Review(ticket=self.ticket1,
                              rating=5,
                              user=self.user2,
                              headline="headline",
                              body="body",
                              time_created=timezone.now())
        self.review1.save()
        self.review2 = Review(ticket=self.ticket2,
                              rating=5,
                              user=self.user3,
                              headline="headline",
                              body="body",
                              time_created=timezone.now())
        self.review2.save()
        viewable_reviews = get_users_viewable_reviews(self.user1)
        self.assertIn(self.review1, viewable_reviews)
        self.assertNotIn(self.review2, viewable_reviews)
        viewable_reviews_as_user_3 = get_users_viewable_reviews(self.user3)
        self.assertIn(self.review1, viewable_reviews_as_user_3)
