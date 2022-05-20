import time

import btpy.py_template.bt as bt
import btpy.btpy_example as btpy_example
import btpy.mu_testsubtree as mu_testsubtree

class Agent:
    def say(self, a, b, c):
        print('Agent say hello !', a, b, c)
    
    def f1(self):
        print('f1')
    
    def f2(self, a):
        print('f2', a)
    
    def a1_true(self):
        print('a1')
        return True
    
    def a2_true(self):
        print('a2')
        return True
    
    def a3_true(self):
        print('a3')
        return True
    
    def a4_true(self):
        print('a4')
        return True
    
    def a1_false(self):
        print('a1')
        return False
    
    def a2_false(self):
        print('a2')
        return False
    
    def a3_false(self):
        print('a3')
        return False
    
    def a4_false(self):
        print('a4')
        return False
    
    def recvDamage(self, attackerId, skillId, damageType, damage):
        print('recvDamage', attackerId, skillId, damageType, damage)
    
    def randomWalk(self, basePos):
        print('randomWalk', basePos)

agent = Agent()
t = bt.BT(agent)
# btpy_example.Create(t)
mu_testsubtree.Create(t)
print(t.exec())
# for _ in range(100):
#     print(t.exec())
#     time.sleep(1.0)
# print(t.ttt)