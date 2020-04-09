from bs4 import BeautifulSoup
import requests
from tabulate import tabulate

def solve():
    shop_url = "https://www.shopclues.com/search?q="

    words = input( 'Enter Product :' )
    words = words.split()

    for i in words:
        shop_url += i
        shop_url += "%20"
    shop_url = shop_url[:-3]

    print( 'Website if you want to visit the store : ' , shop_url )
    shopclue( shop_url )


def shopclue(shop_url):
    try:
        list = requests.get( shop_url )
        list = list.content

        soup = BeautifulSoup( list , "lxml" )
        product = soup.findAll( 'h2' )
        # print(product[0].text)
        price = soup.findAll( 'span' , {'class': "p_price"} )
        # print(price[0].text)
        if (len( product ) > 0 and len( price ) > 0):
            printall( product , price )
        else:
            print( 'Shopclue dont sell this product' )
    except:
        print( 'You dont have better internet connection. Hope you correct it.' )


def printall(product , price):
    allproduct = product[0:5]
    allprice = price[0:5]

    printall = []
    num = min( len( allprice ) , len( allproduct ) )
    index = 1
    '''
    try:
        for i in allprice:
            print(i.text[8:])
    except:
        print("Shrey Noob")
    '''
    for i in range( num ):
        printall.append( [index , allproduct[i].text , allprice[i].text] )
        index += 1

    print()
    print( tabulate( printall , headers = ['Index' , 'Products from Shopclue ' , 'Price'] , tablefmt = "fancygrid" ) )
    print()


if __name__ == '__main__':
    print( '\n----------- Welcome to Shopclue Price Comparison ------------\n' )
    solve()