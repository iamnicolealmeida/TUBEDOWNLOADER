import os
import subprocess
import sys
import time
from yt_dlp import YoutubeDL

# Cores em arco-íris
rainbow_colors = [
    "\033[91m",  # Vermelho
    "\033[93m",  # Amarelo
    "\033[92m",  # Verde
    "\033[96m",  # Ciano
    "\033[94m",  # Azul
    "\033[95m",  # Magenta
]

# Outra paleta de cores para a barra de carregamento alternativa
alternative_colors = [
    "\033[92m",  # Verde
    "\033[94m",  # Azul
    "\033[93m",  # Amarelo
    "\033[95m",  # Magenta
]

class Colors:
    RED = "\033[91m"
    GREEN = "\033[92m"
    BLUE = "\033[94m"
    YELLOW = "\033[93m"
    BOLD = "\033[1m"
    RESET = "\033[0m"

def clear_screen():
    """Limpa a tela e exibe a marca."""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{get_colored_name('Powered by Nicole')}")
    print("\n")  # Adiciona uma linha após a marca

def get_colored_name(name):
    """Retorna o nome colorido em arco-íris."""
    colored_name = ""
    for i, char in enumerate(name):
        colored_name += f"{rainbow_colors[i % len(rainbow_colors)]}{char}"
    return colored_name + "\033[0m"  # Resetar cor ao final

def loading_bar_alternative(downloaded_bytes, total_bytes):
    """Mostra uma barra de carregamento colorida com outra paleta."""
    bar_length = 50
    percent = (downloaded_bytes / total_bytes) * 100
    num_hashes = int(percent / 2)
    
    bar = ''.join(alternative_colors[j % len(alternative_colors)] + '#' for j in range(num_hashes))
    bar += '-' * (bar_length - num_hashes)  # Espaços restantes na barra
    print(f"\r{Colors.BLUE}{Colors.BOLD}[{bar}] {percent:.2f}% | Tamanho total: {total_bytes / (1024 * 1024):.2f} MB", end="")

def loading_bar_rainbow(total_size):
    """Mostra uma barra de carregamento colorida em arco-íris."""
    bar_length = 50
    for downloaded_bytes in range(total_size + 1):
        percent = (downloaded_bytes / total_size) * 100
        num_hashes = int(percent / 2)
        bar = ''.join(rainbow_colors[j % len(rainbow_colors)] + '#' for j in range(num_hashes))
        bar += '-' * (bar_length - num_hashes)  # Espaços restantes na barra
        print(f"\r{Colors.GREEN}{Colors.BOLD}[{bar}] {percent:.2f}% | ", end="")
        time.sleep(0.1)  # Simular o tempo de download
    print()  # Nova linha após a barra

def install(package):
    """Instala o pacote usando pip."""
    print(f"{Colors.BLUE}Instalando {package}...{Colors.RESET}")
    loading_bar_rainbow(100)  # Exibe uma barra de carregamento por 3 segundos
    # Redireciona a saída para evitar mensagens do CMD
    subprocess.check_call([sys.executable, "-m", "pip", "install", package], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def check_and_install_packages():
    """Verifica se os pacotes estão instalados e os instala se não estiverem."""    
    required_packages = ["yt-dlp"]
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            print(f"{Colors.RED}{Colors.BOLD}{package} não está instalado.{Colors.RESET}")
            install_prompt = input(f"{Colors.YELLOW}Pretende instalar {Colors.BOLD}{package}? [s/n]: {Colors.RESET}")
            if install_prompt.lower() == 's':
                install(package)
                time.sleep(1)
                print(f"{Colors.GREEN}{Colors.BOLD}{package} instalado com sucesso!{Colors.RESET}")
                print(f"{Colors.YELLOW}{Colors.BOLD}\nPor favor aguarde...{Colors.RESET}")
                time.sleep(5)
            else:
                print(f"{Colors.RED}{Colors.BOLD}Instalação de {package} cancelada. O programa não funcionará corretamente.{Colors.RESET}")
                sys.exit(1)
        else:
            print(f"{Colors.GREEN}{Colors.BOLD}{package} já está instalado.{Colors.RESET}")

# Limpar a tela no início
clear_screen()

# Verificar e instalar pacotes antes de continuar
check_and_install_packages()

# Limpar a tela novamente
clear_screen()

# Função para solicitar o nome da pasta
def get_folder_name():
    while True:
        folder_name = input(f'{Colors.BLUE}{Colors.BOLD}Nome da pasta para salvar o vídeo: {Colors.RESET}')
        folder_path = os.path.join(os.path.expanduser("~"), "Downloads", folder_name)
        
        if os.path.exists(folder_path):
            choice = input(f"{Colors.YELLOW}A pasta '{folder_name}' já existe.\nDeseja:\n[1] Usar a pasta existente\n[2] Criar uma nova pasta\n=» {Colors.RESET}")
            if choice == '1':
                return folder_path
            elif choice == '2':
                continue
            else:
                print(f"{Colors.RED}Opção inválida. Tente novamente.{Colors.RESET}")
        else:
            return folder_path

def download_video(video_url, folder_path):
    """Função para fazer o download do vídeo e mostrar a barra de carregamento."""
    def hook(d):
        """Função de gancho para monitorar o progresso do download."""
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes', None)
            downloaded_bytes = d.get('downloaded_bytes', None)
            if total_bytes and downloaded_bytes:
                loading_bar_alternative(downloaded_bytes, total_bytes)  # Chama a barra de carregamento alternativa com o tamanho total
        elif d['status'] == 'finished':
            print("\nDownload finalizado!")

    # Definir as opções de download
    ydl_opts = {
        'format': 'best',  # Melhor qualidade
        'noplaylist': True,  # Não baixar playlists
        'outtmpl': os.path.join(folder_path, '%(title)s.%(ext)s'),  # Caminho e nome do arquivo
        'quiet': True,  # Oculte mensagens de log
        'progress_hooks': [hook],
    }

    print(f"{Colors.BLUE}{Colors.BOLD}Iniciando o download do vídeo...{Colors.RESET}")
    
    # Chama a função de download
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

def main():
    while True:
        # Limpar a tela antes de solicitar o link do vídeo
        clear_screen()
        
        # Solicitar o link do vídeo
        while True:
            video_url = input(f'{Colors.BLUE}{Colors.BOLD}Link do vídeo: {Colors.RESET}')
            if not video_url.startswith("https://www.youtube.com/"):
                print(f"{Colors.RED}Por favor, insira um link válido do YouTube.{Colors.RESET}")
                continue
            break

        # Limpar a tela
        clear_screen()

        # Obter o caminho da pasta
        folder_path = get_folder_name()

        # Criar a pasta se não existir
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            print(f"{Colors.GREEN}{Colors.BOLD}Pasta '{os.path.basename(folder_path)}' criada em: {folder_path}{Colors.RESET}")

        time.sleep(1)  # Espera antes de continuar

        # Limpar a tela antes de iniciar o download
        clear_screen()

        # Fazer o download do vídeo
        download_video(video_url, folder_path)

        # Mensagem de sucesso
        print(f"{Colors.GREEN}{Colors.BOLD}Download concluído com sucesso!{Colors.RESET}")

        # Perguntar se o usuário deseja baixar outro vídeo
        again = input(f"{Colors.YELLOW}Deseja baixar outro vídeo? [s/n]: {Colors.RESET}")
        if again.lower() != 's':
            despedida = 'Obrigada por usar o programa!'
            print(get_colored_name(despedida))
            break

if __name__ == "__main__":
    main()
