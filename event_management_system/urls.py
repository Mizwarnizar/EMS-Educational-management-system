"""
URL configuration for event_management_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from userapp import views
from userapp.views import mark_attendance, unmark_attendance

urlpatterns = [
    path('', views.login_view, name='login'),
    path('user_registration/', views.user_register),
    path('logout/', views.logout_view, name='logout'),
    path('user_registration_success/', views.user_registration_success, name='user_registration_success'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('teacher_dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student_dashboard/', views.student_dashboard, name='student_dashboard'),
    path('parent_dashboard/', views.parent_dashboard, name='parent_dashboard'),
    path('event-proposal/', views.event_proposal, name='event_proposal'),
    path('create_event_admin/', views.create_event_admin, name='create_event_admin'),
    path('propose_event_teacher/', views.teacher_event_proposal, name='teacher_event_proposal'),

    path("approve_event/<int:event_id>/", views.approve_event, name="approve_event"),
    path("reject_event/<int:event_id>/", views.reject_event, name="reject_event"),

    #  TEACHER ACTIONS
    path("edit_event/<int:event_id>/", views.edit_event, name="edit_event"),
    path("manage_participants/<int:event_id>/", views.manage_participants, name="manage_participants"),

    #  Student Event Actions
    path('register_event/<int:event_id>/', views.register_for_event, name='register_for_event'),
    path('unregister_event/<int:event_id>/', views.unregister_event, name='unregister_event'),


    # Manage Participants
    path('manage_participants/<int:event_id>/', views.manage_participants, name='manage_participants'),
    path("mark_attendance/<int:participant_id>/", mark_attendance, name="mark_attendance"),
    path("unmark_attendance/<int:participant_id>/", unmark_attendance, name="unmark_attendance"),


]



