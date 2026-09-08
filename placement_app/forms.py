from django import forms
from django.contrib.auth.models import User
from placement_app.models import UserProfile, JobRole, Question, Topic, MockTest, InterviewQuestion, Category

class StudentAccountForm(forms.Form):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter your first name'}))
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter your last name'}))
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Choose a username'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Enter email address'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Create password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Confirm password'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Username already registered. Please login or choose another.')
        return username

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class ProfileSetupForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['department', 'year_of_study', 'grade_type', 'score_value', 'skills', 'target_role', 'custom_target_role', 'current_level']
        widgets = {
            'department': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'year_of_study': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'grade_type': forms.Select(attrs={'class': 'form-select form-select-lg', 'id': 'id_grade_type'}),
            'score_value': forms.NumberInput(attrs={'class': 'form-control form-control-lg', 'step': '0.01', 'placeholder': 'Enter CGPA or % (e.g. 8.5 or 85)'}),
            'skills': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'e.g. Python, SQL, Excel, Accounting, Communication'}),
            'target_role': forms.Select(attrs={'class': 'form-select form-select-lg'}),
            'custom_target_role': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Or type custom target role (e.g. Financial Analyst)'}),
            'current_level': forms.Select(attrs={'class': 'form-select form-select-lg'}),
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['category', 'topic', 'question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_option', 'explanation', 'difficulty', 'is_diagnostic']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'topic': forms.Select(attrs={'class': 'form-select'}),
            'question_text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'option_a': forms.TextInput(attrs={'class': 'form-control'}),
            'option_b': forms.TextInput(attrs={'class': 'form-control'}),
            'option_c': forms.TextInput(attrs={'class': 'form-control'}),
            'option_d': forms.TextInput(attrs={'class': 'form-control'}),
            'correct_option': forms.Select(attrs={'class': 'form-select'}),
            'explanation': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
            'is_diagnostic': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['category', 'target_role', 'title', 'description', 'day_number', 'content']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'target_role': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'day_number': forms.NumberInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 6}),
        }


class MockTestForm(forms.ModelForm):
    class Meta:
        model = MockTest
        fields = ['title', 'description', 'category', 'job_role', 'duration_minutes', 'pass_percentage', 'questions']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'job_role': forms.Select(attrs={'class': 'form-select'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control'}),
            'pass_percentage': forms.NumberInput(attrs={'class': 'form-control'}),
            'questions': forms.SelectMultiple(attrs={'class': 'form-select', 'size': '8'}),
        }


class InterviewQuestionForm(forms.ModelForm):
    class Meta:
        model = InterviewQuestion
        fields = ['category', 'job_role', 'question_type', 'company_tag', 'question', 'answer_guide', 'tips', 'difficulty']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'job_role': forms.Select(attrs={'class': 'form-select'}),
            'question_type': forms.Select(attrs={'class': 'form-select'}),
            'company_tag': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. TCS, Infosys, Zoho'}),
            'question': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'answer_guide': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'tips': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'difficulty': forms.Select(attrs={'class': 'form-select'}),
        }

