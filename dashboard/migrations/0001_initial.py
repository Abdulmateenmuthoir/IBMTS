from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(name='Testimonial', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(max_length=255)), ('role', models.CharField(max_length=255)),
            ('quote', models.TextField()), ('photo_url', models.URLField(blank=True)),
            ('display_on_site', models.BooleanField(default=True)), ('created_at', models.DateTimeField(auto_now_add=True)),
        ]),
        migrations.CreateModel(name='TeamMember', fields=[
            ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ('name', models.CharField(max_length=255)), ('role', models.CharField(max_length=255)),
            ('photo_url', models.URLField(blank=True)), ('display_on_site', models.BooleanField(default=True)),
            ('sort_order', models.PositiveIntegerField(default=0)),
        ], options={'ordering': ('sort_order', 'name')}),
    ]
