from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=150, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class JobRole(models.Model):
    name = models.CharField(max_length=100)
    departments = models.ManyToManyField(
        Department, related_name='job_roles', blank=True,
        help_text="Departments this role should be shown to"
    )
    description = models.TextField()
    icon_class = models.CharField(max_length=50, default="bi-briefcase-fill")
    required_skills = models.CharField(max_length=255, help_text="Comma separated skills")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    ]
    
    YEAR_CHOICES = [
        ('1st Year', '1st Year'),
        ('2nd Year', '2nd Year'),
        ('3rd Year', '3rd Year'),
        ('Final Year', 'Final Year'),
    ]

    GRADE_TYPE_CHOICES = [
        ('CGPA', 'CGPA (out of 10)'),
        ('Percentage', 'Percentage (%)'),
    ]

    DEPARTMENT_CHOICES = [
        ('B.Sc Computer Science', 'B.Sc Computer Science'),
        ('B.Sc Information Technology', 'B.Sc Information Technology'),
        ('B.Sc Data Science', 'B.Sc Data Science'),
        ('B.Sc Computer Science with Artificial Intelligence', 'B.Sc Computer Science with Artificial Intelligence'),
        ('B.Sc Mathematics', 'B.Sc Mathematics'),
        ('B.Sc Physics', 'B.Sc Physics'),
        ('B.Sc Chemistry', 'B.Sc Chemistry'),
        ('B.Sc Biotechnology', 'B.Sc Biotechnology'),
        ('B.Sc Microbiology', 'B.Sc Microbiology'),
        ('B.Sc Psychology', 'B.Sc Psychology'),
        ('BCA', 'BCA (Bachelor of Computer Applications)'),
        ('B.Com General', 'B.Com General'),
        ('B.Com Computer Applications', 'B.Com Computer Applications'),
        ('B.Com Accounting & Finance', 'B.Com Accounting & Finance'),
        ('BBA', 'BBA (Bachelor of Business Administration)'),
        ('B.A English', 'B.A English'),
        ('B.A Tamil', 'B.A Tamil'),
        ('B.A Economics', 'B.A Economics'),
        ('B.A History', 'B.A History'),
        ('B.A Sociology', 'B.A Sociology'),
        ('B.A Visual Communication', 'B.A Visual Communication'),
        ('B.A Journalism', 'B.A Journalism'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    department = models.CharField(max_length=150, choices=DEPARTMENT_CHOICES, default="B.Sc Computer Science")
    year_of_study = models.CharField(max_length=20, choices=YEAR_CHOICES, default="Final Year")
    grade_type = models.CharField(max_length=20, choices=GRADE_TYPE_CHOICES, default="CGPA")
    score_value = models.FloatField(default=8.0, help_text="CGPA value or Percentage value")
    skills = models.TextField(blank=True, help_text="Comma-separated skills (e.g. Python, SQL, Accounting, Excel)")
    target_role = models.ForeignKey(JobRole, on_delete=models.SET_NULL, null=True, blank=True)
    custom_target_role = models.CharField(max_length=100, blank=True, help_text="Custom target job role if not in list")
    current_level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='Beginner')
    streak_count = models.IntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    profile_setup_completed = models.BooleanField(default=False)
    assessment_completed = models.BooleanField(default=False)

    @property
    def effective_target_role(self):
        if self.custom_target_role:
            return self.custom_target_role
        return self.target_role.name if self.target_role else "Placement Candidate"

    def update_streak(self):
        today = timezone.now().date()
        if self.last_activity_date is None:
            self.streak_count = 1
        elif self.last_activity_date == today:
            pass
        elif self.last_activity_date == today - timezone.timedelta(days=1):
            self.streak_count += 1
        else:
            self.streak_count = 1
        self.last_activity_date = today
        self.save()

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon_class = models.CharField(max_length=50, default="bi-folder-fill")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Topic(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='topics')
    target_role = models.ForeignKey(JobRole, on_delete=models.SET_NULL, null=True, blank=True, related_name='topics')
    title = models.CharField(max_length=200)
    description = models.TextField()
    day_number = models.IntegerField(default=1, help_text="Day in recommended roadmap")
    content = models.TextField(help_text="Detailed HTML study material")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['day_number', 'id']

    def __str__(self):
        return f"Day {self.day_number}: {self.title}"


class Task(models.Model):
    TASK_TYPES = [
        ('Reading', 'Reading Material'),
        ('Quiz', 'Quick Quiz'),
        ('Coding Practice', 'Coding Practice'),
        ('Exercise', 'Practical Exercise'),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=200)
    task_type = models.CharField(max_length=30, choices=TASK_TYPES, default='Reading')
    estimated_minutes = models.IntegerField(default=15)
    order = models.IntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.topic.title} - {self.title}"


class UserTaskProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='task_progress')
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'task')

    def __str__(self):
        return f"{self.user.username} - {self.task.title} ({'Done' if self.completed else 'Pending'})"


class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    OPTION_CHOICES = [
        ('A', 'Option A'),
        ('B', 'Option B'),
        ('C', 'Option C'),
        ('D', 'Option D'),
    ]

    DEPARTMENT_GROUP_CHOICES = [
        ('All', 'All Departments (Common)'),
        ('Computer/IT', 'Computer / IT (CS, IT, AI, DS, BCA)'),
        ('Science', 'Science (Maths, Physics, Chemistry, Bio, Micro, Psych)'),
        ('Commerce', 'Commerce / Management (B.Com, BBA)'),
        ('Arts', 'Arts (English, Tamil, Economics, History, Sociology, VisComm, Journalism)'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True, blank=True, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=300)
    option_b = models.CharField(max_length=300)
    option_c = models.CharField(max_length=300)
    option_d = models.CharField(max_length=300)
    correct_option = models.CharField(max_length=1, choices=OPTION_CHOICES)
    explanation = models.TextField(blank=True, help_text="Explanation of correct answer")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='Medium')
    is_diagnostic = models.BooleanField(default=False, help_text="Include in diagnostic skill assessment")
    department_group = models.CharField(
        max_length=20,
        choices=DEPARTMENT_GROUP_CHOICES,
        default='All',
        help_text="Which department stream sees this question in diagnostic quiz"
    )

    def __str__(self):
        return f"[{self.category.name}] {self.question_text[:50]}..."



class MockTest(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    job_role = models.ForeignKey(JobRole, on_delete=models.SET_NULL, null=True, blank=True)
    duration_minutes = models.IntegerField(default=30)
    pass_percentage = models.IntegerField(default=60)
    questions = models.ManyToManyField(Question, related_name='mock_tests')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TestResult(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_results')
    test = models.ForeignKey(MockTest, on_delete=models.SET_NULL, null=True, blank=True, related_name='results')
    is_initial_assessment = models.BooleanField(default=False)
    total_questions = models.IntegerField()
    correct_answers = models.IntegerField()
    score_percentage = models.FloatField()
    category_scores = models.JSONField(default=dict, help_text="Category name to score percentage mapping")
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        test_name = self.test.title if self.test else "Diagnostic Assessment"
        return f"{self.user.username} - {test_name}: {self.score_percentage}%"


class InterviewQuestion(models.Model):
    QUESTION_TYPES = [
        ('HR', 'HR & Behavioral'),
        ('Attire', 'Dress Code & Appearance'),
        ('Communication', 'Communication Skills'),
        ('PreInterview', 'Before the Interview Checklist'),
        ('PostInterview', 'After the Interview Etiquette'),
        ('Technical', 'Technical Concepts'),
        ('SQL', 'SQL & Databases'),
        ('Python', 'Python Coding'),
        ('Java', 'Java Programming'),
        ('Aptitude', 'Aptitude & Logic'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='interview_questions')
    job_role = models.ForeignKey(JobRole, on_delete=models.SET_NULL, null=True, blank=True)
    question_type = models.CharField(max_length=30, choices=QUESTION_TYPES, default='Technical')
    question = models.TextField()
    answer_guide = models.TextField()
    tips = models.TextField(blank=True, help_text="Key talking points or tips for student")
    difficulty = models.CharField(max_length=10, default="Medium")
    company_tag = models.CharField(max_length=100, blank=True, help_text="Company tag (e.g. TCS, Infosys, Zoho, Wipro)")

    def __str__(self):
        return f"[{self.question_type}] {self.question[:50]}..."