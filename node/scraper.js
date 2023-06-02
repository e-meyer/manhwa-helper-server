const express = require('express');
const puppeteer = require('puppeteer');

const app = express();
const port = 3000;

async function scrapeWebsite(url) {
  const browser = await puppeteer.launch();

  const page = await browser.newPage();
  await page.goto(url);

  // Find data to scrape
  const data = await page.evaluate(() => {
    const manhwaTitles = document.querySelectorAll('a.series');
    // const 

    const luminousData = [];

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

app.get('/', async (req, res) => {
  try {
    const url = 'https://www.luminousscans.com';
    const data = await scrapeWebsite(url);

    res.send(data.join('<br>'));
  } catch (error) {
    console.error(error);
    res.send('An error occurred while scraping the website.');
  }
});

app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});