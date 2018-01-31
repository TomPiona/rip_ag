__out_of__ = 1

try:
	data = np.array(unemployment_data[:len(unemployment_data)])
    if all(total_unemployed == data[:,1]) and all(unemp_15_weeks == data[:,2]):
        __score__ += 1
except: 
  pass