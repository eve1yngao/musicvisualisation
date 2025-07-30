import sympy as sp

# Define variables
x, y = sp.symbols('x y')

# Translate coordinates
X = x + 2
Y = y - 1.5

# Rotation angle components (from direction vector <4,3>)
cos_theta = 4 / 5
sin_theta = 3 / 5

# Semi-major and semi-minor axes
a = 3.5
b_squared = 6

# Rotated ellipse equation
expr = ((cos_theta * X + sin_theta * Y)**2) / (a**2) + ((sin_theta * X - cos_theta * Y)**2) / b_squared - 1

# Expand and simplify
cartesian_eq = sp.simplify(sp.expand(expr))
print("Cartesian form of the ellipse:")
sp.pprint(cartesian_eq)
