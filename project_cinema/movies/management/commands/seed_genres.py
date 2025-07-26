from django.core.management.base import BaseCommand
from movies.models import Genre


class Command(BaseCommand):
    help = 'Insere gêneros iniciais no banco de dados'

    def handle(self, *args, **options):
        # Lista de gêneros para inserir
        genres_data = [
            {'name': 'Ação', 'description': 'Filmes com sequências de ação, aventura e adrenalina'},
            {'name': 'Comédia', 'description': 'Filmes humorísticos e divertidos'},
            {'name': 'Drama', 'description': 'Filmes dramáticos com foco em desenvolvimento de personagens'},
            {'name': 'Terror', 'description': 'Filmes de horror e suspense'},
            {'name': 'Ficção Científica', 'description': 'Filmes futuristas e de ficção científica'},
            {'name': 'Romance', 'description': 'Filmes românticos e histórias de amor'},
            {'name': 'Thriller', 'description': 'Filmes de suspense e tensão'},
            {'name': 'Aventura', 'description': 'Filmes de aventura e exploração'},
            {'name': 'Animação', 'description': 'Filmes animados para todas as idades'},
            {'name': 'Documentário', 'description': 'Documentários e filmes baseados em fatos reais'},
            {'name': 'Fantasia', 'description': 'Filmes de fantasia e mundos imaginários'},
            {'name': 'Musical', 'description': 'Filmes musicais com canções e danças'},
            {'name': 'Crime', 'description': 'Filmes policiais e de investigação criminal'},
            {'name': 'Guerra', 'description': 'Filmes sobre conflitos bélicos e guerra'},
            {'name': 'Western', 'description': 'Filmes de faroeste e velho oeste'},
        ]

        created_count = 0
        existing_count = 0

        for genre_data in genres_data:
            genre, created = Genre.objects.get_or_create(
                name=genre_data['name'],
                defaults={'description': genre_data['description']}
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Gênero "{genre.name}" criado com sucesso')
                )
            else:
                existing_count += 1
                self.stdout.write(
                    self.style.WARNING(f'⚠ Gênero "{genre.name}" já existe')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'\n📊 Resumo:'
                f'\n   • {created_count} gêneros criados'
                f'\n   • {existing_count} gêneros já existiam'
                f'\n   • Total de gêneros no banco: {Genre.objects.count()}'
            )
        )