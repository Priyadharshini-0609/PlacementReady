from django.urls import path
from placement_app import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('profile-setup/', views.profile_setup_view, name='profile_setup'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    
    path('assessment/', views.skill_assessment_view, name='skill_assessment'),
    path('assessment/result/<int:result_id>/', views.assessment_result_view, name='assessment_result'),
    
    path('roadmap/', views.roadmap_view, name='roadmap'),
    path('task/toggle/<int:task_id>/', views.toggle_task_view, name='toggle_task'),
    path('topic/<int:topic_id>/', views.task_detail_view, name='task_detail'),
    
    path('tests/', views.mock_test_list_view, name='mock_tests'),
    path('test/take/<int:test_id>/', views.take_test_view, name='take_test'),
    path('test/result/<int:result_id>/', views.test_result_view, name='test_result'),
    
    path('interview-prep/', views.interview_prep_view, name='interview_prep'),
    
    # API endpoints
    path('api/job-roles/', views.get_job_roles_api, name='get_job_roles_api'),
    
    # Admin URLs
    path('admin-panel/', views.admin_dashboard_view, name='admin_dashboard'),
    path('admin-panel/questions/', views.admin_manage_questions_view, name='admin_questions'),
    path('admin-panel/topics/', views.admin_manage_topics_view, name='admin_topics'),
    path('admin-panel/tests/', views.admin_manage_tests_view, name='admin_tests'),
]
