from django.shortcuts import (render, redirect,
                              get_object_or_404, resolve_url)
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.conf import settings
from datetime import datetime, date, timedelta
from django.http import JsonResponse
from django.db.models import Q
import pytz

from .models import StatDate
from first_app.forms import ExportExcelFrom
from first_app.models import Patient, Consultation
from appcon.models import ServiceConsultation


@login_required
def stats_page(request):
    return render(request, 'statchart/statchart.html',
                {'section': 'stats'})


@login_required
def change_stat_periode(request):
    if request.method == 'POST':
        form = ExportExcelFrom(request.POST)
        if form.is_valid():
            # delete past stat dates
            if request.user.statdates.all():
                request.user.statdates.all().delete()
            # clean data
            cd = form.cleaned_data
            StatDate.objects.create(user=request.user, date1=cd['date1'],
                                date2=cd['date2'])
            return HttpResponse(status=204,
                                headers={'HX-Trigger': 'statDatesChanged'})
    else:
        if request.user.statdates.all():
            stat = request.user.statdates.first()
            stat_date = {'date1': stat.date1, 'date2': stat.date2}
            form = ExportExcelFrom(stat_date)
        else:
            form = ExportExcelFrom()

    return render(request, 'statchart/stat_dates_form.html',
                  {'form': form})

@login_required
def show_periode(request):
    date1 = datetime.today() - timedelta(days=1)
    date2 = datetime.today()
    statdates = request.user.statdates.all()
    patients = Patient.objects.all()

    if statdates:
        periode = statdates.first()
        date1 = periode.date1
        date2 = periode.date2

    elif patients:
        first_patient = patients.first()
        last_patient = patients.last()
        date1 = last_patient.created
        date2 = first_patient.created

    html = f'Période entre le {date1.day}/{date1.month}/{date1.year} et {date2.day}/{date2.month}/{date2.year}'
    return HttpResponse(html)

# Patients
@login_required
def patient_chart_data(request):
    statdates = request.user.statdates.all()
    if statdates:
        stat = statdates.first()
        casablanca = pytz.timezone('Africa/Casablanca')
        date1 = datetime(stat.date1.year, stat.date1.month, stat.date1.day, 0, 0, tzinfo=casablanca)
        date2 = datetime(stat.date2.year, stat.date2.month, stat.date2.day, 23, 59, tzinfo=casablanca)
        patients = Patient.objects.filter(
            Q(created__gte=date1), Q(created__lte=date2)
        )
        homme = patients.filter(sexe='homme').count()
        femme = patients.filter(sexe='femme').count()
    else:
        homme = Patient.objects.filter(sexe='homme').count()
        femme = Patient.objects.filter(sexe='femme').count()
    return JsonResponse(data={
        'labels': ['Homme', 'Femme'],
        'data': [homme, femme],
    })

@login_required
def patient_chart(request):
    return render(request, 'statchart/patient_chart.html')

# Patient categorie
@login_required
def patient_categories_data(request):
    statdates = request.user.statdates.all()
    moins_15 = 0
    entre_15_25 = 0
    entre_25_40 = 0
    entre_40_70 = 0
    plus_70 = 0
    if statdates:
        stat = statdates.first()
        casablanca = pytz.timezone('Africa/Casablanca')
        date1 = datetime(stat.date1.year, stat.date1.month, stat.date1.day, 0, 0, tzinfo=casablanca)
        date2 = datetime(stat.date2.year, stat.date2.month, stat.date2.day, 23, 59, tzinfo=casablanca)
        patients = Patient.objects.filter(
            Q(created__gte=date1), Q(created__lte=date2)
        )
        for p in patients:
            if p.age < 15:
                moins_15 += 1
            elif p.age < 25:
                entre_15_25 += 1
            elif p.age < 40:
                entre_25_40 += 1
            elif p.age < 70:
                entre_40_70 += 1
            else:
                plus_70 += 1
    else:
        for p in Patient.objects.all():
            if p.age < 15:
                moins_15 += 1
            elif p.age < 25:
                entre_15_25 += 1
            elif p.age < 40:
                entre_25_40 += 1
            elif p.age < 70:
                entre_40_70 += 1
            else:
                plus_70 += 1
    return JsonResponse(data={
        'labels': ['Moins de 15 ans', 'Entre 15 et 25 ans', 'Entre 25 et 40 ans',
                  'Entre 40 et 70 ans', 'Plus de 70 ans'],
        'data': [moins_15, entre_15_25, entre_25_40, entre_40_70, plus_70],
    })


@login_required
def patient_categories_chart(request):
    return render(request, 'statchart/patient_categories_chart.html')

