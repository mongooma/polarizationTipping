import numpy as np
import random
import os
import math
from sim_utilities import polarization
import time

def update_we(Z, kwargs):
	def update_n(Z):
		"""
		local; choose a node to update
		:return:
		"""
		i = random.randint(0, N-1)   # randomly choose a node
		update_node_we(Z, i, kwargs)  # Z is changed

	def update_C():
		"""
		calculate the intolerance level \alpha
		local
		:return
		"""
		C = 0 * kwargs["alpha"] + 1 * (1-kwargs["alpha"])
		kwargs.update({"C": C})

	N = kwargs["N"]

	step_lim = kwargs['step_lim']   # debug

	# update the normalizer for this round
	update_C()

	step = 0
	results = [-1]
	results_1 = [-1] # init
	ind = random.randint(0, 10000)
	# the output indicator number, for multiple outputs from a single process, increase the range when the number of
	# outputs is high (calculate the collision prob. if necessary)

	params = ['alpha', 'party_w', 'M_static', 'M_dyn', 'shock', 'shock_time_std', 'log_s']

	if kwargs['shock_incre'] or kwargs['party_w_incre'] or kwargs['alpha_incre']:
		# if hysteresis test, add the direction information
		params.append('direct')
	subfolder = 'current'    #
	print(''.join(['{:.2f}\t'.format(kwargs[param]) for param in params]),
							file=open("{}{}/{}_{}_T_res_std".format(kwargs['path'],
												  subfolder,
										   os.getpid(), ind), 'a'))

	print(''.join(['{:.2f}\t'.format(kwargs[param]) for param in params]),
							file=open("{}{}/{}_{}_T_res_partyDiff".format(kwargs['path'],
														subfolder,
										   os.getpid(), ind), 'a'))

	shock_flg = 0
	kwargs['shock_start'] = False
	while step < step_lim+1:
			# or abs(results[-1] - results[-2]) > 5:  # for energy
			# err > 0.00001:
			# :
		# if not kwargs["w_static"]:
		# 	pass
			# update_C(global_=True, MAX=1)

		if kwargs['shock'] > 0 and shock_flg == 0:
			if kwargs['shock_time_std'] < 0:
				# if \sigma is not specified, add the shock after full convergence of the last round
				if kwargs['init'] == False:  # not a starting round
					if step == 0:   # add the shock at the beginning of this round
						shock_flg = 1
			elif abs(results[-1]-kwargs['shock_time_std']) < 0.01:
				# if \sigma is specified, add the shock when polarization reaches \sigma
				shock_flg = 1
			else:
				pass

			if shock_flg == 1:   # add the shock
				new_dim = np.array([1 for i in range(kwargs['N'])]).reshape(-1, 1) # everyone on 1 on this shock issue
				Z = np.hstack((new_dim, Z))  # the shock dimension is added in as the first dimension
				kwargs['M_dyn'] += 1  # increment the number of dynamic dimensions
				kwargs['shock_start'] = True
				# record the precise step where the shock was added in
				print('shock_start={}'.format(step-1),
										file=open("{}{}/{}_{}_T_res_shockRecord".format(kwargs['path'],
																	subfolder,
																	os.getpid(), ind), 'a'))

		results.append(polarization.polarization_std(Z[:, :kwargs['M_dyn']]))  # extremism
		results_1.append(polarization.polarization_party_diff(np.hstack([Z[:, :kwargs['M_dyn']],
																	Z[:, -1:]])))  # partisan difference
		if step % 100 == 0:
			print(time.time())
			print("steps_cnt =", step, "polarization=", results[-1], ' ', results_1[-1])
			# load the result ()
			if kwargs['shock'] > 0:  # T, polarization, polarization_shock
				print('{}\t{:.10f}\t{:.10f}\n'.format(step, results[-1], polarization.polarization_std(Z)),
										file=open("{}{}/{}_{}_T_res_std".format(kwargs['path'],
																							subfolder,
																							os.getpid(), ind), 'a'))
				print('{}\t{:.10f}\t{:.10f}\n'.format(step, results_1[-1], polarization.polarization_party_diff(
												np.hstack([Z[:, :1], Z[:, -1:]]))),
										file=open("{}{}/{}_{}_T_res_partyDiff".format(kwargs['path'],
																						subfolder,
																						os.getpid(), ind), 'a'))
			else:  # T, polarization
				print('{}\t{:.10f}\n'.format(step, results[-1]),
										file=open("{}{}/{}_{}_T_res_std".format(kwargs['path'],
																						subfolder,
																						os.getpid(), ind), 'a'))
				print('{}\t{:.10f}\n'.format(step, results_1[-1]),
										file=open("{}{}/{}_{}_T_res_partyDiff".format(kwargs['path'],
																							subfolder,
																							os.getpid(), ind), 'a'))
		update_n(Z)
		kwargs['step'] = step
		step += 1

	return Z


