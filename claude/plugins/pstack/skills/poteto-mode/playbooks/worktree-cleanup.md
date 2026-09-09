### Worktree cleanup
Start with a read-only inventory from git worktree list --porcelain. Determine
which worktrees have uncommitted work, unpushed commits, open PRs or active users.
Use [scripts/worktree-audit.sh](../scripts/worktree-audit.sh) on systems with
Bash, Git and jq, and inspect its results. GitHub PR checks also require gh.
The `safe` bucket is a clean, merged candidate, not permission to delete it;
check active users separately. Unknown checks require review. If the host or
user supplies a current-project transcript directory, pass it through
PSTACK_TRANSCRIPTS_DIR; otherwise chat activity remains unknown.

Remove only worktrees demonstrated disposable within the user's requested scope.
Never force-remove a dirty tree or infer that an old directory is abandoned.
Keep a clear record of candidates retained and why. Do not extend a worktree
cleanup into browser, IDE, simulator or system-cache deletion unless requested.
