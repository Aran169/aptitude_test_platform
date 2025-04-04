from django.db import models

class Student(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]

    GRADE_CHOICES = [
        ('1-3', '1-3'),
        ('4-6', '4-6'),
        ('7-9', '7-9'),
        ('10-12', '10-12'),
        ('ug', 'ug'),
        ('pg','pg'),
    ]

    full_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    grade = models.CharField(max_length=20, choices=GRADE_CHOICES)
    parent_name = models.CharField(max_length=100)
    contact_email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    logical_score = models.IntegerField(blank=True, null=True)
    numerical_score = models.IntegerField(blank=True, null=True)
    verbal_score = models.IntegerField(blank=True, null=True)
    spatial_score = models.IntegerField(blank=True, null=True)
    reasoning_score = models.IntegerField(blank=True, null=True)
    numerical1_score = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.full_name



class LogicalQuestion(models.Model):
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1)

    def __str__(self):
        return self.question_text[:50] + "..."

class NumericalQuestion(models.Model):
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1)

    def __str__(self):
        return self.question_text[:50] + "..."

class NumericalQuestion1(models.Model):
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1)

    def __str__(self):
        return self.question_text[:50] + "..."


class VerbalQuestion(models.Model):
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1)

    def __str__(self):
        return self.question_text[:50] + "..."

class SpatialQuestion(models.Model):
    question_text = models.TextField()
    # You might store image paths or descriptions here
    image = models.ImageField(upload_to='spatial_questions/', blank=True, null=True)
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1)

    def __str__(self):
        return self.question_text[:50] + "..."

class ReasoningQuestion(models.Model):
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1)

    def __str__(self):
        return self.question_text[:50] + "..."
    


class Feedback(models.Model):
    overall_experience_rating = models.IntegerField(
        blank=True, null=True, choices=[(i, str(i)) for i in range(1, 6)]
    )
    difficulty_level = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        choices=[
            ('very_easy', 'Very Easy'),
            ('easy', 'Easy'),
            ('moderate', 'Moderate'),
            ('difficult', 'Difficult'),
            ('very_difficult', 'Very Difficult'),
        ],
    )
    instructions_clarity_rating = models.IntegerField(
        blank=True, null=True, choices=[(i, str(i)) for i in range(1, 6)]
    )
    time_provided_rating = models.IntegerField(
        blank=True, null=True, choices=[(i, str(i)) for i in range(1, 6)]
    )
    interface_usability_rating = models.IntegerField(
        blank=True, null=True, choices=[(i, str(i)) for i in range(1, 6)]
    )
    favorite_section = models.CharField(max_length=50, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback submitted on {self.submission_date.strftime('%Y-%m-%d %H:%M:%S')}"



