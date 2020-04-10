from tkinter import *
from tkinter import ttk
from bs4 import BeautifulSoup
import requests
from tabulate import tabulate

root=Tk()
root.title('Demo 1')
root.geometry('1000x600')
root.config(bg="skyblue")

label1=Label(root,text="Product Grabber",fg="white",bg="Blue",font=('Arial',19,'bold'))
label1.place(anchor=CENTER,relx=0.5,rely=0.10,relwidth=0.4,relheight=0.1)

label2=Label(root,text="Enter the product name : ",font=('Arial',19,'bold'))
label2['fg']='black'
label2['bg']='white'
label2.place(anchor=CENTER,relx=0.25,rely=0.3,relwidth=0.3)

input=Entry(root)
input.insert(0,'')
input.place(anchor=CENTER,relx=0.75,rely=0.3,relwidth=0.3)

def checkFlp():
    flipkart_url = 'https://www.flipkart.com/search?q='

    words=input.get()
    input.delete( 0 , 'end' )
    words = words.split()
    #print(words)

    for i in words:
        flipkart_url+=i
        flipkart_url+="+"
    flipkart_url = flipkart_url[:-1]

    op='Website if you want to visit the store : '+flipkart_url
    #print(op)
    labeloutput=Label(root,text=op)
    labeloutput.place(anchor=CENTER,relx=0.5,rely=0.6,relwidth=0.6)
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
    labeloutput.place( anchor = CENTER , relx = 0.5 , rely = 0.7 , relwidth = 0.6 )

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
    listBox.column( 'Index' , anchor = CENTER , minwidth = 150 , width = 150 , stretch = NO )
    listBox.column( 'Product in flipkart' , anchor = CENTER , minwidth = 400 , width = 500 , stretch = NO )
    listBox.column( 'Price' , anchor = CENTER , minwidth = 150 , width = 150 , stretch = NO )

    for i,j,k in printall:
        listBox.insert("","end",value=(i,j,k))

    listBox.place( anchor = CENTER , relx = 0.5 , rely = 0.84 , relwidth = 0.8 ,relheight=0.28)

check=Button(root,text="Check for product in flipkart",command=checkFlp)
check.place(anchor=CENTER,relx=0.5,rely=0.5,relwidth=0.2)

root.mainloop()