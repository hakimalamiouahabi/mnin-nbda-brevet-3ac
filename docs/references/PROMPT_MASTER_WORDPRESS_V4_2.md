# PROMPT MASTER V4 EXÉCUTABLE — MNIN NBDA
## WordPress • Brevet 3AC • “Le chemin lumineux” • moteur pédagogique dédié • livraisons progressives
### Version verrouillée pour développement, tests et ZIP installables

---

# 0. MISSION

Tu agis comme une équipe senior réunissant :

- product architect ;
- lead WordPress engineer ;
- PHP engineer ;
- frontend engineer ;
- UI/UX designer ;
- brand designer ;
- learning-experience designer ;
- accessibility specialist ;
- security reviewer ;
- QA engineer ;
- performance engineer.

Tu dois transformer MNIN NBDA en une plateforme EdTech marocaine premium exclusivement dédiée au Brevet 3AC.

Le résultat final doit être :

- réellement installable sur WordPress ;
- réellement testable ;
- réellement utilisable par un collégien marocain ;
- modulaire ;
- maintenable ;
- bilingue FR/AR ;
- responsive ;
- accessible ;
- sécurisé ;
- livré sous forme de ZIP ;
- accompagné de rapports de tests factuels.

Tu ne dois pas produire une simple maquette.

Tu ne dois jamais annoncer qu’une fonction est “prête” si elle n’a pas été réellement codée et testée.

---

# 1. DÉCISIONS TECHNIQUES DÉSORMAIS FIGÉES

Ces décisions ne sont plus ouvertes à interprétation.

## 1.1 Moteur pédagogique

**MNIN NBDA utilisera son propre moteur pédagogique dans `mnin-nbda-core`.**

Tutor LMS est EXCLU du périmètre de cette V4.

Raison :
MNIN NBDA nécessite une logique spécifique de :

- diagnostic ;
- prérequis ;
- remise à niveau ciblée ;
- progression ;
- maîtrise ;
- erreurs ;
- révisions ;
- relation Parent → Enfant ;
- droits par matière ;
- examens ;
- activités ;
- reporting familial.

Il est interdit de coder simultanément un moteur MNIN NBDA et une seconde architecture Tutor LMS.

Une intégration Tutor LMS pourra être étudiée dans le futur via un adaptateur séparé, mais elle ne doit pas influencer le schéma métier de la V4.

## 1.2 WordPress

Le produit est composé de deux ZIP principaux :

### `mnin-nbda-theme.zip`
Présentation, templates, design system, Gutenberg, styles, navigation, assets.

### `mnin-nbda-core.zip`
Logique métier, données, permissions, progression, diagnostic, examens, comptes Parent/Élève, REST API et administration MNIN NBDA.

La logique métier ne doit jamais dépendre du thème.

## 1.3 Bilinguisme

Architecture de contenu retenue :

**Polylang Free comme moteur de contenu bilingue recommandé et supporté.**

Le thème et le plugin doivent cependant :

- rester activables sans Polylang ;
- utiliser les fonctions WordPress i18n pour toutes les chaînes d’interface ;
- détecter Polylang proprement ;
- afficher le sélecteur FR/AR uniquement lorsque la configuration multilingue est prête ;
- fournir RTL ;
- ne jamais provoquer d’erreur fatale si Polylang est absent.

WPML pourra être rendu compatible plus tard, mais n’est pas la dépendance de référence de la V4.

## 1.4 Paiement

Aucun prestataire de paiement ne doit être inventé.

La V4 doit créer une **couche de paiement abstraite** mais l’intégration réelle du prestataire marocain est reportée à la Livraison 4.

Créer une interface logique du type :

`PaymentProviderInterface`

avec au minimum :

- `create_payment()`
- `verify_payment()`
- `handle_webhook()`
- `refund_payment()`
- `get_payment_status()`

Aucun provider fictif ne doit être activé en production.

## 1.5 Mineurs

Le parent est le compte responsable du foyer.

Le profil enfant est minimaliste.

Par défaut :

- ne pas exiger d’adresse email personnelle de l’enfant ;
- ne pas exiger de date de naissance exacte ;
- utiliser le niveau scolaire / tranche d’âge uniquement si nécessaire ;
- minimiser toute donnée personnelle ;
- séparer identifiants de connexion et données pédagogiques ;
- donner au parent les fonctions nécessaires de gestion, export et suppression compatibles avec l’architecture retenue ;
- ne jamais exposer les données d’un enfant à un autre foyer ;
- journaliser les actions administratives sensibles.

Toute exigence juridique locale spécifique doit être validée séparément par le porteur du projet avant ouverture au public.

## 1.6 Validation

Un ZIP n’est “prêt à installer” que si l’installation et l’activation ont été réellement testées sur une installation WordPress propre.

Un test non exécuté doit être marqué :

**NON TESTÉ**

et jamais :

**PASS**

---



# 1.7 POLITIQUE ABSOLUE — AUCUNE API PAYANTE

MNIN NBDA doit pouvoir fonctionner sans abonnement à une API tierce payante.

Interdictions :

- OpenAI API payante ;
- Anthropic API payante ;
- Gemini API payante ;
- Mapbox payant ;
- Algolia payant ;
- Twilio payant ;
- SendGrid payant ;
- services OCR payants ;
- services de traduction payants ;
- services analytics payants obligatoires ;
- CDN, stockage, recherche ou IA nécessitant un abonnement payant ;
- toute dépendance SaaS dont le fonctionnement essentiel du site cesse sans paiement.

Priorité obligatoire :

1. fonctionnalités natives WordPress ;
2. code local dans `mnin-nbda-core` ;
3. bibliothèques open source ;
4. services gratuits sans verrouillage fournisseur, uniquement s’ils sont réellement nécessaires ;
5. traitement côté serveur/local lorsque possible.

Le produit doit conserver ses fonctions essentielles même si aucun service externe optionnel n’est configuré.

## IA

Aucune IA distante payante n’est requise pour faire fonctionner le produit.

Si une fonction IA future est souhaitée, elle doit être :

- optionnelle ;
- désactivée par défaut ;
- isolée derrière une interface/provider ;
- remplaçable ;
- non nécessaire au parcours pédagogique principal.

Prévoir éventuellement des connecteurs futurs vers des modèles locaux ou auto-hébergés, mais ne pas en faire une dépendance de la V4.

## Recherche

Utiliser la recherche WordPress ou un moteur local/open source.
Ne pas imposer Algolia, Elastic Cloud ou autre service payant.

## Emails

Utiliser l’envoi WordPress standard ou un SMTP configuré par le propriétaire.
Ne pas imposer un fournisseur d’email transactionnel payant.

## Analytics

Utiliser au besoin :

- statistiques internes minimales ;
- logs WordPress ;
- solution open source / auto-hébergée optionnelle.

Ne pas rendre Google Analytics, Mixpanel, Amplitude ou un SaaS analytics obligatoire.

