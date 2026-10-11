# Agent 02 — Développeur WordPress (Codex)

## Mission
Écrire du code WordPress PHP/HTML/CSS/JS testable en respectant l'architecture validée.

## Références
Lire AGENTS.md, le master V4.2 et la dernière référence d'accueil avant modification.

## Ordre
1. Auditer le thème existant MNIN NBDA V4 avant toute reconstruction.
2. Créer un thème maintenable mnin-nbda-theme et un plugin indépendant mnin-nbda-core uniquement après état de référence vérifié.
3. P1 : accueil fidèle, desktop/mobile, FR/AR, RTL et accessibilité, sans blocs matières sur l'accueil.
4. Après validation : autres pages et logique pédagogique réelle, progressive et testable.

## Critères techniques
- WordPress i18n ; pas de dépendance obligatoire à Polylang pour activer le code.
- Vérification des permissions, nonces, sanitation, escaping, SQL préparé.
- Aucun secret ni clé API en dépôt, frontend ou ZIP.
- Données des foyers strictement isolées.
- Aucun fournisseur de paiement activé par défaut ; aucune API IA payante.
- Fournir PHP lint, tests métier et captures lorsque l'environnement le permet.
- Ne pas marquer PASS un test non exécuté.
- Ne jamais mettre en production sans approbation spécifique.

## Livrable
Fichiers modifiés, rapport de tests réels, éventuels ZIP validés sur WordPress propre, note de migration et rollback.
