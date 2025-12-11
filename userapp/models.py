import datetime

from django.db import models
from django.conf import settings
from django.utils import timezone

class UserProfile(models.Model):

    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('parent', 'Parent'),
        ('admin', 'Admin'),
    )

    DEPARTMENT_CHOICES = (
        ('science', 'Science'),
        ('mathematics', 'Mathematics'),
        ('arts', 'Arts & Humanities'),
        ('commerce', 'Commerce'),
        ('computer_science', 'Computer Science'),
        ('administration', 'Administration'),
    )

    # From First Name & Last Name fields
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    # From Email field
    email = models.EmailField(unique=True)

    # From Department dropdown
    department = models.CharField(
        max_length=50,
        choices=DEPARTMENT_CHOICES
    )

    # From Designation / Class field
    designation = models.CharField(max_length=100)

    # From Role dropdown
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES
    )

    # From Password field (plain for now – machine test use)
    password = models.CharField(max_length=128)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.role}"


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    EVENT_TYPE_CHOICES = (
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('cultural_fest', 'Cultural Fest'),
        ('sports_event', 'Sports Event'),
        ('club_event', 'Club Event'),
        ('exam_related', 'Exam Related'),
    )

    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)

    department = models.CharField(max_length=100)

    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    #  NEW FIELD — VENUE
    venue = models.CharField(max_length=150)

    #  NEW FIELD — STAFF COORDINATORS (comma-separated for simplicity)
    staff_coordinators = models.CharField(max_length=255)

    #  NEW FIELD — EQUIPMENT / RESOURCES
    equipment_required = models.TextField(blank=True, null=True)

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_by_id = models.IntegerField()

    def __str__(self):
        return self.title




class Participant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    student_name = models.CharField(max_length=100)
    student_email = models.EmailField()


class EventRegistration(models.Model):
    # Reference the UserProfile defined earlier in this file — no circular import needed
    student = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name="registrations"
    )
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="registrations")
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'event')



class Feedback(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    rating = models.IntegerField()
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.first_name} - {self.event.title}"
