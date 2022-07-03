import path from "path"
import cp from "child_process"
import { test } from "@jest/globals"

test("test runs", () => {
  const np = process.execPath
  const ip = path.join(__dirname, "..", "lib", "main.js")
  const options: cp.ExecFileSyncOptions = { env: process.env }
  cp.execFileSync(np, [ip], options).toString()
})