## Cartes / géolocalisation

Aucune carte externe payante ne doit être nécessaire.
Le produit n’en a normalement pas besoin.

## Médias

Stockage local WordPress par défaut.
Aucun stockage cloud payant obligatoire.

## Paiement — exception de nature commerciale

Un prestataire de paiement peut facturer des frais de transaction : cela ne constitue pas une “API payante” au sens d’un abonnement logiciel obligatoire.

Cependant :

- aucun abonnement API ne doit être requis ;
- aucun prestataire ne doit être intégré tant qu’il n’est pas choisi ;
- la plateforme doit fonctionner en mode pédagogique sans paiement configuré ;
- toute intégration paiement doit rester modulaire et remplaçable.

## Critère d’acceptation

Le QA final doit contenir une ligne explicite :

`Dépendance à une API payante pour les fonctions essentielles : NON`

Si la réponse est OUI, la livraison est REFUSÉE.


# 2. STRATÉGIE DE LIVRAISON OBLIGATOIRE

Le projet est divisé en 4 livraisons.

Il est interdit de développer les quatre phases dans un seul bloc impossible à valider.

Chaque livraison possède :

- son périmètre ;
- ses ZIP ;
- ses tests ;
- ses critères d’acceptation ;
- son rapport QA ;
- son point de validation.

Si une livraison échoue à ses critères d’acceptation :
**ne pas passer à la suivante.**

---

# 3. LIVRAISON 0 — AUDIT ET REPRISE DU PROJET EXISTANT

Avant le développement :

1. inspecter le site / code / exports existants ;
2. inventorier les contenus ;
3. inventorier les utilisateurs si accessibles ;
4. inventorier les médias ;
5. inventorier les slugs ;
6. inventorier les fonctionnalités ;
7. inventorier les rôles ;
8. inventorier les formulaires ;
9. inventorier les données à conserver ;
10. inventorier les dépendances ;
11. inventorier les intégrations ;
12. identifier tout risque de migration.

Créer :

`AUDIT_EXISTANT.md`

Il doit contenir un tableau :

| Élément existant | Emplacement | À conserver | À migrer | À supprimer | Risque | Action |
|---|---|---:|---:|---:|---|---|

Ne jamais supprimer une donnée existante sans stratégie de migration explicitement documentée.

---

# 4. LIVRAISON 1 — IDENTITÉ + THÈME WORDPRESS + HOME

## 4.1 Objectif

Créer la fondation visuelle définitive de MNIN NBDA.

La Livraison 1 contient :

- identité ;
- logo ;
- thème WordPress ;
- Header ;
- Footer ;
- Home ;
- huit matières ;
- page Méthode ;
- page Matières ;
- pages publiques structurelles minimales ;
- responsive ;
- FR/AR ;
- RTL ;
- design system ;
- Gutenberg ;
- performance de base.

Cette livraison ne contient PAS encore tout le moteur pédagogique.

## 4.2 Livrables

- `mnin-nbda-theme.zip`
- première version installable de `mnin-nbda-core.zip` uniquement pour les fondations nécessaires
- `README_INSTALLATION.md`
- `QA_PHASE_1.md`
- `ASSET_MANIFEST.md`
- `DESIGN_SYSTEM.md`
- captures desktop/tablette/mobile.

---

# 5. IDENTITÉ OFFICIELLE

## 5.1 Signature

La signature officielle exacte est :

**Quand tu ne sais pas mnin tbda.**

Interdiction absolue d’écrire :

- mmin tbda ;
- min tbda ;
- autre variante.

## 5.2 Concept officiel

**LE CHEMIN LUMINEUX**

Le symbole officiel évoque :

- un point de départ ;
- une trajectoire ;
- un horizon ;
- un soleil levant ;
- une progression ;
- l’ouverture des possibilités.

Le symbole doit rester :

- simple ;
- mémorable ;
- lisible à petite taille ;
- non scolaire ;
- non générique ;
- distinctif.

## 5.3 Ce que le logo ne doit PAS être

Pas de :

- livre ;
- toque ;
- crayon ;
- ampoule ;
- boussole générique ;
- phare générique ;
- simple initiales MN ;
- icône éducative de banque d’icônes.

Le chemin doit être un **ruban de progression abstrait**, pas une route touristique réaliste.

## 5.4 Versions à produire

- logo horizontal ;
- logo vertical ;
- symbole seul ;
- monochrome ;
- fond clair ;
- fond sombre ;
- favicon ;
- app icon ;
- SVG optimisé ;
- PNG transparent ;
- WebP si utile.

Tester le symbole à :

- 16 px ;
- 32 px ;
- 48 px ;
- 64 px ;
- 180 px ;
- 512 px.

---

# 6. CHARTE GRAPHIQUE

Palette :

### Vert pétrole
Couleur dominante.

Usage :
- titres ;
- header ;
- texte fort ;
- composants principaux.

### Orange solaire
Accent.

Usage :
- CTA ;
- états actifs ;
- progression ;
- repères ;
- micro-interactions.

### Crème
Fond dominant.

### Anthracite / bleu profond
Texte et contrastes.

Interdiction :
ne pas appliquer un gros dégradé orange/vert au H1.

Hiérarchie :

**Vert pétrole = information**
**Orange = action**
**Crème = respiration**

---

# 7. HOME — PRIORITÉ ABSOLUE

La Home doit être finalisée avant de décliner le système ailleurs.

Ordre :

1. Header
2. Hero Amine
3. 8 matières
4. Méthode
5. Diagnostic
6. Démo pédagogique
7. Parcours pédagogique
8. Zone “Ton avenir commence maintenant”
9. Révisions / examens blancs
10. Suivi parent
11. Préparation Brevet
12. Tarifs
13. FAQ
14. CTA final
15. Footer

---

# 8. HEADER

Navigation :

- Accueil
- Matières
- Méthode
- Démo
- Tarifs
- FAQ

À droite :

- FR / العربية
- Connexion
- Commencer

Responsive :

- menu mobile ;
- focus visible ;
- touch target minimum ;
- navigation clavier.

---

# 9. HERO

Personnage unique :

**Amine**

Âge :
14–15 ans.

Contraintes :

- adolescent marocain crédible ;
- photo naturelle ;
- ni trop jeune ni adulte ;
- tenue contemporaine ;
- pas de toque ;
- pas de stéréotype scolaire.

Copy :

Sur-titre :

**Spécial Brevet 3AC**

H1 :

**Quand tu ne sais pas mnin tbda.**

Sous-titre :

**Prépare ton Brevet 3AC à ton rythme, depuis les bases jusqu’aux exercices d’examen.**

Texte :

**Diagnostic, remise à niveau, apprentissage, exercices et révisions : avance étape par étape, au bon niveau.**

CTA primaire :

**Découvrir les matières**

CTA secondaire :

**Voir comment ça marche**

Cartes flottantes :

- Mathématiques
- Physique-Chimie
- SVT
- Français

