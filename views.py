from django.shortcuts import render, redirect
from .models import Question
from .models import Answer, Appointment
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from account.models import Account, CounsellorProfile
from .decorators import validate_user_test, validate_answer_count
# Create your views here.


@login_required
def dashboard(request):

    print(Answer.objects.filter(patient=request.user).count())
    approved_appointments = Appointment.objects.exclude(appointment_status='Pending').filter( patient=request.user).count()

    pending_appointments = Appointment.objects.filter(appointment_status='Pending', patient=request.user).count()

    total = Appointment.objects.filter(patient=request.user).count()

    context = {
        'approved_appointments': approved_appointments,
        'pending_appointments': pending_appointments,
        'total': total,

    }

    return render(request, 'patient_app/dashboard.html', context)

@login_required
def go_to_test_page(request):
    return render(request, 'patient_app/go-to-test-page.html')


@login_required
@validate_user_test
def take_test(request):
    questions = Question.objects.all()

    
    if request.method == 'POST':
        for question in questions:
            
            
            answer = request.POST.get('q_' + str(question.id))

            new_answer = Answer(
                question=question,
                answer=answer,
                patient=request.user
            )

            new_answer.save()
            
        request.user.took_test = True
        request.user.save()
        messages.success(request, 'Test has been submitted successfully')
        return redirect('patient:dashboard')
            

        return redirect('patient:dashboard')
    context = {
        'questions': questions,
    }
    return render(request, 'patient_app/test.html', context)

@login_required
@validate_answer_count
def appointment(request):

    if request.user.took_test == False:
        messages.error(request, 'You have to take the test first')
        return redirect('patient:go-to-test-page')

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        appointment_for = request.POST.get('appointment_for')
        preffered_date = request.POST.get('date')
        preffered_time_range = request.POST.get('time')

        new_appointment = Appointment(
            patient=request.user,
            name=name,
            email=email,
            phone=phone,
            appointment_for=appointment_for,
            preffered_date=preffered_date,
            preffered_time_range=preffered_time_range,
        )

        user_answer = Answer.objects.get(patient = request.user, question__question_text = 'Do you prefer to pair with a male counselor?')

        if user_answer.answer == 'Yes':
            try:
                
                counsellor = CounsellorProfile.objects.filter(gender = 'Male').order_by('?').first()
                
            except CounsellorProfile.DoesNotExist:
                
                counsellor = CounsellorProfile.objects.filter(gender = 'Female').order_by('?').first()
        else:
            try:
                
                counsellor = CounsellorProfile.objects.filter(gender = 'Female').order_by('?').first()
                
            except CounsellorProfile.DoesNotExist:
                
                counsellor = CounsellorProfile.objects.filter(gender = 'Male').order_by('?').first()

        print(counsellor)
        assigned_counsellor = Account.objects.get(id = counsellor.counsellor_id)

        new_appointment.counsellor = assigned_counsellor
        new_appointment.save()
        messages.success(request, 'Appointment has been created successfully')
        return redirect('patient:pending_appointments') 
       

    return render(request, 'patient_app/appointment.html')

@login_required
@validate_answer_count
def approved_appointments(request):

    if request.user.took_test == False:
        messages.error(request, 'You have to take the test first')
        return redirect('patient:go-to-test-page')

    approved_appointments = Appointment.objects.exclude(appointment_status='Pending', patient=request.user)
    context = {
        'approved_appointments': approved_appointments,
    }
    return render(request, 'patient_app/approved-appointments.html', context)

@login_required
@validate_answer_count
def pending_appointments(request):

    if request.user.took_test == False:
        messages.error(request, 'You have to take the test first')
        return redirect('patient:go-to-test-page')

    pending_appointments = Appointment.objects.filter(appointment_status='Pending', patient=request.user)
    context = {
        'pending_appointments': pending_appointments,
    }
    return render(request, 'patient_app/pending-appointments.html', context)

@login_required
@validate_answer_count
def verify_payment(request):

    if request.user.took_test == False:
        messages.error(request, 'You have to take the test first')
        return redirect('patient:go-to-test-page')

    if request.method == 'GET':
        app_id = request.GET.get('id')
    appointment = Appointment.objects.get(id=app_id)
  
    appointment.is_paid = True

    appointment.save()

    return redirect('patient:pending_appointments')
