from django.test import TestCase, Client
from django.contrib.auth.models import User
from placement_app.models import UserProfile, JobRole, Category, Question, MockTest, TestResult
from placement_app.utils import calculate_readiness_score

class PlacementReadyTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.role = JobRole.objects.create(
            name="Data Analyst",
            description="Analyzes data",
            required_skills="SQL, Python"
        )
        self.user = User.objects.create_user(
            username="teststudent",
            password="password123",
            first_name="Test",
            last_name="Student"
        )
        self.profile = UserProfile.objects.create(
            user=self.user,
            department="B.Sc Computer Science",
            year_of_study="Final Year",
            grade_type="CGPA",
            score_value=8.2,
            target_role=self.role,
            profile_setup_completed=True,
            assessment_completed=True
        )
        self.category = Category.objects.create(name="SQL", description="SQL queries")
        self.question = Question.objects.create(
            category=self.category,
            question_text="Select query test?",
            option_a="Option A", option_b="Option B", option_c="Option C", option_d="Option D",
            correct_option="A",
            is_diagnostic=True
        )

    def test_readiness_score_calculation(self):
        readiness = calculate_readiness_score(self.user)
        self.assertIn('overall_score', readiness)
        self.assertIn('category_scores', readiness)
        self.assertIsInstance(readiness['overall_score'], int)

    def test_user_onboarding_flow(self):
        res = self.client.get('/')
        self.assertEqual(res.status_code, 302)
        self.assertIn('/register/', res.url)

        login_success = self.client.login(username="teststudent", password="password123")
        self.assertTrue(login_success)
        
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test")

    def test_assessment_page(self):
        self.client.login(username="teststudent", password="password123")
        response = self.client.get('/assessment/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Diagnostic Skill Assessment Test")
