### Manhwa Alert Server

This is the server for the manhwa-alert-app project.
It's currently just a basic scrape testing.

I've tried Node.js for the scraping part but noticed that Python with Flask performs somewhat better.
And also, I thought that threading might be a good idea because I don't want to be tied to only one task at a time but rather be able to make multiple requests for scraping simultaneously.