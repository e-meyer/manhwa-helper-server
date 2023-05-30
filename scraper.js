const puppeteer = require('puppeteer');

async function scrapeWebsite(url) {
  const browser = await puppeteer.launch();

  const page = await browser.newPage();
  await page.goto(url);

  // Find data to scrape
  const data = await page.evaluate(() => {
    const manhwaTitles = document.querySelectorAll('a.series');
    // const 

    const luminousData = [];
    websiteOrder.push('Luminous');

    for (const manhwaTitle of manhwaTitles) {
      // The titles are duplicated, only titles that don't have the rel attribute should be added
      if(!manhwaTitle.getAttribute('rel'))
      luminousData.push(manhwaTitle.getAttribute('title'));
    }

    return luminousData;
  });

  await browser.close();
  return data;
}

(async () => {
  const url = 'https://www.luminousscans.com';
  const data = await scrapeWebsite(url);

  console.log(data);
})();