Badge :

**Objectif Brevet 3AC**

---

# 10. LES 8 MATIÈRES

Afficher :

1. Mathématiques
2. Français
3. Arabe
4. Physique-Chimie
5. SVT
6. Histoire-Géographie & Citoyenneté
7. Éducation islamique
8. Anglais

Chaque carte :

- icône dédiée ;
- titre ;
- courte description ;
- lien ;
- état hover/focus ;
- responsive.

Pas d’autre niveau scolaire.

---

# 11. MÉTHODE

Titre :

**Le programme reste le même. Le chemin s’adapte à l’élève.**

Étapes :

01 Diagnostic
02 Remise à niveau
03 Apprentissage
04 Révision

Le tracé du parcours doit reprendre le vocabulaire graphique du logo.

---

# 12. DIAGNOSTIC

Titre :

**Avant d’apprendre, savoir où commencer.**

Trois états :

- bases maîtrisées ;
- notions à consolider ;
- prérequis à reprendre.

Si des nombres sont simulés :
ajouter explicitement **Exemple**.

---

# 13. DÉMO PÉDAGOGIQUE

Créer une vraie interaction.

Flux :

1. objectif ;
2. rappel ;
3. explication ;
4. exemple ;
5. question ;
6. réponse ;
7. feedback ;
8. bilan.

Aucun bouton décoratif inactif.

---

# 14. ZONE NARRATIVE 14 → 26 ANS

Cette section vient APRÈS la proposition pédagogique.

Elle ne doit pas dominer la page.

Titre :

**Ton avenir commence maintenant.**

Personnages principaux :

- Amine
- Wassim Jad
- Yasmina

Personnages secondaires :

- Salma
- Adam
- Lina
- Ilyas
- Nour
- Mehdi
- Aya
- Youssef
- Imane

Timeline :

- 14
- 15
- 16
- 18
- 21
- 23
- 26

Message :

**À 14 ans, tu n’as pas besoin de savoir exactement ce que tu deviendras. Mais chaque effort peut ouvrir de nouvelles possibilités.**

Jauge :

**Efforts d’aujourd’hui**

Actions :

- comprendre ;
- corriger ;
- pratiquer ;
- réviser ;
- terminer.

Futurs possibles :

- médecin ;
- pilote ;
- enseignant ;
- ingénieur ;
- architecte ;
- pharmacien ;
- chercheur ;
- ingénieur logiciel ;
- data scientist ;
- entrepreneur ;
- expert-comptable ;
- environnement.

Toujours afficher :

**Un exemple de futur possible.**

Option obligatoire :

**Je ne sais pas encore**

Réponse :

**Tu n’as pas besoin de tout décider aujourd’hui. Commence simplement par construire de bonnes bases.**

La version cinématographique du chemin lumineux peut être utilisée ici.

Elle ne remplace jamais le logo minimaliste.

---

# 15. ACCEPTATION LIVRAISON 1

La Livraison 1 est PASS uniquement si :

- thème installable ;
- plugin fondation installable ;
- activation sans erreur fatale ;
- Home terminée ;
- logo final intégré ;
- signature exacte ;
- Amine au Hero ;
- huit matières ;
- FR ;
- AR ;
- RTL ;
- mobile 320 px ;
- tablette ;
- desktop ;
- navigation clavier ;
- reduced motion ;
- aucune mention primaire/lycée ;
- aucune donnée commerciale inventée ;
- Lighthouse / contrôle performance documenté ;
- aucun secret.

Le rapport doit distinguer :

- PASS ;
- FAIL ;
- NON TESTÉ.

---

# 16. LIVRAISON 2 — MOTEUR PÉDAGOGIQUE

## 16.1 Objectif

Prouver le moteur sur **une seule matière complète** avant de généraliser.

Matière pilote recommandée :

**Mathématiques**

Ne pas développer les huit matières en profondeur avant validation du pilote.

## 16.2 Parcours de référence

Créer :

**Matière → Diagnostic → Prérequis → Leçon → Exercices → Feedback → Maîtrise → Révision**

## 16.3 Une vraie leçon

La matière pilote doit contenir au minimum une leçon réellement complète.

La leçon doit inclure :

- objectif ;
- prérequis ;
- rappel ;
- explication ;
- illustration ;
- exemple ;
- interaction ;
- exercice ;
- indice ;
- correction ;
- feedback ;
- mini-évaluation ;
- bilan ;
- score ;
- maîtrise ;
- prochaine étape.

---

# 17. MODÈLE DE CONTENU PÉDAGOGIQUE

## 17.1 Contenu éditorial

Utiliser WordPress natif.

Recommandation :

- CPT `mnin_lesson`
- CPT `mnin_exam`
- taxonomy `mnin_subject`
- taxonomy `mnin_semester`

Le contenu d’une leçon utilise Gutenberg et des blocs MNIN NBDA.

Éviter de stocker une leçon complète dans un JSON opaque si Gutenberg peut la représenter proprement.

## 17.2 Questions

Les questions peuvent être :

- CPT interne ;
- ou structure métier dédiée si nécessaire.

Le choix doit être documenté.

---

# 18. DONNÉES À FORT VOLUME

Ne pas stocker l’historique complet de progression dans un champ `user_meta` sérialisé unique.

Créer des tables dédiées si nécessaire.

Préfixes :
utiliser `$wpdb->prefix`.

Tables recommandées :

- `mnin_child_profiles`
- `mnin_parent_child`
- `mnin_attempts`
- `mnin_progress`
- `mnin_revision_queue`
- `mnin_entitlements`
- `mnin_audit_events`

Utiliser :

- `dbDelta`
- version de schéma
- migrations idempotentes.

Documenter toutes les colonnes.

---

# 19. API

Namespace :

`mnin/v1`

Créer uniquement les endpoints utiles.

Exemples :

- progression ;
- diagnostic ;
- tentative ;
- révision ;
- dashboard.

Chaque endpoint doit avoir :

- validation ;
- sanitation ;
- permission callback ;
- erreurs structurées ;
- aucun accès croisé entre foyers.

---

# 20. RÔLES

Créer :

### `mnin_student`

### `mnin_parent`

Administrateurs :
utiliser capabilities spécifiques plutôt qu’un nouveau rôle surpuissant si inutile.

Capabilities métier explicites.

Ne jamais vérifier une autorisation uniquement avec un nom de rôle.

Utiliser `current_user_can()`.

---

# 21. ACCEPTATION LIVRAISON 2

PASS seulement si :

- matière pilote complète ;
- diagnostic fonctionnel ;
- au moins une vraie leçon ;
- exercices enregistrés ;
- feedback ;
- progression enregistrée ;
- erreurs enregistrées ;
- révision générée ;
- REST sécurisé ;
- migration DB testée ;
- tests de permissions ;
- activation/désactivation propres ;
- aucune régression Livraison 1.

---

