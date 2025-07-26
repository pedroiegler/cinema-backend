from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    help = 'Remove o arquivo de controle de setup para forçar nova inicialização'

    def handle(self, *args, **options):
        setup_flag = "/project_cinema/.setup_done"
        
        if os.path.exists(setup_flag):
            os.remove(setup_flag)
            self.stdout.write(
                self.style.SUCCESS('✅ Arquivo de controle removido. O setup será executado na próxima inicialização.')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠️  Arquivo de controle não encontrado. O setup já será executado na próxima inicialização.')
            )