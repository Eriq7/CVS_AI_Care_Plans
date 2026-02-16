def serialize_careplan(p):
    return {
        'id': p.id,
        'patient_name': p.patient_name,
        'patient_mrn': p.patient_mrn,
        'medication': p.medication,
        'icd10_code': p.icd10_code,
        'provider_name': p.provider_name,
        'provider_npi': p.provider_npi,
        'status': p.status,
        'care_plan_text': p.care_plan_text if p.status == 'completed' else '',
        'created_at': p.created_at.isoformat(),
    }
