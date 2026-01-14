import os                       # Pour lire les "Secrets" de GitHub (ta clé API)
import requests                 # Pour aller chercher des données sur Internet (PandaScore)
from icalendar import Calendar, Event # Pour créer le format de fichier calendrier .ics
from datetime import datetime    # Pour manipuler les dates et les heures

# GitHub ira chercher ta clé ici automatiquement
API_KEY = os.getenv("PANDASCORE_API_KEY")
TEAM_ID = "132514" # ID pour Gentle Mates

def update_m8_calendar():
    url = f"https://api.pandascore.co/teams/{TEAM_ID}/matches?filter[future]=true"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "application/json"
    }

    response = requests.get(url, headers=headers)
    matches = response.json()

    cal = Calendar()
    cal.add('prodid', '-//Gentle Mates Fans//FR')
    cal.add('version', '2.0')
    cal.add('x-wr-calname', 'Gentle Mates Matches')

    for match in matches:
        event = Event()
        event.add('summary', match['name'])
        
        # Conversion de la date API en format Calendrier
        start_date = datetime.strptime(match['begin_at'], "%Y-%m-%dT%H:%M:%SZ")
        event.add('dtstart', start_date)
        
        # Ajout du lien Twitch dans la description
        if match['streams_list']:
            twitch_url = match['streams_list'][0]['raw_url']
            event.add('description', f"Regarder en direct : {twitch_url}")
        
        event.add('uid', f"m8-{match['id']}@gentlemates.com")
        cal.add_component(event)

    # Sauvegarde du fichier

    with open('gentlemates.ics', 'wb') as f:
        f.write(cal.to_ical())

if __name__ == "__main__":
    update_m8_calendar()
