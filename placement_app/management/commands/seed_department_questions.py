from django.core.management.base import BaseCommand
from placement_app.models import Category, Question

class Command(BaseCommand):
    help = 'Seeds department-specific diagnostic questions for Commerce, Science, Arts, and Computer/IT'

    def get_or_create_category(self, name, description, icon_class='bi-folder-fill'):
        cat, _ = Category.objects.get_or_create(
            name=name,
            defaults={'description': description, 'icon_class': icon_class}
        )
        return cat

    def seed_question(self, category, question_text, option_a, option_b, option_c, option_d,
                      correct_option, explanation, difficulty, department_group, is_diagnostic=True):
        q, created = Question.objects.get_or_create(
            question_text=question_text,
            defaults={
                'category': category,
                'option_a': option_a, 'option_b': option_b,
                'option_c': option_c, 'option_d': option_d,
                'correct_option': correct_option,
                'explanation': explanation,
                'difficulty': difficulty,
                'is_diagnostic': is_diagnostic,
                'department_group': department_group,
            }
        )
        if not created:
            q.department_group = department_group
            q.is_diagnostic = is_diagnostic
            q.save()
        return created

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Seeding department-specific diagnostic questions...'))

        # Tag existing CS questions correctly
        cs_fragments = [
            'type([1, 2, 3])', 'def', 'Java', 'extends',
            'SQL', 'JOIN', 'DISTINCT', 'DBMS', 'ACID'
        ]
        for frag in cs_fragments:
            Question.objects.filter(question_text__icontains=frag).update(department_group='Computer/IT', is_diagnostic=True)

        apt_cat    = self.get_or_create_category('Aptitude', 'Quantitative math, percentages, ratios', 'bi-calculator')
        verbal_cat = self.get_or_create_category('Verbal', 'English grammar, vocabulary, reading', 'bi-chat-text')
        lr_cat     = self.get_or_create_category('Logical Reasoning', 'Series, puzzles, and analytical logic', 'bi-puzzle')
        hr_cat     = self.get_or_create_category('HR/Communication', 'HR interview and soft skills', 'bi-person-badge')

        acc_cat    = self.get_or_create_category('Accounting & Finance', 'Accounting principles, financial statements, tally', 'bi-cash-stack')
        biz_cat    = self.get_or_create_category('Business & Management', 'Business concepts, marketing, operations', 'bi-briefcase')

        sci_cat    = self.get_or_create_category('General Science', 'Physics, chemistry, biology fundamentals', 'bi-flask')
        stat_cat   = self.get_or_create_category('Statistics & Math', 'Probability, statistics, mathematical reasoning', 'bi-graph-up')

        english_cat = self.get_or_create_category('English & Communication', 'Grammar, writing, comprehension', 'bi-pen')
        gk_cat      = self.get_or_create_category('General Knowledge', 'Current affairs, history, geography', 'bi-globe')

        commerce_questions = [
            (acc_cat, 'What is the fundamental accounting equation?',
             'Assets = Liabilities + Owner\'s Equity', 'Assets = Liabilities - Owner\'s Equity',
             'Liabilities = Assets + Owner\'s Equity', 'Owner\'s Equity = Assets + Liabilities',
             'A', 'The fundamental accounting equation is Assets = Liabilities + Owner\'s Equity.', 'Easy', 'Commerce'),

            (acc_cat, 'Which financial statement shows a company\'s revenues and expenses over a period?',
             'Balance Sheet', 'Income Statement (P&L)', 'Cash Flow Statement', 'Trial Balance',
             'B', 'The Income Statement (P&L Account) shows revenues, expenses, and net profit/loss over a period.', 'Easy', 'Commerce'),

            (acc_cat, 'What does GST stand for in taxation?',
             'General Sales Tax', 'Goods and Services Tax', 'Government Service Tax', 'Gross Sales Tax',
             'B', 'GST stands for Goods and Services Tax.', 'Easy', 'Commerce'),

            (acc_cat, 'Which type of account is a Bank Account?',
             'Personal Account', 'Real Account', 'Nominal Account', 'Representative Account',
             'A', 'A Bank Account is a Personal Account.', 'Easy', 'Commerce'),

            (acc_cat, 'In double-entry bookkeeping, when cash is received into business, which entry is made?',
             'Debit Cash Account', 'Credit Cash Account', 'Debit Capital Account', 'Credit Revenue Account',
             'A', 'Cash Account is debited when cash is received.', 'Easy', 'Commerce'),

            (acc_cat, 'What is Working Capital?',
             'Total Assets - Total Liabilities', 'Fixed Assets - Current Liabilities',
             'Current Assets - Current Liabilities', 'Total Revenue - Total Expenses',
             'C', 'Working Capital = Current Assets - Current Liabilities.', 'Easy', 'Commerce'),

            (biz_cat, 'What does ROI stand for in financial management?',
             'Return on Investment', 'Rate of Interest', 'Return on Income', 'Revenue on Investment',
             'A', 'ROI stands for Return on Investment.', 'Easy', 'Commerce'),

            (biz_cat, 'What does SWOT Analysis stand for in business strategy?',
             'Strengths, Weaknesses, Opportunities, Threats', 'Strategy, Work, Operations, Targets',
             'Sales, Workforce, Output, Targets', 'Strengths, Workload, Opportunities, Trends',
             'A', 'SWOT stands for Strengths, Weaknesses, Opportunities, and Threats.', 'Easy', 'Commerce'),

            (biz_cat, 'Which marketing concept focuses primarily on satisfying customer needs profitably?',
             'Production Concept', 'Selling Concept', 'Marketing Concept', 'Product Concept',
             'C', 'The Marketing Concept focuses on customer needs.', 'Easy', 'Commerce'),

            (apt_cat, 'A trader buys an article for ₹500 and sells it for ₹625. What is the profit percentage?',
             '20%', '25%', '15%', '30%',
             'B', 'Profit = ₹125. Profit % = (125/500)*100 = 25%.', 'Easy', 'Commerce'),

            (apt_cat, 'Simple interest on ₹2000 at 5% per annum for 3 years is:',
             '₹300', '₹200', '₹350', '₹250',
             'A', 'SI = (P*R*T)/100 = (2000*5*3)/100 = ₹300.', 'Easy', 'Commerce'),

            (hr_cat, 'When answering "Tell me about yourself" in a job interview, what is the best structure?',
             'Describe personal life and family background', 'Use Past-Present-Future: Degree background, key skills, career goal',
             'Read directly from resume', 'List your weaknesses first',
             'B', 'Past-Present-Future is the recommended professional structure.', 'Easy', 'Commerce'),

            (lr_cat, 'Suresh is older than Rahul. Ramesh is older than Suresh. Rahul is older than Ramesh. If first 2 statements are true, the 3rd is:',
             'True', 'False', 'Uncertain', 'None of these',
             'B', 'Ramesh > Suresh > Rahul, so Rahul cannot be older than Ramesh.', 'Easy', 'Commerce'),

            (verbal_cat, 'Choose the word OPPOSITE in meaning to "EXPAND":',
             'Convert', 'Condense', 'Congest', 'Conclude',
             'B', 'Opposite of Expand is Condense.', 'Easy', 'Commerce'),
        ]

        science_questions = [
            (sci_cat, 'What is the SI unit of force?',
             'Joule', 'Newton', 'Pascal', 'Watt',
             'B', 'The SI unit of force is Newton (N).', 'Easy', 'Science'),

            (sci_cat, 'Which gas is most abundant in the Earth\'s atmosphere?',
             'Oxygen', 'Carbon Dioxide', 'Nitrogen', 'Argon',
             'C', 'Nitrogen makes up approx 78% of Earth\'s atmosphere.', 'Easy', 'Science'),

            (sci_cat, 'What is the pH of pure water at 25°C?',
             '5', '6', '7', '8',
             'C', 'Pure water is neutral with pH 7.', 'Easy', 'Science'),

            (sci_cat, 'Which organelle is known as the powerhouse of the cell?',
             'Nucleus', 'Ribosome', 'Mitochondria', 'Golgi Apparatus',
             'C', 'Mitochondria generate cellular ATP.', 'Easy', 'Science'),

            (stat_cat, 'What is the median of the dataset: 3, 7, 2, 9, 5?',
             '5', '7', '3', '9',
             'A', 'Sorted dataset: 2, 3, 5, 7, 9. Median is 5.', 'Easy', 'Science'),

            (stat_cat, 'Standard deviation measures:',
             'The central value of dataset', 'The dispersion or spread of data from the mean',
             'The most frequent value', 'The maximum value',
             'B', 'Standard deviation measures data dispersion.', 'Easy', 'Science'),

            (apt_cat, 'A car travels 120 km in 2 hours. What is its speed?',
             '40 km/hr', '50 km/hr', '60 km/hr', '80 km/hr',
             'C', 'Speed = 120/2 = 60 km/hr.', 'Easy', 'Science'),

            (lr_cat, 'Find the next number in the series: 1, 4, 9, 16, 25, ?',
             '30', '36', '49', '32',
             'B', 'Series of perfect squares: 6^2 = 36.', 'Easy', 'Science'),

            (verbal_cat, 'Which type of sentence best states a scientific hypothesis?',
             'Higher temperatures will increase the rate of plant growth', 'Plants grow sometimes when hot',
             'Temperature maybe affects plants', 'Plant growth is good',
             'A', 'A hypothesis should be clear and testable.', 'Easy', 'Science'),
        ]

        arts_questions = [
            (english_cat, 'Identify the figure of speech in: "The wind whispered through the trees."',
             'Simile', 'Metaphor', 'Personification', 'Hyperbole',
             'C', 'Giving human qualities to non-human objects is personification.', 'Easy', 'Arts'),

            (english_cat, 'What is the plural form of "analysis"?',
             'Analysises', 'Analysies', 'Analyses', 'Analyzes',
             'C', 'Plural of analysis is analyses.', 'Easy', 'Arts'),

            (english_cat, 'A "lede" in news writing refers to:',
             'The final paragraph', 'The opening sentence summarizing key facts',
             'The headline', 'The author name',
             'B', 'The lede is the introductory lead paragraph in journalism.', 'Easy', 'Arts'),

            (gk_cat, 'Who is known as the Father of the Indian Constitution?',
             'Mahatma Gandhi', 'Jawaharlal Nehru', 'Dr. B.R. Ambedkar', 'Sardar Patel',
             'C', 'Dr. B.R. Ambedkar chaired the drafting committee.', 'Easy', 'Arts'),

            (gk_cat, 'What does GDP stand for in economics?',
             'Gross Development Product', 'Gross Domestic Product',
             'General Domestic Produce', 'Global Development Plan',
             'B', 'GDP stands for Gross Domestic Product.', 'Easy', 'Arts'),

            (apt_cat, 'If 15 workers complete a job in 8 days, how many days will 24 workers take?',
             '3 days', '4 days', '5 days', '6 days',
             'C', 'Work = 15*8 = 120 worker-days. Days = 120/24 = 5 days.', 'Easy', 'Arts'),

            (lr_cat, 'Complete the analogy: Book : Library :: Painting : ?',
             'Artist', 'Museum', 'Gallery', 'Canvas',
             'C', 'Books are in a library, paintings in a gallery.', 'Easy', 'Arts'),
        ]

        for q_list in [commerce_questions, science_questions, arts_questions]:
            for cat, text, a, b, c, d, correct, explanation, diff, grp in q_list:
                self.seed_question(cat, text, a, b, c, d, correct, explanation, diff, grp)

        self.stdout.write(self.style.SUCCESS('Successfully seeded department questions!'))
