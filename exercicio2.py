import requests
import concurrent.futures
import csv
import time

from bs4 import BeautifulSoup

# URL da página com a lista dos filmes
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
url = "https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm"


filmes = []
def extract_movies_details(li):
    # Coleta o título e a classificação de cada filme
    global filmes 

    # Encontra o elemento <a> com a classe "title"
    a = li.find("h3", class_="ipc-title__text")
    title = a.text

    # Encontra o elemento <div> com a classe "rating"
    div = li.find("div", class_="sc-94da5b1b-0 soBIM meter-const-ranking sc-479faa3c-6 glWBvR cli-meter-title-header")
    rating = div.text

    # Cria um dicionário com as informações do filme
    filme = {"titulo": title, "classificacao": rating}

    # Adiciona o dicionário à lista de filmes
    filmes.append(filme)


MAX_THREADS = 5


def extract_movies():
    # Faz a requisição da página
    response = requests.get(url, headers=headers)

    # Extrai o conteúdo da página
    html = response.content

    # Cria um objeto BeautifulSoup para parsear o conteúdo da página
    soup = BeautifulSoup(html, "html.parser")

    # Encontra a tag <ul> com a classe "ipc-metadata-list ipc-metadata-list--dividers-between sc-9d2f6de0-0 iMNUXk compact-list-view ipc-metadata-list--base"
    ul = soup.find("ul", class_="ipc-metadata-list ipc-metadata-list--dividers-between sc-9d2f6de0-0 iMNUXk compact-list-view ipc-metadata-list--base")

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        executor.map(extract_movies_details, ul.find_all("li"))

    # Abre o arquivo CSV para escrita
    with open("./filmes.csv", "w", newline="") as f:

        # Cria um escritor CSV
        writer = csv.writer(f)

        # Escreve as informações dos filmes no CSV
        for filme in filmes:
            writer.writerow([filme["titulo"], filme["classificacao"]])



def main():
    start_time = time.time()

    # Main function to extract the 100 movies from IMDB Most Popular Movies
    extract_movies()

    end_time = time.time()
    print('Total time taken: ', end_time - start_time)


if __name__ == '__main__':
    main()
