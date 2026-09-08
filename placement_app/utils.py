from placement_app.models import Category, TestResult, UserTaskProgress, Topic, Task, JobRole

def calculate_readiness_score(user):
    """
    Calculates overall placement readiness score across Aptitude, Reasoning, Verbal, Python, Java, SQL, and HR/Communication.
    """
    categories = Category.objects.all()
    cat_scores = {cat.name: 0.0 for cat in categories}
    cat_counts = {cat.name: 0 for cat in categories}
    
    # Core 7 categories
    core_cats = ['Aptitude', 'Logical Reasoning', 'Verbal', 'Python', 'Java', 'SQL', 'HR/Communication']
    for c in core_cats:
        if c not in cat_scores:
            cat_scores[c] = 0.0
            cat_counts[c] = 0

    results = TestResult.objects.filter(user=user)
    
    for r in results:
        if r.category_scores:
            for cat_name, score in r.category_scores.items():
                if cat_name in cat_scores:
                    cat_scores[cat_name] += float(score)
                    cat_counts[cat_name] += 1

    final_cat_scores = {}
    for cat_name in core_cats:
        total_score = cat_scores.get(cat_name, 0.0)
        count = cat_counts.get(cat_name, 0)
        if count > 0:
            final_cat_scores[cat_name] = round(total_score / count, 1)
        else:
            if hasattr(user, 'profile') and user.profile.assessment_completed:
                final_cat_scores[cat_name] = 50.0
            else:
                final_cat_scores[cat_name] = 0.0

    # Roadmap completion calculation
    target_role = getattr(user.profile, 'target_role', None) if hasattr(user, 'profile') else None
    if target_role:
        topics = Topic.objects.filter(target_role=target_role)
    else:
        topics = Topic.objects.all()
        
    total_tasks = Task.objects.filter(topic__in=topics).count()
    if total_tasks > 0:
        completed_tasks = UserTaskProgress.objects.filter(user=user, completed=True, task__topic__in=topics).count()
        roadmap_progress = round((completed_tasks / total_tasks) * 100, 1)
    else:
        completed_tasks = 0
        roadmap_progress = 0.0

    # Overall Readiness Score Calculation
    tested_cats = [v for k, v in final_cat_scores.items() if cat_counts.get(k, 0) > 0]
    if tested_cats:
        avg_test_score = sum(tested_cats) / len(tested_cats)
        overall_score = round((avg_test_score * 0.75) + (roadmap_progress * 0.25), 1)
    else:
        overall_score = round(roadmap_progress * 0.5, 1)

    overall_score = min(100.0, overall_score)

    strong_skills = [cat for cat, score in final_cat_scores.items() if score >= 70]
    weak_skills = [cat for cat, score in final_cat_scores.items() if score > 0 and score < 70]
    untested_skills = [cat for cat, score in final_cat_scores.items() if score == 0]

    recommendations = []
    if not hasattr(user, 'profile') or not user.profile.assessment_completed:
        recommendations.append({
            'type': 'warning',
            'title': 'Take Diagnostic Skill Assessment',
            'message': 'Complete your diagnostic skill assessment test to unlock your personalized placement analytics.'
        })
    
    if weak_skills:
        weak_str = " & ".join(weak_skills[:2])
        recommendations.append({
            'type': 'danger',
            'title': f'Focus Priority: {weak_str}',
            'message': f'Your performance in {weak_str} is currently below 70%. Practice daily tasks and mock tests in these areas.'
        })

    if strong_skills:
        strong_str = ", ".join(strong_skills[:2])
        recommendations.append({
            'type': 'success',
            'title': f'Strong Performance in {strong_str}',
            'message': f'Great job! Maintain your performance in {strong_str} by taking advanced mock tests.'
        })

    return {
        'overall_score': int(overall_score),
        'category_scores': final_cat_scores,
        'strong_skills': strong_skills,
        'weak_skills': weak_skills,
        'untested_skills': untested_skills,
        'roadmap_progress': int(roadmap_progress),
        'completed_tasks': completed_tasks,
        'total_tasks': total_tasks,
        'recommendations': recommendations
    }
