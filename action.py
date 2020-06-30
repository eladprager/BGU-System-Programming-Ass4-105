from Repository import repo
import os
import sys
import DTO
import DAO
import sqlite3
import printdb

def run():
    inputfilename = sys.argv[1]
    cursor = repo.getconn().cursor()
    with open(inputfilename, "r") as inputfile:
        for line in inputfile:
            line = line.strip()
            line = line.split(", ")
            activity = DTO.Activitie(line[0], line[1], line[2], line[3])
            repo.activities.insert(activity)
    repo.getconn().commit()
    # cursor.execute("SELECT * FROM Activities ORDER BY Activities.date ASC")
    # tmp = cursor.fetchall()
    tmp = DAO._Products.sort(repo)
    repo.getconn().commit()
    for i in tmp:
        product = repo.products.find(i[0])
        quan = product.quantity
        if i[1] > 0:
            repo.products.update(quan+i[1], i[0])
        else:
            if int(quan + i[1]) >= 0:
                repo.products.update(quan+i[1], i[0])
            else:
                DAO._Activities.delete_row(repo,i[0],i[1],i[2],i[3])

    repo.getconn().commit()


run()
printdb.printDB()