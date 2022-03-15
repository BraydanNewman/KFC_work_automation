# KFC Work Automation

---

## This project is only built for RITEQ and uses GCP as a provider for image processing calendar

### In the main folder create the files:

#### OAuth_ClientID.json

This file is from the GCP OAuth 2.0 Client ID's, this is needed to connect 
to the different services need to extract the data and add events to your calendar 

#### API_key.json

This file is the API key for the image to text processing and to access the calendar

#### credentials.json

This file is where you would store your login details for RITEQ

---

### The Chrome Driver will need to updated depending on your version of chrome

### Details will need to be added at top of scraper class for use

### Comment out the line below to get a window of what the program is doing
    self.driver = webdriver.Chrome('chromedriver.exe', options=self.chrome)