fun = lambda num,num2: num*num2
print(fun(5,2))
print((lambda num,num2: num*num2)(5,2))



print((lambda x: x*2)(8))

print((lambda name: f"Привет, {name}!")('Ирина'))