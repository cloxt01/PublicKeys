const puppeteer = require('puppeteer');

(async () => {
  // Meluncurkan browser Chromium bawaan Puppeteer
  const browser = await puppeteer.launch({ headless: false });
  const page = await browser.newPage();

  // Menavigasi ke URL dan mencetak judul halaman
  await page.goto('https://tokopedia.com');
  console.log('Page title:', await page.title());

  // Menutup browser
  await browser.close();
})();
