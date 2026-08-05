import { mkdir, rm } from 'node:fs/promises'
import { resolve } from 'node:path'

export default async function globalSetup() {
  const temporaryDirectory = resolve(process.cwd(), '..', '.tmp')
  await rm(temporaryDirectory, { recursive: true, force: true })
  await mkdir(temporaryDirectory, { recursive: true })
}
