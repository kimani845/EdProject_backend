from django.urls import path
from . import views

urlpatterns = [
    path('', views.ClassListCreateView.as_view(), name='class_list_create'),
    path('<int:pk>/', views.ClassDetailView.as_view(), name='class_detail'),
    path('my-classes/', views.TutorClassesView.as_view(), name='tutor_classes'),
    path('enrolled/', views.StudentClassesView.as_view(), name='student_classes'),
    path('<int:class_id>/enroll/', views.enroll_in_class, name='enroll_in_class'),
    path('<int:class_id>/rate/', views.rate_tutor, name='rate_tutor'),
]