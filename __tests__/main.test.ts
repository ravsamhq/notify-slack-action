const env = process.env

beforeEach(() => {
  jest.resetModules()
  process.env = { ...env }
})

afterEach(() => {
  process.env = env
})

const buildPayload = async (env?: Record<string, string>) => {
  process.env = {
    ...process.env,
    GITHUB_WORKFLOW: "test-workflow",
    GITHUB_REPOSITORY: "test/test",
    GITHUB_SHA: "2fa67bb0998a39d9b697772782aa94599cfda489",
    INPUT_ICON_SUCCESS: ":DONE:",
    INPUT_ICON_FAILURE: ":FAIL:",
    ...env,
  }

  const fn = require("../src/main").buildPayload

  const rep = await fn()
  return JSON.parse(rep)
}

const getAttachment = async (env?: Record<string, string>) => {
  const payload = await buildPayload(env)
  return payload.attachments[0]
}

test("build payload structure", async () => {
  const rep = await buildPayload()
  expect(rep).toBeDefined()
  expect(rep).toHaveProperty("attachments")
  expect(rep.attachments).toHaveLength(1)
  expect(rep.attachments[0]).toHaveProperty("text")
  expect(rep.attachments[0]).toHaveProperty("fallback")
  expect(rep.attachments[0]).toHaveProperty("pretext")
  expect(rep.attachments[0]).toHaveProperty("color")
  expect(rep.attachments[0]).toHaveProperty("mrkdwn_in")
  expect(rep.attachments[0]).toHaveProperty("footer")
})

test("minimal workflow (success)", async () => {
  const rep = await getAttachment({
    INPUT_STATUS: "success",
  })

  expect(rep.color).toBe("good")
})

test("minimal workflow (failure)", async () => {
  const rep = await getAttachment({
    INPUT_STATUS: "failure",
  })

  expect(rep.color).toBe("danger")
})

test("expanded workflow", async () => {
  const rep = await getAttachment({
    INPUT_STATUS: "success",
    INPUT_NOTIFICATION_TITLE: "{workflow} has {status_message}",
    INPUT_MESSAGE_FORMAT: "{emoji} *{workflow}* {status_message} in <{repo_url}|{repo}>",
    INPUT_FOOTER: "Linked Repo <{repo_url}|{repo}> | <{workflow_url}|View Workflow>",
  })

  expect(rep.text).toBe(":DONE: *test-workflow* passed in <https://github.com/test/test|test/test>")
  expect(rep.fallback).toBe("test-workflow has passed")
  expect(rep.pretext).toBe("test-workflow has passed")
  expect(rep.color).toBe("good")
  expect(rep.footer).toBe(
    "Linked Repo <https://github.com/test/test|test/test> | <test-workflow-url|View Workflow>"
  )
})

test("workflow with mentions users", async () => {
  let rep

  rep = await getAttachment({
    INPUT_STATUS: "failure",
    INPUT_MESSAGE_FORMAT: "{emoji} *{workflow}* {status_message}",
    INPUT_MENTION_USERS: "U0160UUNH8S,U0080UUAA9N",
    INPUT_MENTION_USERS_WHEN: "failure,warnings",
  })
  expect(rep.text).toBe(":FAIL: *test-workflow* failed\n<@U0160UUNH8S> <@U0080UUAA9N>")

  // should not mention users if no INPUT_MENTION_USERS_WHEN
  rep = await getAttachment({
    INPUT_STATUS: "success",
    INPUT_MESSAGE_FORMAT: "{emoji} *{workflow}* {status_message}",
    INPUT_MENTION_USERS: "U0160UUNH8S,U0080UUAA9N",
  })
  expect(rep.text).toBe(":DONE: *test-workflow* passed")

  // should not mention users if status not in INPUT_MENTION_USERS_WHEN
  rep = await getAttachment({
    INPUT_STATUS: "success",
    INPUT_MESSAGE_FORMAT: "{emoji} *{workflow}* {status_message}",
    INPUT_MENTION_USERS: "U0160UUNH8S,U0080UUAA9N",
    INPUT_MENTION_USERS_WHEN: "failure,warnings",
  })
  expect(rep.text).toBe(":DONE: *test-workflow* passed")
})

test("workflow with mentions groups", async () => {
  let rep

  rep = await getAttachment({
    INPUT_STATUS: "failure",
    INPUT_MESSAGE_FORMAT: "{emoji} *{workflow}* {status_message}",
    INPUT_MENTION_GROUPS: "SAZ94GDB8,!channel",
    INPUT_MENTION_GROUPS_WHEN: "failure,warnings",
  })
  expect(rep.text).toBe(":FAIL: *test-workflow* failed\n<!subteam^SAZ94GDB8> <!channel>")
})

test("workflow with mention users & groups", async () => {
  let rep

  rep = await getAttachment({
    INPUT_STATUS: "failure",
    INPUT_MESSAGE_FORMAT: "{emoji}",
    INPUT_MENTION_USERS: "U0160UUNH8S,U0080UUAA9N",
    INPUT_MENTION_USERS_WHEN: "failure,warnings",
    INPUT_MENTION_GROUPS: "SAZ94GDB8,!channel",
    INPUT_MENTION_GROUPS_WHEN: "failure,warnings",
  })
  expect(rep.text).toBe(":FAIL:\n<@U0160UUNH8S> <@U0080UUAA9N>\n<!subteam^SAZ94GDB8> <!channel>")
})
