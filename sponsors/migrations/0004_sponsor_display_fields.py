from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('sponsors', '0003_alter_sponsor_sponsorship_tier')]
    operations = [
        migrations.AddField(model_name='sponsor', name='display_on_site', field=models.BooleanField(default=False)),
        migrations.AddField(model_name='sponsor', name='logo_url', field=models.URLField(blank=True, help_text='Public logo URL shown on the website')),
    ]
