from django.urls import path
from .views import RegisterAPIView, LoginAPIView, UserListCreateAPIView, UserRetrieveUpdateDestroyView, \
    AddToPatientAPIView, DoctorPatientListAPIView
urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('users/', UserListCreateAPIView.as_view()),
    path('users/<uuid:pk>/', UserRetrieveUpdateDestroyView.as_view()),
    path('add-to-patient/', AddToPatientAPIView.as_view()),
    path('doctor-patients/<uuid:doctor_id>/', DoctorPatientListAPIView.as_view()),

]
