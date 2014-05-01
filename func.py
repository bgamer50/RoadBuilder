def shash(n):
	return hash(str(n))
def cleanZones(g):
    k = 0
    while k < len(g.zones):
      if len(g.zones[k]) == 0:
		try:
			g.zones.pop(k)
		except:
			pass
      k += 1
			  
class fakeObject:
	list = []
