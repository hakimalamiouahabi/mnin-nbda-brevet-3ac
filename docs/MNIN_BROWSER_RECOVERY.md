# MNIN NBDA — Déblocage navigateur Codex / captures privées

**Objectif :** contourner le démarrage impossible du navigateur interne Codex (Windows os error 3) sans modifier WordPress.

## Diagnostic
Sous Windows, le code d'erreur système 3 signifie généralement chemin introuvable. Si l'erreur survient avant l'ouverture de WordPress, distinguer :
1. Démarrage du navigateur : dossier de travail, exécutable, configuration et dépendances.
2. Session WordPress : authentification manuelle et stockage local sécurisé.
3. Navigation vers un aperçu privé : nonce émis par WordPress, puis capture à résolution contrôlée.

## Réparation portable
Le propriétaire dispose dans ChatGPT de l'archive MNIN_NBDA_Reparation_Navigateur_Codex_Playwright.zip : scripts Windows et Python indépendants, tests, outils de capture privée, de comparaison et maquette. Extraire le ZIP hors du dépôt, ne pas y placer ses cookies ni les captures d'utilisateurs.

Test de démarrage réalisable directement avec ce dépôt :

    py -3 -m venv .venv
    .\.venv\Scripts\python.exe -m pip install playwright
    .\.venv\Scripts\python.exe -m playwright install chromium
    .\.venv\Scripts\python.exe scripts\browser_smoke.py

Si Chromium ne démarre pas, tester le navigateur Microsoft Edge installé :

    .\.venv\Scripts\python.exe scripts\browser_smoke.py --channel msedge

Ne pas effacer les profils Chrome/Edge ni désactiver les protections WordPress.

## Référence visuelle
La référence PNG fournie dans la conversation mesure réellement **1586 × 992 px**, contrairement aux 1597 × 976 px cités auparavant. Les comparaisons pixel à pixel ne sont recevables qu'avec des captures de mêmes dimensions. Capturer également tablette/mobile et déclarer les comparaisons NON TESTÉ tant qu'aucune référence correspondante n'existe.

La police exacte de la maquette ne peut pas être certifiée par les métadonnées du PNG : identifier les sources de conception ou comparer les polices calculées du site et les glyphes.

## Sécurité
Ne pas envoyer les fichiers de session Playwright, captures d'enfants, noms d'élèves ou jetons nonce sur GitHub, Lovable, dans les logs publics ou les artefacts CI. Les dossiers concernés sont ignorés par Git.

**Interdiction de modifier le thème, les extensions, l'accueil, la base élèves ou de publier le tableau de bord sans accord explicite.**

## Réception
PASS = opération spécifiée réellement exécutée avec preuve. FAIL = anomalie constatée. BLOQUÉ = accès / navigateur indisponible. NON TESTÉ = résultat pas vérifié. Le test du navigateur autonome ne prouve PAS que le navigateur interne Codex est réparé.
