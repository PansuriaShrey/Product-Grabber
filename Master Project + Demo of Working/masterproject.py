from tkinter import *
from tkinter import ttk
from bs4 import BeautifulSoup
import requests
from tabulate import tabulate
import webbrowser

root=Tk()
root.title('Product Grabber')
root.geometry('1400x800')
root.config(bg="#74a7da")

label1=Label(root,text="PRODUCT GRABBER",fg="white",bg="#74a7da",font=('Comic Sans MS',50,'bold','underline'))
label1.place(anchor=CENTER,relx=0.5,rely=0.09,relwidth=0.5,relheight=0.12)

label2=Label(root,text="Enter the product you want to search : ",font=('Arial',19,'bold'))
label2['bg']='#7474da'
label2['fg']='#74dada'
label2.place(anchor=CENTER,relx=0.25,rely=0.18,relwidth=0.3,relheight=0.04)

input=Entry(root)
input.insert(0,'')
input.place(anchor=CENTER,relx=0.75,rely=0.18,relwidth=0.3,relheight=0.04)

def callback(url):
    webbrowser.open_new(url)

def calculate():
    checkFlp()
    checkebay()
    checkSnapdeal()
    checkShopclue()
    checkPaytmMall()
    input.delete(0,'end')

def checkFlp():
    flipkart_url = 'https://www.flipkart.com/search?q='

    words=input.get()
    #input.delete( 0 , 'end' )
    words = words.split()
    #print(words)

    for i in words:
        flipkart_url+=i
        flipkart_url+="+"
    flipkart_url = flipkart_url[:-1]

    op='Website if you want to visit the store : '
    #print(op)
    labeloutput=Label(root,text=op)
    labeloutput.place(anchor=CENTER,relx=0.25,rely=0.37,relheight=0.04,relwidth=0.2)
    link=Button(root,text="FlipKart",fg="blue",cursor="hand2")
    link.pack()
    link.bind("<Button-1>",lambda e:callback(flipkart_url))
    link.place(relx=.36,rely=0.35,relheight=0.04)
    flipkart(flipkart_url)

def flipkart(flipkart_url):
    op=""
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
            return
        else:
            op='Flipkart dont sell anything like these.'
    except:
        op='You dont have better internet connection. Hope you correct it.'

    labeloutput = Label( root , text = op )
    labeloutput.place( anchor = CENTER , relx = 0.25 , rely = 0.47 , relwidth = 0.48 ,relheight=0.04 )

def flipkart_money(product,price):
    print_product=product[0:5]
    print_price=price[0:5]

    printall=[]
    num=1
    for i,j in zip(print_product,print_price):
        printall.append([num,i.text,j.text])
        num+=1

    '''
    op=tabulate(printall,headers = ['Index','Product in flipkart','Price'],tablefmt = "simple")
    #print(op)
    labeloutput = Label( root , text = op )
    labeloutput.place( anchor = CENTER , relx = 0.5 , rely = 0.84 , relwidth = 0.6 ,relheight=0.28)
    '''

    cols = ('Index' , 'Product in flipkart' , 'Price')
    listBox = ttk.Treeview( root , columns = cols , show = 'headings' )
    for col in cols:
        listBox.heading(col,text=col,anchor=CENTER)
    listBox.column( 'Index' , anchor = CENTER , minwidth = 72 , width = 72 , stretch = NO )
    listBox.column( 'Product in flipkart' , anchor = CENTER , minwidth = 500 , width = 500 , stretch = NO )
    listBox.column( 'Price' , anchor = CENTER , minwidth = 100 , width = 100 , stretch = NO )

    for i,j,k in printall:
        listBox.insert("","end",value=(i,j,k))

    listBox.place( anchor = CENTER , relx = 0.25 , rely = 0.47 , relwidth = 0.48 ,relheight=0.14)

