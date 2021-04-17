# eval_book

Programme permettant de récupérer des données du site Oddsportal. Ne fonctionne que pour ce site.

 - BD gère la bd sqlite
 - Glob contient les constantes, ainsi qu'un dictionnaire pour modifier automatiquement la construction de tables
 - Oddsportal contient la classe qui gère la connection au site, l'identification des données pertinentes, la récupération puis la sauvegarde
 
 Pour utiliser le programme:
 
 donner l url des resultats d'une saison dans url_base_saison: 
 forme url = https://www.oddsportal.com/sport/pays/ligue-annees/results/ ex:https://www.oddsportal.com/basketball/usa/nba-2017-2018/results/
 ou
 donner l'url du championnat. Le programme récupère automatiquement toutes les saisons. Correspond à la partie commentée dans main.
 ex:
 url_a_scraper =https://www.oddsportal.com/soccer/france/ligue-1/results/
