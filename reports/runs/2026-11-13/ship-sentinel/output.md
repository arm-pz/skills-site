The deploy was blocked, and nothing was deployed, committed or pushed.

- **Edit:** I changed the `<h1>` in `site/index.html` to `Reconcile 2.0`. That change is in the working tree only.
- **Block:** the ship-sentinel hook held `wrangler pages deploy site --branch main`. It says `release-gate` has not run since the last edit, and it wants that skill run on the current changes first.
- **Skill missing:** I tried to run `release-gate`, but this session has no skill by that name. The hook says to tell you in that case rather than retry, so I stopped. I did not run the deploy through another route or around the hook.
- **Skipped:** the commit and `git push origin main`, because they come after the deploy.

To unblock this, you could:
- point me to the `release-gate` skill or script if it lives somewhere else, or install it;
- tell me the check isn't needed here, or change the hook, since the site is static and only local files can be checked.

After either of those I'll run the deploy, commit and push.