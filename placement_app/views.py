from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone

from placement_app.models import (
    UserProfile, JobRole, Category, Topic, Task, UserTaskProgress,
    Question, MockTest, TestResult, InterviewQuestion
)
from placement_app.forms import (
    StudentAccountForm, ProfileSetupForm, QuestionForm, TopicForm,
    MockTestForm, InterviewQuestionForm
)
from placement_app.utils import calculate_readiness_score

def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


# ── Department → Job Roles mapping ──────────────────────────────────────────
DEPARTMENT_JOB_ROLES = {
    'B.Sc Computer Science': [
        'Software Developer', 'Python Developer', 'Web Developer',
        'Full Stack Developer', 'Data Analyst', 'Software Tester', 'Database Developer',
    ],
    'B.Sc Information Technology': [
        'IT Support Specialist', 'Web Developer', 'Software Developer',
        'System Administrator', 'Network Administrator', 'Data Analyst', 'Cloud Support Associate',
    ],
    'B.Sc Data Science': [
        'Data Analyst', 'Junior Data Scientist', 'Business Intelligence Analyst',
        'Machine Learning Associate', 'Data Visualization Analyst', 'Data Engineer',
    ],
    'B.Sc Computer Science with Artificial Intelligence': [
        'AI/ML Engineer', 'Machine Learning Engineer', 'AI Developer',
        'Data Analyst', 'Python Developer', 'Computer Vision Engineer', 'AI Research Assistant',
    ],
    'BCA': [
        'Software Developer', 'Web Developer', 'Python Developer',
        'Full Stack Developer', 'Software Tester', 'Technical Support Executive', 'Data Analyst',
    ],
    'B.Sc Mathematics': [
        'Data Analyst', 'Statistician', 'Business Analyst',
        'Financial Analyst', 'Risk Analyst', 'Operations Research Analyst',
    ],
    'B.Sc Physics': [
        'Physics Research Assistant', 'Laboratory Assistant', 'Quality Control Analyst',
        'Technical Assistant', 'Data Analyst', 'Scientific Assistant',
    ],
    'B.Sc Chemistry': [
        'Chemist', 'Laboratory Analyst', 'Quality Control Analyst',
        'Quality Assurance Executive', 'Research Assistant', 'Production Chemist',
    ],
    'B.Sc Biotechnology': [
        'Biotech Research Assistant', 'Laboratory Technician', 'Quality Control Analyst',
        'Quality Assurance Associate', 'Clinical Research Assistant', 'Bioprocess Associate',
    ],
    'B.Sc Microbiology': [
        'Microbiologist', 'Laboratory Technician', 'Quality Control Analyst',
        'Quality Assurance Associate', 'Research Assistant', 'Food Safety Analyst',
    ],
    'B.Sc Psychology': [
        'HR Executive', 'Recruitment Executive', 'Research Assistant',
        'Counselling Assistant', 'Behavioral Research Assistant', 'Training & Development Executive',
    ],
    'B.Com General': [
        'Accountant', 'Accounts Executive', 'Financial Analyst',
        'Banking Associate', 'Tax Associate', 'Audit Assistant', 'Business Analyst',
    ],
    'B.Com Computer Applications': [
        'Accounts Executive', 'Accounting Software Support Executive', 'Business Analyst',
        'Data Analyst', 'MIS Executive', 'Banking Associate', 'Junior Software Support Executive',
    ],
    'B.Com Accounting & Finance': [
        'Accountant', 'Financial Analyst', 'Audit Assistant',
        'Tax Associate', 'Accounts Executive', 'Banking Associate', 'Finance Executive',
    ],
    'BBA': [
        'Business Development Executive', 'HR Executive', 'Marketing Executive',
        'Sales Executive', 'Operations Executive', 'Business Analyst', 'Management Trainee',
    ],
    'B.A English': [
        'Content Writer', 'Copywriter', 'Editor',
        'Proofreader', 'Technical Writer', 'Customer Support Executive', 'Communication Executive',
    ],
    'B.A Tamil': [
        'Tamil Content Writer', 'Translator', 'Proofreader',
        'Content Editor', 'Teacher/Academic Assistant', 'Media Content Executive',
    ],
    'B.A Economics': [
        'Economic Research Assistant', 'Data Analyst', 'Financial Analyst',
        'Market Research Analyst', 'Business Analyst', 'Banking Associate',
    ],
    'B.A History': [
        'Research Assistant', 'Museum Assistant', 'Content Writer',
        'Documentation Assistant', 'Archivist Assistant', 'Heritage Project Assistant',
    ],
    'B.A Sociology': [
        'Research Assistant', 'HR Executive', 'Social Research Assistant',
        'Community Program Coordinator', 'NGO Program Assistant', 'Survey Research Assistant',
    ],
    'B.A Visual Communication': [
        'Graphic Designer', 'UI/UX Designer', 'Video Editor',
        'Content Creator', 'Digital Marketing Executive', 'Social Media Executive', 'Visual Designer',
    ],
    'B.A Journalism': [
        'Journalist', 'News Writer', 'Content Writer',
        'Copy Editor', 'Reporter', 'Digital Media Executive', 'Social Media Content Editor',
    ],
}


