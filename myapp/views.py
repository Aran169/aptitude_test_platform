from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import (
    Student,
    LogicalQuestion,
    NumericalQuestion,
    VerbalQuestion,
    SpatialQuestion,
    NumericalQuestion1,
    ReasoningQuestion,
    Feedback
)
import random

TOTAL_ASSESSMENT_TIME = timedelta(minutes=20)
SECTIONS = [
    'logical',
    'numerical',
    'verbal',
    'spatial',
    'numerical1',
    'reasoning',
]
SECTION_TITLES = {
    'logical': {'title': 'Section 1: Logical Reasoning', 'description': 'Questions to test analytical thinking and problem-solving abilities.'},
    'numerical': {'title': 'Section 2: Numerical Ability-1', 'description': 'Questions to test mathematical skills and number sense.'},
    'verbal': {'title': 'Section 3: Verbal Reasoning', 'description': 'Questions to test language skills and verbal comprehension.'},
    'spatial': {'title': 'Section 4: Data Interpretation', 'description': 'Questions to test visualization skills and spatial reasoning.'},
    'numerical1': {'title': 'Section 5: Numerical Ability-2', 'description': 'Questions to test recall and retention abilities.'},
    'reasoning': {'title': 'Section 6: Reasoning Ability', 'description': 'Activities to encourage imaginative thinking and creative expression.'},
}
QUESTIONS_PER_SECTION = 5

def home(request):
    return render(request, 'home.html')

def student_details(request):
    if request.method == "POST":
        full_name = request.POST.get("fullName")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        grade = request.POST.get("grade")
        parent_name = request.POST.get("parentName")
        contact_email = request.POST.get("contactEmail")

        if not all([full_name, age, gender, grade, parent_name, contact_email]):
            print("Missing form fields!")
            return render(request, "student_details.html", {'error': 'All fields are required.'})

        student = Student(
            full_name=full_name,
            age=age,
            gender=gender,
            grade=grade,
            parent_name=parent_name,
            contact_email=contact_email,
        )
        student.save()
        print(f"Student {student.full_name} saved successfully!")

        request.session["student_id"] = student.id
        request.session["assessment_start_time"] = timezone.now().isoformat()
        request.session["current_section_index"] = 0
        return redirect("exam_pattern")
    return render(request, "student_details.html")

def exam_pattern(request):
    return render(request, 'exam_pattern.html')

def instructions(request):
    return render(request, 'instructions.html')

def camera_access(request):
    return render(request, 'camera_access.html')

def start_test(request):
    request.session["assessment_start_time"] = timezone.now().isoformat()
    request.session["current_section_index"] = 0
    return redirect("exam_section", section_name=SECTIONS[0])

