from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from speakers.models import Speaker


class Command(BaseCommand):
    help = 'Seed IBMTS speaker slots using the six existing website images.'

    def handle(self, *args, **options):
        images_dir = Path(settings.BASE_DIR) / 'static' / 'images'
        for number in range(1, 7):
            speaker, _ = Speaker.objects.update_or_create(
                email=f'speaker{number}@ibmts.local',
                defaults={
                    'name': f'Speaker {number} — To Be Announced',
                    'phone': '',
                    'topic': 'To be announced',
                    'bio': '',
                    'display_title': 'IBMTS 2027 Speaker',
                    'status': 'approved',
                    'display_on_site': True,
                    'sort_order': number,
                },
            )
            image_path = images_dir / f'speaker-{number}.jpg'
            if image_path.exists() and not speaker.image:
                with image_path.open('rb') as image_file:
                    speaker.image.save(image_path.name, File(image_file), save=True)
        self.stdout.write(self.style.SUCCESS('Seeded six IBMTS speaker image records.'))
