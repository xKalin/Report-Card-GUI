test = [('Cruyff', 104), ('Eusebio', 120), ('Messi', 125), ('Ronaldo', 132), ('Pele', 150)]

test2 = ['Ariana Ajan', 'Ayaz Aravinthan', 'Luke Cai', 'Katty Chen', 'Joshua Cheng', 'Marco Cheung', 'Martin Cheung', 'Marcus Chiu', 'Yixin Dong', 'Elvin Feng', 'Candice Lee', 'Hayley Liang', 'Aiden Lin', 'Jolie Liu', 'Antheia Lu', 'Alexis Popovitch', 'Lucas Wang', 'Jackson Wen', 'Priscilla Wong', 'Paris Yi', 'Priscilla Zhu', 'Ayaz Arvinthan', 'You Allen', 'A A']

test3 = sorted(test2, key=lambda x: x.split()[-1])

print(test3)