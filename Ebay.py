from bs4 import BeautifulSoup
import requests
from tabulate import tabulate

def solve():
    ebay_url = 'https://www.ebay.com/sch/i.html?_nkw='

    words=input('Enter Product :')
    words=words.split()

    for i in words:
        ebay_url+=i
        ebay_url+='+'
    ebay_url = ebay_url[:-1]

    print('Website if you want to visit the store : ',ebay_url)
    ebay(ebay_url)

def ebay(url):
    try:
        source = requests.get( url ).content
        soup = BeautifulSoup( source , 'lxml' )
        products = soup.find_all( "h3" , {"class": "s-item__title"} )
        price = soup.find_all( "span" , {"class": "s-item__price"} )
        if (len(products)>0 and len(price)>0):
            n=len(products)
            idx=1
            results = []
            for i in range(n):
                if products[i].string is not None:
                    # print(price[i].text)
                    # must have to check for the price whihc are of type "INR 20 to INR 40"
                    #price[i].text = update( price[i].text )
                    #print( price[i].text )
                    results.append( [idx , products[i].string , update( price[i].text )] )
                    idx += 1
                if (idx==6):
                    break;
            print( tabulate( results , headers = ["Index" ,"Product on Ebay" , "Price"] , tablefmt = "fancy_grid" ) )
        else:
            print( "Ebay does not sell this product." )
    except:
        print( " Please check your internet connection and try again." )

def update(str):
    finalstring=str[0:4]
    for i in range(4,len(str)):
        if(str[i]==' '):
            break
        else:
            finalstring+=str[i]
    return finalstring

if __name__=='__main__':
    print('\n----------- Welcome to Ebay Price Comparison ------------\n')
    solve()
