from flask import Flask,request, url_for, redirect, render_template
import requests
from bs4 import BeautifulSoup
import pprint
import smtplib
from email.message import EmailMessage
import csv
import schedule
import time


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")
x = 1
y=1
@app.route('/price',methods=['POST','GET'])
def input():
    
    url = request.form['1']
    req_price = int(request.form['2'])
    email_user = request.form['3']
    #print(url)
    #print(req_price)
    #print(email_user)
    global x
    if "flipkart" in url.lower() :
        print("Flipkart:\n")
        res = requests.get(f'{url}')
        soup = BeautifulSoup(res.text,'html.parser')
        name = soup.select('._35KyD6')[0].getText()
        print("\n"+name)
        price = soup.select('._3qQ9m1')[0].getText()
        price = int(price[1:].replace(",",""))
        print(price)
    elif "amazon" in url.lower():
        print("Amazon:\n")
        res = requests.get(url,headers=headers)
        soup = BeautifulSoup(res.text,'html.parser')
        name = soup.select("#title")[0].getText().strip()
        try:
            price = soup.select("#priceblock_dealprice")[0].getText().strip()
        except:
            price = soup.select("#priceblock_ourprice")[0].getText().strip()
        price_num = price.replace("₹","")
        price_num = price_num.replace(",","")
        price = int(float(price_num))
        #print(f"{name} with a price of {price}")
        print(f"\n{name}\n {price}")
    if (price <= req_price) :
            email = EmailMessage()
            email['from'] = 'Price tracker'
            email['to'] = email_user
            email['subject'] = 'The price of product is drop down to your requirment... GO check out'

            email.set_content(f'Product Name: {name}\nPrice:{price}\n Link: "{url}"')
            with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login('deltadelta371@gmail.com','delta@31')
                smtp.send_message(email)
                print("Email Send!")
                
            fields=[name,price,req_price,email_user,url]
            with open(r'data_user.csv', 'a',newline="") as f:
                writer = csv.writer(f)
                writer.writerow(fields)
            x=x+1
    else:
        global y
        print(y)
        if (y<=1):
            email = EmailMessage()
            email['from'] = 'Price tracker'
            email['to'] = email_user
            email['subject'] = 'Price Tracker'

            email.set_content(f'We Will Let You Know When The Price of the product dropped down to you requirement. \nProduct Name: {name}\nCurrent Price:{price}\n')
            with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
                smtp.ehlo()
                smtp.starttls()
                smtp.login('deltadelta371@gmail.com','delta@31')
                smtp.send_message(email)
                y=y+1
                print("EMail Send")
        else:
            print("Price Is Still Larger Than The Required Price")
    return render_template("result.html",user=name,useremail=email_user,price=price,userprice=req_price,url=url)
    
    

    # schedule.every(2).seconds.do(check)
    # while x == 1:
    #     schedule.run_pending()
    #     time.sleep(1)
        
  
if __name__ == '__main__':
    app.run(debug=True)


