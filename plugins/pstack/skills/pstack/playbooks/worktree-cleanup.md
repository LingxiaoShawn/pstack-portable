### Worktree cleanup
Start with a read-only inventory from git worktree list --porcelain. Determine
which worktrees have uncommitted work, unpushed commits, open PRs or active users.
Use scripts/worktree-audit.sh only on supported systems and inspect its results.

Remove only worktrees demonstrated disposable within the user's requested scope.
Never force-remove a dirty tree or infer that an old directory is abandoned.
Keep a clear record of candidates retained and why. Do not extend a worktree
cleanup into browser, IDE, simulator or system-cache deletion unless requested.
