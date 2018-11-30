from bs4 import BeautifulSoup
from bs4.element import Comment
import urllib.request

# to download the page
import requests

# use for time delay on scraping
import time

# allows us to email
import smtplib

# email sender's username
username = 'username'

#email sender's password
password = 'password'

#email recipient's username
target_email = 'target@gmail.com';

old_txt = ""

# this method was adapted from code found here:
# https://www.pythonforbeginners.com/code-snippets-source-code/using-python-to-send-email
def sendemail(from_addr, to_addr_list, cc_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = """From: %s
    """ % from_addr
    header += """To: %s
""" % ','.join(to_addr_list)
    header += """Cc: %s
""" % ','.join(cc_addr_list)
    header += """Subject: %s
""" % subject
    message = header + message
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()
    
# The following two methods were obtained from:
# https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

# sends email to 'to_addr_list' recipient(s), from 'from_addr'.
# e-mail sender's login (username) and password required (last 2 parameters)
def email():
    sendemail(from_addr    = 'OSRS News ', 
          to_addr_list = [target_email],
          cc_addr_list = [], 
          subject      = 'There is a new announcement on the OSRS webpage!', 
          message      = 'https://oldschool.runescape.com/ \n This message was sent via python code.', 
          login        = username, 
          password     = password)

# sends initial email to user who just signed up
def initialEmail():
    sendemail(from_addr    = 'OSRS News', 
          to_addr_list = [target_email],
          cc_addr_list = [], 
          subject      = 'You have signed up for OSRS news notifications', 
          message      = 'This message was sent via python code.', 
          login        = username, 
          password     = password) 
    

while True:
    html = urllib.request.urlopen('https://oldschool.runescape.com/').read()
    txt = text_from_html(html)
    # shortening the string because text before cut-off point is randomly generated (changing) and irrelevant
    txt = txt[txt.find('Manually select world'):]
    if (old_txt != txt):
        if (old_txt == ""):
            initialEmail()
            print("Mailed initial news.")
        else:
            email()
            print("Mailed news.")
    else:
        # check for news every 60 seconds
        time.sleep(60)     
    old_txt = txt



    
