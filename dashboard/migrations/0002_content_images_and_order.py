from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [('dashboard', '0001_initial')]
    operations = [
        migrations.AddField(model_name='testimonial', name='image', field=models.ImageField(blank=True, upload_to='testimonials/')),
        migrations.AddField(model_name='testimonial', name='sort_order', field=models.PositiveIntegerField(default=0)),
        migrations.AddField(model_name='teammember', name='image', field=models.ImageField(blank=True, upload_to='team/')),
    ]
