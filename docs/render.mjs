import { execSync } from 'node:child_process'
const CHROME = 'C:/Program Files/Google/Chrome/Application/chrome.exe'
const files = [
  ['docs/diagrams/use-case.mmd', 'docs/diagrams/use-case.svg', 'Use Case Diagram'],
  ['docs/diagrams/erd.mmd', 'docs/diagrams/erd.svg', 'Tabel ERD'],
]
for (const [src, out, title] of files) {
  try {
    execSync(`npx mmdc -i ${src} -o ${out} -b ${CHROME} -t dark -s 2`, { stdio: 'inherit' })
    console.log('OK', out)
  } catch (e) {
    console.log('FAIL', out, e.message)
  }
}
