from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('attendees', '0001_initial')]

    operations = [
        migrations.AddField(
            model_name='attendee', name='is_paid',
            field=models.BooleanField(default=True), preserve_default=False,
        ),
        migrations.AddField(model_name='attendee', name='ticket_amount', field=models.PositiveIntegerField(default=0, help_text='Amount in naira')),
        migrations.AddField(model_name='attendee', name='payment_reference', field=models.CharField(blank=True, max_length=100, null=True, unique=True)),
        migrations.AddField(model_name='attendee', name='payment_transaction_id', field=models.CharField(blank=True, max_length=100)),
        migrations.AddField(model_name='attendee', name='payment_status', field=models.CharField(default='pending', max_length=20)),
        migrations.AddField(model_name='attendee', name='paid_at', field=models.DateTimeField(blank=True, null=True)),
        migrations.AddField(model_name='attendee', name='registration_email_sent', field=models.BooleanField(default=False)),
    ]