# 22. LIVRAISON 3 — ESPACES ÉLÈVE + PARENT

## 22.1 Élève

Écrans :

- connexion ;
- dashboard ;
- matière ;
- diagnostic ;
- leçon ;
- progression ;
- planning ;
- flashcards ;
- erreurs ;
- favoris ;
- examens ;
- réussites ;
- révisions ;
- minuteur ;
- paramètres ;
- aide.

Priorité Dashboard :

**Ta prochaine étape**

## 22.2 Parent

Écrans :

- connexion ;
- dashboard ;
- ajouter enfant ;
- accès enfant ;
- progression ;
- rapport ;
- commandes structurelles ;
- notifications ;
- export ;
- paramètres.

---

# 23. RELATION PARENT / ENFANT

Architecture :

`Parent WordPress User`
→ relation contrôlée
→ `Child Profile`
→ éventuellement `Student WordPress User`

Le profil enfant doit posséder un identifiant interne immuable.

Le parent ne doit voir que les enfants liés à son foyer.

L’Admin autorisé peut gérer la relation.

Ne jamais utiliser un paramètre URL seul comme preuve d’autorisation.

---

# 24. DONNÉES MINEURS — RÈGLES

Par défaut :

Ne pas collecter :

- adresse postale ;
- téléphone enfant ;
- date de naissance exacte ;
- photo obligatoire ;- email enfant obligatoire ;
- école exacte si non indispensable.

Collecter uniquement ce qui sert au produit.

Prévoir :

- export des données du foyer ;
- suppression / anonymisation selon politique définie ;
- journal d’actions sensibles ;
- session sécurisée ;
- expiration / logout ;
- mot de passe robuste ;
- récupération contrôlée par parent selon le modèle choisi.

Créer :

`DATA_PRIVACY_MODEL.md`

Il doit décrire :

- données collectées ;
- finalité ;
- emplacement ;
- accès ;
- durée de conservation ;
- suppression ;
- export ;
- logs.

Ne jamais prétendre à une conformité juridique spécifique sans validation externe.

---

# 25. ACCEPTATION LIVRAISON 3

PASS uniquement si :

- un parent peut accéder uniquement à son foyer ;
- un élève ne peut voir que son compte ;
- dashboards réels ;
- progression réelle ;
- rapport parent réel ;
- permissions testées ;
- tentatives d’accès croisé testées ;
- FR/AR ;
- mobile ;
- régressions phases 1–2 absentes.

---

# 26. LIVRAISON 4 — COMMERCIALISATION + ADMIN + FINALISATION

Contient :

- abonnements ;
- commandes ;
- droits ;
- paiement ;
- remboursements ;
- administration métier ;
- analytics ;
- audit ;
- sécurité ;
- performance ;
- tests de charge raisonnables ;
- préparation production.

---

# 27. MODÈLE COMMERCIAL

Créer les concepts :

### Product / Offer
Ce qui est vendu.

### Order
Commande.

### Payment
Paiement.

### Entitlement
Droit d’accès.

### Subscription
Uniquement si réellement utilisé.

Ne jamais confondre paiement et droit d’accès.

Un paiement confirmé peut générer un entitlement.

Un remboursement peut modifier l’entitlement selon règle explicite.

---

# 28. TABLES COMMERCIALES

Selon besoin :

- `mnin_orders`
- `mnin_order_items`
- `mnin_payments`
- `mnin_payment_events`
- `mnin_entitlements`
- `mnin_subscriptions`

Utiliser identifiants uniques.

Webhooks :

- authentifiés ;
- vérifiés ;
- idempotents ;
- journalisés.

Ne jamais créditer deux fois une commande suite au même webhook.

---

# 29. PRESTATAIRE DE PAIEMENT

Aucune intégration finale tant que le porteur du projet n’a pas fourni :

- nom du prestataire ;
- documentation API ;
- environnement test ;
- mécanisme webhook ;
- règles de remboursement ;
- devise ;
- frais ;
- conditions.

Si ces informations manquent :

marquer la tâche :

**BLOQUÉE — PRESTATAIRE NON FOURNI**

et ne pas inventer.

---

# 30. ADMINISTRATION MÉTIER

Créer des écrans WordPress dédiés :

- Dashboard MNIN NBDA
- Contenus
- Catalogue
- Sources
- Publication
- Utilisateurs
- Familles
- Abonnements
- Finance
- Sécurité
- Commandes
- Droits
- Analytics
- Système
- Audit
- Paramètres

Utiliser les APIs WordPress.

Ne pas remplacer l’admin WordPress native.

---

# 31. STRATÉGIE HÉBERGEMENT WORDPRESS.COM

Cible déclarée :

**WordPress.com Personnel**

Ne jamais supposer qu’un environnement de préproduction, SSH, sauvegarde one-click ou accès serveur avancé existe.

La stratégie de validation doit donc être indépendante de ces fonctions.

## 31.1 Environnement de test obligatoire

Avant production :

- installation WordPress propre locale ou de test ;
- import / installation du thème ;
- installation du plugin ;
- activation ;
- tests ;
- captures ;
- rapport.

Outils possibles :

- `wp-env`
- WordPress Playground
- Docker WordPress
- autre installation de test réellement disponible.

## 31.2 Production

Avant installation en production :

- exporter le contenu lorsque possible ;
- conserver copie des ZIP actifs ;
- documenter procédure de retour arrière ;
- éviter toute migration destructive ;
- faire les migrations additives ;
- vérifier les limites de l’hébergement.

Si le plan/hébergement bloque une fonctionnalité requise :
documenter précisément le blocage avant déploiement.

---

# 32. ROLLBACK

Créer :

`ROLLBACK.md`

Pour chaque livraison :

- fichiers modifiés ;
- tables créées ;
- options créées ;
- migrations ;
- procédure de désactivation ;
- procédure de restauration ;
- limites.

La désactivation du plugin ne doit pas supprimer les données automatiquement.

La suppression définitive nécessite une action explicite.

---

# 33. FR / AR

Toutes les chaînes interface utilisent :

- `__()`
- `_e()`
- `esc_html__()`
- fonctions WordPress i18n appropriées.

Text domain :

`mnin-nbda`

Fournir POT.

RTL :

- layout ;
- flèches ;
- breadcrumbs ;
- timeline ;
- progression ;
- navigation ;
- formulaires.

Tester au moins :

- Home AR ;
- Matières AR ;
- Connexion AR ;
- Dashboard élève AR.

---

# 34. ACCESSIBILITÉ

Cible :

WCAG 2.2 AA autant que raisonnablement possible.

Obligatoire :

- structure sémantique ;
- landmarks ;
- skip link ;
- focus visible ;
- labels ;
- erreurs de formulaire ;
- contraste ;
- touch targets ;
- clavier ;
- reduced motion ;
- alt ;
- pas de hover-only ;
- pas de scroll-jacking ;
- aucune information uniquement par couleur.

---

# 35. PERFORMANCE

