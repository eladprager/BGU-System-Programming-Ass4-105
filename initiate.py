from Repository import repo
import DAO
import DTO
import sys
import os

def main(args):
    repo.create_tables()
    conn = repo.getconn()
    inputfilename=args[1]
    with open(inputfilename, "r") as inputfile:
        for line in inputfile:
            line = line.strip()
            line = line.split(", ")
            if line[0] == 'C':
                coffee_stand = DTO.Coffee_stand(line[1], line[2], line[3])
                DAO._Coffee_stands.insert(repo,coffee_stand)
            if line[0] == 'S':
                supplier = DTO.Supplier(line[1], line[2], line[3])
                DAO._Suppliers.insert(repo,supplier)
            if line[0] == 'E':
                employee = DTO.Employee(line[1], line[2], line[3],line[4])
                DAO._Employees.insert(repo,employee)
            if line[0] == 'P':
                product = DTO.Product(line[1], line[2], line[3], 0)
                DAO._Products.insert(repo,product)
    conn.commit()


if __name__ == '__main__':
    main(sys.argv)

