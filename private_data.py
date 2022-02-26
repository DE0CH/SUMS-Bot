emails = set()
with open('emails.txt') as f:
    for line in f:
        emails.add(line.strip())

