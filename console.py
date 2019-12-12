import psycopg2
import texttable
connection = psycopg2.connect(user = "201701147",
                              password = "P@tel@vi741",
                              host = "10.100.71.21",
                              port = "5432",
                              database = "201701147")

print("You are connected to - 201701147 \n")

cursor = connection.cursor()
curs=connection.cursor()
cursor.execute("set search_path to toyota")

def select():
    x = input(" enter your query : \n ")
    y= x+" LIMIT 0"
    curs.execute(y)
    colnames = [desc[0] for desc in curs.description]
    print(colnames)
    cursor.execute(x)
    rows = cursor.fetchall()
    for r in rows:
        print(r)

def update():
    x = input("enter your update query : \n ")
    cursor.execute(x)
    print(cursor.statusmessage)
    connection.commit()

def selspecific():
     list=["Give all the details of a customer who spend maximum amount in an order.",
           "Give all details of customer who gave you maximum profit amount.",
           "find sales details of car sold in gujarat where car name is ='Toyota Fortuner' with diesel version.",
           "determine total profit a company has till now.",
           "Name and contact number of customers who doesn&#39;t register for service their product after 1 year of use.",
           "Average time at which customer service their product.(in days)",
           "find total profit of last 1 month from gujarat.",
           "find the percentage of products bought by customers using loan or by emi.",
           "profit made by each showroom.",
           "find the product details which is supplied maximum in quantity from all stockhouse.",
           "number of products have been sold by each showroom.",
           "List stockhouse_id,stockhouse_name and remaining capacities for every stockhouse."]
     listq=["select * from customer where customer_id = (select customer_id from payment "+
            "natural join sales_details where total_amount =(select max(total_amount) "+
            "from payment natural join sales_details))",
             "select * from customer "+
             "where customer_id = (select customer_id from  sales_details "+
             "where invno =( select invno from payment natural join sales_details "+
             "natural join product_details where (total_amount - unit_price)= "+
             "(select  max(total_amount - unit_price) "+  
             "from payment natural join sales_details "+
             "natural join product_details)  order by invdate desc limit 1))",
            "Select sales_details.invno,sales_details.showroom_id,sales_details.code, "+
            "sales_details.product_id,product_details.product_name,"+
                "Product_details.model_type, sales_details.transaction_id,"+
                "payment.total_amount from sales_details join product_details on "+
                "(sales_details.code=product_details.code and "+
                "sales_details.product_id=product_details.product_id) join showroom on "+
                "(sales_details.showroom_id=showroom.showroom_id) join payment on "+
                "(sales_details.transaction_id=payment.transaction_id) where "+
                "product_name='Toyota Fortuner' and (model_type='Diesel Automatic version' or "+
                "model_type='Diesel Manual version') and state='gujarat' order by invno",
             "select sum(payment.total_amount - product_details.unit_price) as total_profit "+
            "from sales_details join payment on (sales_details.transaction_id=payment.transaction_id) "+
            "join product_details on (product_details.code=sales_details.code and "+
            "product_details.product_id=sales_details.product_id)",
            "select customer_id,customer_name,contact_no "+
                "from customer natural join sales_details "+
                "where current_date - sales_details.invdate > 360 except "+
                "select customer_id,customer_name,contact_no "+
                "From serviced_by  natural join registration  natural join customer",
            "select avg(abs(serviced_by.service_date - sales_details.invdate)) "+
                "from serviced_by  natural join registration natural join sales_details",
            "select sum(payment.total_amount - product_details.unit_price) as total_profit "+
                "from sales_details join payment "+
                "on (sales_details.transaction_id=payment.transaction_id) "+
                "join product_details on "+
                "(product_details.code=sales_details.code and product_details.product_id=sales_details.product_id) "+
                "join showroom on (showroom.showroom_id=sales_details.showroom_id) "+
                "where sales_details.invdate>=date_trunc('day', NOW() - interval '1 month') and showroom.state='gujarat'",
            "select (select count(sales_details.invno) as cnt from sales_details where sales_details.invno in "+
                "(select invno from loan) or sales_details.transaction_id in (select transaction_id from by_emi))*100 / "+
                "(select count(invno) from sales_details) as percentage_of_products_bought_on_loan_or_emi",
            "select showroom_id,sum(profit_per_item) as profit from profit_per_sale "+
                "group by showroom_id order by showroom_id",
            "Select product_details.code,product_details.product_id,product_details.product_name, "+
                "product_details.model_type,product_details.series,price from product_details join "+
                "(select max(maximum.supply_per_product) as max_supply,maximum.code,maximum.product_id from "+
                 "(select sum(numofunits) as supply_per_product,code,product_id from supply_details "+
                  "group by code,product_id order by code,product_id) as maximum group by code,product_id limit 1) "+
                "as finl on (finl.code=product_details.code and finl.product_id=product_details.product_id)",
            "select showroom_id,showroom_name,count(customer_id) "+
                 "from sales_details natural join showroom "+
                "group by(showroom_id,showroom_name) "+
                "order by count(customer_id) desc",
            "select sh_name,stockhouse.sh_id,(stock_capacity-stock) from stockhouse "+
                "join (select sh_id, sum(numofunits) as stock from stocked_in group by sh_id) as abc "+
                "on (abc.sh_id=stockhouse.sh_id)"]


            
     print(" Enter a number to choose query from list")
     z=int(input("\n Enter 1: "+list[0]+"\n Enter 2:"+list[1]+"\n Enter 3: "+list[2]+
             "\n Enter 4: "+list[3]+"\n Enter 5:"+list[4]+"\n Enter 6: "+list[5]+
             "\n Enter 7: "+list[6]+"\n Enter 8:"+list[7]+"\n Enter 9: "+list[8]+
             "\n Enter 10: "+list[9]+"\n Enter 11:"+list[10]+"\n Enter 12: "+list[11]+"\n"))
     if(z>12):
        print("Enter valid number \n")
        selspecific()
     x=listq[int(z-1)]
     y=x+" LIMIT 0"
     curs.execute(y)
     colnames = [desc[0] for desc in curs.description]
     print(colnames)
     cursor.execute(x)
     rows = cursor.fetchall()
     for r in rows:
        print(r)
     print("\n\n")
            