Mesurer et documenter.

Optimiser :

- SVG logo ;
- images responsive ;
- WebP/AVIF ;
- lazy-loading ;
- JS par page ;
- CSS non bloquant lorsque possible ;
- fonts locales ;
- éviter librairies lourdes ;
- animations GPU-friendly ;
- pas de boucle permanente inutile.

La zone 14→26 ne doit pas pénaliser fortement le premier rendu.

La charger après le contenu critique si nécessaire.

---

# 36. SÉCURITÉ

Obligatoire :

- nonces ;
- capabilities ;
- sanitation ;
- escaping ;
- prepared SQL ;
- REST permission callbacks ;
- validation MIME ;
- uploads sécurisés ;
- aucun secret dans Git/ZIP ;
- aucune clé dans JS ;
- aucune donnée d’un autre foyer via IDOR.

Créer des tests manuels d’autorisation.

---

# 37. TESTS D’INSTALLATION RÉELS

Pour chaque phase :

1. démarrer une WordPress propre ;
2. installer le plugin ZIP ;
3. activer ;
4. installer le thème ZIP ;
5. activer ;
6. vérifier absence erreur fatale ;
7. créer/importer contenu démo ;
8. tester frontend ;
9. tester admin ;
10. tester désactivation/réactivation ;
11. tester mise à jour si applicable.

Conserver les résultats dans le QA report.

---

# 38. FORMAT QA

Pour chaque test :

| ID | Test | Environnement | Résultat | Preuve / commentaire |
|---|---|---|---|---|
| QA-001 | Activation plugin | WP x / PHP x | PASS | ... |

Valeurs autorisées :

- PASS
- FAIL
- NON TESTÉ
- BLOQUÉ

Aucune autre formulation ambiguë.

---

# 39. LIVRABLES PAR PHASE

Chaque phase crée :

- ZIP thème si modifié ;
- ZIP plugin si modifié ;
- changelog ;
- QA report ;
- notes migration ;
- captures ;
- liste risques.

---

# 40. LIVRAISON FINALE

Créer :

`mnin-nbda-wordpress-distribution.zip`

Structure :

```text
mnin-nbda-wordpress-distribution/
├── mnin-nbda-theme.zip
├── mnin-nbda-core.zip
├── README_INSTALLATION.md
├── README_DEPLOY.md
├── AUDIT_EXISTANT.md
├── DATA_PRIVACY_MODEL.md
├── ROLLBACK.md
├── QA_REPORT_FINAL.md
├── CHANGELOG.md
├── ASSET_MANIFEST.md
├── DESIGN_SYSTEM.md
└── screenshots/
```

---

# 41. CRITÈRES FINAUX MESURABLES

Le projet final est accepté seulement si :

### Installation
- thème ZIP s’installe ;
- plugin ZIP s’installe ;
- activation sans erreur fatale.

### Branding
- logo chemin lumineux ;
- signature exacte ;
- palette validée ;
- favicon lisible.

### Public
- Home complète ;
- huit matières ;
- Méthode ;
- Démo ;
- Tarifs sans prix inventé ;
- FAQ.

### Pédagogie
- matière pilote validée ;
- diagnostic réel ;
- leçon réelle ;
- exercice réel ;
- progression réelle ;
- révision réelle.

### Élève
- authentification ;
- dashboard ;
- progression ;
- leçon ;
- erreurs ;
- révisions.

### Parent
- relation foyer ;
- dashboard ;
- rapport ;
- séparation stricte des données.

### Admin
- gestion contenu ;
- familles ;
- droits ;
- audit.

### Langues
- FR ;
- AR ;
- RTL.

### Accessibilité
- clavier ;
- focus ;
- reduced motion ;
- contraste vérifié.

### Sécurité
- tests IDOR ;
- capabilities ;
- nonces ;
- REST sécurisé.

### QA
- tous les tests classés PASS/FAIL/NON TESTÉ/BLOQUÉ ;
- aucun test non exécuté présenté comme réussi.

---

# 42. MÉTHODE D’EXÉCUTION

Exécuter exactement :

## PHASE 0
Audit.

## PHASE 1
Identité + thème + Home.

### GATE 1
Tester.
Livrer.
Ne pas poursuivre si FAIL.

## PHASE 2
Moteur pédagogique sur Mathématiques.

### GATE 2
Tester.
Livrer.
Ne pas poursuivre si FAIL.

## PHASE 3
Élève + Parent.

### GATE 3
Tester.
Livrer.
Ne pas poursuivre si FAIL.

## PHASE 4
Commercialisation + paiement + Admin + production readiness.

### GATE 4
Tester.
Livrer.

---

# 43. RÈGLE POUR UN AGENT AUTONOME

Si l’agent peut demander validation humaine :

**s’arrêter après chaque Gate et demander l’acceptation avant la phase suivante.**

Si aucune validation humaine intermédiaire n’est possible :

- exécuter les phases ;
- NE PAS masquer un Gate en échec ;
- interrompre immédiatement la suite si un Gate critique échoue ;
- livrer l’état exact.

---

# 44. INTERDICTIONS

Ne jamais :

- développer Tutor LMS en parallèle ;
- coder deux moteurs pédagogiques ;
- inventer un prestataire paiement ;
- inventer des tarifs ;
- inventer des statistiques ;
- inventer des témoignages ;
- collecter inutilement des données mineurs ;
- faire dépendre le produit d’Elementor ;
- mettre toute la logique dans le thème ;
- supprimer des données à la désactivation ;
- contourner WordPress capabilities ;
- livrer un ZIP non testé en disant “prêt” ;
- annoncer un déploiement non effectué ;
- promettre une réussite scolaire ;
- promettre un métier futur ;
- écrire “mmin tbda” ;
- rendre une API payante obligatoire ;
- ajouter une dépendance SaaS payante pour une fonction essentielle.

---

# 45. VISION PRODUIT

L’utilisateur doit vivre trois étapes :

### 1.
**Je comprends où commencer.**

### 2.
**Je peux progresser étape par étape.**

### 3.
**Mes efforts d’aujourd’hui ouvrent des possibilités pour demain.**

Le produit ne vend pas un rêve abstrait.

Il prouve sa valeur par :

**Diagnostic → Remise à niveau → Apprentissage → Exercices → Maîtrise → Révision → Brevet.**

Puis seulement, il permet à l’élève de se projeter vers l’avenir.

---

# 46. RÉPONSE FINALE DE L’AGENT

À la fin de CHAQUE livraison, répondre avec :

1. périmètre réellement livré ;
2. fichiers créés/modifiés ;
3. ZIP générés ;
4. tests exécutés ;
5. nombre PASS ;
6. nombre FAIL ;
7. nombre NON TESTÉ ;
8. nombre BLOQUÉ ;
9. risques connus ;
10. prochaines étapes.

À la fin du projet :

