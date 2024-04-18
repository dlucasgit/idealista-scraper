"""
This module defines the `main()` coroutine for the Apify Actor, executed from the `__main__.py` file.

Feel free to modify this file to suit your specific needs.

To build Apify Actors, utilize the Apify SDK toolkit, read more at the official documentation:
https://docs.apify.com/sdk/python
"""

from urllib.parse import urljoin
from playwright.async_api import async_playwright
from apify import Actor
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time
import asyncio
import re

# To run this Actor locally, you need to have the Playwright browsers installed.
# Run `playwright install --with-deps` in the Actor's virtual environment to install them.
# When running on the Apify platform, they are already included in the Actor's Docker image.


async def main(page_url, filename) -> None:

    """
    The main coroutine is being executed using `asyncio.run()`, so do not attempt to make a normal function
    out of it, it will not work. Asynchronous execution is required for communication with Apify platform,
    and it also enhances performance in the field of web scraping significantly.
    """
    async with Actor:
        async with async_playwright() as p:

            # FUNCIONS
            async def obtenir_num_propietats(page):
                try:
                    # Obtener el HTML de la página
                    html_content = await page.content()

                    # Crear un objeto BeautifulSoup para analizar el HTML
                    soup = BeautifulSoup(html_content, 'html.parser')

                    # Utilizar el método find() o select_one() para encontrar el primer elemento <h1>
                    h1_element = soup.find('h1')  # O también puedes usar soup.select_one('h1')
                    print(h1_element.text)
                    # Verificar si se encontró el elemento <h1>
                    if h1_element:
                        # Capturar el texto dentro del elemento <h1>
                        h1_text = h1_element.text.strip()  # Utiliza .strip() para eliminar espacios en blanco adicionales

                        # Utilizar una expresión regular para extraer solo los números
                        numeros = re.findall(r'\d+', h1_text)

                        # Convertir la lista de números a una cadena
                        numeros_str = ''.join(numeros)

                        print(f'Hi ha {numeros_str} propietats')
                        return numeros_str
                    else:
                        return "No se encontró ningún elemento <h1> en la página."
                except Exception as e:
                    print(f"Error: {e}")
                    return None

            # Creamos una función para extraer los datos de una página
            async def extract_data_from_page(page, n_prop, link):
                try:
                    filtres = "aire acondicionado - 2 hab - 2 lavabos"
                    poblacio = "Barcelona"
                    districte = "Eixample"
                    data_extraccio = datetime.datetime.now().date()
                    # pisos = page.locator('div[class="item-info-container"]').all()
                    # amb xpath completo
                    pisos = await page.locator('article').filter(has=page.locator('//div/div[@class="price-row"]')).all()
                    num_propietats = len(pisos)
                    print(f'Hi ha: {num_propietats} pisos.')

                    pisos_list = []
                    volta = 1

                    for pis in pisos:
                        print(f'Hotel: {volta}')
                        pis_dict = {}
                        pis_dict['poblacio'] = poblacio
                        pis_dict['districte'] = districte

                        locator_preus = pis.locator('//div/div[@class="price-row"]')

                        preus = await locator_preus.all_inner_texts()
                        # preu_sense_simbol = preu[2:]
                        preu = preus[0]
                        pis_dict['preu'] = preu
                        pis_dict['filtres'] = filtres
                        print(preu)
                        pis_dict['num_propietats'] = n_prop
                        pis_dict['data'] = data_extraccio
                        pis_dict['link'] = link
                        pisos_list.append(pis_dict)
                        volta += 1
                except TimeoutError:
                    print("TimeoutError: S'ha excedit el temps dins la funcio")
                    return pisos_list
                return pisos_list
            # Aquesta funcio retorna el dia de la setmana d'avui en catala: DILLUNS, DIMARTS, ETC.
            """def obtenir_dia_setmana(data):
                dias_semana = ["Dilluns", "Dimarts", "Dimecres", "Dijous", "Divendres", "Dissabte", "Diumenge"]
                dia_numero = data.weekday()
                return dias_semana[dia_numero]
            # Aquesta funcio sempre retorna la data del proper divendres
            def obtenir_data_entrada(dia_setmana):
                data = datetime.datetime.now().date()
                if dia_setmana == "Dilluns":
                    data_entrada = data + datetime.timedelta(days=4)
                elif dia_setmana == "Dimarts":
                    data_entrada = data + datetime.timedelta(days=3)
                elif dia_setmana == "Dimecres":
                    data_entrada = data + datetime.timedelta(days=2)
                elif dia_setmana == "Dijous":
                    data_entrada = data + datetime.timedelta(days=1)
                elif dia_setmana == "Divendres":
                    data_entrada = data
                elif dia_setmana == "Dissabte":
                    data_entrada = data + datetime.timedelta(days=6)
                elif dia_setmana == "Diumenge":
                    data_entrada = data + datetime.timedelta(days=5)
                return data_entrada
            """
            # FINAL FUNCIONS

            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()

            page = await context.new_page()
            # Iteramos a través de las páginas de resultados
            all_pisos = []
            page_number = 1
            await page.goto(page_url)
            await asyncio.sleep(15)
            cookies_container = page.locator('div[data-testid="notice"]')

            # encara l'he de provar
            # button_aceptar = cookies_container.locator('button[aria-label="Aceptar y cerrar: Aceptar nuestro procesamiento de datos y cerrar"]')

            # encara l'he de provar
            button_aceptar = cookies_container.locator('//div/div[2]') # Aquest funciona

            # button_aceptar = page.locator('/html/body/div[1]/div/div/div/div/div[2]/button[3]')
            await asyncio.sleep(1)
            await button_aceptar.click()
            #page.get_by_role('button', name='Aceptar y continuar').click()

            i = 1
            await asyncio.sleep(3)
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(3)

            # Obtenir numero de propietats
            n_propietats = await obtenir_num_propietats(page)

            # Fer scroll fins a baix de tot de la pantalla per a que es carregui tota la pagina
            #page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

            print("Entro al bucle")

            j = 1
            while True:
                try:
                    print(f'Carrego pagina: {j}')

                    await asyncio.sleep(5)

                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

                    await page.wait_for_selector('article')
                    pisos_on_page = await extract_data_from_page(page, n_propietats, page_url)
                    j = j+1
                    if not pisos_on_page:
                        break  # Si no hay más hoteles en la página, terminamos el bucle

                    all_pisos.extend(pisos_on_page)
                    page_number += 1
                    print("Ja he executat la funcio, ara a comprobar si hi ha siguiente. Si no n'hi ha a exportar i tancar")
                    await asyncio.sleep(3)
                    # Hacemos clic en el botón "Siguiente" para avanzar a la siguiente página
                    try:
                        await page.get_by_role('link', name='Siguiente').click()
                        # Assigno la url de la següent pagina a la variable per tornar a fer scraper
                        page_url = page.url
                        await page.goto(page_url)
                        await asyncio.sleep(5)  # Esperamos un breve tiempo para que cargue la siguiente página
                    except:
                        print("No hi ha mes botons de 'Siguiente', sortim del bucle")
                        break  # Si no hay más botones de "Siguiente", terminamos el bucle

                except TimeoutError:
                    print("Se ha excedido el tiempo de espera. Intentando cargar la página nuevamente...")
                    continue  # Intentamos cargar la página nuevamente

            if len(all_pisos) > 0 :
                # Convertimos todos los datos recopilados en un DataFrame de Pandas
                ruta = "/storage/datasets/default/"
                df = pd.DataFrame(all_pisos)
                dades = df.to_json()
                await Actor.push_data(dades)
                # Guardamos los datos en archivos CSV y Excel
                df.to_excel(f'{filename}.xlsx', index=False)
                df.to_csv(f'{filename}.csv', index=False)
                #df.to_excel(f'{filename}.xlsx', index=False)
                #df.to_csv(f'{filename}.csv', index=False)
                print("Exportant dades i tancant el programa")
            else:
                print("Tancant el programa")

            await browser.close()
