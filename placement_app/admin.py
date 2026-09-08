from django.contrib import admin
from placement_app.models import (
    Department, JobRole, UserProfile, Category, Topic, Task,
    UserTaskProgress, Question, MockTest, TestResult, InterviewQuestion
)

admin.site.register(Department)
admin.site.register(Category)
admin.site.register(Task)
admin.site.register(UserTaskProgress)
admin.site.register(TestResult)

@admin.register(JobRole)
class JobRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    filter_horizontal = ('departments',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'department', 'target_role', 'current_level')
    list_filter = ('department', 'current_level')

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'day_number', 'category', 'target_role')
    list_filter = ('target_role', 'category')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'category', 'difficulty', 'is_diagnostic')
    list_filter = ('category', 'difficulty', 'is_diagnostic')

@admin.register(MockTest)
class MockTestAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'job_role', 'duration_minutes')

@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_type', 'category', 'job_role', 'difficulty')
    list_filter = ('question_type', 'category', 'job_role')