1. lien/chemin distribution ZIP ;
2. lien/chemin thème ZIP ;
3. lien/chemin plugin ZIP ;
4. version WordPress testée ;
5. version PHP testée ;
6. QA final ;
7. instructions d’installation ;
8. points restant à configurer.

Ne jamais embellir l’état réel du projet.

---


# ANNEXE TECHNIQUE V4.2 — VERROUILLAGE AVANT DÉVELOPPEMENT
## À joindre au Prompt Master V4/V4.1 sans réécrire les sections existantes

Cette annexe prévaut sur toute formulation plus vague du Prompt Master précédent.
Elle verrouille le modèle pédagogique, les comptes Parent/Élève, les droits d’accès, le bilinguisme dynamique, la charte chiffrée et le périmètre exact du pilote.

---

# A. PHASE 0 ÉTENDUE — ARCHITECTURE AVANT DESIGN

La Phase 0 doit désormais produire et faire valider, avant la finalisation du thème :

1. `AUDIT_EXISTANT.md`
2. `PEDAGOGICAL_MODEL.md`
3. `PEDAGOGICAL_GRAPH.json`
4. `DATA_MODEL.md`
5. `AUTHORIZATION_MODEL.md`
6. `ENTITLEMENT_MODEL.md`
7. `I18N_DATA_MODEL.md`
8. `DESIGN_TOKENS.json`
9. `SECURITY_MODEL.md`
10. `MIGRATION_PLAN.md`

Le Gate 0 est obligatoire.

Il est interdit de lancer la Phase 1 si un de ces documents est absent ou incohérent avec le modèle de données réel.

---

# B. MODÈLE PÉDAGOGIQUE — RÈGLES EXPLICITES

## B.1 Unité centrale : la compétence

Le moteur ne raisonne pas seulement en “leçons”.

Créer un référentiel de compétences.

Chaque compétence possède au minimum :

- `skill_id`
- matière
- semestre
- titre FR
- titre AR
- description FR
- description AR
- niveau de granularité
- prérequis directs
- objectifs associés
- leçons associées
- questions diagnostiques associées
- questions d’entraînement associées
- niveau de maîtrise de l’élève
- date de dernière preuve de maîtrise
- date de prochaine révision

Exemple structurel :

```json
{
  "skill_id": "math.eq.linear.solve",
  "subject": "MATH",
  "prerequisites": [
    "math.signed.operations",
    "math.literal.reduction"
  ]
}
```

Les exemples ne constituent pas une validation pédagogique.
Le graphe réel doit être validé par une personne compétente en pédagogie / programme 3AC avant généralisation.

---

# C. GRAPHE DE DÉPENDANCES

Les compétences forment un graphe orienté acyclique autant que possible.

Relation :

`A → B`

signifie :

**A est un prérequis de B.**

Le moteur doit pouvoir :

- récupérer les prérequis directs ;
- récupérer les prérequis transitifs ;
- détecter une boucle lors de l’édition du graphe ;
- interdire la publication d’un graphe cyclique non justifié ;
- versionner le graphe ;
- identifier les compétences affectées par une modification.

Créer un outil Admin permettant de visualiser au minimum :

- compétence ;
- prérequis ;
- dépendants ;
- état de publication.

---

# D. OBJECTIFS PÉDAGOGIQUES

Chaque leçon est reliée à un ou plusieurs objectifs observables.

Chaque objectif possède :

- `objective_id`
- compétence associée
- formulation FR
- formulation AR
- niveau de difficulté
- type de preuve attendu
- questions permettant de l’évaluer

Ne pas utiliser des formulations vagues comme :

“comprendre les équations”.

Préférer une formulation observable telle que :

“résoudre une équation du premier degré à une inconnue dans un cas donné”.

Le contenu réel doit être validé pédagogiquement.

---

# E. DIAGNOSTIC — MÉCANIQUE DE DÉCISION

## E.1 Une question ne diagnostique jamais “une leçon”

Chaque question diagnostique une ou plusieurs compétences précises.

Structure minimale :

- question
- compétences principales
- compétences secondaires éventuelles
- difficulté
- réponse correcte
- distracteurs
- explication
- poids diagnostique

## E.2 Analyse d’une erreur

Lorsqu’un élève échoue :

1. identifier la compétence directement évaluée ;
2. regarder les compétences prérequises ;
3. consulter les preuves récentes disponibles sur ces prérequis ;
4. si les prérequis sont incertains, proposer une question de discrimination ;
5. éviter de conclure à une lacune sur la base d’une seule erreur si aucune preuve complémentaire n’existe ;
6. calculer un niveau de confiance ;
7. recommander la prochaine action.

Le moteur doit pouvoir renvoyer :

- compétence probablement maîtrisée ;
- compétence incertaine ;
- compétence à consolider ;
- prérequis probablement manquant ;
- preuve insuffisante.

## E.3 Question de discrimination

Exemple de logique :

Erreur sur une équation.

Le moteur ne suppose pas immédiatement :
“l’élève ne sait pas résoudre une équation”.

Il teste si nécessaire :

- calcul avec nombres relatifs ;
- réduction d’expression ;
- opération inverse ;
- résolution.

Le système doit pouvoir isoler la source probable de la difficulté.

---

# F. SCORE DE MAÎTRISE

Le niveau de maîtrise est stocké par compétence.

Échelle technique recommandée :

`0.00 → 1.00`

États UI dérivés :

- `0.00–0.39` : À reprendre
- `0.40–0.64` : À consolider
- `0.65–0.84` : En bonne voie
- `0.85–1.00` : Maîtrisé

IMPORTANT :
ces seuils sont des valeurs techniques initiales configurables.
Ils ne deviennent définitifs qu’après validation pédagogique et tests utilisateurs.

Le score ne doit jamais reposer uniquement sur la dernière réponse.

Le calcul doit prendre en compte :

- récence ;
- difficulté ;
- nombre de preuves ;
- réussite ;
- échec ;
- aide utilisée ;
- répétition excessive de la même question.

Documenter la formule dans `PEDAGOGICAL_MODEL.md`.

---

# G. RÈGLE DE PASSAGE À LA SUITE

Une compétence peut être considérée comme “maîtrisée” seulement si :

1. le score dépasse le seuil configuré ;
2. au moins plusieurs preuves indépendantes existent ;
3. les preuves ne proviennent pas toutes de répétitions identiques ;
4. aucune lacune critique prérequise n’est active ;
5. une vérification différée peut être planifiée.

Le nombre exact de preuves est configurable.

Valeur initiale de test recommandée :
3 preuves indépendantes.

Ne pas présenter cette valeur comme une vérité pédagogique universelle.

---

# H. REMISE À NIVEAU

Lorsqu’un prérequis manque :

1. suspendre la progression sur la compétence cible si le blocage est critique ;
2. proposer une micro-remédiation ciblée ;
3. ne pas renvoyer automatiquement l’élève vers un chapitre entier ;
4. réévaluer le prérequis ;
5. reprendre la compétence cible lorsque la preuve devient suffisante.

