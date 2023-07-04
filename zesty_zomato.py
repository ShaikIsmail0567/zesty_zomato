
# Dish Inventory...
import json
class DishInventory:
    def __init__(self):
        self.inventory = self.load_from_file()
    
    # load from file
    @staticmethod
    def load_from_file():
        try:
            with open("./dish_inventory.json","r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def see_all_dish(self):
        if len(self.inventory) == 0:
            print('No dish is available in the inventory!')
        else:
            for dish in self.inventory:
                print(dish)     

            

    def add_dish(self,dish_id, name, price,stock, availability):
        dish = {
                 'id': dish_id,
                 'name': name,
                 'price': price, 
                 'stock': stock,  
                 'availability': availability
                }

        self.inventory.append(dish)
        print("Dish added to the inventory. ")
        self.save_to_file()
    
    # add data to file
    def save_to_file(self):
        with open("./dish_inventory.json",'w') as file:
            json.dump(self.inventory,file)

    

    def romove_dish(self,dish_id):
        for dish in self.inventory:
            if dish['id'] == dish_id:
               self.inventory.remove(dish)
               self.save_to_file()
               print("Dish removed successfully!")
               break
        else:
            print("Dish not found in inventory!")   


    def update_availability(self,dish_id,availability):
        for dish in self.inventory:
            if dish['id'] == dish_id:
                dish['availability'] = availability
                self.save_to_file()
                print("Dish availability updated successfully!")
                
                break
        else:
            print("Dish not found in the inventory!")    
    

# Order managemnt is here...
class OrderRecords:
    def __init__(self) -> None:
        self.orders = self.load_orders_from_file()
        self.order_id_count = self.get_next_order_id_from_file()
    
    # load order from file
    @staticmethod
    def load_orders_from_file():
        try:
            with open("./orders.list.json","r") as file:
               return json.load(file)
        except FileNotFoundError:
            return []
    
    # save orders to file
    def save_orders_to_file(self):
        with open("./orders.list.json",'w') as file:
            json.dump(self.orders,file)

    # get current order count form count file
    @staticmethod
    def get_next_order_id_from_file():
        with open("./count.txt",'r') as file:
            try:
               content =  file.read()
               curr_count = int(content.split("=")[1].strip())
               return curr_count
            except FileNotFoundError:
               return 1


    def get_next_order_id(self):
        order_id = self.order_id_count
        self.order_id_count += 1
        with open("./count.txt",'w') as file:
            file.write(f'count = {self.order_id_count}')
        return order_id

    def record_order(self, customer_name, dish_id, quantity, dish_inventory):
        dish_found = False
        dish_to_remove = []
        for dish in dish_inventory.inventory:
            if dish['id'] == dish_id:
                dish_found  = True
                if dish['availability'] == "yes":
                    if dish['stock'] >= quantity:
                        dish['stock'] -= quantity
                        self.orders.append({
                           'customer_name': customer_name,
                           'order_id':self.get_next_order_id(),
                           'quantity': quantity,
                           'total_price':quantity * dish['price'],
                           'status': 'received'
                        })
                        self.save_orders_to_file()
                        print("Order Placed!")
                        dish_inventory.save_to_file()
                        if dish['stock'] == 0:
                           dish_to_remove.append(dish)
                        break
                    else:
                        print("Insufficient Stock!")
                else:
                    print("Dish is not available!")
        if not dish_found:
            print("Dish not found in the inventory!")

        # remove the dish with 0 stock
        for dish in dish_to_remove:
            dish_inventory.inventory.remove(dish)
        dish_inventory.save_to_file()

            
    def see_all_orders(self):
        if len(self.orders) == 0:
            print("No orders present right now!")
        else:
            for order in self.orders:
              print(order)

    def change_order_status(self,order_id,status):
        order_found = False
        for order in self.orders:
            if order['order_id'] == order_id:
                order_found = True
                order['status'] = status
                self.save_orders_to_file()
                print("Order status has been updated successfully!")

        if not order_found:
            print("No orders found!") 
            
            



dish_inventory = DishInventory()
order_records = OrderRecords()
def display_menu():
    print()
    print("*************  Zesty - Zomato  ***************")
    print("============================================================")
    print()
    print("1. See all the available dish in the inventory")
    print("2. Add a dish to the inventory")
    print("3. Remove a dish from the invenotory")
    print("4. Update Availibilty")
    print("5. Order a dish")
    print("6. Update the status of a order ")
    print("7. See All Orders")
    print("8. Exit")


def get_input(message):
    return input(message)    

def see_inventory():
    print("Available dish :")
    dish_inventory.see_all_dish()

def add_dish_to_inventory():
    dish_id = int(get_input("Enter dish ID:(Integer) "))
    name = get_input("Enter dish name: ")
    price = int(get_input("Enter dish price: "))
    stock = int(get_input("Enter stock: "))
    availability = get_input("Enter dish availability (yes/no): ")
    dish_inventory.add_dish(dish_id, name, price,stock, availability)
    print()


def remove_dish_from_inventory():
    dish_id = int(get_input("Enter dish ID:(Integer) "))
    dish_inventory.romove_dish(dish_id)


def update_dish_availability():
    dish_id = int(get_input("Enter dish ID:(Integer) "))
    availability = get_input("Enter dish availability (yes/no): ")
    dish_inventory.update_availability(dish_id, availability)

def make_order():
    dish_id = int(get_input("Enter dish ID:(Integer) "))
    quantity = int(get_input("Enter the quantity: "))
    customer_name = get_input("Enter your name: ")
    order_records.record_order(customer_name,dish_id,quantity,dish_inventory)

def change_order_status():
    order_id = int(get_input("Enter order ID (Integer): "))
    new_status = get_input("Enter new status of order: ")
    order_records.change_order_status(order_id,new_status)

def see_all_orders():
    order_records.see_all_orders()
    

while True:
    display_menu()
    choice = get_input("Enter your choice: ")

    if choice == '1':
        see_inventory()
    elif choice == '2':  
        add_dish_to_inventory() 
    elif choice == '3':
        remove_dish_from_inventory()
    elif choice == '4':
        update_dish_availability()
    elif choice == '5':
        make_order()
    elif choice == '6':
        change_order_status()
    elif choice == '7':
        see_all_orders()
    elif choice == '8':        
        break
    else:
        print("Invalid input. please give correct input.")        