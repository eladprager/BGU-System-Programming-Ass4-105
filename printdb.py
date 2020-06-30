from Repository import repo

def printDB():
    print("Activities")
    for row in repo.activities.find_all():
        t=(row.product_id,row.quantity,row.activator_id,row.date)
        print(t)

    print("Coffee stands")
    for row in repo.coffee_stands.find_all():
        t = (row.id,row.location,row.number_of_employees)
        print(t)

    print("Employees")
    for row in repo.employees.find_all():
        t = (row.id,row.name,row.salary,row.coffee_stand)
        print(t)

    print("Products")
    for row in repo.products.find_all():
        t = (row.id,row.description,row.price,row.quantity)
        print(t)

    print("Suppliers")
    for row in repo.suppliers.find_all():
        t = (row.id,row.name,row.contact_information)
        print(t)

    print("\nEmployees report")
    for line in repo.eReport():
        for i in line:
            print(end='')
            tmp = [str(e) for e in i]
            print(' '.join(tmp), end='')
            print("")

    if len(repo.activities.find_all()) != 0:
        print("\nActivities")
        for line in repo.aReport():
            for i in line:
                print('(', end='')
                tmp = [str(e) for e in i]
                print(', '.join(tmp), end='')
                print(')')
    # for row in repo.products.find_all():
    #     t = (row.description)

