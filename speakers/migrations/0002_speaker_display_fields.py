from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [('speakers', '0001_initial')]
    operations = [
        migrations.AddField(model_name='speaker', name='display_on_site', field=models.BooleanField(default=False)),
        migrations.AddField(model_name='speaker', name='display_title', field=models.CharField(blank=True, help_text='Role or session title shown on the website', max_length=255)),
        migrations.AddField(model_name='speaker', name='photo_url', field=models.URLField(blank=True, help_text='Public image URL shown on the website')),
    ]
