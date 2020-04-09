from bs4 import BeautifulSoup
import requests
from tabulate import tabulate

def solve():
    snapdeal_url = 'https://www.snapdeal.com/search?keyword='

    words=input('Enter Product :')
    words=words.split()

    for i in words:
        snapdeal_url+=i
        snapdeal_url+='%20'
    snapdeal_url = snapdeal_url[:-3]

    print('Website if you want to visit the store : ',snapdeal_url)
    snapdeal(snapdeal_url)

def snapdeal(url):
    try:
        source = requests.get( url ).content
        soup = BeautifulSoup( source , 'lxml' )
        products = soup.find_all( "p" , {"class": "product-title"} )
        price = soup.find_all( "span" , {"class": "lfloat product-price"} )
        if (len( products ) > 0 and len( price ) > 0):
            products = products[0:5]
            price = price[0:5]
            results = []
            for item , money in zip( products , price ):
                results.append( [item.string , money.text] )
            print( tabulate( results , headers = ["Product on Snapdeal" , "Price"] , tablefmt = "fancy_grid" ) )
        else:
            print( "SnapDeal does not sell this product." )
    except:
        print( " Please check your internet connection and try again." )


if __name__=='__main__':
    print('\n----------- Welcome to Snapdeal Price Comparison ------------\n')
    solve()
