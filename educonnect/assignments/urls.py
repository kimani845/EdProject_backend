from django.urls import path
from . import views

urlpatterns = [
    path('student/', views.StudentAssignmentsView.as_view(), name='student_assignments'),
    path('tutor/', views.TutorAssignmentsView.as_view(), name='tutor_assignments'),
    path('<int:pk>/', views.AssignmentDetailView.as_view(), name='assignment_detail'),
    path('<int:assignment_id>/submit/', views.submit_assignment, name='submit_assignment'),
    path('<int:assignment_id>/submissions/', views.assignment_submissions, name='assignment_submissions'),
    path('submissions/<int:submission_id>/grade/', views.grade_submission, name='grade_submission'),
]