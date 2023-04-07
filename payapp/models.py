from django.contrib.auth.models import User
from django.db import models


class Transaction(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_from')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_by')
    amount = models.FloatField()

    is_completed = models.FloatField()
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return f"Transferred {self.amount} from {self.sender.get_full_name()} to {self.receiver.get_full_name()}"


class TransactionRequest(models.Model):
    STATUS_CHOICE = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('cancelled', 'Cancelled'),
    )
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_from')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_to')
    amount = models.FloatField()

    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='pending')
    created_on = models.DateTimeField(auto_now_add=True)
    checked_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Transactions Requests'
        ordering = ['-created_on']

    def __str__(self):
        return f"Transferred {self.amount} from {self.sender.get_full_name()} to {self.receiver.get_full_name()}"
