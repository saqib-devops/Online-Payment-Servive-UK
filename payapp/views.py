from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView

from payapp.models import Transaction, TransactionRequest
from register.models import User

""" TRANSACTION VIEWS"""


class DashboardTemplateView(TemplateView):
    template_name = 'payapp/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(DashboardTemplateView, self).get_context_data(**kwargs)
        transactions = Transaction.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user))
        context['recent_transactions'] = transactions[0:10]
        context['total_transactions'] = transactions.count()
        context['total_amount'] = User.objects.get(id=self.request.user.id)
        return context


class TransactionListView(ListView):
    template_name = 'payapp/dashboard.html'
    context_object_name = 'objects'

    def get_queryset(self):
        return Transaction.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user))


class TransactionDetailView(DetailView):

    def get_object(self, queryset=None):
        return get_object_or_404(
            Transaction.objects.filter(Q(sender=self.request.user) | Q(receiver=self.request.user)),
            pk=self.kwargs['pk']
        )


class TransactionCreateView(View):
    template_name = ''

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        amount = request.POST.get('amount')

        # IF: missing parameters
        if not email or not amount:
            messages.warning(request, "Email or Amount is missing")
            return redirect('payapp:transaction-create')

        receiver = User.objects.filter(email=email)

        # IF: no receiver
        if not receiver:
            messages.error(request, "User doesn't exists with this email address")
            return redirect('payapp:transaction-create')

        sender = request.user
        receiver = receiver[0]

        # IF: same user
        if receiver == sender:
            messages.warning(request, "You can't sent amounts to yourself")
            return redirect('payapp:transaction-create')

        # IF: amount issue
        if sender.total_amount <= float(amount):
            messages.warning(request, "In sufficient balance to perform this transaction")
            return redirect('payapp:transaction-create')

        # ADD: transaction
        Transaction.objects.create(sender=sender, receiver=receiver, amount=amount)

        receiver.total_amount += float(amount)
        receiver.save()

        sender.total_amount -= float(amount)
        sender.save()

        messages.success(request, "Amount Transferred successfully.")
        return redirect('payapp:transactions')


""" TRANSACTION REQUEST VIEWS"""


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
    template_name = ''

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        amount = request.POST.get('amount')

        # IF: no status parameter
        if not email or not amount:
            messages.warning(request, "Email or Amount is missing")
            return redirect('payapp:request-create')

        # IF: receiver not available
        request_from = User.objects.filter(email=email)
        if not request_from:
            messages.error(request, "User doesn't exists with this email address")
            return redirect('payapp:request-create')

        request_to = request.user
        request_from = request_from[0]

        # IF: same user
        if request_from == request_to:
            messages.warning(request, "You can't request amounts from yourself")
            return redirect('payapp:request-create')

        # SUCCESS: create transaction
        TransactionRequest.objects.create(sender=request_to, receiver=request_from, amount=amount)
        messages.success(request, "Your transactions request added successfully")
        return redirect('payapp:requests')


class TransactionRequestUpdateView(View):
    template_name = ''

    def get(self, request, pk):
        transaction_request = get_object_or_404(
            TransactionRequest.objects.filter(receiver=request.user, status='pending'), pk=pk
        )

        return render(request, self.template_name)

    def post(self, request, pk):

        # IF: no status parameter
        status = request.GET.get('status')

        # IF: get transaction or 404
        transaction_request = get_object_or_404(
            TransactionRequest.objects.filter(receiver=request.user, status='pending'), pk=pk
        )
        sender = transaction_request.receiver
        receiver = transaction_request.sender
        amount = transaction_request.amount

        # IF: wrong parameter
        if status not in ['approved', 'cancel']:
            messages.warning(request, "Some parameters are missing")
            return redirect('payapp:request-update')

        # IF: sender amount is less
        if amount > sender.total_amount:
            messages.warning(request, "In sufficient balance to perform this transaction")
            return redirect('payapp:request-update')

        # ADD: transaction
        Transaction.objects.create(
            sender=sender, receiver=receiver, amount=amount
        )

        # UPDATE: request
        transaction_request.status = 'accepted'
        transaction_request.save()

        # UPDATE: sender and receiver amounts
        sender.total_amount -= amount
        sender.save()
        receiver.total_amount += amount
        receiver.save()

        # SUCCESS: message and redirect
        messages.success(request, "Request approved and transaction performed successfully")
        return redirect('payapp:requests')
