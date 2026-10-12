# Reprise Home MNIN NBDA — contrôle du 12 octobre 2026

## Périmètre et référence officielle

- Ticket de cadrage : [#5](https://github.com/hakimalamiouahabi/mnin-nbda-brevet-3ac/issues/5).
- La dernière image approuvée **« Ta mission : un déclic aujourd’hui. »** prévaut sur les chartes précédentes.
- Source PNG reçue directement du propriétaire ; SHA-256 contrôlé : `393dfd6498180398023b712ef9d68e95a902ac6e0d5b5845818bc75c3b53166e`.
- Dimensions `1024 × 1536`, format PNG RGBA. **PASS** sur le fichier transmis le 12/10/2026.
- L'original binaire **n'est pas inclus dans cette branche documentaire** ; il doit être remis à Codex depuis l'archive officielle vérifiée. Aucun JPEG ou PNG régénéré ne saurait s'y substituer.

## Audit du dépôt

- La branche `main` vérifiée au commit `f7f9627f00329598b9227f980fbca30f34a59f39` contient les instructions, rôles et scripts de validation du référentiel, **pas** les fichiers du prototype local décrits dans la transcription Codex.
- Seule `main` était visible lors de l'audit du 12 octobre (avant la création de cette branche de reprise).
- Le ticket [#5](https://github.com/hakimalamiouahabi/mnin-nbda-brevet-3ac/issues/5) est accessible et ouvert. Les tickets #1–#4 sont également ouverts.
- Les commits `7ca83f7` (machine d'état) et `ef24acc` (intégration Hero) sont signalés dans la transcription Codex, mais **leur présence dans le dépôt distant n'est pas vérifiée**. Ne jamais les recréer à l'aveugle, ni écraser le worktree original.

## Ce qui est confirmé vs ce qui est rapporté

| Sujet | Statut | Preuve ou réserve |
|---|---|---|
| Original PNG et SHA-256 | PASS | Vérification des octets et métadonnées image dans la session du 12/10 |
| Lecture du ticket #5 | PASS | GitHub API |
| Présence sur main du prototype Codex | BLOQUÉ | Absent de l'arbre de main lors de l'audit |
| Rapport de tests statiques Codex | NON TESTÉ ici | Transcription : 8/8 unitaires, 5/5 E2E, 2/2 visuels ; preuves originales non récupérées |
| 9 cibles tactiles sous 44 px | FAIL selon transcription | À reproduire et corriger sur mobile |
| Sculpture Blender d'Amine | BLOQUÉ | Modèle procédural rejeté pour manque de fidélité |
| Firefox/Safari/iOS/Android, CWV réels | NON TESTÉ | Aucune mesure fiable transférée au dépôt |

## Reprise impérative

1. **Sauvegarder la session Codex avant toute écriture** : recenser `.worktrees/chemin-lumineux`, `git status`, `git log --all` et les commits locaux ; pousser les travaux sur une branche isolée. Ne pas merger sans revue.
2. **Importer l'original depuis l'archive officielle** et recontrôler le SHA-256. Inventorier les assets individuels et droits dans `ASSET_MANIFEST.md`; ne jamais déduire que le PNG aplati fournit des sources éditables.
3. **Créer un vrai responsive HTML/CSS** (texte HTML, pas page affichée comme PNG) et tester les 17+ viewports du ticket #5 ; supprimer les 9 défauts de cibles tactiles à 375 px.
4. **Préserver Amine tel quel en état statique.** Rendre la 3D optionnelle tant que la similitude n'est pas explicitement acceptée. Garder les fallbacks WebGL/JS/reduced-motion/saveData.
5. **Consigner les preuves** : captures viewport + full page, tests clavier/tactile/RTL, LCP/CLS/INP lorsque mesurables, détails des commits.

## Contraintes

- Aucun changement graphique, texte, logo, personnage ou section sans nouvelle validation.
- **Aucun bloc dédié aux matières dans le corps de cette Home approuvée.**
- Pas de redéploiement WordPress, pas de DNS, pas de paiement, pas d'API IA payante.
- Les 43 profils sont des définitions documentées : ne pas affirmer qu'ils sont autonomes ou lancés.
- Ne pas déclarer « pixel-perfect » simplement parce qu'un screenshot a été affiché : tester la structure responsive réelle.

**Cette note est un document de reprise, pas une validation de publication ni une fusion dans main.**
