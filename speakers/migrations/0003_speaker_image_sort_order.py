from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('speakers', '0002_speaker_display_fields')]
    operations = [
        migrations.AddField(model_name='speaker', name='image', field=models.ImageField(blank=True, upload_to='speakers/')),
        migrations.AddField(model_name='speaker', name='sort_order', field=models.PositiveIntegerField(default=0)),
    ]