def exam_section(request, section_name):
    student_id = request.session.get("student_id")
    if not student_id:
        return redirect("student_details")

    start_time_str = request.session.get("assessment_start_time")
    if not start_time_str:
        return redirect("start_test")
    start_time = timezone.datetime.fromisoformat(start_time_str)
    time_elapsed = timezone.now() - start_time
    time_remaining = TOTAL_ASSESSMENT_TIME - time_elapsed
    time_remaining_seconds = int(time_remaining.total_seconds())

    if time_remaining.total_seconds() <= 0:
        return redirect("feedback")

    current_section_index = request.session.get("current_section_index", 0)
    if SECTIONS[current_section_index] != section_name:
        return redirect("exam_section", section_name=SECTIONS[current_section_index])

    if request.method == 'POST':
        form_data = request.POST.copy()
        form_data.pop('csrfmiddlewaretoken', None)
        if 'next_section' in form_data or 'previous_section' in form_data:
            request.session[f'answers_{section_name}'] = dict(form_data)
            if 'next_section' in request.POST:
                if current_section_index < len(SECTIONS) - 1:
                    request.session["current_section_index"] = current_section_index + 1
                    return redirect("exam_section", section_name=SECTIONS[request.session["current_section_index"]])
                else:
                    return redirect("feedback")
            elif 'previous_section' in request.POST:
                if current_section_index > 0:
                    request.session["current_section_index"] = current_section_index - 1
                    return redirect("exam_section", section_name=SECTIONS[request.session["current_section_index"]])
                else:
                    return redirect("exam_section", section_name=SECTIONS[0])

    questions = []
    if section_name == 'logical':
        all_questions = list(LogicalQuestion.objects.all())
        questions = random.sample(all_questions, min(QUESTIONS_PER_SECTION, len(all_questions)))
    elif section_name == 'numerical':
        all_questions = list(NumericalQuestion.objects.all())
        questions = random.sample(all_questions, min(QUESTIONS_PER_SECTION, len(all_questions)))
    elif section_name == 'verbal':
        all_questions = list(VerbalQuestion.objects.all())
        questions = random.sample(all_questions, min(QUESTIONS_PER_SECTION, len(all_questions)))
    elif section_name == 'spatial':
        all_questions = list(SpatialQuestion.objects.all())
        questions = random.sample(all_questions, min(QUESTIONS_PER_SECTION, len(all_questions)))
    elif section_name == 'numerical1':
        all_questions = list(NumericalQuestion1.objects.all())
        questions = random.sample(all_questions, min(QUESTIONS_PER_SECTION, len(all_questions)))
    elif section_name == 'reasoning':
        all_questions = list(ReasoningQuestion.objects.all())
        questions = random.sample(all_questions, min(QUESTIONS_PER_SECTION, len(all_questions)))

    submitted_answers = request.session.get(f'answers_{section_name}', {})

    context = {
        "section_name": section_name,
        "section_title": SECTION_TITLES[section_name]['title'],
        "section_description": SECTION_TITLES[section_name]['description'],
        "time_remaining": time_remaining,
        "total_sections": len(SECTIONS),
        "current_section_number": current_section_index + 1,
        "questions": questions,
        "submitted_answers": submitted_answers,
        "time_remaining_seconds": time_remaining_seconds, 
        "total_assessment_time_seconds": int(TOTAL_ASSESSMENT_TIME.total_seconds()),
    }
    return render(request, "exam.html", context)