Structure :

`Compétence cible`
→ `Prérequis manquant`
→ `Micro-remédiation`
→ `Vérification`
→ `Retour à la compétence cible`

L’interface doit expliquer la logique à l’élève en langage simple.

Exemple :

**On revoit d’abord cette base, puis on reprend ton exercice.**

---

# I. RÉVISION ESPACÉE

La révision est pilotée par compétence.

Prévoir un scheduler interne WordPress basé sur :

- date de maîtrise ;
- qualité de la preuve ;
- historique de révision ;
- échecs récents.

Première politique technique configurable :

- révision 1 : J+1
- révision 2 : J+3
- révision 3 : J+7
- révision 4 : J+14
- révision 5 : J+30

En cas d’échec :
réduire l’intervalle.

En cas de réussite robuste :
augmenter progressivement.

Ces intervalles sont des paramètres techniques initiaux et doivent être validés pédagogiquement.

Ne pas dépendre d’une API externe pour le scheduling.

---

# J. PROCHAINE ÉTAPE — ALGORITHME

La fonction `get_next_best_action(student_id)` doit produire une recommandation déterministe et explicable.

Ordre de priorité proposé :

1. prérequis critique manquant ;
2. activité diagnostique nécessaire ;
3. leçon en cours non terminée ;
4. exercice de consolidation ;
5. révision arrivée à échéance ;
6. nouvelle compétence débloquée ;
7. examen blanc si conditions remplies.

Chaque décision doit pouvoir retourner un `reason_code`.

Exemples :

- `MISSING_PREREQUISITE`
- `DIAGNOSTIC_NEEDED`
- `CONTINUE_LESSON`
- `CONSOLIDATION_REQUIRED`
- `REVISION_DUE`
- `NEW_SKILL_AVAILABLE`

L’interface peut alors expliquer :

**Pourquoi cette étape ?**

---

# K. PILOTE MATHÉMATIQUES — DÉFINITION EXACTE

Ne plus utiliser l’expression ambiguë “matière pilote complète”.

La Phase 2 doit livrer un :

# **PILOTE PÉDAGOGIQUE MATHÉMATIQUES DE BOUT EN BOUT**

Il doit couvrir au minimum :

- 1 mini-domaine cohérent ;
- 3 compétences reliées par prérequis ;
- 1 graphe de dépendances réel ;
- 1 diagnostic initial ;
- au moins 3 leçons complètes ;
- au moins 8 questions diagnostiques ;
- au moins 15 exercices d’entraînement ;
- indices ;
- corrections ;
- feedbacks ;
- 1 chemin de remise à niveau ;
- calcul de maîtrise ;
- file de révision ;
- `get_next_best_action()` ;
- dashboard élève reflétant les résultats ;
- dashboard parent reflétant ces mêmes données.

Pourquoi 3 compétences :
une seule notion ne permet pas de tester réellement la logique de prérequis et de remédiation.

Le pilote est considéré validé seulement si un scénario complet fonctionne :

**diagnostic → détection d’un prérequis faible → remédiation → validation → retour à la notion cible → maîtrise → révision planifiée**

---

# L. COMPTES PARENT / ÉLÈVE — MODÈLE FIGÉ

## L.1 Parent

Le parent possède un compte WordPress réel avec :

- email ;
- mot de passe ;- rôle/capabilities Parent.

## L.2 Enfant

Par défaut, l’enfant possède :

- un `child_profile_id` interne ;
- prénom ou pseudonyme d’usage ;
- langue ;
- niveau 3AC ;
- identifiant élève unique ;
- mot de passe élève.

Aucune adresse email enfant n’est requise.

## L.3 Création

Le parent crée l’enfant depuis son espace.

Le serveur :

1. crée `child_profile`;
2. génère un identifiant unique lisible ;
3. propose la création ou génère un mot de passe initial robuste ;
4. stocke uniquement le hash selon les mécanismes WordPress ;
5. affiche les identifiants au parent une seule fois si générés ;
6. journalise la création.

L’identifiant doit pouvoir être régénéré uniquement via une procédure contrôlée.

---

# M. SESSIONS ÉLÈVE

L’authentification doit utiliser les mécanismes sécurisés WordPress ou une couche dédiée compatible WordPress, sans stockage de mot de passe en clair.

Règles :

- cookies sécurisés ;
- SameSite approprié ;
- HTTPS obligatoire en production ;
- expiration de session ;
- possibilité de déconnexion ;
- invalidation après changement de mot de passe ;
- rate limiting des tentatives ;
- message d’erreur ne révélant pas si un identifiant existe.

Le parent doit pouvoir :

- réinitialiser les accès de son enfant ;
- révoquer les sessions enfant si cette fonction est implémentée ;
- ne jamais voir le mot de passe actuel.

---

# N. CONTRÔLE D’ACCÈS FOYER

Chaque requête serveur concernant un enfant doit vérifier :

`current_parent_id`
→ relation active
→ `child_profile_id`

Ne jamais autoriser l’accès uniquement parce que l’URL contient un ID valide.

Tests obligatoires :

- Parent A tente enfant B → REFUS
- Élève A tente progression élève B → REFUS
- ID modifié manuellement → REFUS
- REST endpoint avec ID tiers → REFUS
- objet supprimé/désactivé → REFUS

---

# O. DROITS D’ACCÈS — ENTITLEMENTS DÈS LA PHASE 0

Les droits d’accès existent AVANT le paiement.

Le paiement ne crée qu’un événement commercial qui peut accorder un droit.

Créer le modèle :

`Entitlement`

Champs minimum :

- `entitlement_id`
- bénéficiaire (`child_profile_id`)
- type
- matière ou bundle
- date début
- date fin nullable
- statut
- source
- référence source
- créé par
- date création

Statuts :

- ACTIVE
- SCHEDULED
- EXPIRED
- SUSPENDED
- REVOKED

Types exemples :

- SUBJECT_ACCESS
- ALL_SUBJECTS
- EXAM_ACCESS
- PREMIUM_TOOLS

La vérification d’accès se fait via :

`student_has_entitlement(student_id, resource)`

et jamais via :
“a-t-il payé ?”

---

# P. RÈGLES D’ACCÈS PAR DURÉE

Le moteur de droits doit supporter dès le départ :

- accès permanent ;
- accès du X au Y ;
- accès par matière ;
- accès à toutes les matières ;
- période d’essai si décidée plus tard ;
- droit accordé manuellement par Admin ;
- droit importé lors d’une migration.

Même sans paiement configuré, l’Admin doit pouvoir attribuer et révoquer un entitlement.

---

# Q. BILINGUISME DES DONNÉES PÉDAGOGIQUES

Le bilinguisme ne concerne pas seulement les menus WordPress.

Doivent être traduisibles :

