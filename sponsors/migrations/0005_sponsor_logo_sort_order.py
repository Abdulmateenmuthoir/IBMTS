from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('sponsors', '0004_sponsor_display_fields')]
    operations = [
        migrations.AddField(model_name='sponsor', name='logo', field=models.ImageField(blank=True, upload_to='sponsors/')),
        migrations.AddField(model_name='sponsor', name='sort_order', field=models.PositiveIntegerField(default=0)),
    ]
