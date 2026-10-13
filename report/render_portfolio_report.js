const { chromium } = require('playwright');
const path = require('node:path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage();
    await page.goto(`file://${path.join(process.cwd(), 'AttendWise_Portfolio_Report.html')}`, { waitUntil: 'load' });
    await page.pdf({ path: path.join(process.cwd(), 'AttendWise_Portfolio_Report.pdf'), format: 'A4', printBackground: true, preferCSSPageSize: true });
    await page.screenshot({ path: path.join(process.cwd(), 'screenshots', 'report-cover-preview.png'), fullPage: false });
    console.log('Rendered portfolio report PDF.');
  } finally { await browser.close(); }
})();
