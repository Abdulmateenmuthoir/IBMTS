from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('attendees', '0002_attendee_payment_fields')]

    operations = [
        migrations.AlterField(
            model_name='attendee',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
