grade = 1
total = 4

average = float(grade / total)
average =("{:.2f}".format(average)).replace('0.', '') + '%'


print(average)
