# Cycle DSI — Home MNIN NBDA & maintenance, Chat Only 700

**Date : 13 octobre 2026.** Mode : **une seule conversation ChatGPT**, référentiel exact de 700 rôles préexistants, aucun agent autonome démarré. Périmètre non destructif : audit réel HTML/PNG local + métadonnées en lecture seule Cloudflare D1 et WordPress.

## Référence officielle
- Home V1.0 originale : `MNIN_NBDA_HOME_REFERENCE_V1_0.png` — **1024 × 1536 px**.
- SHA-256 vérifié dans les fichiers originaux de la conversation : `393dfd6498180398023b712ef9d68e95a902ac6e0d5b5845818bc75c3b53166e`.
- **L'image originale n'a pas été réécrite.** Aucun original privé ajouté à ce dépôt public.
- Conflit à résoudre : la référence finale V1.0 approuvée exclut la nouvelle section Parents, mais `docs/references/PROMPT_MASTER_HOME_DESKTOP_XL_2026-10-11.md` demande cette section. Ne pas additionner les deux versions silencieusement.

## Home : navigateur réel, HTML actuel des fichiers de conversation
- **21 / 21 dimensions** rendues par Chromium/Playwright en mémoire, à partir de `MNIN_NBDA_RESPONSIVE_FINAL/index.html` et des images originales disponibles.
- **0 débordement horizontal** et **0 erreur JavaScript** dans les 21 formats.
- Captures pleine page conservées dans le pack de conversation : Laptop Small **1280 × 720** (maquette 07 pour revue), tablette **834 × 1194**, mobile **390 × 844**.
- **1 fichier CSS manquant** : `assets/cityline-crop.png`, utilisé pour la skyline mobile ; la vue mobile perd le décor urbain derrière son soleil.
- Selon la dimension testée, **9 à 12 images visibles sur 14 images HTML** ne satisfont pas le seuil indicatif largeur native ≥ 2 × largeur rendue, ce qui explique des risques de pixellisation sur écrans denses.
- Exemples vérifiés des fichiers actuels : logo **224 × 113**, pictogrammes **95 × 87**, cartes 1AC/2AC/3AC **322 × 215**, **305 × 215**, **322 × 215**, Amine **1024 × 1536**.
- **Pas de validation 8K/pixel-perfect** : la montée en taille d'un petit PNG n'ajoute pas de détail. Priorité aux véritables masters HD et au vectoriel lorsque c'est une illustration vectorielle.
- Plusieurs liens de la Home sont des ancres locales de démonstration : tests fonctionnels WordPress/authentification **NON TESTÉS**.

## Cloudflare / WordPress : lecture seule du 13 octobre
- D1 strictement ciblée : **`mnin-nbda-staging`** ; **42 tables, 30 index**, fichier signalé par Cloudflare à **1 159 168 octets**. Les trois autres bases Cloudflare ne font pas partie de la mission.
- Noms de tables avec événements/sessions/audit identifiés sans lire leurs données : structures potentiellement sensibles, **aucune purge autorisée**.
- Ces indicateurs ne démontrent ni index inutiles ni données expirées ; toute optimisation exige examen des requêtes, TTL, dépendances et restauration.
- WordPress staging : thème **MNIN NBDA V4** actif (`mnin-nbda`), **11 extensions (8 actives, 3 inactives, 0 mise à jour annoncée)**.
- Inactives : **Classic Editor, Crowdsignal Dashboard, Crowdsignal Forms**. Aucun jugement d'inutilité sans vérifier les dépendances ; aucune désinstallation.
- Jetpack Backup : **actif**, **4 sauvegardes**, dernière tentative le **12/10/2026 16:53:50**, statut `finished`, `last_attempt_failed=false`. **Restauration NON TESTÉE.**
- GitHub rapporte actuellement que ce dépôt est **public**, malgré d'anciennes consignes faisant référence à un dépôt privé. Pas de données d'élèves, de secrets ni d'archives SQL privées dans le dépôt.

## Rôles existants réellement consultés comme grilles de revue

Tous les identifiants ci-dessous sont issus **des 700 profils déjà catalogués** dans `mnin-bridge/agentgrid/profiles-700.json` ; **0 nouvel agent**.

- **DSI_01 — Design** : `EX_1_01_1_09` cohérence visuelle ; `EX_1_04_1_02` vectoriel SVG ; `EX_1_06_1_01` responsive.
- **DSI_02 — WordPress & logiciel** : `EX_2_01_1_01` architecte WordPress ; `EX_2_03_1_01` ingénieur frontend ; `EX_2_05_1_05` images responsives ; `EX_2_06_1_02` QA automation.
- **DSI_04 — Données** : `EX_4_01_1_01` data engineer ; `EX_4_02_1_01` data architect ; `EX_4_02_1_09` auditeur data.
- **DSI_05 — Sécurité et continuité** : `EX_5_01_1_05` sécurité WordPress ; `EX_5_06_1_06` sauvegarde ; `EX_5_06_1_07` restauration.

**Une seule session ChatGPT a effectué les contrôles** en appliquant ces perspectives métier ; aucun sous-agent IA indépendant n'a produit de livrable. Les autres profils restent disponibles, non mobilisés pour cette mission.

## Priorités P0 / P1
1. **P0** : conserver le PNG maître SHA-256 ; arbitrer le conflit de sections avant tout développement de contenu.
2. **P0** : retrouver un original HD/SVG du logo, des 4 icônes et des trois cartes ; ne pas remplacer silencieusement leur identité visuelle.
3. **P0** : remettre le fichier de skyline mobile manquant uniquement dans une copie de travail, puis valider sur les 21 formats.
4. **P0** : compléter l'inventaire des dépendances D1/WP sans contenu d'élèves et sans aucune purge.
5. **P1** : refaire les rendus à densité élevée avec assets maîtres, clavier/RTL/accessibilité et mesures de performance réelles.
6. **P1** : test contrôlé de restauration WordPress avant toute proposition de nettoyage, avec autorisation distincte.

## Statuts et preuves
- **PASS** : SHA-256 officiel, structure locale sur 21 viewports, détection des lacunes d'assets, inventaire D1 et plugins WP, existence d'une sauvegarde récente.
- **NON TESTÉ** : pixel-perfect face à la maquette, qualité HD native, scénarios de connexion, navigation réelle, métriques Web Vitals, restauration WordPress, optimisation de données effective.
- **BLOQUÉ** : masters graphiques natifs manquants, `cityline-crop.png` absent, conflit avec un ancien prompt Desktop XL.
- **ÉCRITURES** : zéro sur WordPress / Cloudflare D1, aucune purge GitHub ; cette branche contient uniquement un rapport.

Les captures PNG, l'original et le rapport JSON détaillé sont fournis dans le pack téléchargeable **de la conversation**, et non téléversés dans GitHub public. Le plugin MCP indépendant reste non installé dans ChatGPT : le mode Chat Only n'en dépend pas.
