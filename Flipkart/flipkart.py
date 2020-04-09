from bs4 import BeautifulSoup
import requests
from tabulate import tabulate

def solve():
    flipkart_url = 'https://www.flipkart.com/search?q='

    words=input('Enter Product :')
    words=words.split()

    for i in words:
        flipkart_url+=i
        flipkart_url+="+"
    flipkart_url = flipkart_url[:-1]

    print('Website if you want to visit the store : ',flipkart_url)
    flipkart(flipkart_url)

def flipkart(flipkart_url):
    try:
        list = requests.get( flipkart_url )
        list = list.content

        soup = BeautifulSoup( list , 'lxml' )
        product = soup.findAll( 'a' , {'class': '_2cLu-l'} )
        price = soup.findAll( "div" , {"class": "_1vC4OE"} )

        if (len( product ) == 0 or len( price ) == 0):
            product = soup.findAll( 'div' , {'class': "_3wU53n"} )
            price = soup.findAll( "div" , {"class": "_1vC4OE _2rQ-NK"} )

        if (len( product ) > 0 and len( price ) > 0):
            flipkart_money( product , price )
        else:
            print( 'Flipkart dont sell anything like these.' )
    except:
        print('You dont have better internet connection. Hope you correct it.')

def flipkart_money(product,price):
    print_product=product[0:5]
    print_price=price[0:5]

    printall=[]
    num=1
    for i,j in zip(print_product,print_price):
        printall.append([num,i.text,j.text])
        num+=1

    print()
    print(tabulate(printall,headers = ['Index','Product in flipkart','Price'],tablefmt = "pipe"))
    print()

if __name__=='__main__':
    print('\n----------- Welcome to Flipkart Price Comparison ------------\n')
    solve()