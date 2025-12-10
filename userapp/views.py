from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from event_management_system import settings
from . import models
from .models import UserProfile, Event, EventRegistration,Participant


# -------------------------------
# LOGIN (CUSTOM - USING UserProfile)
# -------------------------------
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print("EMAIL:", email)       # ✅ DEBUG
        print("PASSWORD:", password)

        try:
            user = UserProfile.objects.get(email=email, password=password)
        except UserProfile.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid email or password'})

        request.session['user_id'] = user.id
        request.session['user_role'] = user.role

        if user.role == 'admin':
            return redirect('admin_dashboard')
        elif user.role == 'teacher':
            return redirect('teacher_dashboard')
        elif user.role == 'student':
            return redirect('student_dashboard')
        else:
            return redirect('parent_dashboard')

    return render(request, 'login.html')

# -------------------------------
# USER REGISTER
# -------------------------------
def user_register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        department = request.POST.get('department')
        designation = request.POST.get('designation')
        role = request.POST.get('role')
        password = request.POST.get('password')

        UserProfile.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            department=department,
            designation=designation,
            role=role,
            password=password
        )

        return redirect('/user_registration_success')

    return render(request, 'user_registration.html')

# -------------------------------
# USER REGISTRATION SUCCESS
# -------------------------------

def user_registration_success(request):
    return render(request, 'user_registration_success.html')

# -------------------------------
# LOGOUT
# -------------------------------
def logout_view(request):
    request.session.flush()
    return redirect('/login')


# -------------------------------
# DASHBOARDS (SESSION BASED)
# -------------------------------
def admin_dashboard(request):
    if request.session.get('user_role') != 'admin':
        return redirect('login')

    events = Event.objects.all()
    return render(request, 'admin_dashboard.html', {'events': events})


def teacher_dashboard(request):
    if request.session.get('user_role') != 'teacher':
        return redirect('login')

    teacher_id = request.session.get('user_id')

    # ✅ Only events created by THIS teacher and approved by admin
    approved_events = Event.objects.filter(
        created_by_id=teacher_id,
        status='approved'
    ).order_by('-id')

    context = {
        'events': approved_events
    }

    return render(request, 'teacher_dashboard.html', context)


def student_dashboard(request):
    if request.session.get('user_role') != 'student':
        return redirect('login')

    events = Event.objects.filter(status='approved').order_by('-date')

    return render(request, 'student_dashboard.html', {'events': events})



def parent_dashboard(request):
    if request.session.get('user_role') != 'parent':
        return redirect('login')

    events = Event.objects.filter(status='approved')
    return render(request, 'parent_dashboard.html', {'events': events})


def event_proposal(request):
    if request.session.get('user_role') != 'teacher':
        return redirect('login')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        event_type = request.POST.get('event_type')
        department = request.POST.get('department')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        venue = request.POST.get('venue')

        Event.objects.create(
            title=title,
            description=description,
            event_type=event_type,
            department=department,
            date=date,
            start_time=start_time,
            end_time=end_time,
            venue=venue,
            created_by_id=request.session['user_id'],
            status='pending'
        )

        return redirect('teacher_dashboard')

    return render(request, 'event_proposal.html')


# -------------------------------
# ADMIN DASHBOARD
# -------------------------------

import datetime  # make sure this is at the top of the file

def admin_dashboard(request):
    if request.session.get('user_role') != 'admin':
        return redirect('login')

    pending_events = Event.objects.filter(status='pending')
    approved_events = Event.objects.filter(status='approved')
    today = datetime.date.today()
    today_events = Event.objects.filter(date=today)

    recent_events = Event.objects.order_by('-id')[:5]

    context = {
        'pending_events': pending_events,
        'pending_count': pending_events.count(),
        'approved_count': approved_events.count(),
        'today_count': today_events.count(),   # 👈 NEW
        'recent_events': recent_events,
    }

    return render(request, 'admin_dashboard.html', context)


# -------------------------------
# EVENT CREATION ADMIN
# -------------------------------

