=== MNIN NBDA — Progress & Quality ===
Contributors: MNIN NBDA
Tags: edtech, student-progress, privacy
Requires at least: 6.6
Requires PHP: 7.4
Stable tag: 1.0.3
License: GPL-2.0-or-later

== Description ==
Version 1.0.3 du plugin métier existant. Conserve les tables de progression
et les historiques actuels ; ne migre ni ne supprime aucune donnée à l'installation.

== Nouveautés ==
- GET /wp-json/mnin-progress/v1/overview : vue consolidée, strictement personnelle, en lecture seule.
- Aucun pourcentage général inventé. Leçons, atelier, QCM, objectif principal et Student Journey gardent leurs périmètres.
- Export et effacement WordPress des cinq autres catégories de données élèves : anciennes leçons, objectif Pixel/Learning, historique des objectifs Pixel, Student Journey et derniers résultats de QCM.
- Le compte, les autorisations 3AC et les cours restent conservés.
- L'export/effacement existant des tentatives SQL et du carnet par Progress & Quality reste inchangé.

== Installation et sûreté ==
Livraison sur branche de développement : ne pas activer sur le staging avant
revue humaine et vérifications fonctionnelles sur comptes de test anonymisés.
Faire une sauvegarde/restauration testable au préalable.
Un administrateur ne voit jamais les données d'un autre élève via l'API overview :
l'endpoint est limité aux données du compte actuellement authentifié.
L'export WordPress relève du circuit de demande d'export vérifiée par l'utilisateur.
L'effacement WordPress exige la confirmation de la demande dans ce circuit.

== Contrôles indispensables avant publication ==
1. Le plugin original 1.0.2 continue à fournir toutes ses APIs et tables.
2. GET /overview : 401 sans session ; 403 avec session non-3AC ; résultat personnel avec compte 3AC.
3. Tester l'export avec un compte factice comprenant les cinq méta et vérifier que le fichier est complet.
4. Tester l'effacement après validation WordPress ; vérifier que le compte et _mnin_student_access sont conservés.
5. Vérifier que le portail ne réutilise pas un « pourcentage global » trompeur.
6. Sécurité mobile/RTL et interactions élève à tester séparément.

== Limites ==
Pas de migration inter-magasin automatique. L'API est un contrat d'agrégation
en lecture seule, pas un réécriture des tableaux de bord existants.
Tests unitaires dans GitHub ≠ tests d'intégration en production.
