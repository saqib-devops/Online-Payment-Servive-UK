from django.urls import path

from .views import (
    TransactionListView, TransactionCreateView,
    TransactionRequestListView, TransactionRequestCreateView, TransactionRequestUpdateView,
    CurrencyConversionAPI, DashboardTemplateView
)


app_name = 'payapp'
urlpatterns = [

    path('dashboard/', DashboardTemplateView.as_view(), name='dashboard'),
    path('transaction/', TransactionListView.as_view(), name='transactions'),
    path('transaction/create/', TransactionCreateView.as_view(), name='transaction-create'),

    path('request/', TransactionRequestListView.as_view(), name='requests'),
    path('request/create/', TransactionRequestCreateView.as_view(), name='request-create'),
    path('request/<int:pk>/update/', TransactionRequestUpdateView.as_view(), name='request-update'),
    path(
        'conversion/<str:currency1>/<str:currency2>/<str:amount>/',
        CurrencyConversionAPI.as_view(), name='currency-conversion-api'
    )

]
