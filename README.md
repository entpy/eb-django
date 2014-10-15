eb-django
=========

Essere &amp; Benessere django project

"""
== Todo list ==
- V (viene già fatto da django) Sovrascrivere il delete delle promozioni eliminando anche le relative righe in campagne
- V Aggiungere ulteriori link nella index dell'admin
- V Al salvataggio del form di mofica/inserimento promozione generare, se non esiste, anche un codice della campagna.
- V template + invio della mail
- V Funzione per invio mail al compleanno
- V filtrare le promozioni scadute nell'admin
- V Sovrascrivere il metodo save dell'immagine per farne prima il resize e capire come ridimensionarla
- V Schedulare le mail al compleanno
- Capire il context dei template per passare variabili comuni
- Modifica testi e immagini e fixare eventuali rotture con opportuni fix CSS
- Test

== Su ambiente ==
- installare django_cron con pip ed eseguire python manage.py runcrons ogni tot di minuti da crontab
"""

Dipendenze
----------
Django==1.6.5
PIL==1.1.7
Pillow==2.4.0
South==1.0
argparse==1.2.1
distribute==0.6.24
django-common-helpers==0.6.1
django-cron==0.3.4
psycopg2==2.5.3
wsgiref==0.1.2

pip install django-cron
pip install pil
