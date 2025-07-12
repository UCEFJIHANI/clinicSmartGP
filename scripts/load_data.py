import pandas as pd
from consultation.models import (NomMedicament, Posologie, ExamenClinique,
                                 MotifConsultation, Quantite)
from first_app.models import TestName, Patient, Appointement, Consultation, Analyse
from datetime import datetime, timedelta

# Write data to database


def load_bilan():
    df = pd.read_csv('scripts/ref_bilan.csv')
    for bilan in df['bilan'].values:
        test = TestName.objects.create(name=bilan)
        print(test)


def load_medicament():
    # read data
    df = pd.read_csv('scripts/clean-ref-medicaments-cnops-2014.csv')
    for i in range(len(df)):
        line = df.iloc[i]
        medicament = NomMedicament(code=str(line['CODE']),
                                   nom=line['NOM'], dci1=line['DCI1'],
                                   form=line['FORME'], presentation=line['PRESENTATION'],
                                   princeps_generique=line['PRINCEPS_GENERIQUE'],
                                   taux_remboursement=line['TAUX_REMBOURSEMENT']
                                   )
        if line['DOSAGE1'] and line['UNITE_DOSAGE1']:
            dosage = f"{line['DOSAGE1']} {line['UNITE_DOSAGE1']}"
            medicament.dosage = dosage
        elif line['DOSAGE1']:
            medicament.dosage = line['DOSAGE1']

        try:
            ppv = float(line['PPV'])
            medicament.ppv = ppv
        except:
            pass
        try:
            ph = float(line['PH'])
            medicament.ph = ph
        except:
            pass
        try:
            Prix = float(line['PRIX_BR'])
            medicament.Prix = Prix
        except:
            pass
        medicament.save()
        print(f'medicament N° {i}')


def clean_medicament():
    i = 1
    for med in NomMedicament.objects.all():
        if med.dosage == 'nan nan':
            print(i)
            med.dosage = ''
            med.save()
            i += 1


def load_posologie():
    # read data
    df = pd.read_csv('scripts/posologies.csv')
    for poso in df['posologie'].values:
        p = Posologie.objects.create(nom=poso)
        print(p)


def load_quantite():
    # read data
    df = pd.read_csv('scripts/quantites.csv')
    for poso in df['quantite'].values:
        p = Quantite.objects.create(nom=poso)
        print(p)


def load_examen():
    # read data
    df = pd.read_csv('scripts/ref_examen.csv')
    for exam in df['examen'].values:
        p = ExamenClinique.objects.create(nom=exam)
        print(p)


def load_motif():
    # read data
    df = pd.read_csv('scripts/ref_motif.csv')
    for motif in df['motif'].values:
        m = MotifConsultation.objects.create(nom=motif)
        print(m)

# load fake data


def load_test_bilan():
    df = pd.read_csv('scripts/fake-bilan.csv', parse_dates=['date'])
    created = datetime.now() - timedelta(days=2)
    patients = Patient.objects.all()
    prog = 1
    for p in patients[:5]:
        for i in range(len(df) - 1):
            line = df.iloc[i]
            anal = Analyse.objects.create(
                patient=p,
                name=line['name'],
                value=line['value'],
                date=line['date'],
            )
            anal.created = created
            anal.updated = created
            anal.save()
            print(anal)
            print(prog)
            prog += 1


def load_consultation():
    # load consultation file
    df = pd.read_csv('scripts/fake_consultations.csv', parse_dates=['date'])
    patients = Patient.objects.all()
    for p in patients[:100]:
        for i in range(len(df) - 1):
            line = df.iloc[i]
            con = Consultation.objects.create(
                patient=p,
                motif=line.motif,
                antecedant=line.antecedant,
                diagnostique=line.diagnostique,
                examen=line.examen,
                poids_kg=line.poids_kg,
                taille_cm=line.taille_cm,
                imc=round(line.imc, 2),
                sao2=line.sao2,
                temperature_degC=line.temperature_degC,
                frequence_cardiaque=line.frequence_cardiaque,
                pression_arterielle=line.pression_arterielle
            )
            con.created = line.date
            con.updated = line.date
            con.save()
            print(con)


def load_appointemnet():
    i = 2
    now = datetime.now()
    patients = Patient.objects.all()
    for p in patients[: 500]:
        date_time = now + timedelta(hours=i)
        appoint = Appointement.objects.create(
            patient=p,
            date=date_time.date(),
            hour=date_time.time(),
        )
        print(appoint)
        i += 2


def load_patient():
    df = pd.read_csv('scripts/patients-test.csv')
    for i in range(len(df)):
        patient = Patient.objects.create(
            first_name=df.iloc[i].first_name,
            last_name=df.iloc[i].last_name,
            sexe=df.iloc[i].sexe,
            year_of_birth=df.iloc[i].year_of_birth,
            cnie=df.iloc[i].cnie,
            mutuelle=df.iloc[i].mutuelle,
            phone_number=df.iloc[i].phone_number,
            email=df.iloc[i].email,
            address=df.iloc[i].adresse
        )
        print(patient)


# excute code
load_examen()
load_motif()
load_bilan()
load_medicament()
clean_medicament()
load_posologie()
load_quantite()
# fake data
# load_patient()
# load_appointemnet()
# load_consultation()
# load_test_bilan()
