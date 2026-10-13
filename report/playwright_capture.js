const { chromium } = require('playwright');
const path = require('node:path');
const fs = require('node:fs');

const targetUrl = 'http://127.0.0.1:4173';
const artifactDir = path.join(process.cwd(), 'screenshots');
fs.mkdirSync(artifactDir, { recursive: true });

(async () => {
  const browser = await chromium.launch({ headless: true });
  try {
    const context = await browser.newContext({ viewport: { width: 1440, height: 960 }, deviceScaleFactor: 1 });
    const page = await context.newPage();
    await page.goto(targetUrl, { waitUntil: 'domcontentloaded' });
    await page.getByRole('heading', { name: 'Your semester, in focus.' }).waitFor();
    await page.screenshot({ path: path.join(artifactDir, '01-sign-in.png'), fullPage: true });

    await page.getByRole('button', { name: 'Create account' }).click();
    const suffix = Date.now();
    await page.getByLabel('Your name').fill('Portfolio Demo');
    await page.getByLabel('Email address').fill(`portfolio-demo-${suffix}@example.com`);
    await page.getByLabel('Password').fill('portfolio-demo-pass');
    await page.getByRole('button', { name: /Create my account/ }).click();
    await page.getByRole('heading', { name: 'Make today count.' }).waitFor();
    await page.getByRole('button', { name: /Add subject/ }).first().click();
    await page.getByLabel('Subject name').fill('Data Structures');
    await page.getByLabel('Course code').fill('CS201');
    await page.getByLabel('Already attended').fill('18');
    await page.getByLabel('Already missed').fill('4');
    await page.getByRole('button', { name: /Add subject/ }).last().click();
    await page.getByText('Data Structures').first().waitFor();
    await page.screenshot({ path: path.join(artifactDir, '02-dashboard.png'), fullPage: true });

    await page.setViewportSize({ width: 390, height: 844 });
    await page.screenshot({ path: path.join(artifactDir, '03-mobile-dashboard.png'), fullPage: true });
    console.log(JSON.stringify({ title: await page.title(), screenshots: fs.readdirSync(artifactDir) }));
  } finally { await browser.close(); }
})();