def submit_assessment(request):
    if request.method == 'POST':
        student_id = request.session.get('student_id')
        if not student_id:
            return redirect('home')

        try:
            student = Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            return redirect('home')

        scores = {}
        total_questions = {}

        all_answers = {}
        for section in SECTIONS:
            answers = request.session.get(f'answers_{section}', {})
            for key, value in answers.items():
                if key.endswith(f'_{section.lower()}'):
                    question_id = key.split('_')[-2]
                    all_answers[f'{section}_question_{question_id}'] = value[0] if isinstance(value, list) else value # Handle both list and single value
                else:
                    all_answers[key] = value[0] if isinstance(value, list) else value

        all_answers.update(request.POST.dict())
        for key, value in request.POST.items():
            if not key in all_answers:
                all_answers[key] = value

        # Logical Questions
        logical_score = 0
        logical_questions = LogicalQuestion.objects.all()
        total_questions['logical'] = len(logical_questions)
        for question in logical_questions:
            submitted_answer = all_answers.get(f'logical_question_{question.id}')
            if submitted_answer and submitted_answer == question.correct_answer:
                logical_score += 1
        scores['logical'] = logical_score
        print(f"Logical Score: {logical_score}, Total Logical Questions: {len(logical_questions)}")

        # Numerical Questions
        numerical_score = 0
        numerical_questions = NumericalQuestion.objects.all()
        total_questions['numerical'] = len(numerical_questions)
        for question in numerical_questions:
            submitted_answer = all_answers.get(f'numerical_question_{question.id}')
            if submitted_answer and submitted_answer == question.correct_answer:
                numerical_score += 1
        scores['numerical'] = numerical_score
        print(f"Numerical Score: {numerical_score}, Total Numerical Questions: {len(numerical_questions)}")

        # Numerical Questions 1
        numerical1_score = 0
        numerical1_questions = NumericalQuestion1.objects.all()
        total_questions['numerical1'] = len(numerical1_questions)
        for question in numerical1_questions:
            submitted_answer = all_answers.get(f'numerical1_question_{question.id}')
            if submitted_answer and submitted_answer == question.correct_answer:
                numerical1_score += 1
        scores['numerical1'] = numerical1_score
        print(f"Numerical1 Score: {numerical1_score}, Total Numerical1 Questions: {len(numerical1_questions)}")

        # Verbal Questions
        verbal_score = 0
        verbal_questions = VerbalQuestion.objects.all()
        total_questions['verbal'] = len(verbal_questions)
        for question in verbal_questions:
            submitted_answer = all_answers.get(f'verbal_question_{question.id}')
            if submitted_answer and submitted_answer == question.correct_answer:
                verbal_score += 1
        scores['verbal'] = verbal_score
        print(f"Verbal Score: {verbal_score}, Total Verbal Questions: {len(verbal_questions)}")

        # Spatial Questions
        spatial_score = 0
        spatial_questions = SpatialQuestion.objects.all()
        total_questions['spatial'] = len(spatial_questions)
        for question in spatial_questions:
            submitted_answer = all_answers.get(f'spatial_question_{question.id}')
            if submitted_answer and submitted_answer == question.correct_answer:
                spatial_score += 1
        scores['spatial'] = spatial_score
        print(f"Spatial Score: {spatial_score}, Total Spatial Questions: {len(spatial_questions)}")

        # Reasoning Questions
        reasoning_score = 0
        reasoning_questions = ReasoningQuestion.objects.all()
        total_questions['reasoning'] = len(reasoning_questions)
        for question in reasoning_questions:
            submitted_answer = all_answers.get(f'reasoning_question_{question.id}')
            if submitted_answer and submitted_answer == question.correct_answer:
                reasoning_score += 1
        scores['reasoning'] = reasoning_score
        print(f"Reasoning Score: {reasoning_score}, Total Reasoning Questions: {len(reasoning_questions)}")

        print(f"Total Questions: {total_questions}")
        print(f"Raw Scores: {scores}")
        print(f"All Answers: {all_answers}")

        results = {}
        for section, score in scores.items():
            if section in total_questions and total_questions[section] > 0:
                results[section] = round((score / total_questions[section]) * 100)
            else:
                results[section] = 0

        print(f"Calculated Results: {results}")

        # Store the results in the Student model
        student.logical_score = results.get('logical', 0)
        student.numerical_score = results.get('numerical', 0)
        student.numerical1_score = results.get('numerical1', 0)
        student.verbal_score = results.get('verbal', 0)
        student.spatial_score = results.get('spatial', 0)
        student.reasoning_score = results.get('reasoning', 0)
        student.save()

        overall_average = calculate_overall_average(results)

        request.session['assessment_results'] = results
        request.session['overall_average'] = overall_average
        request.session.pop("assessment_start_time", None)
        request.session.pop("current_section_index", None)
        for section in SECTIONS:
            request.session.pop(f'answers_{section}', None)
        return redirect('result')

    return redirect('exam_start')

def calculate_overall_average(results):
    total_percentage = 0
    valid_sections = 0
    for score in results.values():
        total_percentage += score
        valid_sections += 1
    if valid_sections > 0:
        return round(total_percentage / valid_sections)
    return None

def feedback(request):
    if request.method == 'POST':
        overall_experience = request.POST.get('overall_experience')
        difficulty = request.POST.get('difficulty')
        instructions_clarity = request.POST.get('instructions_clarity')
        time_provided = request.POST.get('time_provided')
        interface_usability = request.POST.get('interface_usability')
        favorite_section = request.POST.get('favoriteSection')
        comments = request.POST.get('comments')

        Feedback.objects.create(
            overall_experience_rating=overall_experience,
            difficulty_level=difficulty,
            instructions_clarity_rating=instructions_clarity,
            time_provided_rating=time_provided,
            interface_usability_rating=interface_usability,
            favorite_section=favorite_section,
            comments=comments,
        )
        return redirect('result')

    return render(request, 'feedback.html')

def result(request):
    student_id = request.session.get('student_id')
    results = request.session.get('assessment_results', {})
    overall_average = request.session.get('overall_average')
    student = None
    max_score = None
    min_score = None

    if student_id:
        try:
            student = Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            pass

    if results:
        scores_list = list(results.values())
        if scores_list:
            max_score = max(scores_list)
            min_score = min(scores_list)

    context = {
        'student': student,
        'results': results,
        'max_score': max_score,
        'min_score': min_score,
        'overall_average': overall_average,
    }
    return render(request, 'result.html', context)