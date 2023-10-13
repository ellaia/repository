import requests

# Remplacez 'votre_token_d_acces' par le jeton d'accès que vous avez obtenu
access_token = 'AQWPTurPJkJmzmujYiFkzW3Uk2h0HMZS_fMFRKSi0Bgsk3AcKBhKhgfU2dZzrA7V_kCvzFgS1NHx4bAkv8DpHxjnbvXggS7MLMxjHPg9iDmFB9fgvdSJx-pf-rRxBhJfBgbiu0dpjQnLnvt05q7HJui9skou-9zaT_sBgV1RItVd9lEGU9Nf6kk_m75iZvAAODW59Z379hlVkRoBSpfgziWUfThnq6K8xJrMHhM3Y4Vvc6_RUn-N_PgdsWPp7ZyH_Q24ja0GYuBFhs9PvkpCmGMmTCdVjBoUN7EH0-bIvek6yRxeBzxvCxMXuZAjmqCT6sJdgQoUDFW0a4lnPS5lePx-8PXttw'

headers = {'Authorization': f'Bearer {access_token}'}

# Remplacez 'votre_id_utilisateur' par votre ID utilisateur LinkedIn
user_id = '10087745'

# Récupérer les posts
response = requests.get(f'https://api.linkedin.com/v2/ugcPosts?q=authors:urn:li:person:{user_id}', headers=headers)

# Vérifier si la requête a réussi
if response.status_code == 200:
    posts_data = response.json()
    for post in posts_data['elements']:
        print(post['localizedBody'])
else:
    print(f'Erreur: {response.status_code}')
