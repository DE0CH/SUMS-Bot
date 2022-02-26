emails = set()
with open('private_data/emails.txt') as f:
    for line in f:
        emails.add(line.strip())
