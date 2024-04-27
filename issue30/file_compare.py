filename1 = 'pwmH.log'
filename2 = 'pwmP.log'
filename3 = 'pwmB.log'

file1 = open(filename1, 'r')
file2 = open(filename2, 'r')
file3 = open(filename3, 'r')

lines1 = file1.readlines()
lines2 = file2.readlines()
lines3 = file3.readlines()

first_matches = []

if len(lines1)>len(lines2):
    for line in lines1:
        if line in lines2:
            first_matches.append(line)
else:
    for line in lines2:
        if line in lines1:
            first_matches.append(line)

second_matches = []

if len(first_matches)>len(lines3):
    for line in first_matches:
        if line in lines3:
            second_matches.append(line)
else:
    for line in lines3:
        if line in first_matches:
            second_matches.append(line)

print(*second_matches, sep = "\n")
print(filename1, len(lines1), "lines")
print(filename2, len(lines2), "lines")
print(filename3, len(lines3), "lines")
print("resulting in", len(second_matches), "matches")
