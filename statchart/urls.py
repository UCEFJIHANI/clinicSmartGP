from django.urls import path
from . import views

urlpatterns = [
    # stat page
    path('stats-page/', views.stats_page, name='stats_page'),
    path('change-stat-periode/', views.change_stat_periode,
      name='change_stat_periode'),
    path('change-stat-periode/', views.change_stat_periode,
      name='change_stat_periode'),
    path('show-periode/', views.show_periode,
      name='show_periode'),
    # add patient chart
    path('patient-chart-data/', views.patient_chart_data,
      name='patient_chart_data'),
    path('patient-chart/', views.patient_chart,
      name='patient_chart'),
    # patient categorie chart
    path('patient-categories-data/', views.patient_categories_data,
      name='patient_categories_data'),
    path('patient-categories-chart/', views.patient_categories_chart,
      name='patient_categories_chart'),
    # consultation chart
    path('consultation-chart-data/', views.consultation_chart_data,
      name='consultation_chart_data'),
    path('consultation-chart/', views.consultation_chart,
      name='consultation_chart'),
    # consultation categories
    path('consultation-categorie-data/', views.consultation_categorie_data,
      name='consultation_categorie_data'),
    path('consultation-categories/', views.consultation_categories,
        name='consultation_categories'),
    # payments categories
    path('payments-categorie-data/', views.payments_categorie_data,
      name='payments_categorie_data'),
    path('payments-categories/', views.payments_categories,
        name='payments_categories'),
    # payments par prestation
    path('payments-prestation-data/', views.payments_prestation_data,
      name='payments_prestation_data'),
    path('payments-prestation/', views.payments_prestation,
        name='payments_prestation'),
    ]
