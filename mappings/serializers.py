from rest_framework import serializers

from patients.models import Patient

from .models import PatientDoctorMapping


class PatientDoctorMappingSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id', 'patient', 'doctor', 'patient_name', 'doctor_name',
            'created_by', 'created_at',
        ]
        read_only_fields = ['id', 'created_by', 'created_at']

    def validate_patient(self, patient):
        request = self.context['request']
        if patient.created_by_id != request.user.id:
            raise serializers.ValidationError('You can only assign doctors to your own patients.')
        return patient

    def validate(self, attrs):
        patient = attrs.get('patient') or getattr(self.instance, 'patient', None)
        doctor = attrs.get('doctor') or getattr(self.instance, 'doctor', None)
        if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists():
            raise serializers.ValidationError('This doctor is already assigned to this patient.')
        return attrs
