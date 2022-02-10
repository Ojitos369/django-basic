# Python
import datetime as dt

# Django
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

# User
from .models import *


def create_question(question_text = "Some text", days = 0, hours = 0, minutes = 0, seconds = 0):
    """
    Create a question with the given "question_text" and published the
    given number of days, hours, minutes and seconds offset to now (negative for questions published in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + dt.timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    #print()
    #print(f"Now: {timezone.now()}")
    #print(f"Days: {days}, Hours: {hours}, Minutes: {minutes}, Seconds: {seconds}")
    #print(f"Time: {time}")
    #print()
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    
    def test_was_published_recently_with_future_questions(self):
        """ was_published_recently returns False for questions whose pub_date is in the future """
        future_question = create_question(days = 30)
        self.assertIs(future_question.was_published_recently(), False)
        
    def test_was_published_recently_with_old_questions(self):
        """ was_published_recently returns False for questions whose pub_date is older than 1 day """
        old_question = create_question(days = -1)
        self.assertIs(old_question.was_published_recently(), False)
        
    def test_was_published_recently_with_now_questions(self):
        """ was_published_recently returns True for questions whose pub_date is within the last day """
        now_question = create_question(hours = -23, minutes = -59, seconds = -59)
        self.assertIs(now_question.was_published_recently(), True)
        time = timezone.now()
        new_question = Question(question_text = "Any Question", pub_date = time)
        self.assertIs(now_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    
    def test_no_cuestions(self):
        """If not question exist, an appropiate message is displayed"""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])
        
    def test_get_queryset_with_future_questions(self):
        """If question.pub_date is in the future, it is not displayed"""
        future_question = create_question(days = 30)
        future_question.save()
        response = self.client.get(reverse('polls:index'))
        self.assertNotIn(future_question, response.context['latest_question_list'])
        
    def test_get_queryset_with_old_questions(self):
        """If question.pub_date is older than 1 day, it is not displayed"""
        old_question = create_question(days = -1)
        old_question.save()
        response = self.client.get(reverse('polls:index'))
        self.assertIn(old_question, response.context['latest_question_list'])
        
    def test_future_question_and_past_question(self):
        """Even if both past and future questions exist, only past questions are displayed"""
        future_question = create_question(days = 30)
        past_question = create_question(days = -30)
        response = self.client.get(reverse('polls:index'))
        self.assertIn(past_question, response.context['latest_question_list'])
        
        
    
    def test_two_past_question(self):
        """The questions index page may display multiple questions."""
        past_q_1 = create_question(days = -30)
        past_q_2 = create_question(hours = -1, minutes = -30)
        response = self.client.get(reverse('polls:index'))
        self.assertIn(past_q_1, response.context['latest_question_list'])
        self.assertIn(past_q_2, response.context['latest_question_list'])
        
    def test_two_future_question(self):
        """The questions index page may display multiple questions."""
        future_q_1 = create_question(days = 1, hours = -1, minutes = -30)
        future_q_2 = create_question(hours = 1, minutes = 30)
        response = self.client.get(reverse('polls:index'))
        self.assertNotIn(future_q_1, response.context['latest_question_list'])
        self.assertNotIn(future_q_2, response.context['latest_question_list'])


class QuestionDetailViewTest(TestCase):
    
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 error not found.
        """
        future_question = create_question(hours = 1, minutes = 30)
        response = self.client.get(reverse('polls:detail', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)
    
    def test_past_questions(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(minutes = -15)
        response = self.client.get(reverse('polls:detail', args=(past_question.id,)))
        self.assertContains(response, past_question.question_text)


class QuestionResultsView(TestCase):
    
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 error not found.
        """
        future_question = create_question(hours = 1, minutes = 30)
        response = self.client.get(reverse('polls:results', args=(future_question.id,)))
        self.assertEqual(response.status_code, 404)
    
    def test_past_questions(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(minutes = -15)
        response = self.client.get(reverse('polls:results', args=(past_question.id,)))
        self.assertContains(response, past_question.question_text)
    