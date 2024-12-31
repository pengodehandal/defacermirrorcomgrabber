
import requests
from bs4 import BeautifulSoup
import pyfiglet
from colorama import Fore, init

init(autoreset=True)

def get_page_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Terjadi kesalahan saat mengambil page: {e}")
        return None

def extract_domains(soup):
    links = soup.find_all('a', href=True)
    domains = set()

    for link in links:
        href = link['href']
        if "http" in href:
            domain = href.split('/')[2]
            if domain != "defacermirror.com":
                domains.add(domain)
    
    return domains

def save_domains_to_file(domains, filename):
    with open(filename, "a") as f:
        for domain in domains:
            f.write(domain + "\n")

def scrape_defacermirror(page_start, page_end, url_type, filename, category_name):
    total_domains_found = 0

    print(f"\nSedang menggrab data di kategori: {category_name}...\n")

    for page_number in range(page_start, page_end + 1):
        url = f"{url_type}{page_number}"

        print(f"Mengambil data dari halaman {page_number}")

        page_content = get_page_content(url)

        if page_content:
            soup = BeautifulSoup(page_content, 'html.parser')
            domains = extract_domains(soup)

            if domains:
                save_domains_to_file(domains, filename)
                total_domains_found += len(domains)
                print(f"Menemukan {len(domains)} domain di halaman {page_number}")
            else:
                print(f"Tidak ada domain ditemukan di halaman {page_number}.")
        else:
            print(f"Gagal mengambil konten dari halaman {page_number}. Proses selesai.")
            break
    
    print(f"\nTotal {total_domains_found} domain telah disimpan di {filename}")

def scrape_all():
    pages_to_scrape = [
        ("https://defacermirror.com/archive.php?page=", "semua.txt", "Archive"),
        ("https://defacermirror.com/onhold.php?page=", "semua.txt", "Onhold"),
        ("https://defacermirror.com/special.php?page=", "semua.txt", "Special")
    ]
    
    for base_url, filename, category_name in pages_to_scrape:
        page_start = 1
        page_end = 100
        
        print(f"\nMulai scraping untuk kategori {category_name}...\n")
        scrape_defacermirror(page_start, page_end, base_url, filename, category_name)

def display_menu():
    ascii_banner = pyfiglet.figlet_format("Simple Grabber DefacerMirror")
    print(Fore.CYAN + ascii_banner)
    print(Fore.YELLOW + "===========================================")
    print(Fore.GREEN + "PengodeHandal Scraper Tool - Grabber")
    print(Fore.YELLOW + "===========================================")
    print(Fore.WHITE + "1. Archive Grabber")
    print(Fore.WHITE + "2. Onhold Grabber")
    print(Fore.WHITE + "3. Special Grabber")
    print(Fore.WHITE + "4. Grab Semua (Archive, Onhold, Special)")
    print(Fore.YELLOW + "===========================================")
    print(Fore.CYAN + "Github : " + Fore.WHITE + "https://github.com/pengodehandal/defacermirrorcomgrabber/")
    print(Fore.YELLOW + "===========================================")

def main():
    display_menu()
    
    choice = input(Fore.CYAN + "Masukkan pilihan (1 untuk Archive, 2 untuk Onhold, 3 untuk Special, atau 4 untuk Grab Semua): ")

    if choice == '1':
        page_start = int(input("Masukkan page awal: "))
        page_end = int(input("Masukkan page akhir: "))
        scrape_defacermirror(page_start, page_end, "https://defacermirror.com/archive.php?page=", "defacermirrorarchive.txt", "Archive")
    elif choice == '2':
        page_start = int(input("Masukkan page awal: "))
        page_end = int(input("Masukkan page akhir: "))
        scrape_defacermirror(page_start, page_end, "https://defacermirror.com/onhold.php?page=", "defacermirroronhold.txt", "Onhold")
    elif choice == '3':
        page_start = int(input("Masukkan page awal: "))
        page_end = int(input("Masukkan page akhir: "))
        scrape_defacermirror(page_start, page_end, "https://defacermirror.com/special.php?page=", "defacermirrorspecial.txt", "Special")
    elif choice == '4':
        scrape_all()
    else:
        print(Fore.RED + "Pilihan tidak valid.")

if __name__ == '__main__':
    main()
