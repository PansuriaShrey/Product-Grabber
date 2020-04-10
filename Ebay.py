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
                try:
                    if (len(products[i].string)!=0):
                        print(price[i].text)
                        results.append( [idx, products[i].string , price[i].text] )
                        idx+=1
                except:
                    temp=1
                if (idx==6):
                    break;
            print( tabulate( results , headers = ["Index" ,"Product on Ebay" , "Price"] , tablefmt = "fancy_grid" ) )
        else:
            print( "Ebay does not sell this product." )
    except:
        print( " Please check your internet connection and try again." )


if __name__=='__main__':
    print('\n----------- Welcome to Ebay Price Comparison ------------\n')
    solve()
