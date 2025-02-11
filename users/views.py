from rest_framework import generics, permissions
from .models import User, Patient, DOCTOR, ORDINARY_USER
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer, AddToPatientSerializer
from rest_framework.response import Response
from django.contrib.auth import login, authenticate
from rest_framework import status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, render
from django.utils import timezone


def index(request):
    return render(request, 'index.html')


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]


class LoginAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        password = request.data.get('password')
        # user = authenticate(request, phone_number=phone_number, password=password)
        user = User.objects.filter(phone_number=phone_number).first()
        if user is not None:
            return Response(
                {
                    'id': user.id,
                    'access_token': user.token()['access_token'],
                    'refresh_token': user.token()['refresh_token'],
                    'username': user.phone_number,
                    'roles': user.user_roles,
                }, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {
                    'success': False,
                    'message': 'username or password invalid'
                }, status=status.HTTP_401_UNAUTHORIZED
            )

# class UserListCreateAPIView(generics.ListCreateAPIView):
#     permission_classes = [permissions.AllowAny]
#     serializer_class = UserSerializer
#     queryset = User.objects.all()

# class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [permissions.AllowAny]
#     serializer_class = UserSerializer
#     queryset = User.objects.all()

class UserListCreateAPIView(APIView):
    def get(self, request, *args, **kwargs):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserRetrieveUpdateDestroyView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data)
    
    def put(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AddToPatientAPIView(APIView):
    def post(self, request):
        serializer = AddToPatientSerializer(data=request.data)
        if serializer.is_valid():
            sender_id = serializer.validated_data['sender'].id
            doctor_id = serializer.validated_data['doctor'].id
            patient_id = serializer.validated_data['patient'].id
            created_at = serializer.validated_data['created_at']

            try:
                sender = User.objects.get(id=sender_id)
                doctor = User.objects.get(id=doctor_id)
                patient = User.objects.get(id=patient_id)

                add_to_patient_on_doctor = Patient.objects.create(
                    sender=sender,
                    doctor=doctor,
                    patient=patient,
                    created_at=created_at
                )

                return Response(
                    data={
                        'id': add_to_patient_on_doctor.id,
                        'success': True,
                        'message': 'Added patient to doctor'
                    },
                    status=status.HTTP_201_CREATED
                )
            except User.DoesNotExist:
                return Response(
                    data={
                        'success': False,
                        'message': 'Sender, doctor, or patient not found'
                    },
                    status=status.HTTP_400_BAD_REQUEST
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
            # Construct the full URL for the image
            image_url = request.build_absolute_uri(patient.patient.image.url) if patient.patient.image else None
            patient_info = {
                'patient_id': patient.id,
                'id': patient.patient.id,
                'username': patient.patient.username,
                'first_name': patient.patient.first_name,
                'last_name': patient.patient.last_name,
                'created_at': patient.patient.created_at,
                'complaint': patient.patient.complaint,
                'image': image_url,
                'phone_number': patient.patient.phone_number,
                'region': patient.patient.region,
                'recommendation': patient.patient.recommendation,
            }
            patient_data.append(patient_info)
        return Response(patient_data)

class DoctorListAPIView(APIView):
    def get(self, request):
        doctors = User.objects.filter(user_roles=DOCTOR)
        serializer = UserSerializer(instance=doctors, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class PatientListAPIView(APIView):
    def get(self, request):
        patients = User.objects.filter(user_roles=ORDINARY_USER)
        serializer = UserSerializer(instance=patients, many=True, context={'request': request})
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class TodayPatientView(generics.ListAPIView):
    serializer_class = AddToPatientSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        today = timezone.now().date()
        doctor_id = self.kwargs['doctor_id']
        doctor = User.objects.get(id=doctor_id)
        return Patient.objects.filter(doctor=doctor, created_at__date=today)