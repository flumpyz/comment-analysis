import csv
def copy_please():
    # read
    data = []
    with open('comment_reply.csv', 'r', newline='', encoding='utf-8') as f:
        f_csv = csv.reader(f)
        # header = next(f_csv)
        for row in f_csv:
            data.append(row)
    # write
    with open('newtest.csv', 'a', newline='', encoding='utf-8') as new_cSv:
        writer = csv.writer(new_cSv)
        writer.writerows(data)
