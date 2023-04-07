from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
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

    def get(self, request):
        pass


    def post(self, request):
        email = request.POST.get('email')
        amount = request.POST.get('amount')

        if not email or not amount:
            messages.warning(request, "Email or Amount is missing")

        receiver = User.objects.filter(email=email)
        if not receiver:
            messages.error(request, "User doesn't exists with this email address")

        sender = request.user
        receiver = receiver[0]
        if receiver == request.user:
            messages.warning(request, "You can't sent amounts to yourself")

        # TODO: user amount check
        # if user.total_amount <= float(amount):
        #     messages.warning(request, "In sufficient balance to perform this transaction")

        # TODO: Transaction

        Transaction.objects.create(sender=sender, receiver=receiver, amount=amount)
        Transaction.save()

        receiver.total_amount += float(amount)
        receiver.save()

        sender.total_amount -= float(amount)
        sender.save()

        messages.success(request, "Amount Transferred successfully.")
        return redirect('payapp:transactions')


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
