#!/usr/bin/env bash
# Adapted from Lauren Tan's pstack (MIT). Inspect worktrees without deleting them.
# Usage: worktree-audit.sh [repo-path]
# Optional PSTACK_TRANSCRIPTS_DIR must be a host/user-supplied project directory.
set -u

repo="${1:-$(git rev-parse --show-toplevel 2>/dev/null)}"
[ -z "$repo" ] && { echo "not in a git repo; pass a repo path" >&2; exit 1; }
cd "$repo" || exit 1

worktrees=$(mktemp) || exit 1
prs=$(mktemp) || { rm -f "$worktrees"; exit 1; }
trap 'rm -f "$worktrees" "$prs"' EXIT
git worktree list --porcelain -z > "$worktrees" || exit 1
IFS= read -r -d '' first_entry < "$worktrees" || exit 1
main_wt=${first_entry#worktree }

# origin/main drives the ancestry check; PR head IDs also cover squash merges.
git fetch origin main --quiet 2>/dev/null || echo "warn: could not fetch origin/main; merged column may be stale" >&2
prs_known=no
if gh pr list --state all --limit 1000 --json number,state,headRefName,headRefOid \
    > "$prs" 2>/dev/null && jq -e 'type == "array"' "$prs" >/dev/null 2>&1; then
    prs_known=yes
else
    echo "[]" > "$prs"
    echo "warn: PR state unavailable; candidates require review" >&2
fi

transcripts=${PSTACK_TRANSCRIPTS_DIR:-}
now=$(date +%s)
printf "SIZE\tAGE\tMERGED\tDIRTY\tREMOTE\tPR\tLAST_CHAT\tBUCKET\tWORKTREE\n"

# NUL-delimited records preserve spaces and Git's unquoted filesystem paths.
while IFS= read -r -d '' entry; do
    case "$entry" in worktree\ *) wt=${entry#worktree } ;; *) continue ;; esac
    [ "$wt" = "$main_wt" ] && continue

    size=$(du -sh "$wt" 2>/dev/null | awk '{print $1}')
    head=$(git -C "$wt" rev-parse HEAD 2>/dev/null) || head=""
    head_ts=$(git -C "$wt" log -1 --format='%ct' HEAD 2>/dev/null || echo 0)
    age=$([ "$head_ts" -gt 0 ] 2>/dev/null && echo "$(( (now - head_ts) / 86400 ))d" || echo "?")
    git merge-base --is-ancestor "$head" origin/main 2>/dev/null
    case "$?" in 0) merged=YES ;; 1) merged=no ;; *) merged=unknown ;; esac

    if ! porcelain=$(git -C "$wt" status --porcelain --untracked-files=all 2>/dev/null); then
        dirty=unknown
    elif [ -z "$porcelain" ]; then
        dirty=clean
    else
        # Untracked files may be valuable work too; never call them disposable.
        dirty="wip:$(printf '%s\n' "$porcelain" | wc -l | tr -d ' ')"
    fi

    branch=$(git -C "$wt" symbolic-ref --quiet --short HEAD 2>/dev/null || echo "")
    if [ -z "$branch" ]; then remote=detached
    elif git -C "$wt" show-ref --verify --quiet "refs/remotes/origin/$branch"; then
        [ "$(git -C "$wt" rev-parse "origin/$branch" 2>/dev/null)" = "$head" ] \
            && remote=pushed \
            || remote="ahead$(git -C "$wt" rev-list --count "origin/$branch..HEAD" 2>/dev/null)"
    else remote=no-remote; fi

    pr="-"; pr_merged=no
    if [ -n "$branch" ] && [ "$prs_known" = yes ]; then
        # Check every matching PR: a historical merge must not hide an open PR.
        pr=$(jq -r --arg b "$branch" \
            '.[] | select(.headRefName==$b) | "#\(.number)/\(.state)"' "$prs" | paste -sd, -)
        [ -z "$pr" ] && pr="-"
        if [ -n "$head" ] && jq -e --arg b "$branch" --arg h "$head" \
            'any(.[]; .headRefName==$b and .state=="MERGED" and .headRefOid==$h)' \
            "$prs" >/dev/null; then pr_merged=yes; fi
    fi

    # No guessed client transcript paths. Absence is unknown, not inactivity.
    last="?"; last_ts=0
    if [ -n "$transcripts" ] && [ -d "$transcripts" ]; then
        f=$(rg -l --null --fixed-strings -e "${wt}/" -e "${wt}\"" "$transcripts" 2>/dev/null \
            | xargs -0 stat -f '%m %N' 2>/dev/null | sort -rn | head -1)
        if [ -n "$f" ]; then
            last_ts=$(echo "$f" | awk '{print $1}')
            last=$(date -r "$last_ts" '+%Y-%m-%d' 2>/dev/null)
        fi
    fi
    recent=$([ "$last_ts" -gt 0 ] 2>/dev/null && [ $(( (now - last_ts) / 86400 )) -le 4 ] && echo yes || echo no)

    case "$dirty" in
        wip:*) bucket=hold-wip ;;
        unknown) bucket=review ;;
        *)
            case "$pr" in
                *OPEN*) bucket=hold-open-pr ;;
                *)
                    if [ "$recent" = yes ]; then bucket=verify-recent-chat
                    elif [ "$prs_known" != yes ] || [ -z "$head" ]; then bucket=review
                    elif [ "$merged" = YES ] || [ "$pr_merged" = yes ]; then bucket=safe
                    else bucket=review; fi ;;
            esac ;;
    esac

    printf "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" \
        "$size" "$age" "$merged" "$dirty" "$remote" "$pr" "$last" "$bucket" "$wt"
done < "$worktrees" | sort -t$'\t' -k1,1 -rh
