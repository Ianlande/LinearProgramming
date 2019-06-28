# -*- coding: utf-8 -*-

from pyomo.environ import *

model = AbstractModel()
model.Products = Set()
model.Weight = Param(model.Products,within=PositiveIntegers)
model.Value = Param(model.Products,within=PositiveIntegers)
model.MaxWeight = Param()
model.Quantity = Var(model.Products,within=Binary)

# 输出
def maxprofit_rule(model):
    return sum(model.Value[i]*model.Quantity[i] for i in model.Products)
    
# 最优
model.obj = Objective(rule=maxprofit_rule,sense=maximize)

# 约束条件
def _maxweight(model):
    return sum(model.Quantity[i]*model.Weight[i] for i in model.Products)<=model.MaxWeight
model.maxweight = Constraint(rule=_maxweight)

instance = model.create_instance("ProductPlan.dat")

# ipopt求解器和glpk求解器
#opt = SolverFactory("ipopt")
opt = SolverFactory("glpk")

result = opt.solve(instance)

# 输出
print("Result: ")
for index in instance.Quantity:
    print(index, ": ", instance.Quantity[index].value)

