from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import mysql.connector
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configure the Selenium WebDriver
driver = webdriver.Firefox()  # Change to the appropriate WebDriver for your browser


# Create a connection to the MySQL database using the URL
conn = mysql.connector.connect(
    host='containers-us-west-77.railway.app',
    user='root',
    password='oTaGZXop5rJcyyYr5tg7',
    database='railway',
    port ='6165'
)


# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create the credentials table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS credentials (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL
                )''')

# Insert sample credentials into the table
# cursor.execute("INSERT INTO credentials (username, password) VALUES (%s, %s)", ('aakashaman9931@gmail.com', ''))
# cursor.execute("INSERT INTO credentials (username, password) VALUES (%s, %s)", ('user2@example.com', 'password2'))

# Commit the changes to the database
conn.commit()

# Retrieve credentials from the database
cursor.execute("SELECT * FROM credentials")
credentials = cursor.fetchall()

# Iterate through each set of credentials
for credential in credentials:
    username = credential[1]
    password = credential[2]

    # Navigate to the LinkedIn login page
    driver.get('https://www.linkedin.com/login')

    # Find and populate the login form with the credentials
    email_input = driver.find_element(By.ID, 'username')
    email_input.send_keys(username)

    password_input = driver.find_element(By.ID, 'password')
    password_input.send_keys(password)

    # Submit the login form
    submit_button = driver.find_element(By.XPATH, "/html/body/div/main/div[2]/div[1]/form/div[3]/button")
    submit_button.click()

    # Wait for the page to load after login
    WebDriverWait(driver, 30).until(EC.url_contains('https://www.linkedin.com/feed/'))

    # Retrieve the number of unread messages and notifications
    notification_locator = (By.XPATH, '/html/body/div[5]/header/div/nav/ul/li[5]/a/div/span/span[1]')
    unread_notification_count = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(notification_locator))
    unread_notification = int(unread_notification_count.text)



    unread_message_count = driver.find_element(By.XPATH, '/html/body/div[5]/header/div/nav/ul/li[4]/a/div/span/span[1]')
    unread_message = int(unread_message_count.text)

    # Print the results
    print(f"Username: {username}")
    print(f"Number of Unread Notifications: {unread_notification}")
    print(f"Number of Unread Messages: {unread_message}")
    print()

    sender_email = 'Aakash.12015092@lpu.in'  # Replace with your email address
    sender_password = 'Akash@123'  # Replace with your email password
    receiver_email = 'aakashaman9931@gmail.com'  # Use the username as the recipient email address

    # Create the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = receiver_email
    message['Subject'] = 'LinkedIn Unread Notifications and Messages'

    # Compose the email body
    email_body = f'''
    Hello {username},
    
    Here are your LinkedIn unread notifications and messages:
    Number of Unread Notifications: {unread_notification}
    Number of Unread Messages: {unread_message}
    
    Thank you.
    '''

    # Attach the email body as plain text
    message.attach(MIMEText(email_body, 'plain'))

    # Create a secure connection with the SMTP server
    with smtplib.SMTP('smtp.office365.com', 587) as server:
        server.ehlo()
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(message)

    driver.delete_all_cookies()
    driver.get('https://www.linkedin.com/login')
 

# Close the browser
driver.quit()



# Close the database connection
cursor.close()
conn.close()
