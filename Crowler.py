from selenium.webdriver.common.by import By
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
from itertools import zip_longest

driver = webdriver.Edge()

# Link do box do livro Trono de Vidro
url = "https://www.amazon.com.br/Box-Trono-Vidro-Acompanha-Marcadores/product-reviews/850130395X/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"

driver.get(url)

# Espera inicial para garantir que a página seja carregada
time.sleep(10)

# Lista para armazenar os dados
avaliacoes = []
comentarios = []

try:
    while len(avaliacoes) < 250:  # Continua até coletar 250 avaliações
        # Obtendo o conteúdo da página
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # Encontrar todas as estrelas da Avaliacao com a classe "a-icon-alt"
        star_div = soup.find_all("span", class_="a-icon-alt")

        # Encontrar todos os comentários com a classe "a-size-base review-text review-text-content"
        comentarios_div = soup.find_all("span", class_="a-size-base review-text review-text-content")

        # Adicionando as avaliações e comentários às listas
        for estrelas, comentario in zip_longest(star_div, comentarios_div, fillvalue=None):
            if estrelas:
                estrelas_texto = estrelas.get_text(strip=True)
                avaliacoes.append(estrelas_texto)
            else:
                avaliacoes.append('nulo')

            if comentario:
                comentario_texto = comentario.get_text(strip=True)
                comentarios.append(comentario_texto)
            else:
                comentarios.append('nulo')

        print(f"Coletadas {len(avaliacoes)} avaliações até agora.")

        # Tentar clicar no botão "Próximo"
        try:
            # Localizar o botão "Próximo" e clicar
            proximo_botao = driver.find_element(By.CLASS_NAME, 'a-last')
            proximo_botao.find_element(By.TAG_NAME, 'a').click()
            time.sleep(5)  # Espera o carregamento da nova página
        except Exception as e:
            print("Botão 'Próximo' não encontrado ou não é clicável:", e)
            break  # Se não encontrar o botão, sai do loop

# Tratativa de erro em casos de classes, span ou links não encontrados
except Exception as e:
    print(f"Ocorreu um erro: {e}")

finally:
    # Salvando os dados coletados em um arquivo CSV
    with open('avaliacoes_comentarios.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Avaliacao', 'Comentario'])  # Cabeçalho
        for aval, coment in zip(avaliacoes, comentarios):
            writer.writerow([aval, coment])

    driver.quit()
