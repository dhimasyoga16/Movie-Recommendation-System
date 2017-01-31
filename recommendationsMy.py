from math import sqrt

critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
'The Night Listener': 3.0},
'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 3.5},
'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
'Superman Returns': 3.5, 'The Night Listener': 4.0},
'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
'The Night Listener': 4.5, 'Superman Returns': 4.0,
'You, Me and Dupree': 2.5},
'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
'You, Me and Dupree': 2.0},
'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

# Returns a distance-based similarity score for person1 and person2
def sim_dist(data,p1,p2):
	# Get the list of shared_items
	shared=[] 
	for movie in data[p1]:
		if movie in data[p2]:
			shared[movie]=1
	# if they have no ratings in common, return 0
	if len(shared)==0:
		return 0
	# Add up the squares of all the differences
	ssd=sum([pow((data[p1][movie]-data[p2][movie]),2) for movie in shared])
	return 1/(1+ssd)
	
# Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(data,p1,p2):
	# Get the list of mutually rated items
	shared=[]
	for movie in data[p1]:
		if movie in data[p2]:
			shared[movie]=1
	# Find the number of elements
	n=len(shared)
	# if they are no ratings in common, return 0
	if n==0: return 0
	# Add up all the preferences
	sigmaX=sum([data[p1][movie] for movie in shared])
	sigmaY=sum([data[p2][movie] for movie in shared])
	# Sum up the squares
	sigmaX2=sum(pow([data[p1][movie],2) for movie in shared])
	sigmaY2=sum(pow([data[p2][movie],2) for movie in shared])
	# Sum up the products
	sigmaXY=sum([data[p1][movie]*[data[p2][movie] for movie in shared])
	# Calculate Pearson score
	num=sigmaXY-sigmaX*sigmaY/n
	den=sqrt((sigmaX2-pow(sigmaX,2)/n)*(sigmaY2-pow(sigmaY,2)/n))
	if den==0: return 0
	return num/den
	
# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.
def topMatches(data,p,n=5,sim=pearson):
	scores=[(sim(data,p,per),per) for per in data if per!=p]
	# Sort the list so the highest scores appear at the top
	scores.sort()
	scores.reverse()
	if n>len(scores): 
		n=len(scores)
	return scores[0:n]
	
# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(data,p,sim=sim_pearson):
	# don't compare me to myself
	totals={}
	simSums={}
	for per in data:
		if per==p: continue
		similarity=sim(data,p,per)
		# ignore scores of zero or lower
		if similarity<0:continue
		for movie in data[per]:
			# only score movies I haven't seen yet
			if movie not in data[per] or len(data[per])==0:
				# Similarity * Score
				totals.setdefault(movie,0)
				totals+=data[per][movie]*similarity
				# Sum of similarities
				simSums.setdefault
				simSums+=similarity
				# Create the normalized list
				# Return the sorted list
	# Create the normalized list
	rankings=[(total/simSums[item],item) for item,total in totals.items( )]
	# Return the sorted list
	rankings.sort( )
	rankings.reverse( )
	return rankings			