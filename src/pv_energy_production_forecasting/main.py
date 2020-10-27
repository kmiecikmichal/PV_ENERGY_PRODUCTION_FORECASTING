from user import User


print("Hello")
Michal = User("U001", "Michal", 20000, 20, 40, 40.002, 21.008)
Piotr = User("U002", "Piotr", 10000, 20, 40, 40.002, 21.008)

Michal.add_to_database()
Piotr.add_to_database()
Piotr.delete_from_database()