def update_node_we(Z, i, kwargs):  # Z is changed
	"""
	choose a nbr from the rest N-1 agents to update
	:param nbrs:
	:param kwargs:
	:return:
	"""
	N = kwargs["N"]
	nbr = i
	while nbr == i:
		nbr = random.randint(0, N-1)

	update_disagreement_weightedEdges(Z, i, nbr, **kwargs)

def update_disagreement_weightedEdges(Z, i, j, **kwargs):
	'''
	update one pair of nodes (i, j)
	'''

	if kwargs['shock'] > 0 and kwargs['shock_start']==True:  # the first dimension is a exo-shock
		x = np.array(Z[i, 1:-1]) - np.array(Z[j, 1:-1])
		x = np.linalg.norm(x, ord=2)   # euclidean
		x = x / math.sqrt(4*(Z.shape[1]-2))   # normalize euclidean distance to the unit
		x1 = abs(Z[i, 0] - Z[j, 0]) / 2   # the normalized euclidean distance on the shock dimension
		y = abs(Z[i, -1] - Z[j, -1]) / 2  # the normalized euclidean distance on the party dimension
		# the weighted distance including the shock issue and others
		norm = kwargs['shock'] * x1 + (1-kwargs['shock']) * ((1-kwargs['party_w']) * x + kwargs['party_w'] * y)

	else:
		x = np.array(Z[i, :-1]) - np.array(Z[j, :-1]) # x as the direction
		x = np.linalg.norm(x, ord=2)
		x = x / math.sqrt(4*(Z.shape[1]-1))
		y = abs(Z[i, -1] - Z[j, -1]) / 2
		# the weighted distance including all issues and the party dimension
		norm = (1-kwargs['party_w']) * x + kwargs['party_w'] * y

	w = norm - kwargs['C']

	def log_sample(w):
		return 1/(1+np.e**(w*kwargs['log_s']))
	#
	# stochastic alpha
	#
	coin = random.random()   # utilize the PDF for getting positive/negative influence from nbr
	r = log_sample(w)
	if coin < r:  # rejection sampling; positive influence
		dis = random.random()
		Z[i, :-1] = Z[i, :-1] + (Z[j, :-1]-Z[i, :-1])*(1-norm)*dis
	elif coin >= r:     # negative influence
		for d in range(Z.shape[1]-1):  # for every dyn dimension
			if Z[j, d] > Z[i, d]:
				Z[i, d] = Z[i, d] - random.random() * norm * (Z[i, d]-(-1))
			elif Z[j, d] < Z[i, d]:
				Z[i, d] = Z[i, d] + random.random() * norm * (1-Z[i, d])
			else:
				if Z[j, d] > 0:
					# move randomly lower
					Z[i, d] = Z[i, d] - random.random()
				elif Z[j, d] < 0:
					# move randomly higher
					Z[i, d] = Z[i, d] + random.random()
				else:
					# move randomly randomly
					dr = random.random() > 0
					if dr:
						Z[i, d] = Z[i, d] + random.random()
					else:
						Z[i, d] = Z[i, d] - random.random()

