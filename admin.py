from django.contrib import admin
from .models import Question, Answer, Appointment
# Register your models here.


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'options']


    class Meta:
        model = Question
        ordering = ['-id']

class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer', 'patient']

    class Meta:
        model = Answer
        ordering = ['-id']


class AppointmentAdmin(admin.ModelAdmin):

    list_display = ['patient', 'name', 'email', 'phone', 'appointment_for', 'appointment_status', 'preffered_date', 'preffered_time_range', 'counsellor']

    class Meta:
        model = Appointment
        ordering = ['-id']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(Appointment, AppointmentAdmin)