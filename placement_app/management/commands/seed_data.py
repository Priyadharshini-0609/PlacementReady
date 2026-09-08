from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from placement_app.models import (
    JobRole, Category, Topic, Task, Question, MockTest, InterviewQuestion, UserProfile
)

class Command(BaseCommand):
    help = 'Seeds complete placement preparation data across all subject categories and academic departments'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Starting database seeding..."))

        # 1. Job Roles across Tech, Commerce, Arts & Science
        roles_data = [
            {
                'name': 'Data Analyst',
                'description': 'Analyzes datasets to extract business insights using SQL, Excel, Python, and visualization tools.',
                'icon_class': 'bi-bar-chart-line-fill',
                'required_skills': 'SQL, Python, Excel, PowerBI, Data Visualization'
            },
            {
                'name': 'Software Engineer',
                'description': 'Designs, develops, and maintains software applications using core programming languages and data structures.',
                'icon_class': 'bi-code-slash',
                'required_skills': 'Python, Java, Data Structures, SQL, Algorithms'
            },
            {
                'name': 'Full Stack Developer',
                'description': 'Builds complete web applications covering both frontend UI and backend services.',
                'icon_class': 'bi-layers-fill',
                'required_skills': 'HTML/CSS, JavaScript, Django/React, REST APIs, SQL'
            },
            {
                'name': 'Financial Analyst & Accountant',
                'description': 'Analyzes financial statements, budgets, accounting records, and financial trends for business decisions.',
                'icon_class': 'bi-cash-coin',
                'required_skills': 'Accounting Principles, Financial Modeling, Tally, Excel, Financial Analysis'
            },
            {
                'name': 'Business Analyst',
                'description': 'Bridges business requirements and technical solutions through data modeling, documentation, and process optimization.',
                'icon_class': 'bi-diagram-3-fill',
                'required_skills': 'Business Analysis, Requirement Gathering, SQL, Excel, Process Mapping'
            },
            {
                'name': 'Digital Marketing & Content Specialist',
                'description': 'Creates marketing campaigns, SEO strategy, content writing, and social media engagement.',
                'icon_class': 'bi-megaphone-fill',
                'required_skills': 'Content Writing, SEO, Digital Marketing, Social Media Analytics, Communication'
            },
            {
                'name': 'HR & Talent Acquisition Specialist',
                'description': 'Manages campus recruitment, employee engagement, HR policies, and behavioral assessment.',
                'icon_class': 'bi-person-badge-fill',
                'required_skills': 'HR Policies, Talent Acquisition, Communication, Conflict Resolution, Interviewing'
            },
            {
                'name': 'Software Quality Assurance (QA) Specialist',
                'description': 'Executes manual and automated test cases to ensure software quality and defect resolution.',
                'icon_class': 'bi-bug-fill',
                'required_skills': 'Software Testing, Test Case Writing, Bug Tracking, Automation Basics, SQL'
            }
        ]

        roles_dict = {}
        for r_info in roles_data:
            role, _ = JobRole.objects.get_or_create(name=r_info['name'], defaults=r_info)
            roles_dict[role.name] = role

        self.stdout.write("Created Job Roles across Tech, Commerce & Arts.")

        # 2. Categories: Aptitude, Logical Reasoning, Verbal, Python, Java, SQL, HR/Communication
        categories_data = [
            {'name': 'Aptitude', 'description': 'Quantitative math, percentages, ratios, and numerical problem solving', 'icon_class': 'bi-calculator'},
            {'name': 'Logical Reasoning', 'description': 'Analytical logic, series, puzzles, and spatial reasoning', 'icon_class': 'bi-puzzle'},
            {'name': 'Verbal', 'description': 'English grammar, reading comprehension, vocabulary, and sentence correction', 'icon_class': 'bi-chat-text'},
            {'name': 'Python', 'description': 'Core Python programming, data structures, and script development', 'icon_class': 'bi-filetype-py'},
            {'name': 'Java', 'description': 'Java syntax, object-oriented programming (OOP), and exception handling', 'icon_class': 'bi-filetype-java'},
            {'name': 'SQL', 'description': 'Database queries, joins, aggregations, and subqueries', 'icon_class': 'bi-table'},
            {'name': 'HR/Communication', 'description': 'HR interview round preparation, soft skills, and behavioral communication', 'icon_class': 'bi-person-badge'}
        ]

        cat_dict = {}
        for c_info in categories_data:
            cat, _ = Category.objects.get_or_create(name=c_info['name'], defaults=c_info)
            cat_dict[cat.name] = cat

        self.stdout.write("Created all 7 Subject Categories.")

        # 3. Comprehensive Question Bank
        questions_list = [
            # Aptitude
            {
                'category': cat_dict['Aptitude'],
                'question_text': 'A train running at 60 km/hr crosses a pole in 9 seconds. What is the length of the train?',
                'option_a': '120 meters', 'option_b': '150 meters', 'option_c': '180 meters', 'option_d': '324 meters',
                'correct_option': 'B',
                'explanation': 'Speed in m/s = 60 * (5/18) = 50/3 m/s. Length = Speed * Time = (50/3) * 9 = 150 meters.',
                'difficulty': 'Easy', 'is_diagnostic': True
            },
            {
                'category': cat_dict['Aptitude'],
                'question_text': 'A sum of money at simple interest doubles itself in 10 years. In how many years will it triple itself?',
                'option_a': '15 years', 'option_b': '20 years', 'option_c': '25 years', 'option_d': '30 years',
                'correct_option': 'B',
                'explanation': 'Interest for 10 years = Principal (P). To triple, interest needed = 2P. Time needed = 10 * 2 = 20 years.',
                'difficulty': 'Medium', 'is_diagnostic': True
            },
            # Logical Reasoning
            {
                'category': cat_dict['Logical Reasoning'],
                'question_text': 'Look at this series: 2, 1, 1/2, 1/4, ... What number should come next?',
                'option_a': '1/3', 'option_b': '1/8', 'option_c': '2/8', 'option_d': '1/16',
                'correct_option': 'B',
                'explanation': 'This is a division series where each number is half of the previous number.',
                'difficulty': 'Easy', 'is_diagnostic': True
            },
            {
                'category': cat_dict['Logical Reasoning'],
                'question_text': 'Suresh is older than Rahul. Ramesh is older than Suresh. Rahul is older than Ramesh. If the first two statements are true, the third statement is:',
                'option_a': 'True', 'option_b': 'False', 'option_c': 'Uncertain', 'option_d': 'None of these',
                'correct_option': 'B',
                'explanation': 'Since Ramesh > Suresh > Rahul, Rahul cannot be older than Ramesh.',
                'difficulty': 'Easy', 'is_diagnostic': True
            },
            # Verbal
            {
                'category': cat_dict['Verbal'],
                'question_text': 'Choose the word that is most nearly OPPOSITE in meaning to "EXPAND":',
                'option_a': 'Convert', 'option_b': 'Condense', 'option_c': 'Congest', 'option_d': 'Conclude',
                'correct_option': 'B',
                'explanation': 'Expand means to grow larger; Condense means to make smaller or more compact.',
                'difficulty': 'Easy', 'is_diagnostic': True
            },
            {
                'category': cat_dict['Verbal'],
                'question_text': 'Identify the correctly spelt word:',
                'option_a': 'Accommodate', 'option_b': 'Acommodate', 'option_c': 'Accomodate', 'option_d': 'Acomodate',
                'correct_option': 'A',
                'explanation': 'The correct spelling is Accommodate (double c and double m).',
                'difficulty': 'Easy', 'is_diagnostic': False
            },
            # Python
            {
                'category': cat_dict['Python'],
                'question_text': 'What is the output of `print(type([1, 2, 3]))` in Python?',
                'option_a': '<class "tuple">', 'option_b': '<class "list">', 'option_c': '<class "array">', 'option_d': '<class "dict">',
                'correct_option': 'B',
                'explanation': 'Square brackets create a list object in Python.',
                'difficulty': 'Easy', 'is_diagnostic': True
            },
            {
                'category': cat_dict['Python'],
                'question_text': 'Which keyword in Python is used to define a function?',
                'option_a': 'func', 'option_b': 'def', 'option_c': 'function', 'option_d': 'define',
                'correct_option': 'B',
                'explanation': 'The `def` keyword is used to declare user-defined functions in Python.',
                'difficulty': 'Easy', 'is_diagnostic': False
            },
            # Java
            {
                'category': cat_dict['Java'],
                'question_text': 'Which of the following is NOT a primitive data type in Java?',
                'option_a': 'int', 'option_b': 'boolean', 'option_c': 'String', 'option_d': 'double',
                'correct_option': 'C',
                'explanation': '`String` in Java is a reference class object, not a primitive data type.',
                'difficulty': 'Easy', 'is_diagnostic': True
            },
            {
                'category': cat_dict['Java'],
                'question_text': 'Which keyword is used by a class to inherit another class in Java?',
                'option_a': 'implements', 'option_b': 'extends', 'option_c': 'inherits', 'option_d': 'super',
                'correct_option': 'B',
                'explanation': 'The `extends` keyword is used for class inheritance in Java.',
                'difficulty': 'Easy', 'is_diagnostic': False
            },
            # SQL
            {
                'category': cat_dict['SQL'],
                'question_text': 'Which SQL clause is used to filter records before grouping occurs?',
                'option_a': 'HAVING', 'option_b': 'WHERE', 'option_c': 'ORDER BY', 'option_d': 'GROUP BY',
                'correct_option': 'B',
                'explanation': '`WHERE` filters individual rows before `GROUP BY` aggregates them.',
                'difficulty': 'Easy', 'is_diagnostic': True
            },
            {
                'category': cat_dict['SQL'],
                'question_text': 'Which JOIN returns all records from the left table and matched records from the right table?',
                'option_a': 'INNER JOIN', 'option_b': 'RIGHT JOIN', 'option_c': 'LEFT JOIN', 'option_d': 'FULL JOIN',
                'correct_option': 'C',
                'explanation': 'LEFT JOIN includes all rows from the left table regardless of right table match.',
                'difficulty': 'Medium', 'is_diagnostic': True
            },
            # HR & Communication
            {
                'category': cat_dict['HR/Communication'],
                'question_text': 'What is the recommended STAR method structure when answering behavioral interview questions?',
                'option_a': 'Situation, Task, Action, Result',
                'option_b': 'Strategy, Thinking, Answer, Reaction',
                'option_c': 'Speech, Talk, Argument, Resolution',
                'option_d': 'Summary, Topic, Assessment, Review',
                'correct_option': 'A',
                'explanation': 'STAR stands for Situation, Task, Action, and Result.',
                'difficulty': 'Easy', 'is_diagnostic': True
            }
        ]

        created_questions = []
        for q_info in questions_list:
            q, _ = Question.objects.get_or_create(question_text=q_info['question_text'], defaults=q_info)
            created_questions.append(q)

        self.stdout.write("Created Questions across all 7 categories.")

        # 4. Mock Tests for EVERY category
        mock_tests_data = [
            ('Quantitative Aptitude Master Test', cat_dict['Aptitude'], 25, 60, 'Practice mathematical problem solving, ratios, percentages, and time & distance.'),
            ('Logical Reasoning Speed Challenge', cat_dict['Logical Reasoning'], 20, 60, 'Evaluate analytical series, pattern completion, and logical deductions.'),
            ('Verbal Ability & Grammar Assessment', cat_dict['Verbal'], 20, 60, 'Test English vocabulary, sentence correction, and reading comprehension.'),
            ('Python Programming Proficiency Test', cat_dict['Python'], 30, 70, 'Core Python syntax, list operations, functions, and data structures.'),
            ('Java Core & OOP Concepts Assessment', cat_dict['Java'], 30, 70, 'Java fundamentals, object-oriented concepts, inheritance, and exception handling.'),
            ('SQL & Database Queries Challenge', cat_dict['SQL'], 25, 70, 'Structured query language, joins, group by aggregation, and subqueries.'),
            ('HR & Soft Skills Interview Simulation', cat_dict['HR/Communication'], 20, 60, 'Behavioral interview questions, communication etiquette, and STAR framework responses.')
        ]

        for m_title, m_cat, m_dur, m_pass, m_desc in mock_tests_data:
            mtest, _ = MockTest.objects.get_or_create(
                title=m_title,
                defaults={
                    'category': m_cat,
                    'duration_minutes': m_dur,
                    'pass_percentage': m_pass,
                    'description': m_desc
                }
            )
            cat_qs = [q for q in created_questions if q.category == m_cat]
            if not cat_qs:
                cat_qs = created_questions[:5]
            mtest.questions.set(cat_qs)

        self.stdout.write("Created Mock Tests for all 7 Categories.")

        # 5. Topics & Tasks (Roadmaps for Data Analyst, Software Engineer, Financial Analyst)
        t1, _ = Topic.objects.get_or_create(
            target_role=roles_dict['Data Analyst'],
            day_number=1,
            title='Day 1: SQL Database Fundamentals',
            defaults={
                'category': cat_dict['SQL'],
                'description': 'Learn SELECT statements, WHERE filtering, and sorting data.',
                'content': '<p>SQL is essential for Data Analysts. Practice SELECT, WHERE, and ORDER BY queries.</p>'
            }
        )
        Task.objects.get_or_create(topic=t1, title='Read SQL Fundamentals Guide', defaults={'task_type': 'Reading', 'estimated_minutes': 15})

        t2, _ = Topic.objects.get_or_create(
            target_role=roles_dict['Financial Analyst & Accountant'],
            day_number=1,
            title='Day 1: Financial Statements & Accounting Basics',
            defaults={
                'category': cat_dict['Aptitude'],
                'description': 'Master Balance Sheets, Profit & Loss Statements, and Excel formulas.',
                'content': '<p>Understand double-entry bookkeeping, ledger entries, and financial ratio analysis.</p>'
            }
        )
        Task.objects.get_or_create(topic=t2, title='Study Financial Statements & Excel Notes', defaults={'task_type': 'Reading', 'estimated_minutes': 20})

        # 6. Interview Questions (without company tags)
        interview_qa = [
            {
                'category': cat_dict['HR/Communication'],
                'question_type': 'HR',
                'question': 'Tell me about yourself and your academic background.',
                'answer_guide': 'Use the Past-Present-Future framework. State your degree, department, projects, and career goal.',
                'tips': 'Keep your response focused and under 2 minutes.'
            },
            {
                'category': cat_dict['HR/Communication'],
                'question_type': 'HR',
                'question': 'What are your key strengths and areas of improvement?',
                'answer_guide': 'State a job-relevant strength with evidence. State a minor weakness and how you are working to overcome it.',
                'tips': 'Show self-awareness and active learning habits.'
            },
            {
                'category': cat_dict['SQL'],
                'question_type': 'SQL',
                'question': 'How do you retrieve the 2nd highest value from a database table column?',
                'answer_guide': 'Use subquery: SELECT MAX(col) FROM Table WHERE col < (SELECT MAX(col) FROM Table);',
                'tips': 'Remember to handle duplicate top values using DISTINCT.'
            },
            {
                'category': cat_dict['Python'],
                'question_type': 'Python',
                'question': 'What is the difference between a List and a Tuple in Python?',
                'answer_guide': 'Lists are mutable (modifiable) defined with []. Tuples are immutable (read-only) defined with ().',
                'tips': 'Mention memory efficiency and immutability advantages of tuples.'
            },
            {
                'category': cat_dict['Java'],
                'question_type': 'Java',
                'question': 'Explain Method Overloading vs Method Overriding in Java.',
                'answer_guide': 'Overloading occurs in the same class with different parameters (compile-time). Overriding occurs in child class replacing parent method (runtime).',
                'tips': 'Highlight polymorphism types.'
            }
        ]

        for i_info in interview_qa:
            InterviewQuestion.objects.get_or_create(question=i_info['question'], defaults=i_info)

        self.stdout.write("Created Interview Q&A Repository.")

        # 7. Create Demo Users (Admin & Student Priya)
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@placementready.com', 'admin123', first_name='System', last_name='Admin')
            self.stdout.write(self.style.SUCCESS("Superuser created: username='admin', password='admin123'"))

        if not User.objects.filter(username='priya').exists():
            priya_user = User.objects.create_user('priya', 'priya@college.edu', 'priya123', first_name='Priya', last_name='Sharma')
            UserProfile.objects.create(
                user=priya_user,
                department='B.Sc Computer Science',
                year_of_study='Final Year',
                grade_type='CGPA',
                score_value=8.5,
                skills='SQL, Python, Excel, Communication',
                target_role=roles_dict['Data Analyst'],
                current_level='Intermediate',
                streak_count=3,
                profile_setup_completed=True,
                assessment_completed=True
            )
            self.stdout.write(self.style.SUCCESS("Demo Student created: username='priya', password='priya123'"))

        self.stdout.write(self.style.SUCCESS("\nDatabase Seeding Completed Successfully! PlacementReady is updated."))
