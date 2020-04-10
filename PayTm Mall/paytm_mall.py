from bs4 import BeautifulSoup
import requests
from tabulate import tabulate

def solve():
    paytm_url="https://paytmmall.com/shop/search?q="

    words=input('Enter Product :')
    words=words.split()

    for i in words:
        paytm_url+=i
        paytm_url+="%20"
    paytm_url = paytm_url[:-3]

    print('Website if you want to visit the store : ',paytm_url)
    paytm_mall(paytm_url)

def paytm_mall(paytm_url):
    try:
        list=requests.get(paytm_url)
        list=list.content

        soup=BeautifulSoup(list,"lxml")
        product=soup.findAll('div',{'class':"UGUy"})
        #print(product[0].text)
        price=soup.findAll('div',{'class':"_2MEo"})
        #print(price[0].text)
        if(len(product)>0 and len(price)>0):
            printall(product,price)
        else:
            print('Paytm Mall dont sell this product')
    except:
        print('You dont have better internet connection. Hope you correct it.')

def printall(product,price):
    allproduct=product[0:5]
    allprice=price[0:5]

    printall=[]
    num=min(len(allprice),len(allproduct))
    index=1
    '''
    try:
        for i in allprice:
            print(i.text[8:])
    except:
        print("Shrey Noob")
    '''
    for i in range(num):
        printall.append([index,allproduct[i].text,allprice[i].text[8:]])
        index+=1

    print()
    print(tabulate(printall,headers = ['Index','Products from PayTm Mall','Price'],tablefmt = "fancygrid"))
    print()

            
if __name__=='__main__':
    print('\n----------- Welcome to Paytm Mall Price Comparison ------------\n')
    solve()