from rest_framework import generics, permissions
from .models import User, Patient
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, AddToPatientSerializer
from rest_framework.response import Response
from django.contrib.auth import login
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]


class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data.get('phone_number')
            password = serializer.validated_data.get('password')
            user = User.objects.filter(phone_number=phone_number).first()
            if user is not None and user.check_password(password):
                login(request, user)
                return Response(
                    data={
                        'id': user.id,
                        'username': user.phone_number,
                        'user_roles': user.user_roles,
                        'access_token': user.token()['access_token'],
                        'refresh_token': user.token()['refresh_token'],
                        'password': user.password
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    data={
                        'success': False,
                        'message': 'Username or password is invalid.'
                    },
                    status=status.HTTP_401_UNAUTHORIZED
                )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class UserListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class AddToPatientAPIView(APIView):
    def post(self, request):
        serializer = AddToPatientSerializer(data=request.data)
        if serializer.is_valid():
            sender = serializer.validated_data['sender']
            doctor = serializer.validated_data['doctor']
            patient = serializer.validated_data['patient'].id
            try:
                patient = User.objects.get(id=patient)
                print(patient)
                add_to_patent_on_doctor = Patient.objects.create(sender=sender, doctor=doctor, patient=patient)
                return Response(
                    data={
                        'id': add_to_patent_on_doctor.id,
                        'success': True,
                        'message': 'Added patient on docker '
                    }, status=status.HTTP_201_CREATED
                )
            except:
                return Response(
                    data={
                        'success': False,
                        'message': 'Doctor or patient not found '
                    }, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DoctorPatientListAPIView(APIView):
    def get(self, request, doctor_id):
        # Doktorni qidirish
        doctor = get_object_or_404(User, id=doctor_id)
        # Doktorga bog'liq barcha xastalarni olish
        patients = Patient.objects.filter(doctor=doctor)
        # Patientlar uchun serializer
        patient_data = []
        for patient in patients:
            patient_info = {
                'id': patient.id,
                'patient_id': patient.patient.id,
                'patient_username': patient.patient.username,
                'patient_first_name': patient.patient.first_name,
                'patient_last_name': patient.patient.last_name,
                # Boshqa malumotlar
            }
            patient_data.append(patient_info)
        return Response(patient_data)






