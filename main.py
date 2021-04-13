from Oddsportal import Oddsportal, construit_histogramme, trace_histogramme

if __name__ == '__main__':
    
    
    o = Oddsportal("https://www.oddsportal.com")
    
    # Récupère les données pour une saison d'un championnat, et les enregistre
    # TEMPS D EXECUTION: ORDRE DE 5 MINUTES
    
    url_base_saison = "https://www.oddsportal.com/basketball/usa/nba-2017-2018/results/"
    nom_table = "nba_2017_2018"
    datas = o.recupere_donnees_saison(url_base_saison=url_base_saison)
    o.sauvegarde_donnees_saison(nom_table=nom_table, donnees_a_sauvegarder=datas)

    # Construit un histogramme à partir des données sauvées sous table
    # JUSTE POUR EXEMPLE. UN HISTOGRAMME SUR UNE SEULE SAISON N EST PAS REPRESENTATIF
    
    b = construit_histogramme(noms_tables=[nom_table], b_inf=1.0, b_sup=1.9)
    trace_histogramme(b["valeurs_cotes"], [b["probas"]], titre=nom_table, titre_x="cotes", titre_y="proba que le favori gagne")

    # Pour récupérer et sauvegarder les données pour toutes les saisons disponibles d'un championnat -
    # TEMPS D EXECUTION: TRES LENT - ORDRE DE L HEURE
    
    # url_a_scraper = "https://www.oddsportal.com/soccer/france/ligue-1/results/" # url du championnat
    # o2 = Oddsportal(url_a_scraper)
    # o2.recupere_et_sauvegarde_saisons()


