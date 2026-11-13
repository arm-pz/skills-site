// changelog-guard-mod: advisory reminder before shipping a release.
// Reach: $.ui.toast and $.command.register only. No process, file, network or model calls.

const MAX_HOLDS = 2;
const SHIPPING =
  /\bgit\s+tag\s+(?!-l\b|--list\b|-d\b|--delete\b)[^\s]|\bnpm\s+publish\b|\bgh\s+release\s+create\b/;

let checked = false; // changelog-guard expanded since the last edit
let holds = 0;
let snoozed = false;

async function noteSkill($, e, next) {
  if (typeof e.skill === 'string' && e.skill.split(':').pop() === 'changelog-guard') {
    checked = true;
    holds = 0;
  }
  return next(e);
}

async function staleOnEdit($, e, next) {
  const r = await next(e);
  checked = false;
  return r;
}

async function guard($, e, next) {
  const cmd = typeof e.command === 'string' ? e.command : '';
  if (snoozed || checked || !SHIPPING.test(cmd)) return next(e);
  if (holds >= MAX_HOLDS) {
    await $.ui.toast('changelog-guard-mod: letting the release command through after repeated holds.');
    return next(e);
  }
  holds += 1;
  return {
    deny:
      'This looks like a release step (tag/publish). Run the changelog-guard skill first: ' +
      'check package.json version vs CHANGELOG.md, merged PRs since the last tag, and any Unreleased heading. ' +
      'Then retry the command. If the user explicitly wants to ship anyway, retry and it will be let through.',
  };
}

async function start($, e, next) {
  await $.command.register({
    name: 'changelog-guard-snooze',
    description: 'Show changelog-guard-mod state; "off" snoozes it for this session, "on" resumes',
    argumentHint: 'on|off',
    immediate: true,
  });
  return next(e);
}

async function command($, e, next) {
  const arg = String(e.args ?? '').trim().toLowerCase();
  if (arg === 'off') snoozed = true;
  else if (arg === 'on') snoozed = false;
  return { text: `changelog-guard-mod is ${snoozed ? 'snoozed' : 'active'}; changelog checked since last edit: ${checked}.` };
}

export function register(on) {
  on('session.start', start).catch(($, e, next) => next(e));
  on('skill.prompt', noteSkill).catch(($, e, next) => next(e));
  on('tool.call', { tool: ['Edit', 'Write'] }, staleOnEdit).catch(($, e, next) => next(e));
  on('tool.call', { tool: 'Bash' }, guard).catch(($, e, next) => next(e));
  on('command.run', { command: 'changelog-guard-snooze' }, command).catch(($, e, next) => next(e));
}
