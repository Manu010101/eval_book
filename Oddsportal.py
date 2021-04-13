import matplotlib.pyplot as plt

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from typing import List, Tuple

from BD import BD
from Glob import Glob


# Pour construire et tracer histogramme
def construit_histogramme(noms_tables: list[str], b_inf: float, b_sup: float) -> dict:
    """
    - Se connecte à la base de données où sont stockées les données issues de Oddsportal

    - Parcours des tables données dans noms_tables:

        - Récupère le nombre de fois où le favori gagne et le nombre de fois où la cote apparaît pour chaque valeur de cote.
            Donc avec la précision 0.01, celle des cotes

    - Retourne une liste qui, à chaque cote fait correspondre une liste [frequence_victoires, frequences apparitions
        de la cote]

    :param noms_tables:
    :param b_inf:
    :param b_sup:
    :return:
    """
    
    bd = BD(base_donnees=Glob.NOM_BD_SIMU)
    
    valeur_cote = b_inf
    pas = 0.01
    
    li_cotes = []
    li_freqs_apparition = []  # liste contenant pour chaque cote, la fréquence à laquelle le favori gagne et la fréquence
    # apparition de la cote
    li_freqs_victoire = []
    
    while valeur_cote < b_sup:
        
        frequences_apparition = 0
        frequences_victoires = 0
        
        for nom_table in noms_tables:
            requete_apparition = f"SELECT COUNT(*) FROM {nom_table} WHERE min(cote1, cote2, cote3) is {valeur_cote}"
            requete_victoire = requete_apparition + " AND favori is 1"
            
            frequences_apparition += bd.execute_requete(requete_SQL=requete_apparition)
            frequences_victoires += bd.execute_requete(requete_SQL=requete_victoire)
        
        if frequences_apparition > 0:
            li_cotes.append(valeur_cote)
            li_freqs_apparition.append(frequences_apparition)
            li_freqs_victoire.append(frequences_victoires)
        
        valeur_cote += pas
        valeur_cote = round(valeur_cote, 2)
    
    li_probas = [round(li_freqs_victoire[i] / li_freqs_apparition[i], 2) for i in range(0, len(li_cotes))]
    
    resultat = {
        "valeurs_cotes": li_cotes,
        "freqs_apparitions": li_freqs_apparition,
        "freqs_victoire": li_freqs_victoire,
        "probas": li_probas
    }
    return resultat


def trace_histogramme(abcisse: list, ordonnees: list[list], titre="", titre_x="", titre_y="", sauvegarde_sous=None):
    """
    Trace l'histogramme

    Si uniquement une série de valeurs format ordonnees = list[list[valeurs]]
    Si 2 séries de valeurs format ordonnnees = list[list[valeurs], list[valeurs]]

    :param abcisse:
    :param ordonnees:
    :param titre:
    :param titre_x:
    :param titre_y:
    :param sauvegarde_sous:
    :return:
    """
    
    fig, ax = plt.subplots()
    ax.set_title(titre)
    
    ax.set_xlabel(titre_x)
    ax.set_ylabel(titre_y)
    # ax.set_xticks(abcisse)
    
    plt.bar(x=abcisse, height=ordonnees[0], width=0.005, color='blue')
    
    if len(ordonnees) == 2:
        pass
        # ax.plot(x=abcisse, height=ordonnees[1], 'o-', color='red')
    
    ax.grid(True)
    if sauvegarde_sous != None:
        plt.savefig(sauvegarde_sous)
    plt.show()