def checkebay():
    ebay_url = 'https://www.ebay.com/sch/i.html?_nkw='

    words = input.get()
    words = words.split()

    for i in words:
        ebay_url += i
        ebay_url += '+'
    ebay_url = ebay_url[:-1]

    op= 'Website if you want to visit the store : '
    labeloutput = Label( root , text = op )
    labeloutput.place(anchor=CENTER,relx=0.75,rely=0.37,relheight=0.04,relwidth=0.2)
    link=Button(root,text="Ebay",fg="blue",cursor="hand2")
    link.pack()
    link.bind("<Button-1>",lambda e:callback(ebay_url))
    link.place(relx=.86,rely=0.35,relheight=0.04)
    ebay( ebay_url )

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
            #print( tabulate( results , headers = ["Index" ,"Product on Ebay" , "Price"] , tablefmt = "fancy_grid" ) )

            cols = ('Index' , 'Product in Ebay' , 'Price')
            listBox = ttk.Treeview( root , columns = cols , show = 'headings' )
            for col in cols:
                listBox.heading( col , text = col , anchor = CENTER )
            listBox.column( 'Index' , anchor = CENTER , minwidth = 72 , width = 72 , stretch = NO )
            listBox.column( 'Product in Ebay' , anchor = CENTER , minwidth = 500 , width = 500 , stretch = NO )
            listBox.column( 'Price' , anchor = CENTER , minwidth = 100 , width = 100 , stretch = NO )

            for i , j , k in results:
                listBox.insert( "" , "end" , value = (i , j , k) )

            listBox.place( anchor = CENTER , relx = 0.75 , rely = 0.47 , relwidth = 0.48 , relheight = 0.14 )

            return
        else:
            op="Ebay does not sell this product."
    except:
        op=" Please check your internet connection and try again."
    labeloutput = Label( root , text = op )
    labeloutput.place( anchor = CENTER , relx = 0.75 , rely = 0.47 , relwidth = 0.48 , relheight = 0.04 )

def update(str):
    finalstring=str[0:4]
    for i in range(4,len(str)):
        if(str[i]==' '):
            break
        else:
            finalstring+=str[i]
    return finalstring


def checkSnapdeal():
    snapdeal_url = 'https://www.snapdeal.com/search?keyword='

    words = input.get()
    words = words.split()

    for i in words:
        snapdeal_url += i
        snapdeal_url += '%20'
    snapdeal_url = snapdeal_url[:-3]

    op = 'Website if you want to visit the store : '

    labeloutput = Label( root , text = op )
    labeloutput.place( anchor = CENTER , relx = 0.75 , rely = 0.59 , relheight = 0.04 , relwidth = 0.2 )
    link=Button(root,text="SnapDeal",fg="blue",cursor="hand2")
    link.pack()
    link.bind("<Button-1>",lambda e:callback(snapdeal_url))
    link.place(relx=.36,rely=0.57,relheight=0.04)
    snapdeal( snapdeal_url )


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
            index = 1
            for item , money in zip( products , price ):
                results.append( [index , item.string , money.text] )
                index += 1
            # print( tabulate( results , headers = ["Product on Snapdeal" , "Price"] , tablefmt = "fancy_grid" ) )

            cols = ('Index' , 'Product in Snapdeal' , 'Price')
            listBox = ttk.Treeview( root , columns = cols , show = 'headings' )
            for col in cols:
                listBox.heading( col , text = col , anchor = CENTER )
            listBox.column( 'Index' , anchor = CENTER , minwidth = 72 , width = 72 , stretch = NO )
            listBox.column( 'Product in Snapdeal' , anchor = CENTER , minwidth = 500 , width = 500 , stretch = NO )
            listBox.column( 'Price' , anchor = CENTER , minwidth = 100 , width = 100 , stretch = NO )

            for i , j , k in results:
                listBox.insert( "" , "end" , value = (i , j , k) )

            listBox.place( anchor = CENTER , relx = 0.75 , rely = 0.70 , relwidth = 0.48 , relheight = 0.14 )
            return
        else:
            op = "SnapDeal does not sell this product."
    except:
        op = " Please check your internet connection and try again."

    labeloutput = Label( root , text = op )
    labeloutput.place( anchor = CENTER , relx = 0.75 , rely = 0.70 , relwidth = 0.48 , relheight = 0.04 )