def create_event_admin(request):
    if request.session.get('user_role') != 'admin':
        return redirect('login')

    if request.method == 'POST':
        title = request.POST.get('event_name')
        description = request.POST.get('description')
        event_type = request.POST.get('event_type')
        department = request.POST.get('organizing_dept')
        date = request.POST.get('date_start')
        start_time = request.POST.get('time_start')
        venue = request.POST.get('venue_request')

        # Multiple select → convert to string
        staff_list = request.POST.getlist('coordinators')
        staff_coordinators = ", ".join(staff_list)

        # Multiple checkboxes → equipment
        equipment_list = request.POST.getlist('resource_needed')
        equipment_required = ", ".join(equipment_list)

        if not title:
            return render(request, 'event_creation.html', {
                'error': 'Event title is required'
            })

        Event.objects.create(
            title=title,
            description=description,
            event_type=event_type,
            department=department,
            date=date,
            start_time=start_time,
            end_time="23:59",
            venue=venue,
            staff_coordinators=staff_coordinators,
            equipment_required=equipment_required,
            created_by_id=request.session['user_id'],
            status='approved'
        )

        return redirect('admin_dashboard')

    return render(request, 'event_creation.html')




def teacher_event_proposal(request):
    if request.session.get('user_role') != 'teacher':
        return redirect('login')

    if request.method == 'POST':
        print("✅ POST request received")
        title = request.POST.get('title')
        description = request.POST.get('description')
        event_type = request.POST.get('event_type')
        department = request.POST.get('department')
        date = request.POST.get('date')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        venue = request.POST.get('venue')

        print("Title:", title)
        print("Description:", description)
        print("Type:", event_type)
        print("Department:", department)
        print("Date:", date)
        print("Time:", start_time)
        print("Venue:", venue)


        Event.objects.create(
            title=title,
            description=description,
            event_type=event_type,
            department=department,
            date=date,
            start_time=start_time,
            end_time=end_time,
            venue=venue,
            created_by_id=request.session['user_id'],
            status='pending'   # ✅ VERY IMPORTANT
        )

        return redirect('teacher_dashboard')

    return render(request, 'propose_event.html')





from django.shortcuts import get_object_or_404, redirect
from .models import Event

# ✅ ADMIN: APPROVE EVENT
def approve_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.status = "approved"
    event.save()
    return redirect("admin_dashboard")


# ✅ ADMIN: REJECT EVENT
def reject_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.status = "rejected"
    event.save()
    return redirect("admin_dashboard")


# ✅ TEACHER: EDIT EVENT
def edit_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return redirect("teacher_dashboard")  # you can later connect edit form


# ✅ TEACHER: MANAGE PARTICIPANTS
def manage_participants(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return redirect("teacher_dashboard")  # you can later build participants page




from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from .models import Event, EventRegistration, Participant
from django.contrib.auth import get_user_model

User = get_user_model()

def register_for_event(request, event_id):
    print("\n🔥 REGISTER EVENT TRIGGERED")
    print("SESSION USER ID:", request.session.get('user_id'))

    if request.session.get('user_role') != 'student':
        print("❌ Not a student")
        return redirect('login')

    student_id = request.session.get('user_id')

    if not student_id:
        print("❌ No student ID in session")
        return redirect('login')

    # Fetch student
    student = get_object_or_404(UserProfile, id=student_id)
    print("👍 Student found:", student)

    # Fetch event
    event = get_object_or_404(Event, id=event_id)
    print("👍 Event found:", event)

    if request.method == "POST":
        print("➡️ POST request received")

        try:
            registration, created = EventRegistration.objects.get_or_create(
                student=student,
                event=event
            )
            print("📌 EventRegistration created:", created)

            if created:
                print("➡️ Creating Participant Entry...")
                Participant.objects.create(
                    event=event,
                    student_name=f"{student.first_name} {student.last_name}",
                    student_email=student.email
                )
                print("✅ Participant saved!")

                messages.success(request, "Successfully registered!")
            else:
                print("⚠️ Already registered")
                messages.warning(request, "Already registered.")

        except Exception as e:
            print("\n❌ ERROR WHILE SAVING:", e)
            import traceback
            traceback.print_exc()

    return redirect('student_dashboard')


def unregister_event(request, event_id):
    if request.session.get('user_role') != 'student':
        return redirect('login')

    student_id = request.session.get('user_id')
    if not student_id:
        return redirect('login')

    EventRegistration.objects.filter(
        student_id=student_id,
        event_id=event_id
    ).delete()

    return redirect('student_dashboard')




from django.shortcuts import get_object_or_404, redirect
from .models import Participant

def manage_participants(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    participants = Participant.objects.filter(event=event)

    return render(request, "manage_participants.html", {
        "event": event,
        "participants": participants
    })



def mark_attendance(request, p_id):
    participant = get_object_or_404(Participant, id=p_id)
    participant.attended = True
    participant.save()
    return redirect('manage_participants', event_id=participant.event.id)

def unmark_attendance(request, p_id):
    participant = get_object_or_404(Participant, id=p_id)
    participant.attended = False
    participant.save()
    return redirect('manage_participants', event_id=participant.event.id)
