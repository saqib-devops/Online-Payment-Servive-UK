from django.urls import path

from .views import (
    TransactionListView, TransactionDetailView,  TransactionCreateView,
    TransactionRequestListView, TransactionRequestCreateView, TransactionRequestUpdateView, TransactionRequestDetailView
)


app_name = 'payapp'
urlpatterns = [

    path('transaction/', TransactionListView.as_view(), name='transactions'),
    path('transaction/create/', TransactionCreateView.as_view(), name='transaction-create'),

    path('request/', TransactionRequestListView.as_view(), name='requests'),
    path('request/create/', TransactionRequestCreateView.as_view(), name='request-create'),
    path('request/<int:pk>/update/', TransactionRequestUpdateView.as_view(), name='request-update'),

]