- matière ;
- compétence ;
- objectif ;
- titre leçon ;
- contenu leçon ;
- question ;
- réponse ;
- distracteur ;
- indice ;
- feedback ;
- correction ;
- message de diagnostic ;
- raison de prochaine étape ;
- examen ;
- consigne.

Pour les données structurées métier, stocker explicitement une représentation traduisible.

Le modèle choisi doit être documenté dans `I18N_DATA_MODEL.md`.

---

# R. STRATÉGIE DE TRADUCTION

Règle :

- contenus éditoriaux WordPress → Polylang lorsque pertinent ;
- données pédagogiques structurées → champs/objets localisés contrôlés par `mnin-nbda-core`.

Exemple structurel :

```json
{
  "title": {
    "fr": "Équations du premier degré",
    "ar": "معادلات من الدرجة الأولى"
  }
}
```

Ne pas générer automatiquement la traduction à la volée avec une API payante.

Aucune API payante de traduction.

Fallback :

si la traduction AR manque :

- l’Admin voit une alerte ;
- la publication bilingue peut être bloquée selon le type de contenu ;
- ne pas afficher silencieusement du français dans une interface arabe pour un contenu critique.

---

# S. CHARTE GRAPHIQUE CHIFFRÉE

Créer `DESIGN_TOKENS.json`.

Valeurs de référence V4.2 :

## Couleurs

```json
{
  "color": {
    "teal-900": "#0F4C4C",
    "teal-800": "#0B5A5F",
    "teal-600": "#0F766E",
    "orange-500": "#F59E0B",
    "orange-600": "#EA7C0B",
    "cream-50": "#FFF9EF",
    "cream-100": "#FFF7EB",
    "mint-100": "#D1FAE5",
    "ink-900": "#1F2937",
    "ink-700": "#374151",
    "muted-600": "#6B7280",
    "white": "#FFFFFF",
    "success": "#177D5B",
    "warning": "#B96700",
    "danger": "#B42318"
  }
}
```

Les variantes peuvent être affinées après contrôle de contraste, mais les changements doivent être documentés.

## Polices

FR / Latin :
`Inter Variable`, fallback `Arial, sans-serif`

AR :
`Noto Sans Arabic Variable`, fallback `Arial, sans-serif`

## Largeur

- content max : 1200 px
- wide max : 1380 px

## Spacing scale

- 4
- 8
- 12
- 16
- 24
- 32
- 48
- 64
- 80
- 96 px

## Radius

- small : 8 px
- medium : 14 px
- large : 24 px
- xl : 32 px
- pill : 999 px

## Touch

Minimum :
44 × 44 px

## Typographie indicative desktop

- Hero H1 : clamp(48px, 6vw, 80px)
- H2 : clamp(34px, 4vw, 52px)
- H3 : 24–32 px
- Body large : 18 px
- Body : 16 px
- Small : 14 px
- Micro : minimum 12 px, avec contraste suffisant

## Mobile

- H1 : 40–54 px
- H2 : 30–38 px
- Body : 16 px minimum pour champs de formulaire

## Contraste

Cible :
WCAG 2.2 AA.

Le rapport QA doit inclure les couples texte/fond principaux réellement testés.

---

# T. OMBRES ET MOTION

Ombres :

- très légères ;
- pas d’effet “carte flottante SaaS générique” excessif.

Motion :

- 150–250 ms pour micro-interactions ;
- 300–600 ms pour transition de section ;
- easing doux ;
- transform/opacity préférés ;
- aucun scroll-jacking.

`prefers-reduced-motion: reduce`
doit désactiver les mouvements décoratifs non essentiels.

---

# U. GATE 0 — CRITÈRES D’ACCEPTATION

Gate 0 = PASS seulement si :

- audit existant terminé ;
- modèle pédagogique documenté ;
- graphe de compétences défini pour le pilote ;
- modèle de maîtrise défini ;
- règles de remédiation définies ;
- règles de révision définies ;
- modèle Parent/Enfant défini ;
- modèle session défini ;
- entitlements définis ;
- FR/AR dynamique défini ;
- design tokens chiffrés ;
- modèle sécurité défini ;
- plan de migration défini ;
- aucun besoin d’API payante essentielle.

Sinon :
ne pas lancer la Phase 1.

---

# V. GATE 2 — CRITÈRES D’ACCEPTATION RENFORCÉS

Le moteur pédagogique pilote est PASS uniquement si le scénario automatisé ou reproductible suivant fonctionne :

1. créer un élève pilote ;
2. lui accorder Mathématiques ;
3. démarrer diagnostic ;
4. répondre correctement à certaines compétences ;
5. échouer sur une compétence cible ;
6. obtenir une question discriminante ;
7. identifier un prérequis faible ;
8. recevoir la micro-remédiation correspondante ;
9. réussir la vérification ;
10. revenir à la compétence cible ;
11. réussir plusieurs preuves indépendantes ;
12. atteindre l’état Maîtrisé ;
13. obtenir une révision future ;
14. afficher la prochaine étape avec `reason_code` ;
15. refléter le résultat dans le dashboard Élève ;
16. refléter le résultat dans le dashboard Parent.

Tout échec aux étapes 3–16 = Gate 2 FAIL.

---

# W. API PAYANTE — RAPPEL ABSOLU

Fonctions essentielles sans API payante.

Interdits comme dépendance essentielle :

- OpenAI API ;
- Anthropic API ;
- Gemini payant ;
- traduction payante ;
- recherche SaaS payante ;
- email SaaS payant obligatoire ;
- analytics SaaS payant obligatoire ;
- stockage SaaS payant obligatoire.

Le QA final doit contenir :

`Dépendance API payante essentielle : NON`

Le paiement transactionnel futur est traité séparément et ne doit jamais conditionner le fonctionnement pédagogique de base en environnement de test.

---

# X. PREUVE DE FONCTIONNEMENT

Le Prompt Master est une spécification.

Il n’est jamais une preuve de fonctionnement.

Seules constituent des preuves :

- installation réelle ;
- activation réelle ;
- tests réels ;
- captures / logs ;
- scénarios reproduits ;
- QA report ;
- validation des Gates.

Ne jamais confondre :
**“spécifié”** avec **“fonctionnel”**.

---

# Y. ORDRE FINAL DES PHASES

## Phase 0
Audit + modèle pédagogique + données + comptes + droits + sécurité + i18n + design tokens.

## Gate 0
Validation obligatoire.

## Phase 1
Identité + Home + thème + pages publiques.

## Gate 1
Installation et QA.

## Phase 2
Pilote Mathématiques end-to-end sur 3 compétences liées.

## Gate 2
Scénario pédagogique complet obligatoire.

## Phase 3
Élève + Parent.

## Gate 3
Sécurité foyer + progression + rapports.

## Phase 4
Commercialisation + paiement sélectionné + Admin + production readiness.

## Gate 4
Validation finale.

---

# Z. RÈGLE DE PRIORITÉ

En cas de conflit entre cette annexe et la V4/V4.1 :

**cette annexe prévaut.**