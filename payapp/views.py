from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView

from payapp.models import Transaction, TransactionRequest


class TransactionListView(ListView):

    def get_queryset(self):
        return Transaction.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user))


class TransactionDetailView(DetailView):

    def get_object(self, queryset=None):
        return get_object_or_404(
            Transaction.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user)),
            pk=self.kwargs['pk']
        )


class TransactionCreateView(View):

    def get(self, queryset=None):
        pass

    def post(self, request):
        pass


class TransactionRequestListView(ListView):

    def get_queryset(self):
        return TransactionRequest.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user))


class TransactionRequestDetailView(DetailView):

    def get_object(self, queryset=None):
        return get_object_or_404(
            TransactionRequest.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user)),
            pk=self.kwargs['pk']
        )


class TransactionRequestCreateView(View):

    def get(self, queryset=None):
        pass

    def post(self, request):
        pass


class TransactionRequestUpdateView(View):

    def get(self, queryset=None):
        pass

    def post(self, request):
        pass
