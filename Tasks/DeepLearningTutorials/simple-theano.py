import theano
from theano import tensor

# declare two symbolic floating-point scalars
a = tensor.dscalar()
b = tensor.dscalar()
# create a simple symbolic expression
c=a+b
# convert the expression into a callable object that takes (a,b) and computes c
f = theano.function([a,b], c)
#bind1.5to a,2.5to b,andevaluate c
result = f(1.5, 2.5)
print(result)
