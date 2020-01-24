###########################################################################################
##########SCRAPING DE L'ANNUAIRE DES SOCIETES DIGITALES SUR LE SITE DE L'USINE DIGITALE####
###########################################################################################

#### SITE INTERNET SCRAPPÉ : www.usine-digitale.fr/annuaire-start-up
#### utilisation du package concurrent.futures pour permettre le multithread

import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import concurrent.futures
# liste contenant toutes les pages web de l'annuaire jusqu'à la page 200 sur mon navigateur
links = ['https://www.usine-digitale.fr/annuaire-start-up/' +
         str(i) + '/' for i in range(1, 258)]
# liste de toutes les requêtes sur chaque société en mode tuple
# pour permettre conversion en dataframe
records = []


def scrap_usinenouvelle(links):
    # reqête sur page l'annuaire links (pages 1 à 258 ici)
    src2 = requests.get(links).text
    soup2 = BeautifulSoup(src2, 'lxml')
    # récupération du contenu ou se trouve les adresses qui renvoient à la page web des infos sur chaque société
    content_links = soup2.find_all('a', class_='contenu')

    # loop pour aller sur chaque page web de chaque société
    for link in content_links:
        href_ = 'https://www.usine-digitale.fr/annuaire-start-up' + \
            link.get('href')

        src_in = requests.get(href_).text
        soup_in = BeautifulSoup(src_in, 'lxml')
        # clause except  pour gérer les reqêtes vides et empêcher error raises
        try:
            soup_in.find('div', class_='deco').find(
                'p', itemprop='telephone').text
        except(AttributeError, TypeError):
            telephone = ''
        else:
            telephone = soup_in.find('div', class_='deco').find(
                'p', itemprop='telephone').text
        try:
            soup_in.find('a', itemprop='sameAs')['href']
        except(AttributeError, TypeError):
            siteweb = ''
        else:
            siteweb = soup_in.find(
                'a', itemprop='sameAs')['href']
        try:
            nom_societe = soup_in.find('h1', itemprop='name').text
        except(AttributeError, TypeError):
            nom_societe = ''
        else:
            nom_societe = soup_in.find('h1', itemprop='name').text
        try:
            re.sub(r'(\r\n\t)|(\xa0|\n)|(\n)', '', soup_in.find(
                'div', itemprop='description').text)
        except(AttributeError, TypeError):
            presentation = ''
        else:
            presentation = re.sub(r'(\r\n\t)|(\xa0|\n)|(\n)', '', soup_in.find(
                'div', itemprop='description').text)
        try:
            re.sub(r'(\r\n\t)|(\xa0|\n)|(\n)', '',
                   soup_in.find('div', itemprop='review').text)
        except(AttributeError, TypeError):
            genese = ''
        else:
            genese = re.sub(r'(\r\n\t)|(\xa0|\n)|(\n)', '',
                            soup_in.find('div', itemprop='review').text)
        try:
            re.sub(r'(\r\n\t)|(\xa0|\n)|(\n)', '', soup_in.find(
                'div', itemprop='makesOffer').text)
        except(AttributeError, TypeError):
            produits = ''
        else:
            produits = re.sub(r'(\r\n\t)|(\xa0|\n)|(\n)', '',
                              soup_in.find('div', itemprop='makesOffer').text)
        try:
            re.sub(r'(\r\n\t)|(\xa0|\n)|(\n)', '', soup_in.find(
                string='Marché :').next_element.next_element.text)
        except(AttributeError, TypeError):
            marche = ''
        else:
            marche = re.sub(r'(\r\n\t)|(\xa0|\n)|(\n)', '', soup_in.find(
                string='Marché :').next_element.next_element.text)
        try:
            re.sub(r'(\r\n\t)|(\xa0|\n)|(\n)', '',
                   soup_in.find('div', itemprop='founders').text)
        except(AttributeError, TypeError):
            createurs = ''
        else:
            createurs = re.sub(r'(\r\n\t)|(\xa0|\n)|(\n)', '',
                               soup_in.find('div', itemprop='founders').text)
        try:
            re.sub(r'(\r\n\t)|(\xa0|\n)|(\n)', '',
                   soup_in.find('div', itemprop='address').text)
        except(AttributeError, TypeError):
            implantation = ''
        else:
            implantation = re.sub(r'(\r\n\t)|(\xa0|\n)|(\n)', '', soup_in.find(
                'div', itemprop='address').text)
        try:
            soup_in.find(
                'div', class_='titreInfo').next_element.next_element.next_element.text
        except(AttributeError, TypeError):
            date_creation = ''
        else:
            date_creation = soup_in.find(
                'div', class_='titreInfo').next_element.next_element.next_element.text
        try:
            adresse = re.sub(r'(\d\d\d\d\d\s\w+\s)', "", soup_in.find('div',
                                                                      class_='deco').find('p', itemprop='address').text)
        # code postal
            cp_search = soup_in.find('div', class_='deco').find(
                'p', itemprop='address').text
            cp = re.compile(r'(\d\d\d\d\d)')
            code_postal = cp.findall(cp_search)
        except(AttributeError, TypeError):
            code_postal = ''
        else:
            code_postal = cp.findall(cp_search)
        try:
            soup_in.find('div', class_='deco').find('p', itemprop='email').text
        except(AttributeError, TypeError):
            email = ''
        else:
            email = soup_in.find('div', class_='deco').find(
                'p', itemprop='email').text

        records.append((nom_societe, presentation, genese, produits, marche, createurs, implantation,
                        date_creation, adresse, code_postal, telephone, email, siteweb))

    df6 = pd.DataFrame(records, columns=['nom_societe', 'presentation', 'genese', 'produits',
                                         'marche', 'createurs', 'implantation', 'date_creation',
                                         'adresse', 'code_postal', 'telephone', 'email', 'siteweb'])
    df6.to_csv('annuaire_usine_nouvelle_essai4.csv')
    return df6.info()


# clause multi thread qui va permettre de looper à travers plusieurs
# liens de la liste links en même temps
with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.map(scrap_usinenouvelle, links)
#
