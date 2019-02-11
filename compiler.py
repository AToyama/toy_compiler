n = ["0","1","2","3","4","5","6","7","8","9"]
operadores = ['+','-']

entrada = input("")

entrada.replace(" ", "")

def operacao(num1,num2,operador):
	if operador == "+":
		return int(num1) + int(num2)
	if operador == "-":
		return int(num1) - int(num2)

n_ops = 0

for i in entrada:
	if i in operadores:
		n_ops += 1

print(n_ops)

num1 = ""

#index do char da entrada
x = 0

for i in range(0, n_ops):
	num2 = ""
	if num1 == "":
		
		while entrada[x] in n:
			num1 += entrada[x]
			x += 1

		op = entrada[x]

	
