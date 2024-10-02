# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from tqdm import tqdm
import pandas as pd

# Initialize the WebDriver (you can specify your preferred WebDriver here, e.g., Chrome, Firefox)
driver = webdriver.Chrome()

# Function to extract links from all pages
def get_links():
    links = []
    for i in tqdm(range(1, 343), desc="Collecting Links"):
        url = f"https://localestateplanners.com/estate-planning-directory/page/{i}/"
        driver.get(url)
        elems = driver.find_elements(By.XPATH, ".//p[@class='right read-more']")
        links += [elem.find_element(By.XPATH, ".//a").get_attribute("href") for elem in elems]
    return links

# Function to extract lawyer details from each link
def extract_details(links):
    names, firms, phone_numbers, emails, addresses, websites = [], [], [], [], [], []

    for link in tqdm(links, desc="Extracting Lawyer Details"):
        driver.get(link)

        # Extract Lawyer's Name
        try:
            name = driver.find_element(By.XPATH, ".//h2[@class='lawyer-name-top']/strong")
            names.append(name.text)
        except Exception:
            names.append(None)

        # Extract Firm Name
        try:
            firm = driver.find_element(By.XPATH, ".//p[@class='mb-1 firm-name-top']")
            firms.append(firm.text)
        except Exception:
            firms.append(None)

        # Extract About Info Container
        try:
            elem = driver.find_element(By.XPATH, ".//div[@class='about-info']")

            # Extract Phone Number
            try:
                phone_number = driver.execute_script("return document.querySelector('.phone').textContent;")
                phone_numbers.append(phone_number.strip())
            except Exception:
                phone_numbers.append(None)

            # Extract Email
            try:
                email = driver.execute_script("return document.querySelector('.email').textContent;")
                emails.append(email.strip())
            except Exception:
                emails.append(None)

            # Extract Address
            try:
                addr = elem.find_element(By.XPATH, ".//div[@class='adds']")
                addresses.append(addr.text.strip())
            except Exception:
                addresses.append(None)

            # Extract Website URL
            try:
                website_url = driver.find_element(By.XPATH, "//i[@class='fas fa-globe-americas']/following-sibling::a").get_attribute('href')
                websites.append(website_url)
            except Exception:
                websites.append(None)

        except Exception:
            # If 'about-info' section is missing, append None for all data points
            phone_numbers.append(None)
            emails.append(None)
            addresses.append(None)
            websites.append(None)

    return names, firms, phone_numbers, emails, addresses, websites

# Main function to run the scraper
def main():
    links = get_links()  # Get all the lawyer links
    names, firms, phone_numbers, emails, addresses, websites = extract_details(links)  # Extract details

    # Create a dictionary to store the data
    data = {
        'Name': names,
        'Firm': firms,
        'Phone Number': phone_numbers,
        'Email': emails,
        'Address': addresses,
        'Website': websites
    }

    # Convert the dictionary to a DataFrame
    df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file
    df.to_csv('lawyer_data.csv', index=False)
    print("Data saved to 'lawyer_data.csv'")

# Run the scraper
if __name__ == "__main__":
    main()

# Close the WebDriver
driver.quit()
