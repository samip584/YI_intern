import re
from urllib.request import Request, urlopen
import json
import sqlite3
import os
import platform



def make_database():
    # connect to database or create database
    product_db = sqlite3.connect('product.db') 
    c = product_db.cursor()
    
    # try to create table "products" in the sql database if not already created
    try:
        c.execute("""CREATE TABLE products(
                    year integer,
                    petroleum_product text,
                    sales integer
                    )""")

        product_db.commit()
        
    except:
        pass
    
    # collect all the products from the to see if it consists of any data
    c.execute("SELECT * FROM products")
    inserted_data = c.fetchall()

    # if the table has no data add data from the given URL to the table
    if len(inserted_data) == 0:
        print("making database from json please wait")
        
        product_db = sqlite3.connect('product.db')
        c = product_db.cursor()
        
        json_url = 'https://raw.githubusercontent.com/younginnovations/internship-challenges/master/programming/petroleum-report/data.json'

        # open URL and read the html
        req = Request(json_url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req).read().decode('UTF8')

        #convert the html string into json
        json_data = json.loads(html) 
        
        for product in json_data:
            c.execute("INSERT INTO products VAlUES (:year, :petroleum_product, :sale)", product)
            print(product)
            product_db.commit()
        print()
        print()
        print()
        input("Database is ready enter any key")
        


    product_db.close()



def make_table():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')
    # connect to sql database and set curser
    product_db = sqlite3.connect('product.db')
    c = product_db.cursor()
    
    #store minimum yaer into a variable
    c.execute("SELECT min(year) FROM products")
    min_year = c.fetchall()[0][0]
    
    # list consisting of all products
    product_list = []

    # storing the name of products into the list 
    c.execute("SELECT petroleum_product FROM products GROUP BY petroleum_product")
    for product in c.fetchall():
        product_list.append(product[0])

    #final table to be displayed
    final_table = []

    for product in product_list:
        for i in range(2, -1, -1):
            c.execute("SELECT min(sales), max (sales), avg(sales) FROM products WHERE  petroleum_product = :product and year >= :low_year and year < :high_year and sales > 0",{"low_year" : min_year + 5*i, "high_year": min_year + 5*(i+1), "product": product})
            temp = c.fetchall()
            final_table.append({
                "Product" : product,
                "Year" : str(min_year + 5*i) + "-" + str(min_year + 5*(i+1)-1),
                "Min" : temp[0][0],
                "Max" : temp[0][1],
                "Avg" : temp[0][2]
            })
    
    #printing table
    print("{:<30} {:<15} {:<10} {:<10} {:<10} ".format('Product', 'Year', 'Min', 'Max', 'Avg'))
    print("="*80)

    for product in final_table:
        if (product['Min'] == None or product['Min'] == None or product['Min'] == None):
            print ("{:<30} {:<15} {:<10} {:<10} {:<10}".format(product['Product'], product['Year'], '0', '0', '0'))
        else:
            print ("{:<30} {:<15} {:<10} {:<10} {:<10}".format(product['Product'], product['Year'], str(product['Min']), str(product['Max']), str(product['Avg'])))
    
    product_db.close()




def main():
    
    make_database()     # make sqlite database from the given json if not created
    make_table()        # print the asked table from the sqlite database

    

if __name__ == "__main__":
	main()