# Les consultations
@login_required
def consultation_chart_data(request):
    statdates = request.user.statdates.all()
    if statdates:
        stat = statdates.first()
        casablanca = pytz.timezone('Africa/Casablanca')
        date1 = datetime(stat.date1.year, stat.date1.month, stat.date1.day, 0, 0, tzinfo=casablanca)
        date2 = datetime(stat.date2.year, stat.date2.month, stat.date2.day, 23, 59, tzinfo=casablanca)
        consultations = Consultation.objects.filter(
            Q(created__gte=date1), Q(created__lte=date2)
        )
        homme = consultations.filter(patient__sexe='homme').count()
        femme = consultations.filter(patient__sexe='femme').count()
    else:
        homme = Consultation.objects.filter(patient__sexe='homme').count()
        femme = Consultation.objects.filter(patient__sexe='femme').count()
    return JsonResponse(data={
        'labels': ['Homme', 'Femme'],
        'data': [homme, femme],
    })

@login_required
def consultation_chart(request):
    return render(request, 'statchart/consultation_chart.html')

# consultation categorie
@login_required
def consultation_categorie_data(request):
    statdates = request.user.statdates.all()
    far = 0
    cnops = 0
    cnss = 0
    amo = 0
    axa = 0
    assurences = 0
    sans = 0
    if statdates:
        stat = statdates.first()
        casablanca = pytz.timezone('Africa/Casablanca')
        date1 = datetime(stat.date1.year, stat.date1.month, stat.date1.day, 0, 0, tzinfo=casablanca)
        date2 = datetime(stat.date2.year, stat.date2.month, stat.date2.day, 23, 59, tzinfo=casablanca)
        consultations = Consultation.objects.filter(
            Q(created__gte=date1), Q(created__lte=date2)
        )
        for con in consultations:
            if con.patient.mutuelle == 'amo':
                amo += 1
            if con.patient.mutuelle == 'axa':
                axa += 1
            if con.patient.mutuelle == 'far':
                far += 1
            elif con.patient.mutuelle == 'cnops':
                cnops += 1
            elif con.patient.mutuelle == 'cnss':
                cnss += 1
            elif con.patient.mutuelle == 'assurences':
                assurences += 1
            else:
                sans += 1
    else:
        for con in Consultation.objects.all():
            if con.patient.mutuelle == 'amo':
                amo += 1
            if con.patient.mutuelle == 'axa':
                axa += 1
            if con.patient.mutuelle == 'far':
                far += 1
            elif con.patient.mutuelle == 'cnops':
                cnops += 1
            elif con.patient.mutuelle == 'cnss':
                cnss += 1
            elif con.patient.mutuelle == 'assurences':
                assurences += 1
            else:
                sans += 1
    return JsonResponse(data={
        'labels': ['FAR', 'CNOPS', 'CNSS', 'AMO', 'AXA',
                  'ASSURENCES', 'SANS'],
        'data': [far, cnops, cnss, amo, axa, assurences, sans],
    })

@login_required
def consultation_categories(request):
    return render(request, 'statchart/consultation_categories.html')

# Payments ServiceConsultation
@login_required
def payments_categorie_data(request):
    statdates = request.user.statdates.all()
    avecassurance = 0
    sansassurance = 0
    if statdates:
        stat = statdates.first()
        casablanca = pytz.timezone('Africa/Casablanca')
        date1 = datetime(stat.date1.year, stat.date1.month, stat.date1.day, 0, 0, tzinfo=casablanca)
        date2 = datetime(stat.date2.year, stat.date2.month, stat.date2.day, 23, 59, tzinfo=casablanca)
        payments = ServiceConsultation.objects.filter(
            Q(created__gte=date1), Q(created__lte=date2)
        )
        for pay in payments:
            if pay.assurance:
                avecassurance += pay.prix
            else:
                sansassurance += pay.prix
    else:
        for pay in ServiceConsultation.objects.all():
            if pay.assurance:
                avecassurance += pay.prix
            else:
                sansassurance += pay.prix

    return JsonResponse(data={
        'labels': ['AVEC ASSURANCE', 'SANS ASSURANCE'],
        'data': [avecassurance, sansassurance],
    })

@login_required
def payments_categories(request):
    return render(request, 'statchart/payments_categories.html')

# payments par prestation
@login_required
def payments_prestation_data(request):
    statdates = request.user.statdates.all()
    prestation = {}
    if statdates:
        stat = statdates.first()
        casablanca = pytz.timezone('Africa/Casablanca')
        date1 = datetime(stat.date1.year, stat.date1.month, stat.date1.day, 0, 0, tzinfo=casablanca)
        date2 = datetime(stat.date2.year, stat.date2.month, stat.date2.day, 23, 59, tzinfo=casablanca)
        payments = ServiceConsultation.objects.filter(
            Q(created__gte=date1), Q(created__lte=date2)
        )
        for pay in payments:
            if pay.service in prestation:
                prestation[pay.service] = prestation[pay.service] + pay.prix
            else:
                prestation[pay.service] = pay.prix
    else:
        for pay in ServiceConsultation.objects.all():
            if pay.service in prestation:
                prestation[pay.service] = prestation[pay.service] + pay.prix
            else:
                prestation[pay.service] = pay.prix
    labels = []
    data = []
    for pres in prestation:
        labels.append(pres)
        data.append(prestation[pres])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })

@login_required
def payments_prestation(request):
    return render(request, 'statchart/payments_prestation.html')
