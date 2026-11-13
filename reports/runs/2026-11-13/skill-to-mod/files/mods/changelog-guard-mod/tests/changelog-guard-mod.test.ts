import { test, expect } from 'claude-code/testing'

const bottom = ($: any, on: any) => {
  on('tool.call', () => ({ result: 'ok' }))
  on('ui.toast', () => ({ value: undefined }))
  on('command.register', () => ({ value: undefined }))
}

test('holds git tag until the skill has run', async ($, on) => {
  bottom($, on)
  const r = await $.tool.call({ tool: 'Bash', command: 'git tag v1.2.0' })
  expect(r.deny).toContain('changelog-guard')
})

test('lets unrelated and listing commands through', async ($, on) => {
  bottom($, on)
  expect((await $.tool.call({ tool: 'Bash', command: 'git tag -l' })).result).toBe('ok')
  expect((await $.tool.call({ tool: 'Bash', command: 'ls' })).result).toBe('ok')
})

test('passes after the skill was loaded', async ($, on) => {
  bottom($, on)
  await $.skill.prompt({ skill: 'changelog-guard-mod:changelog-guard', text: 'x' })
  expect((await $.tool.call({ tool: 'Bash', command: 'npm publish' })).result).toBe('ok')
})

test('an edit makes the check stale', async ($, on) => {
  bottom($, on)
  await $.skill.prompt({ skill: 'changelog-guard', text: 'x' })
  await $.tool.call({ tool: 'Edit', file_path: 'CHANGELOG.md' })
  expect((await $.tool.call({ tool: 'Bash', command: 'gh release create v1' })).deny).toBeDefined()
})

test('lets the command through after max holds', async ($, on) => {
  bottom($, on)
  await $.tool.call({ tool: 'Bash', command: 'npm publish' })
  await $.tool.call({ tool: 'Bash', command: 'npm publish' })
  expect((await $.tool.call({ tool: 'Bash', command: 'npm publish' })).result).toBe('ok')
})

test('snooze command disables the hold', async ($, on) => {
  bottom($, on)
  await $.command.run({ command: 'changelog-guard-snooze', args: 'off' })
  expect((await $.tool.call({ tool: 'Bash', command: 'npm publish' })).result).toBe('ok')
})
