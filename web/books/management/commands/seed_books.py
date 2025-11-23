from django.core.management.base import BaseCommand
from books.models import Book
from faker import Faker


class Command(BaseCommand):
    help = 'Create fake books for testing'

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=20, help='Number of books to create')

    def handle(self, *args, **options):
        fake = Faker()
        count = options['count']

        self.stdout.write(f'Creating {count} fake books...')

        for i in range(count):
            book = Book(
                title=fake.sentence(nb_words=4).replace('.', ''),
                author=fake.name(),
                summary=fake.paragraph(nb_sentences=2),
                tags=', '.join(fake.words(nb=3)),
                published_date=fake.date_between(start_date='-20y', end_date='today')
            )
            book.save()

            if (i + 1) % 10 == 0:
                self.stdout.write(f'Created {i + 1} books...')

        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} books!'))
