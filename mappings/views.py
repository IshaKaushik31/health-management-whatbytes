from rest_framework import generics, permissions, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from patients.models import Patient

from .models import PatientDoctorMapping
from .serializers import PatientDoctorMappingSerializer


class MappingListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class PatientMappingView(APIView):
    """
    GET    /api/mappings/<patient_id>/  -> list doctors assigned to that patient
    DELETE /api/mappings/<id>/          -> remove a single mapping by its own id
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        patient = Patient.objects.filter(pk=pk, created_by=request.user).first()
        if patient is None:
            raise NotFound('Patient not found.')
        mappings = PatientDoctorMapping.objects.filter(patient=patient)
        serializer = PatientDoctorMappingSerializer(mappings, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        mapping = PatientDoctorMapping.objects.filter(
            pk=pk, created_by=request.user
        ).first()
        if mapping is None:
            raise NotFound('Mapping not found.')
        mapping.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
