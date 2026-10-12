# MNIN NBDA — procédure de sauvegarde du travail Codex local
Date : 12 octobre 2026. Ticket : #5. PR de reprise : #6.

## Ce qui a été vérifié depuis GitHub
- Dépôt privé accessible : `hakimalamiouahabi/mnin-nbda-brevet-3ac`.
- `main` = `f7f9627f00329598b9227f980fbca30f34a59f39` au contrôle du 12/10.
- Branches distantes visibles : `main` et `audit-reprise-home-2026-10-12`.
- Aucun dossier `prototype/chemin-lumineux/` sur ces branches.
- Les identifiants courts `7ca83f7` et `ef24acc` retournent « No commit found for SHA » lors de la recherche GitHub directe. Cela **n'invalide pas** leur existence dans le Git local de la session Codex.
- Aucun accès au système de fichiers du worktree Codex d'origine depuis le connecteur GitHub : **BLOQUÉ** pour une sauvegarde automatique depuis ce chat.

## T0.1 — Dans la session Codex d'origine : INVENTAIRE SANS ÉCRITURE
Se placer dans le dépôt du projet `chemin-lumineux` tel qu'il existait dans Codex.
Ne pas recréer le projet, ne pas changer de branche, ne pas faire de reset, clean, rebase, stash, pull ni checkout.

```bash
pwd
git rev-parse --show-toplevel
git remote -v
git status --short --branch --untracked-files=all
git worktree list --porcelain
git branch -avv
git log --all --oneline --decorate -40
git reflog --all --date=iso -40
for commit in 7ca83f7 ef24acc; do
  if git cat-file -e "${commit}^{commit}" 2>/dev/null; then
    echo "PASS : $commit existe localement"
    git show -s --format='%H %ci %s' "$commit"
  else
    echo "BLOQUÉ : $commit absent de ce magasin Git"
  fi
done
```

Si les deux commits sont absents, examiner les autres worktrees signalés (notamment `.worktrees/chemin-lumineux`) et les journaux du projet **sans modifier leurs répertoires**. En dernier recours seulement, inventorier les commits orphelins avec `git fsck --full --no-reflogs --unreachable`; vérifier les objets avant de leur attribuer une identité.

## T0.2 — Sauvegarde distincte des fichiers non commités
Le branchement de commits **ne sauvegarde pas** les fichiers modifiés ou non suivis.
Avant toute action sur le worktree, relever ces chemins et protéger une copie hors du dépôt, dans le stockage privé de la session, en excluant les secrets, clés, `.env`, caches et dépendances volumineuses. Ne publier aucun fichier sensible sur GitHub.
Ne jamais utiliser `git clean` ni `git reset --hard` pour « réparer » ce blocage.

## T0.3 — Pousser le véritable commit Codex sur une branche isolée
**Uniquement** si l'inventaire prouve la présence du commit et si `git remote -v` confirme le dépôt privé attendu. Remplacer `ef24acc` par `7ca83f7` pour sauvegarder séparément l'autre commit si nécessaire.

```bash
# Aucun changement de branche de travail et aucun force push.
sha=$(git rev-parse --verify 'ef24acc^{commit}') || exit 1
branche="codex-rescue-2026-10-12-${sha:0:12}"
git show-ref --verify --quiet "refs/heads/$branche" && {
  echo "Cette branche existe déjà : vérifier sa cible avant toute intervention"; exit 1;
}
git branch "$branche" "$sha"
git push origin "refs/heads/$branche:refs/heads/$branche"
git ls-remote --heads origin "$branche"
git status --short --branch --untracked-files=all
```

Ne pas lancer cette commande si le remote est différent du dépôt prévu. L'opération crée une **nouvelle référence de sauvegarde** ; elle ne fusionne aucun code et ne sauvegarde pas les changements non commités. Si la branche existe à distance, ne pas l'écraser. Conserver le worktree original.

## T0.4 — Contrôle côté ChatGPT après poussée
1. Vérifier le SHA complet de chaque branche de secours dans GitHub.
2. Lister son arbre et identifier les vrais fichiers de `prototype/chemin-lumineux/`, leurs hashes et les fichiers absents.
3. Comparer la sauvegarde à `main` et à la documentation de la PR #6.
4. Mettre à jour le manifeste des assets sans inventer de fichier.
5. **Seulement ensuite** lancer la correction responsive sur une autre branche, puis les tests multi-appareils.

## Garde-fous
- Maquette officielle prioritaire ; ne pas réintroduire l'ancien design ni un bloc « matières » sur Home.
- Amine d'origine en visuel statique. Le GLB non approuvé reste interdit.
- Aucun écrasement de `main`, aucune fusion automatique.
- Aucun changement WordPress, staging, production, DNS, extension ou dépense.
- Tous résultats de tests doivent être accompagnés de preuves, avec statuts `PASS / FAIL / NON TESTÉ / BLOQUÉ`.

**État actuel : T0 inventaire distant PASS ; récupération des commits locaux BLOQUÉ jusqu'à accès à la session Codex d'origine.**