# pour tourner dans un conteneur - headless
def set_chrome_options() -> None:
    """Sets chrome options for Selenium.
    Chrome options for headless browser is enabled.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_prefs = {}
    chrome_options.experimental_options["prefs"] = chrome_prefs
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    return chrome_options


def creer_nom_table(adresse: str) -> str:
    """
    Création à partir d'une url d un nom de table pour le stockage
    :param adresse:
    :return: nom de table pour le stockage
    """
    nom_table = adresse.split("/")[-3]
    nom_table = nom_table.replace("-", "_")
    return nom_table


class Oddsportal:
    
    def __init__(self, adresse_championnat):
        self.pilote = webdriver.Chrome(options=set_chrome_options())
        self.wait = WebDriverWait(self.pilote, 4)
        self.adresse_championnat = adresse_championnat
        self.xpath_saisons = "//div[@class = 'main-menu2 main-menu-gray']//li//a"
        self.xpath_matchs = "//tr[contains(@class, 'deactivate')]"
        self.xpath_pagination = "//div[@id = 'pagination']/a"
        self.xpath_affiche = ".//td[@class = 'name table-participant']"
        self.xpath_cotes = ".//td[contains(@class, 'odds-nowrp')]"
        self.xpath_cote_gagnante = ".//td[@class = 'result-ok odds-nowrp']"
        self.xpath_score = ".//td[@class = 'center bold table-odds table-score']"
        self.xpath_gagnant = ".//span[@class = 'bold']"
    
    def trouve_urls_base_saisons(self) -> List[str]:
        """
        Renvoie les urls des saisons qui possèdent des données
        1 - Récupération de tous les tags a des saisons
        2 - Pour chaque a on extrait l'url (href) et on vérifie qu'il y a des données avec la méthode trouve_nb_pages
        :return:liste d'urls des saisons qui ont des données
        """
        
        # 1
        self.pilote.get(self.adresse_championnat)
        links = self.wait.until(
            EC.visibility_of_all_elements_located(
                (By.XPATH, self.xpath_saisons)
            )
        )
        
        # 2
        urls = [link.get_attribute('href') for link in links]
        
        urls_saisons_ac_donnees = []
        for url in urls:
            self.pilote.get(url)
            if self.trouve_nb_pages() > 0:
                urls_saisons_ac_donnees.append(url)
            
        
        return urls_saisons_ac_donnees

    def trouve_nb_pages(self) -> int:
        """
        Renvoie le nb de pages que comporte une saison. S'il n'y a pas de données, renvoie 0
        :return:nb de pages d'une saison
        """
        try:
            nb_pages = self.wait.until(
                EC.visibility_of_all_elements_located(
                    (By.XPATH, self.xpath_pagination)
                )
            )
            nb_pages = int(nb_pages[-1].get_attribute('x-page'))
            return nb_pages
        except:
            return 0

    def construit_urls_courantes(self, url_base_saison) -> List[str]:
        """
        Construit les urls courantes d'une saison
            1 - Détermine le nb de pages
            2 - construit les urls en concaténant l'url de base avec i pour i dans le nb de pages
        :return: liste d'urls courantes pour la saison
        """
        self.pilote.get(url_base_saison)
        nb_de_pages = self.trouve_nb_pages()
        
        urls_parcours_saison = [url_base_saison +  "#/page/" + str(i) + "/" for i in range(1, nb_de_pages + 1)]
        
        return urls_parcours_saison

    def trouve_matchs(self):
        
        matchs = self.wait.until(
            EC.visibility_of_all_elements_located(
                (By.XPATH, self.xpath_matchs)
            )
        )
        
        return matchs

    def trouve_affiche(self, match):
        
        affiche = match.find_element_by_xpath(self.xpath_affiche).text.replace("\n ", "")
        return affiche

    def trouve_cotes(self, match) -> Tuple[list, int]:
        """
        trouve les cotes et indique 1 si le favori gagne 0 sinon
        Renvoie un tuple (cotes, indication)
        :param match:
        :return:
        """
        cotes = match.find_elements_by_xpath(self.xpath_cotes)
        cotes = [float(cote.text) for cote in cotes]
        
        cote_favori = float(match.find_element_by_xpath(self.xpath_cote_gagnante).text)
        
        if cote_favori == min(cotes):
            fav_gagne = 1
        else:
            fav_gagne = 0
            
        if len(cotes) == 2:
            cotes.append('')
            
        return cotes, fav_gagne

    def trouve_score(self, match):
        
        score = match.find_element_by_xpath(self.xpath_score).text
        score = [int(s) for s in score.split(":")]
        return score
    
    def trouve_gagnant(self, match):
        
        try:
            gagnant = match.find_element_by_xpath(self.xpath_gagnant).text
    
        except NoSuchElementException:
        
            gagnant = self.trouve_affiche(match)
    
        return gagnant

    def recupere_donnees_saison(self, *, url_base_saison) -> List[list]:
        """
        Récupération des données d'une saison
        :param url_base_saison:
        :return: liste de [affiche, cotes, gagnant]
        """
        urls_courantes = self.construit_urls_courantes(url_base_saison)
        datas_saison = []
        for url_courante in urls_courantes:
            self.pilote.get(url_courante)
            matchs = self.trouve_matchs()
            for match in matchs:
                try:
                    cotes, fav_gagne = self.trouve_cotes(match)
                    datas_match = [self.trouve_affiche(match)] + cotes + [self.trouve_gagnant(match)] + [fav_gagne]
                    print(Glob.couleur_bleue)
                    print(datas_match)
                    datas_saison.append(datas_match)
                except Exception as e:
                    print(Glob.couleur_rouge)
                    print("interception d'une erreur dans la récupération des données d'un match")
                    print(Glob.par_defaut)
        
        return datas_saison
    
    def sauvegarde_donnees_saison(self, nom_table, donnees_a_sauvegarder):
        """
        Sauvegarde dans la table nom_table les données à sauvegarder
        Pour l'instant on utilise une méthode de acquisition insere_matchs qui n'est pas crée pour, mais convient bien,
        par un heureux hasard
        :param nom_table:
        :param donnees_a_sauvegarder:
        :return:
        """
        nom_bd = Glob.NOM_BD_SIMU
        bd = BD(nom_bd)
        bd.creer_table(nom_table=nom_table, descripteur='donnees_simu')
        bd.insere_matchs(nom_table=nom_table, my_donnees=donnees_a_sauvegarder)
        bd.close()
        
    def recupere_et_sauvegarde_saisons(self):
        
        urls_saisons_ac_donnees = self.trouve_urls_base_saisons()
        for url_base in urls_saisons_ac_donnees:
            nom_table = creer_nom_table(adresse=url_base)
            donnees_saison = self.recupere_donnees_saison(url_base_saison=url_base)
            self.sauvegarde_donnees_saison(nom_table=nom_table, donnees_a_sauvegarder=donnees_saison)