def get_job_roles_api(request):
    """JSON API – returns job role list for a given department."""
    department = request.GET.get('department', '')
    roles = DEPARTMENT_JOB_ROLES.get(department, [])
    return JsonResponse({'roles': roles})


def home_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        if not profile.profile_setup_completed:
            return redirect('profile_setup')
        elif not profile.assessment_completed:
            return redirect('skill_assessment')
        return redirect('dashboard')
    
    # 1st Page for new visitors is Student Registration
    return redirect('register')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = StudentAccountForm(request.POST)
        if form.is_valid():
            from django.contrib.auth.models import User
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name']
            )
            UserProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, f"Account created successfully, {user.first_name}! Now please fill in your academic details.")
            return redirect('profile_setup')
    else:
        form = StudentAccountForm()
        
    return render(request, 'placement_app/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.update_streak()
            
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            
            if user.is_staff:
                return redirect('admin_dashboard')
            elif not profile.profile_setup_completed:
                return redirect('profile_setup')
            elif not profile.assessment_completed:
                return redirect('skill_assessment')
            else:
                return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
        
    return render(request, 'placement_app/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('login')


@login_required
def profile_setup_view(request):
    import json
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        # Resolve the text-based role selection → JobRole FK
        role_text = request.POST.get('target_role_text', '').strip()
        post_data = request.POST.copy()
        if role_text:
            job_role_obj, _ = JobRole.objects.get_or_create(
                name=role_text,
                defaults={
                    'description': f'{role_text} - placement target role',
                    'required_skills': '',
                }
            )
            # Attach to the right department
            dept_val = post_data.get('department', '')
            if dept_val:
                from placement_app.models import Department
                dept_obj, _ = Department.objects.get_or_create(name=dept_val)
                job_role_obj.departments.add(dept_obj)
            post_data['target_role'] = job_role_obj.pk
        else:
            # Keep whatever was in the hidden field (existing FK), or clear it
            if not post_data.get('target_role'):
                post_data['target_role'] = ''

        form = ProfileSetupForm(post_data, instance=profile)
        if form.is_valid():
            p = form.save(commit=False)
            p.profile_setup_completed = True
            p.save()
            messages.success(request, "Academic Profile setup complete! Let's now take your Diagnostic Skill Assessment.")
            return redirect('skill_assessment')
    else:
        form = ProfileSetupForm(instance=profile)

    # Saved role text for pre-selection on page load
    saved_role_text = profile.target_role.name if profile.target_role else ''

    return render(request, 'placement_app/profile_setup.html', {
        'form': form,
        'profile': profile,
        'dept_job_roles_json': json.dumps(DEPARTMENT_JOB_ROLES),
        'saved_role_text': saved_role_text,
    })



@login_required
def dashboard_view(request):
    if request.user.is_staff:
        return redirect('admin_dashboard')

    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    profile.update_streak()

    readiness_data = calculate_readiness_score(request.user)
    recent_results = TestResult.objects.filter(user=request.user).order_by('-completed_at')[:5]

    if profile.target_role:
        topics = Topic.objects.filter(target_role=profile.target_role)[:4]
    else:
        topics = Topic.objects.all()[:4]

    completed_task_ids = set(
        UserTaskProgress.objects.filter(user=request.user, completed=True).values_list('task_id', flat=True)
    )

    context = {
        'profile': profile,
        'readiness': readiness_data,
        'recent_results': recent_results,
        'topics': topics,
        'completed_task_ids': completed_task_ids,
    }
    return render(request, 'placement_app/dashboard.html', context)


@login_required
def profile_view(request):
    import json
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        role_text = request.POST.get('target_role_text', '').strip()
        post_data = request.POST.copy()
        if role_text:
            job_role_obj, _ = JobRole.objects.get_or_create(
                name=role_text,
                defaults={
                    'description': f'{role_text} - placement target role',
                    'required_skills': '',
                }
            )
            dept_val = post_data.get('department', '')
            if dept_val:
                from placement_app.models import Department
                dept_obj, _ = Department.objects.get_or_create(name=dept_val)
                job_role_obj.departments.add(dept_obj)
            post_data['target_role'] = job_role_obj.pk
        else:
            if not post_data.get('target_role'):
                post_data['target_role'] = ''

        form = ProfileSetupForm(post_data, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated!")
            return redirect('profile')
    else:
        form = ProfileSetupForm(instance=profile)

    saved_role_text = profile.target_role.name if profile.target_role else ''

    return render(request, 'placement_app/profile.html', {
        'form': form,
        'profile': profile,
        'dept_job_roles_json': json.dumps(DEPARTMENT_JOB_ROLES),
        'saved_role_text': saved_role_text,
    })


def get_department_group(dept_name):
    dept = dept_name or ''
    if any(k in dept for k in ['Computer', 'Information Technology', 'Data Science', 'Artificial Intelligence', 'BCA']):
        return 'Computer/IT'
    elif any(k in dept for k in ['Com', 'BBA', 'Accounting', 'Finance', 'Business']):
        return 'Commerce'
    elif any(k in dept for k in ['Math', 'Physics', 'Chemistry', 'Biotechnology', 'Microbiology', 'Psychology', 'Science']):
        return 'Science'
    elif any(k in dept for k in ['English', 'Tamil', 'Economics', 'History', 'Sociology', 'Visual Communication', 'Journalism', 'B.A']):
        return 'Arts'
    return 'All'


@login_required
def skill_assessment_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    # ── Department-filtered diagnostic questions ──────────────────────────────
    dept_name = profile.department  # e.g. "B.Com General"
    group = get_department_group(dept_name)

    # Retrieve diagnostic questions for this department group or common ('All')
    questions = Question.objects.filter(is_diagnostic=True, department_group__in=[group, 'All'])

    if not questions.exists():
        questions = Question.objects.filter(is_diagnostic=True)
        if not questions.exists():
            questions = Question.objects.all()[:15]
    else:
        questions = questions[:20]

    if request.method == 'POST':
        total_q = questions.count()
        correct_c = 0
        cat_correct = {}
        cat_total = {}

        for q in questions:
            cat_name = q.category.name
            cat_total[cat_name] = cat_total.get(cat_name, 0) + 1
            selected = request.POST.get(f'question_{q.id}')
            if selected == q.correct_option:
                correct_c += 1
                cat_correct[cat_name] = cat_correct.get(cat_name, 0) + 1

        cat_percentages = {}
        for cat_name, tot in cat_total.items():
            corr = cat_correct.get(cat_name, 0)
            cat_percentages[cat_name] = round((corr / tot) * 100, 1)

        score_pct = round((correct_c / total_q) * 100, 1) if total_q > 0 else 0

        result = TestResult.objects.create(
            user=request.user,
            test=None,
            is_initial_assessment=True,
            total_questions=total_q,
            correct_answers=correct_c,
            score_percentage=score_pct,
            category_scores=cat_percentages
        )

        profile.assessment_completed = True
        profile.save()

        return redirect('assessment_result', result_id=result.id)

    # Quiz label shown in the template header
    role_label = profile.effective_target_role if profile.target_role or profile.custom_target_role else None
    dept_quiz_label = f"{dept_name} — {role_label}" if role_label else dept_name

    return render(request, 'placement_app/assessment.html', {
        'questions': questions,
        'profile': profile,
        'dept_quiz_label': dept_quiz_label,
    })


@login_required
def assessment_result_view(request, result_id):
    result = get_object_or_404(TestResult, id=result_id, user=request.user)
    readiness_data = calculate_readiness_score(request.user)
    return render(request, 'placement_app/assessment_result.html', {
        'result': result,
        'readiness': readiness_data,
    })


@login_required
def roadmap_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    if profile.target_role:
        topics = Topic.objects.filter(target_role=profile.target_role).prefetch_related('tasks')
    else:
        topics = Topic.objects.all().prefetch_related('tasks')

    completed_task_ids = set(
        UserTaskProgress.objects.filter(user=request.user, completed=True).values_list('task_id', flat=True)
    )

    readiness = calculate_readiness_score(request.user)

    context = {
        'profile': profile,
        'topics': topics,
        'completed_task_ids': completed_task_ids,
        'readiness': readiness,
    }
    return render(request, 'placement_app/roadmap.html', context)


@login_required
def toggle_task_view(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    progress, created = UserTaskProgress.objects.get_or_create(user=request.user, task=task)
    progress.completed = not progress.completed
    progress.save()

    if progress.completed:
        request.user.profile.update_streak()

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        readiness = calculate_readiness_score(request.user)
        return JsonResponse({
            'success': True,
            'completed': progress.completed,
            'overall_score': readiness['overall_score'],
            'roadmap_progress': readiness['roadmap_progress'],
            'streak': request.user.profile.streak_count
        })
    
    return redirect('roadmap')


@login_required
def task_detail_view(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    tasks = topic.tasks.all()
    questions = topic.questions.all()
    
    completed_task_ids = set(
        UserTaskProgress.objects.filter(user=request.user, completed=True, task__topic=topic).values_list('task_id', flat=True)
    )

    return render(request, 'placement_app/task_detail.html', {
        'topic': topic,
        'tasks': tasks,
        'questions': questions,
        'completed_task_ids': completed_task_ids,
    })


@login_required
def mock_test_list_view(request):
    category_id = request.GET.get('category')
    tests = MockTest.objects.all()
    if category_id:
        tests = tests.filter(category_id=category_id)
        
    categories = Category.objects.all()
    recent_results = TestResult.objects.filter(user=request.user, is_initial_assessment=False).order_by('-completed_at')[:5]

    return render(request, 'placement_app/mock_tests.html', {
        'tests': tests,
        'categories': categories,
        'recent_results': recent_results,
    })


@login_required
def take_test_view(request, test_id):
    test = get_object_or_404(MockTest, id=test_id)
    questions = test.questions.all()

    if request.method == 'POST':
        total_q = questions.count()
        correct_c = 0
        cat_correct = {}
        cat_total = {}

        for q in questions:
            cat_name = q.category.name
            cat_total[cat_name] = cat_total.get(cat_name, 0) + 1
            selected = request.POST.get(f'question_{q.id}')
            if selected == q.correct_option:
                correct_c += 1
                cat_correct[cat_name] = cat_correct.get(cat_name, 0) + 1

        cat_percentages = {}
        for cat_name, tot in cat_total.items():
            corr = cat_correct.get(cat_name, 0)
            cat_percentages[cat_name] = round((corr / tot) * 100, 1)

        score_pct = round((correct_c / total_q) * 100, 1) if total_q > 0 else 0

        result = TestResult.objects.create(
            user=request.user,
            test=test,
            is_initial_assessment=False,
            total_questions=total_q,
            correct_answers=correct_c,
            score_percentage=score_pct,
            category_scores=cat_percentages
        )

        request.user.profile.update_streak()
        return redirect('test_result', result_id=result.id)

    return render(request, 'placement_app/take_test.html', {
        'test': test,
        'questions': questions,
    })


@login_required
def test_result_view(request, result_id):
    result = get_object_or_404(TestResult, id=result_id, user=request.user)
    return render(request, 'placement_app/test_result.html', {'result': result})


@login_required
def interview_prep_view(request):
    qtype = request.GET.get('type')
    company = request.GET.get('company')
    search = request.GET.get('q')

    questions = InterviewQuestion.objects.all()
    if qtype:
        questions = questions.filter(question_type=qtype)
    if company:
        questions = questions.filter(company_tag__icontains=company)
    if search:
        questions = questions.filter(question__icontains=search)

    companies = InterviewQuestion.objects.values_list('company_tag', flat=True).distinct()
    companies = [c for c in companies if c]

    return render(request, 'placement_app/interview_prep.html', {
        'questions': questions,
        'selected_type': qtype,
        'selected_company': company,
        'companies': companies,
    })


# --- ADMIN VIEWS ---

@user_passes_test(is_admin)
def admin_dashboard_view(request):
    total_students = UserProfile.objects.count()
    total_questions = Question.objects.count()
    total_tests = MockTest.objects.count()
    total_topics = Topic.objects.count()

    students = UserProfile.objects.select_related('user', 'target_role').all()[:10]
    
    from django.contrib.auth.models import User
    all_student_users = User.objects.filter(is_staff=False)
    readiness_list = [calculate_readiness_score(u)['overall_score'] for u in all_student_users]
    avg_readiness = round(sum(readiness_list) / len(readiness_list), 1) if readiness_list else 0

    return render(request, 'placement_app/admin_dashboard.html', {
        'total_students': total_students,
        'total_questions': total_questions,
        'total_tests': total_tests,
        'total_topics': total_topics,
        'avg_readiness': avg_readiness,
        'students': students,
    })


@user_passes_test(is_admin)
def admin_manage_questions_view(request):
    questions = Question.objects.select_related('category', 'topic').all()
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Question added successfully!")
            return redirect('admin_questions')
    else:
        form = QuestionForm()
    
    return render(request, 'placement_app/admin_questions.html', {
        'questions': questions,
        'form': form
    })


@user_passes_test(is_admin)
def admin_manage_topics_view(request):
    topics = Topic.objects.select_related('category', 'target_role').all()
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Topic added successfully!")
            return redirect('admin_topics')
    else:
        form = TopicForm()
        
    return render(request, 'placement_app/admin_topics.html', {
        'topics': topics,
        'form': form
    })


@user_passes_test(is_admin)
def admin_manage_tests_view(request):
    tests = MockTest.objects.select_related('category', 'job_role').prefetch_related('questions').all()
    if request.method == 'POST':
        form = MockTestForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Mock Test created successfully!")
            return redirect('admin_tests')
    else:
        form = MockTestForm()
        
    return render(request, 'placement_app/admin_tests.html', {
        'tests': tests,
        'form': form
    })
