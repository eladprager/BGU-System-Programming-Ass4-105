import DTO


class _Employees:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, student):
        self._conn.execute("""
               INSERT INTO Employees (id, name, salary, coffee_stand) VALUES (?, ?, ?, ?)
           """, [student.id, student.name, student.salary, student.coffee_stand])

    def find(self, student_id):
        c = self._conn.cursor()
        c.execute("""
            SELECT name FROM Employee WHERE id = ?
        """, [student_id])

        return DTO.Employee(*c.fetchone())

    def find_all(self):
        c = self._conn.cursor()
        allEmployees = c.execute("""
               SELECT * FROM Employees ORDER BY id ASC
           """).fetchall()

        return [DTO.Employee(*row) for row in allEmployees]

class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
                INSERT INTO Suppliers (id, name, contact_information) VALUES (?, ?, ?)
            """, [supplier.id, supplier.name, supplier.contact_information])

    def find(self, supplier_id):
        c = self._conn.cursor()
        c.execute("""
             SELECT name FROM Suppliers WHERE id = ?
         """, [id])

        return DTO.Supllier(*c.fetchone())

    def find_all(self):
        c = self._conn.cursor()
        allSuppliers = c.execute("""
               SELECT * FROM Suppliers ORDER BY id ASC
           """).fetchall()

        return [DTO.Supplier(*row) for row in allSuppliers]

class _Products:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, product):
        self._conn.execute("""
                 INSERT INTO Products (id, description, price, quantity) VALUES (?, ?, ?, ?)
             """, [product.id, product.description, product.price, product.quantity])

    def find(self, id):
        c = self._conn.cursor()
        c.execute("""
              SELECT * FROM Products WHERE id = ?
          """, [id])
        return DTO.Product(*c.fetchone())

    def update(self, quan, id):
        c = self._conn.cursor()
        c.execute("UPDATE Products SET quantity=? WHERE id=?", (quan, id))
        self._conn.commit()

    def sort(self):
        c = self._conn.cursor()
        self._conn.executescript("""
            DROP TABLE IF EXISTS ActivitiesTMP;
            CREATE TABLE ActivitiesTMP (
            product_id     INTEGER     REFERENCES Product(id),
            quantity     INTEGER     NOT NULL,
            activator_id     INTEGER     NOT NULL,
            date     DATE     NOT NULL 
        );
            """
        )

        self._conn.executescript("""INSERT INTO ActivitiesTMP (product_id, quantity, activator_id, date) 
        SELECT product_id, quantity, activator_id, date FROM Activities ORDER BY date;""")

        self._conn.executescript("""DROP TABLE Activities ;
        ALTER TABLE ActivitiesTMP RENAME TO Activities;""")

        c.execute("SELECT * FROM Activities ORDER BY Activities.date ASC")
        tmp = c.fetchall()
        return tmp

    def find_all(self):
        c = self._conn.cursor()
        allProducts = c.execute("""
               SELECT * FROM Products ORDER BY id ASC
           """).fetchall()

        return [DTO.Product(*row) for row in allProducts]

class _Coffee_stands:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, coffee_stand):
        self._conn.execute("""
                 INSERT INTO Coffee_stands (id, location, number_of_employees) VALUES (?, ?, ?)
             """, [coffee_stand.id, coffee_stand.location, coffee_stand.number_of_employees])

    def find(self, id):
        c = self._conn.cursor()
        c.execute("""
              SELECT number_of_employees FROM Coffee_stands WHERE id = ?
          """, [id])

        return DTO.Coffee_stand(*c.fetchone())

    def find_all(self):
        c = self._conn.cursor()
        allCoffee_stands = c.execute("""
               SELECT * FROM Coffee_stands ORDER BY id ASC
           """).fetchall()

        return [DTO.Coffee_stand(*row) for row in allCoffee_stands]

class _Activities:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, activity):
        self._conn.execute("""
               INSERT INTO Activities (product_id, quantity, activator_id, date) VALUES (?, ?,?,?)
           """, [activity.product_id, activity.quantity, activity.activator_id, activity.date])

    def find(self,product_id,quantity,activator_id,date):
        c = self._conn.cursor()
        c.execute("""
              SELECT quantity FROM Activities WHERE product_id=? AND quantity=? AND activator_id=? AND date=?
          """, [product_id, quantity, activator_id, date])

        return DTO.Activitie(*c.fetchone())

    def find_all(self):
        c = self._conn.cursor()
        allActivities = c.execute("""
               SELECT * FROM Activities
           """).fetchall()

        return [DTO.Activitie(*row) for row in allActivities]

    def delete_row(self,product_id,quantity,activator_id,date):
        self._conn.execute("""
                      DELETE FROM Activities WHERE product_id=? AND quantity=? AND activator_id=? AND date=?
                   """, [product_id, quantity, activator_id, date])
