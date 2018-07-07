import numpy as np
import numpy.random as rn
import operator

class Minecraftworld(object):



	def _transition_probability(self,sFrom,action,sTo):
		if tuple(map(operator.add, sFrom, action)) == sTo:
			return 1
		else:
			return 0


	def __init__(self, grid_dimensions,discount):


		# +x,+z,-x,-z, jumps, jumpuse
		self.actions = ((1,0,0),(0,0,1),(-1,0,0),(0,0,-1),
						(1,1,0),(0,1,1),(-1,1,0),(0,1,-1),
						(0,1,0))
		self.n_actions = len(self.actions)
		# X Y Z
		self.grid_dimensions = grid_dimensions
		self.n_states = grid_dimensions[0]*grid_dimensions[1]*grid_dimensions[2]*16
		self.discount = discount


        self.transition_probability = np.array(
            [[[self._transition_probability(i, j, k)
               for k in range(self.n_states)]
              for j in range(self.n_actions)]
             for i in range(self.n_states)])

	def __str__(self):
		return "Minecraftworld({})".format(self.grid_dimensions)


	def int_to_point(self,i):
		y = i //(self.grid_dimensions[0]*self.grid_dimensions[2])
		xz = i - y*(self.grid_dimensions[0]*self.grid_dimensions[2])
		x = xz // (self.grid_dimensions[2])
		z = xz % (self.grid_dimensions[2])
		return (x,y,z)

	def feature_vector(self,i,feature_map="indent"):
		sx,sy,sz = self.int_to_point(i)








mw = Minecraftworld((2,3,4),0.5)

for i in  range(0,2*3*4):
	print i, mw.int_to_point(i)
