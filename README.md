# Site de la Dre Charlotte Jaloux

Site statique en français et en anglais. Les dix pages et les fichiers publics sont déjà générés. Pour relire la maquette, décompresser le ZIP et ouvrir `index.html` dans un navigateur. Garder les dossiers ensemble.

## Modifier le site

1. Modifier `data/site.json` pour les coordonnées, l’établissement ou le domaine.
2. Modifier `data/content.json` pour les textes. Faire la même mise à jour dans les sections `fr` et `en`. Le titre universitaire est la valeur `rank` dans chaque langue.
3. Lancer `python3 scripts/build.py` avec Python 3.10 ou plus récent. Ouvrir les pages régénérées et vérifier les deux langues.
4. Créer un commit incluant les sources et les fichiers générés. Après le lancement, fusionner dans `main` publie la mise à jour si GitHub Pages utilise cette branche.

Le style se trouve dans `assets/style.css`. Le portrait approuvé est `assets/portrait-charlotte-jaloux.jpg`. Pour ajouter une FAQ, ajouter la paire question-réponse dans chaque langue, puis régénérer. Pour une nouvelle page, ajouter sa route aux deux menus, ses textes et son rendu dans le générateur.

Pour annuler un changement publié, créer un commit d’annulation avec `git revert SHA_DU_COMMIT`, vérifier les pages, puis publier ce commit. Pour une mise à jour fusionnée par pull request, utiliser **Revert** dans la pull request quand l’option est proposée.

## Lancement sur GitHub Pages

1. Créer le dépôt sous le compte `drchajalplastie`. Nom proposé pour le site principal du compte : `drchajalplastie.github.io`. Un dépôt privé peut recevoir la version de révision avec Pages désactivé. Sur GitHub Free, le dépôt doit être public pour activer Pages.
2. Après validation de la maquette et accord sur la publication publique, mettre le contenu du dossier à la racine de `main`. Dans **Settings → Pages → Build and deployment**, sélectionner **Deploy from a branch**, puis **main** et **/(root)**. Vérifier l’adresse GitHub Pages avant la bascule.
3. Dans les paramètres du compte propriétaire **Settings → Pages**, demander la vérification de `charlottejaloux.com`. Chez Squarespace, **Domains → charlottejaloux.com → DNS → Custom records**, ajouter le TXT fourni par GitHub. Puis terminer la vérification chez GitHub. Conserver ce TXT.
4. Avant la bascule, relever les enregistrements existants, les règles de redirection et la destination du site web précédent, le cas échéant. Conserver une copie des réglages. Dans **les paramètres du dépôt → Pages → Custom domain**, enregistrer `charlottejaloux.com`. GitHub crée alors `CNAME` pour la publication depuis une branche. Conserver ce fichier dans les commits ultérieurs.
5. Avec l’accord d’Andrei pour la bascule, remplacer uniquement les enregistrements web incompatibles à l’apex et à `www`. Préserver les MX, les TXT de messagerie et de vérification, et les autres enregistrements sans rapport avec l’hébergement web. Vérifier qui gère les serveurs de noms avant de modifier quoi que ce soit.

| Type | Hôte | Valeur |
| --- | --- | --- |
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| CNAME | www | drchajalplastie.github.io |

6. Une fois le certificat disponible, activer **Enforce HTTPS** dans GitHub Pages. Vérifier les deux variantes du domaine et la redirection vers `https://charlottejaloux.com`, puis tester les pages FR et EN, leurs liens et le portrait.
7. En cas de retour à l’ancien site, restaurer les enregistrements web et les règles de redirection relevés à l’étape 4, puis vérifier l’ancien site avant de retirer l’association au domaine dans GitHub.

[GitHub Pages et domaine personnalisé](https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site) · [Éditer les DNS Squarespace](https://support.squarespace.com/hc/en-us/articles/360002101888-Adding-DNS-records-to-your-domain)

## Google Search Console

Après la bascule, créer une propriété de type **Domaine** pour `charlottejaloux.com`, ajouter dans Squarespace le TXT fourni par Google, puis lancer la vérification. Dans **Sitemaps**, soumettre `https://charlottejaloux.com/sitemap.xml`. Inspecter l’accueil et les pages principales en français et en anglais. Le site ne charge aucun service de statistiques.

[Google Search Console](https://search.google.com/search-console)
