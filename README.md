# eval_book

Programme permettant de récupérer des données du site Oddsportal et de représenter graphiquement un post-traitement statistique. Ne fonctionne que pour ce site.

 - BD gère la bd sqlite
 - Glob contient les constantes, ainsi qu'un dictionnaire pour modifier automatiquement la construction de tables
 - Oddsportal contient la classe qui gère la connection au site, l'identification des données pertinentes, la récupération puis la sauvegarde
 
On peut utiliser le programme, pour récupérer soit:

- Une saison d'un championnat. Dans ce cas on donne l'adresse sous forme adresse = https://www.oddsportal.com/sport/pays/championnat-annees/results/ (exemple: https://www.oddsportal.com/basketball/usa/nba-2017-2018/results/). temps d'exécution de l'ordre de 5 minutes.
 
- La totalité des saisons d'un championnat. Dans ce cas on donne l'adresse sous forme adresse = https://www.oddsportal.com/sport/pays/championnat/results/ (exemple: https://www.oddsportal.com/soccer/france/ligue-1/results/). temps d'exécution de l'ordre de l'heure.
 
 Présence d'un Dockerfile, pour construire une image. La partie graphique (histogramme) ne peut alors être visible.
