import sqlite3
import DAO
import os
import atexit


class _Repository:
    def __init__(self):

        self._conn = sqlite3.connect('moncafe.db')
        self.employees = DAO._Employees(self._conn)
        self.products = DAO._Products(self._conn)
        self.suppliers = DAO._Suppliers(self._conn)
        self.coffee_stands = DAO._Coffee_stands(self._conn)
        self.activities = DAO._Activities(self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def getconn(self):
        return self._conn


    def create_tables(self):
        self._conn.executescript("""
        DROP TABLE IF EXISTS Employees;
        CREATE TABLE Employees (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            salary REAL NOT NULL,
            coffee_stand INTEGER REFERENCES Coffee_stand(id)
        );

        DROP TABLE IF EXISTS Suppliers;
        CREATE TABLE Suppliers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            contact_information TEXT
        );

        DROP TABLE IF EXISTS Products;
        CREATE TABLE Products (
            id INTEGER PRIMARY KEY,
            description TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        );

        DROP TABLE IF EXISTS Coffee_stands;
        CREATE TABLE Coffee_stands (
            id INTEGER PRIMARY KEY,
            location TEXT NOT NULL,
            number_of_employees INTEGER
        );
        
        DROP TABLE IF EXISTS Activities;
        CREATE TABLE Activities (
            product_id     INTEGER     REFERENCES Product(id),
            quantity     INTEGER     NOT NULL,
            activator_id     INTEGER     NOT NULL,
            date     DATE     NOT NULL 
        );
        """)
        self._conn.commit()

    def eReport(self):
        c = self._conn.cursor()
        report = c.execute("""
        SELECT First.name, First.salary, First.location, COALESCE(First.total,0) As total_2
        FROM (SELECT Second.id,Second.name,Second.salary,Second.location, SUM(sales) As total
        FROM (SELECT Employees.id, Employees.name, Employees.salary, Coffee_stands.location,
        ((Activities.quantity * Products.price) * -1) As sales
        FROM ((Employees JOIN Coffee_stands ON Employees.coffee_stand = Coffee_stands.id)
        LEFT JOIN Activities ON Employees.id = Activities.activator_id)
        LEFT JOIN Products ON Activities.product_id = Products.id) As Second GROUP BY Second.id)
        As First
        """).fetchall()

        return [report]

    def aReport(self):
        c = self._conn.cursor()
        report = c.execute("""
        SELECT Activities.date, Products.description, Activities.quantity,
        coalesce(Employees.name,'None'),coalesce(Suppliers.name,'None')
        FROM (((Activities LEFT JOIN Employees ON Activities.activator_id = Employees.id)
        LEFT JOIN (Suppliers) ON Suppliers.id = Activities.activator_id)							   
        LEFT Join (Products) ON Activities.product_id = Products.id) ORDER BY Activities.date ASC
        """).fetchall()

        return [report]


repo = _Repository()
atexit.register(repo._close)
