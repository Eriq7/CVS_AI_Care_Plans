import os

import openai

from .models import CarePlan


def create_careplan(data):
    care_plan = CarePlan.objects.create(
        patient_name=data['patient_name'],
        patient_mrn=data['patient_mrn'],
        medication=data['medication'],
        icd10_code=data['icd10_code'],
        provider_name=data['provider_name'],
        provider_npi=data['provider_npi'],
        status='pending',
    )

    from .tasks import generate_careplan_task
    generate_careplan_task.delay(care_plan.id)

    return care_plan


def get_careplan(pk):
    return CarePlan.objects.get(id=pk)


def list_careplans(query=''):
    plans = CarePlan.objects.all().order_by('-created_at')
    if query:
        plans = plans.filter(patient_name__icontains=query) | \
                plans.filter(medication__icontains=query) | \
                plans.filter(icd10_code__icontains=query) | \
                plans.filter(provider_name__icontains=query)
    return plans


def format_careplan_download(plan):
    return (
        f"Care Plan #{plan.id}\n"
        f"{'=' * 40}\n"
        f"Patient: {plan.patient_name} (MRN: {plan.patient_mrn})\n"
        f"Medication: {plan.medication}\n"
        f"ICD-10: {plan.icd10_code}\n"
        f"Provider: {plan.provider_name} (NPI: {plan.provider_npi})\n"
        f"Status: {plan.status}\n"
        f"Created: {plan.created_at.strftime('%Y-%m-%d %H:%M')}\n"
        f"{'=' * 40}\n\n"
        f"{plan.care_plan_text}\n"
    )


def call_llm(patient_name, medication, icd10_code, provider_name):
    api_key = os.environ.get('OPENAI_API_KEY', '')

    if not api_key or api_key == 'your-api-key-here':
        return (
            f"## Problem List\n"
            f"- Patient {patient_name} requires {medication} therapy management\n"
            f"- Diagnosis: {icd10_code}\n\n"
            f"## Goals\n"
            f"1. Optimize {medication} therapy for maximum efficacy\n"
            f"2. Minimize adverse drug reactions\n"
            f"3. Improve patient medication adherence\n\n"
            f"## Pharmacist Interventions\n"
            f"1. Review current {medication} dosing and adjust as needed\n"
            f"2. Provide patient education on {medication} usage and side effects\n"
            f"3. Coordinate with Dr. {provider_name} on therapy modifications\n"
            f"4. Screen for drug-drug interactions\n\n"
            f"## Monitoring Plan\n"
            f"1. Follow-up assessment in 2 weeks\n"
            f"2. Monitor relevant lab values for {icd10_code}\n"
            f"3. Assess medication adherence at each visit\n"
            f"4. Document and report any adverse effects\n"
        )

    client = openai.OpenAI(api_key=api_key)

    prompt = (
        f"You are a clinical pharmacist. Generate a care plan for:\n\n"
        f"Patient: {patient_name}\n"
        f"Medication: {medication}\n"
        f"ICD-10: {icd10_code}\n"
        f"Provider: Dr. {provider_name}\n\n"
        f"Include these sections with ## markdown headers:\n"
        f"1. Problem List\n"
        f"2. Goals\n"
        f"3. Pharmacist Interventions\n"
        f"4. Monitoring Plan\n"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an experienced clinical pharmacist."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=1500,
    )

    return response.choices[0].message.content
