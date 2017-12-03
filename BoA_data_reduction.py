# Problem:  Processing downloaded bank statements can be cumbersome because there is
# no control of formatting in the description filed.

# Background:  BoA includes the name of the merchant, potentially their address, phone
# number, and any other information the merchant provides in the description field.
# Algorithms that use regex have been tested and fail because a standard bank statement
# has many vendors and therefore many regular expressions to consider.  The overlap tends
# to modify data that it shouldn't.
# Additionally, the reduced data set can be used to eliminate some of the next step in
# preparing an expense report by summarizing the data.

# Purpose:  Produce functions that reduce and summarize the data in the BoA bank statement
# by eliminating as much ancillary data from the description field as possible, without the
# use of regular expressions.



def reduce(row):
# CHECKCARD, PURCHASE, WITHDRAWL, and Deposit all have the same fields in the description.

    nd = "" # holds the new description
    if "CHECKCARD" in row['description']:
        a = row['description'].split(" ")
        for i in range(2, len(a)-4):
            nd += str(a[i]) + " "
        row['description'] = nd.upper().rstrip()
    elif "PURCHASE" in row['description']:
        a = row['description'].split(" ")
        p = a.index('PURCHASE')
        c = a.index('CKCD')
        for i in range(p+1, c):
            nd += str(a[i])+ " "
        row['description'] = nd.upper().rstrip()
    elif "WITHDRWL" in row['description']:
        row['description'] = "WITHDRAWL"
    elif "DEPOSIT" in row['description']:
        row['description'] = "DEPOSIT"

# These are common transactions for me personally.  They can be processed quickly.
    elif "SHAPELL PROP DES" in row['description']:
        row['description'] = "SHAPELL APARTMENT RENTAL"
    elif "WREC DES" in row['description']:
        row['description'] = "WITHLAHOOCHIE ELECTRIC"
    elif "HERN CNTY UTILIT DES" in row['description']:
        row['description'] = "HERNANDO COUNTY UTILITIES"

    return row

def subtotal (stmt):
# Create subtotals based on the reduced data in the descriptions.
    subtotals = {}

    for i in stmt:
        if i['description'] in subtotals:
            new_amount = subtotals[i['description']] + float(i['amount'])
            subtotals[i['description']] = new_amount
        else:
            subtotals.update({i['description'] : float(i['amount'])})
    return subtotals

if __name__ == "__main__":

########## Initialize variables ##########

    f = "/Users/Bob/Desktop/stmtpipe.new" # Bank statement file with | delimiter

    stmt = []                                                   # New statement after data reduction

# BoA includes date, description, amount and balance in each line.  We can eliminate balance
# straight away.

    fields = ['date', 'description', 'amount', 'balance']           # Fields in the bank statement
    new_fields = ['date', 'description', 'amount']                  # Fields desired in the data reduced bank statement

########## Initialize variables ##########

# Open the file with the bank transactions in it.  The downloaded BoA file contains some
# summary data at the beginning.  This should be eliminated by hand because it is not known
# how many lines of summary data there are.  Doing this automatically risks accidentally
# deleting data.

    with open(f) as file_handle:
        file_text = file_handle.readlines()

# Iterate through the file and create a list of dictionary items.
# BoA gives choices for field delimiters, comma is not available because it could be in the
# data.  This program uses the pipe | symbol.

    for row in file_text:
        s = row.split("|")
        r = dict(zip(fields, s))

        row = reduce(r)                                         # Reduce the data in the discription field

# Add the date, amount and new description to a list of dictionary items for future processing

        stmt.append(dict(zip(new_fields, [row['date'], row['description'],row['amount']])))

    subtotals = subtotal(stmt)                                  # Subtotal the new, data reduced statement

# Print results to standard out in pipe delimited format

    for i, j in sorted(subtotals.items()):
        print i,"|",j

# Add some data to show data reduction
    print "-"*40
    print ("%21s %7d" % ("Original Statement:", len(stmt)))
    print ("%20s %7d" % ("After data reduction:", len(subtotals)))