def discount():
    x=str(input("\nEnter showroom_id in format of 20192000xx :"))
    y=str(input("\nEnter code as 1 or 2 or 3 :"))
    z=str(input("\n Enter product_id in format of 20190000xx :"))
    cursor.execute("select * from discout('"+x+"',"+y+",'"+z+"')")
    rows=cursor.fetchall()
    for r in rows:
        r=str(r)
        print("discout = "+r[1:len(r)-2]+"\n")
def totalamount():
    x=str(input("\nEnter showroom_id in format of 20192000xx :"))
    y=str(input("\nEnter code as 1 or 2 or 3 :"))
    z=str(input("\n Enter product_id in format of 20190000xx :"))
    cursor.execute("select * from total_amount('"+x+"',"+y+",'"+z+"')")
    rows=cursor.fetchall()
    for r in rows:
        r=str(r)
        print("total_amount = "+r[1:len(r)-2]+"\n")

if __name__ == "__main__":
    while(1):
        x = input(' Enter 1 for select \n Enter 2 for update \n Enter 3 to select specific query from query list\n Enter 4 to check discount\n Enter 5 to find total amount of any product from any showroom \n Enter 6 to close the connection \n')
        if(int(x) == 1):
            select()
        if(int(x) == 2):
            update()
        if(int(x)==3):
            selspecific()
        if(int(x)==4):
            discount()
        if(int(x)==5):
            totalamount()
        if(int(x)==6):
            cursor.close()
            curs.close()
            connection.close()
            print(" PostgreSQL connection is closed")
            break;
        


