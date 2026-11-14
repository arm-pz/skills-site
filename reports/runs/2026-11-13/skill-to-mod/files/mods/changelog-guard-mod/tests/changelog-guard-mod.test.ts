import { expect, test } from 'claude-code/testing'

// Stands in for Claude Code beneath the mod: every tool "runs" and answers ok,
// and a question to the user (AskUserQuestion) is answered from `answer`.
function engine(on: any, answer: { value: string } = { value: 'Run checks first' }) {
  on('tool.call', ($: any, e: any) =>
    e.tool === 'AskUserQuestion'
      ? { result: { answers: { [e.questions[0].question]: answer.value } } }
      : { result: 'ok' },
  )
  on('skill.prompt', ($: any, e: any) => ({ text: e.text }))
  on('ui.status', () => ({ value: undefined }))
  on('ui.toast', () => ({ value: undefined }))
}

const SHIP = "git tag"
const REQUIRED = ["changelog-guard"]
const CHECK = REQUIRED[0]

test('block: a ship command is refused until the required skill has run', { options: { mode: 'block', required: REQUIRED.join(',') } }, async ($: any, on: any) => {
  engine(on)
  const held = await $.tool.call({ tool: 'Bash', command: SHIP })
  expect(held.deny).toMatch(new RegExp(CHECK))

  for (const skill of REQUIRED) await $.skill.prompt({ skill, text: 'checks' })
  expect(await $.tool.call({ tool: 'Bash', command: SHIP })).toEqual({ result: 'ok' })
})

test('block: a command that does not ship is never held', { options: { mode: 'block' } }, async ($: any, on: any) => {
  engine(on)
  expect(await $.tool.call({ tool: 'Bash', command: 'echo hello && ls' })).toEqual({ result: 'ok' })
})

test('a plugin skill name counts as the check', { options: { mode: 'block', required: CHECK } }, async ($: any, on: any) => {
  engine(on)
  await $.skill.prompt({ skill: 'some-plugin:' + CHECK, text: 'checks' })
  expect(await $.tool.call({ tool: 'Bash', command: SHIP })).toEqual({ result: 'ok' })
})

test('an edit after the checks makes them stale', { options: { mode: 'block', required: REQUIRED.join(',') } }, async ($: any, on: any) => {
  engine(on)
  for (const skill of REQUIRED) await $.skill.prompt({ skill, text: 'checks' })
  expect(await $.tool.call({ tool: 'Bash', command: SHIP })).toEqual({ result: 'ok' })

  await $.tool.call({ tool: 'Edit', file_path: 'src/app.ts', old_string: 'a', new_string: 'b' })
  expect((await $.tool.call({ tool: 'Bash', command: SHIP })).deny).toBeDefined()
})

test('after the holds are used up the command is let through, so a missing skill cannot trap the session', { options: { mode: 'block' } }, async ($: any, on: any) => {
  engine(on)
  expect((await $.tool.call({ tool: 'Bash', command: SHIP })).deny).toBeDefined()
  expect((await $.tool.call({ tool: 'Bash', command: SHIP })).deny).toBeDefined()
  expect(await $.tool.call({ tool: 'Bash', command: SHIP })).toEqual({ result: 'ok' })
})

test('ask: "Ship anyway" lets it through', { options: { mode: 'ask' } }, async ($: any, on: any) => {
  engine(on, { value: 'Ship anyway' })
  expect(await $.tool.call({ tool: 'Bash', command: SHIP })).toEqual({ result: 'ok' })
})

test('ask: "Run checks first" refuses with an instruction Claude can act on', { options: { mode: 'ask' } }, async ($: any, on: any) => {
  engine(on, { value: 'Run checks first' })
  const held = await $.tool.call({ tool: 'Bash', command: SHIP })
  expect(held.deny).toMatch(/Run (that skill|those skills)/)
})

test('nudge: the command runs and Claude is reminded afterwards', { options: { mode: 'nudge' } }, async ($: any, on: any) => {
  engine(on)
  const ran = await $.tool.call({ tool: 'Bash', command: SHIP })
  expect(ran.result).toBe('ok')
  expect(ran.context[0]).toMatch(new RegExp(CHECK))
})

test('off: nothing is ever held', { options: { mode: 'off' } }, async ($: any, on: any) => {
  engine(on)
  expect(await $.tool.call({ tool: 'Bash', command: SHIP })).toEqual({ result: 'ok' })
})

test('the command snoozes and resumes it', { options: { mode: 'block' } }, async ($: any, on: any) => {
  engine(on)
  const off = await $.command.run({ command: "changelog-guard-mod", args: 'off' })
  expect(off.text).toMatch(/snoozed/)
  expect(await $.tool.call({ tool: 'Bash', command: SHIP })).toEqual({ result: 'ok' })

  await $.command.run({ command: "changelog-guard-mod", args: 'on' })
  expect((await $.tool.call({ tool: 'Bash', command: SHIP })).deny).toBeDefined()
})