def checkShopclue():
    shop_url = "https://www.shopclues.com/search?q="

    words = input.get()
    words = words.split()

    for i in words:
        shop_url += i
        shop_url += "%20"
    shop_url = shop_url[:-3]

    op='Website if you want to visit the store : '
    labeloutput = Label( root , text = op )
    labeloutput.place( anchor = CENTER , relx = 0.25 , rely = 0.59 , relheight = 0.04 , relwidth = 0.2 )
    link=Button(root,text="ShopClues",fg="blue",cursor="hand2")
    link.pack()
    link.bind("<Button-1>",lambda e:callback(shop_url))
    link.place(relx=.86,rely=0.57,relheight=0.04)
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
            printallshopclue( product , price )
            return
        else:
            op='Shopclue dont sell this product'
    except:
        op='You dont have better internet connection. Hope you correct it.'

    labeloutput = Label( root , text = op )
    labeloutput.place( anchor = CENTER , relx = 0.25 , rely = 0.70 , relwidth = 0.48 , relheight = 0.14 )


def printallshopclue(product , price):
    allproduct = product[0:5]
    allprice = price[0:5]

    printall = []
    num = min( len( allprice ) , len( allproduct ) )
    index = 1

    for i in range( num ):
        printall.append( [index , allproduct[i].text , allprice[i].text] )
        index += 1

    cols = ('Index' , 'Product in Shopclue' , 'Price')
    listBox = ttk.Treeview( root , columns = cols , show = 'headings' )
    for col in cols:
        listBox.heading( col , text = col , anchor = CENTER )
    listBox.column( 'Index' , anchor = CENTER , minwidth = 72 , width = 72 , stretch = NO )
    listBox.column( 'Product in Shopclue' , anchor = CENTER , minwidth = 500 , width = 500 , stretch = NO )
    listBox.column( 'Price' , anchor = CENTER , minwidth = 100 , width = 100 , stretch = NO )

    for i , j , k in printall:
        listBox.insert( "" , "end" , value = (i , j , k) )

    listBox.place( anchor = CENTER , relx = 0.25 , rely = 0.70 , relwidth = 0.48 , relheight = 0.14 )

def checkPaytmMall():
    paytm_url="https://paytmmall.com/shop/search?q="
    paytm_url_display="https://paytmmall.com/shop/search?q="
    words=input.get()
    words=words.split()

    for i in words:
        paytm_url+=i
        paytm_url+="%20"
    paytm_url = paytm_url[:-3]

    op='Website if you want to visit the store : '
    labeloutput = Label( root , text = op )
    labeloutput.place( anchor = CENTER , relx = 0.5 , rely = 0.81 , relheight = 0.04 , relwidth = 0.2 )
    link=Button(root,text="PaytmMall",fg="blue",cursor="hand2")
    link.pack()
    link.bind("<Button-1>",lambda e:callback(paytm_url))
    link.place(relx=.61,rely=0.79,relheight=0.04)
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
            return
        else:
            op='Paytm Mall dont sell this product'
    except:
        op='You dont have better internet connection. Hope you correct it.'

    labeloutput = Label( root , text = op )
    labeloutput.place( anchor = CENTER , relx = 0.5 , rely = 0.91 , relwidth = 0.48 ,relheight=0.04 )

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

    cols = ('Index' , 'Product in Paytm Mall' , 'Price')
    listBox = ttk.Treeview( root , columns = cols , show = 'headings' )
    for col in cols:
        listBox.heading( col , text = col , anchor = CENTER )
    listBox.column( 'Index' , anchor = CENTER , minwidth = 72 , width = 72 , stretch = NO )
    listBox.column( 'Product in Paytm Mall' , anchor = CENTER , minwidth = 500 , width = 500 , stretch = NO )
    listBox.column( 'Price' , anchor = CENTER , minwidth = 100 , width = 100 , stretch = NO )

    for i , j , k in printall:
        listBox.insert( "" , "end" , value = (i , j , k) )

    listBox.place( anchor = CENTER , relx = 0.5 , rely = 0.91 , relwidth = 0.48 , relheight = 0.14 )

check=Button(root,text="CLICK HERE",command=calculate,activeforeground="red",activebackground="green")
check['font']=('Chalkboard',18,'bold')
check['borderwidth']=40
check.place(anchor=CENTER,relx=0.5,rely=0.23,relwidth=0.16,relheight=0.03)

root.mainloop()