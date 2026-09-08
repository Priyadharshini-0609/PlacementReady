"""
Management command: seed_interview_tips
Seeds detailed, structured English interview preparation guides covering:
1. Dress Code & Appearance (Attire)
2. Communication Skills & Body Language (Communication)
3. Before the Interview Checklist (PreInterview)
4. After the Interview Etiquette (PostInterview)
5. Standard HR & Behavioral Round Questions (HR)

Usage:
    python manage.py seed_interview_tips
"""

from django.core.management.base import BaseCommand
from placement_app.models import Category, InterviewQuestion, JobRole


class Command(BaseCommand):
    help = 'Seeds non-technical interview preparation guides (Dress Code, Communication, Pre/Post Interview Etiquette)'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Seeding interview preparation guides and tips...'))

        hr_cat, _ = Category.objects.get_or_create(
            name='HR/Communication',
            defaults={'description': 'HR interview round, soft skills, and etiquette', 'icon_class': 'bi-person-badge'}
        )

        tips_data = [
            # 👔 DRESS CODE & APPEARANCE (Attire)
            {
                'category': hr_cat,
                'question_type': 'Attire',
                'question': 'How should I dress for a campus placement interview? (Dress Code Guidelines)',
                'answer_guide': (
                    "First impressions matter greatly in placement interviews. Adhere to strict professional formal attire:\n\n"
                    "👔 FOR MALE CANDIDATES:\n"
                    "• Shirt: Full-sleeved, neatly pressed formal shirt in light colors (White, Light Blue, Soft Grey).\n"
                    "• Trousers: Dark formal trousers (Black, Navy Blue, Dark Grey) with a matching dark leather belt.\n"
                    "• Footwear: Clean, polished dark leather formal shoes with dark-colored socks.\n"
                    "• Grooming: Clean-shaven or neatly trimmed beard; neat hairstyle; avoid flashy watches or jewelry.\n\n"
                    "👗 FOR FEMALE CANDIDATES:\n"
                    "• Attire: Neat, well-ironed formal Saree, Salwar-Kameez (with dupatta pinned neatly), or formal Blouse with tailored Trousers/Skirt.\n"
                    "• Colors: Subtle, professional colors (Pastels, White, Navy Blue, Grey, Beige).\n"
                    "• Footwear: Closed-toe formal shoes or neat flat formal sandals; clean and comfortable.\n"
                    "• Grooming: Minimal, natural makeup; neat hairstyle tied back; subtle jewelry (small earrings, plain watch).\n\n"
                    "💡 GENERAL GOLDEN RULE: Dress one level more formal than the company's daily dress code. Ensure clothes fit comfortably so you feel confident."
                ),
                'tips': 'Iron your clothes and polish your shoes the night before. Avoid heavy perfumes or strong deodorants.',
                'company_tag': 'All Companies',
                'difficulty': 'Easy'
            },

            # 🗣️ COMMUNICATION SKILLS & BODY LANGUAGE (Communication)
            {
                'category': hr_cat,
                'question_type': 'Communication',
                'question': 'How should I communicate effectively during the interview?',
                'answer_guide': (
                    "Effective communication is not just about fluency in English—it is about clarity, confidence, active listening, and body language:\n\n"
                    "1. CLEAR & PACED SPEECH:\n"
                    "   • Speak at a moderate, steady pace in clear, professional English.\n"
                    "   • Pause briefly before answering to structure your thoughts instead of rushing.\n"
                    "   • Avoid slang, informal contractions ('gonna', 'wanna'), and filler words ('um', 'like', 'you know').\n\n"
                    "2. POSITIVE BODY LANGUAGE:\n"
                    "   • Sit upright with a relaxed, confident posture. Do not slouch or lean heavily on the table.\n"
                    "   • Maintain steady, natural eye contact with all interviewers on the panel.\n"
                    "   • Keep a warm, pleasant facial expression and smile naturally.\n"
                    "   • Rest your hands gently on your lap or table; avoid nervous fidgeting with pens or hair.\n\n"
                    "3. ACTIVE LISTENING:\n"
                    "   • Listen completely to the interviewer's question without interrupting.\n"
                    "   • If a question is unclear, politely ask: 'Could you please clarify what you mean by X?'"
                ),
                'tips': 'Use the STAR Method (Situation, Task, Action, Result) when describing past experiences or projects.',
                'company_tag': 'All Companies',
                'difficulty': 'Easy'
            },

            # 📋 BEFORE THE INTERVIEW CHECKLIST (PreInterview)
            {
                'category': hr_cat,
                'question_type': 'PreInterview',
                'question': 'What should I do BEFORE attending an interview? (Pre-Interview Preparation)',
                'answer_guide': (
                    "Thorough preparation before the interview day significantly reduces anxiety and boosts confidence:\n\n"
                    "1. COMPANY RESEARCH:\n"
                    "   • Research the company's core business, services, products, mission statement, and recent news.\n"
                    "   • Understand their industry domain, major competitors, and work culture.\n\n"
                    "2. DOCUMENTATION & PORTFOLIO:\n"
                    "   • Carry 3–4 clean copies of your updated Resume/CV printed on quality paper.\n"
                    "   • Arrange all original mark sheets, degree certificates, and project reports in a clean document folder.\n"
                    "   • Keep passport-size photographs and college ID card ready.\n\n"
                    "3. RESUME MASTERY:\n"
                    "   • Be prepared to explain every single line, skill, project, and certification listed on your resume.\n\n"
                    "4. LOGISTICS & TIME MANAGEMENT:\n"
                    "   • Identify the interview location or test your internet/webcam for virtual interviews.\n"
                    "   • Plan your travel so you arrive at the venue 20 to 30 minutes early.\n\n"
                    "5. SELF-CARE:\n"
                    "   • Get 7–8 hours of restful sleep the night before and eat a light, healthy meal."
                ),
                'tips': 'Check your interview venue or video call link at least 1 hour before scheduled time.',
                'company_tag': 'All Companies',
                'difficulty': 'Easy'
            },

            # 🤝 AFTER THE INTERVIEW ETIQUETTE (PostInterview)
            {
                'category': hr_cat,
                'question_type': 'PostInterview',
                'question': 'What should I do AFTER the interview finishes? (Post-Interview Etiquette)',
                'answer_guide': (
                    "Closing an interview gracefully leaves a strong, lasting positive impression:\n\n"
                    "1. ASKING INSIGHTFUL QUESTIONS:\n"
                    "   • When the interviewer asks 'Do you have any questions for us?', ALWAYS ask 1 or 2 thoughtful questions.\n"
                    "   • Good Example Questions:\n"
                    "     - 'What does a typical day look like for a fresher joining this team?'\n"
                    "     - 'What training or learning opportunities are provided for new hires?'\n"
                    "     - 'What are the upcoming priorities for the team over the next 6 months?'\n\n"
                    "2. POLITE CLOSING & THANK YOU:\n"
                    "   • Stand up neatly, smile warmly, and thank the panel for their time and opportunity.\n"
                    "   • Offer a firm handshake (if in-person and appropriate) or a polite nod/greeting.\n\n"
                    "3. FOLLOW-UP THANK-YOU EMAIL:\n"
                    "   • Send a brief, courteous Thank-You email to HR or the recruiter within 24 hours.\n"
                    "   • Express appreciation for their time and reiterate your genuine interest in the role.\n\n"
                    "4. SELF-REFLECTION:\n"
                    "   • Write down questions you struggled with so you can practice and improve for your next round."
                ),
                'tips': 'Never ask about salary or leave policies in the very first technical round unless raised by the interviewer.',
                'company_tag': 'All Companies',
                'difficulty': 'Easy'
            },

            # 💼 STANDARD HR QUESTIONS
            {
                'category': hr_cat,
                'question_type': 'HR',
                'question': 'Tell me about yourself (Self Introduction Guide)',
                'answer_guide': (
                    "Use the 90-Second Past-Present-Future structure:\n\n"
                    "1. GREETING & ACADEMIC BACKGROUND (Past):\n"
                    "   'Good morning/afternoon sir/madam. Thank you for this opportunity. My name is [Name], currently pursuing [Degree, e.g. B.Com / B.Sc / BCA] at [College Name] with a CGPA of [Score].'\n\n"
                    "2. KEY SKILLS & PROJECTS (Present):\n"
                    "   'During my academic journey, I have developed strong skills in [mention 2-3 key skills, e.g. Financial Accounting, Data Analysis, Communication, Python]. For my final project, I worked on [brief 1-line project summary].'\n\n"
                    "3. CAREER OBJECTIVE & FIT (Future):\n"
                    "   'I am eager to start my career with a forward-looking company like [Company Name] where I can apply my domain knowledge, learn continuously, and contribute value to the team.'"
                ),
                'tips': 'Practice speaking your introduction in front of a mirror or friend. Keep it smooth and natural within 90 seconds.',
                'company_tag': 'All Companies',
                'difficulty': 'Easy'
            },

            {
                'category': hr_cat,
                'question_type': 'HR',
                'question': 'What are your strengths and weaknesses?',
                'answer_guide': (
                    "STRUCTURE YOUR RESPONSE WITH PROOF:\n\n"
                    "💪 STRENGTHS:\n"
                    "• Pick 1 or 2 job-relevant strengths (e.g. Quick Learner, Attention to Detail, Problem-Solving, Team Collaboration).\n"
                    "• Provide a brief real example: 'My key strength is adaptability. During our college fest, I managed registrations under tight deadlines and coordinated smoothly with 5 team members.'\n\n"
                    "🌱 WEAKNESS (Turn into positive growth):\n"
                    "• Share a minor, non-critical weakness and explain what action you are taking to overcome it.\n"
                    "• Example: 'Earlier, I used to get hesitant speaking in front of large crowds. To improve this, I actively volunteered for class seminar presentations and joined the college debate club, which helped build my confidence.'"
                ),
                'tips': 'Never say "I have no weaknesses" or "I am a perfectionist". Show genuine self-awareness and active self-improvement.',
                'company_tag': 'All Companies',
                'difficulty': 'Medium'
            },

            {
                'category': hr_cat,
                'question_type': 'HR',
                'question': 'Where do you see yourself in 3 to 5 years?',
                'answer_guide': (
                    "Focus on professional growth, skill mastery, and value addition:\n\n"
                    "Sample Answer:\n"
                    "'In 3 to 5 years, I see myself as a highly skilled and dependable professional in [domain name, e.g. Financial Analysis / Software Development / Operations]. I plan to continuously update my domain expertise, gain industry certifications, and take on greater responsibility such as leading projects or mentoring junior team members within the organization.'"
                ),
                'tips': 'Demonstrate commitment to staying with the company and growing within the role.',
                'company_tag': 'All Companies',
                'difficulty': 'Medium'
            },

            {
                'category': hr_cat,
                'question_type': 'HR',
                'question': 'Why do you want to join our company?',
                'answer_guide': (
                    "Demonstrate company research and personal alignment:\n\n"
                    "Sample Answer:\n"
                    "'I have been following [Company Name]\'s achievements in [mention specific field/news, e.g. innovative financial services / cloud solutions]. I am deeply impressed by your work culture and commitment to employee growth. Joining your organization aligns with my career goal to work in a dynamic environment where I can apply my skills and build a long-term career.'"
                ),
                'tips': 'Mention 1 or 2 specific positive facts about the company (e.g. awards, work culture, recent projects).',
                'company_tag': 'All Companies',
                'difficulty': 'Easy'
            }
        ]

        count = 0
        for data in tips_data:
            q, created = InterviewQuestion.objects.get_or_create(
                question=data['question'],
                defaults=data
            )
            if not created:
                q.answer_guide = data['answer_guide']
                q.tips = data['tips']
                q.question_type = data['question_type']
                q.company_tag = data['company_tag']
                q.save()
            count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {count} interview preparation guides and tips!'))
