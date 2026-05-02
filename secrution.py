x1 = int(input())
y1 = int(input())
x2 = int(input())
y2 = int(input())

x12 = ''
y12 = ''

if x1 < x2:
	x12 = "E" * (x2 - x1)
if x1 > x2:
	x12 = "W" * (x1 - x2)
if y1 < y2:
	y12 = "N" * (y2 - y1)
if y1 > y2:
	y12 = "S" * (y1 - y2)
print(x12 + y12)
