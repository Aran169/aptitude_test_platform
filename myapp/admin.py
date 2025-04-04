from django.contrib import admin
from .models import (
    LogicalQuestion,
    NumericalQuestion,
    VerbalQuestion,
    SpatialQuestion,
    NumericalQuestion1,
    ReasoningQuestion,
    Student,
    Feedback
)

admin.site.register(LogicalQuestion)
admin.site.register(NumericalQuestion)
admin.site.register(VerbalQuestion)
admin.site.register(SpatialQuestion)
admin.site.register(NumericalQuestion1)
admin.site.register(ReasoningQuestion)
admin.site.register(Student)
admin.site.register(Feedback)