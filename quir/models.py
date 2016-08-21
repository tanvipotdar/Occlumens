
from sklearn.feature_extraction import text
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import Counter
from django.db import models
import numpy as np
import json
import random
import collections


def query_models():
	counts = []
	titles = []
	tcount = Talk.objects.all()
	lcount = List.objects.all()
	vcount = Venue.objects.all()
	scount = Speaker.objects.all()
	print 'k'
	for x in tcount:
		counts = counts + x.title.split(' ')
		titles.append((x.title).encode('ascii','ignore'))
	for x in lcount:
		counts = counts + x.title.split(' ')
		titles.append((x.title).encode('ascii','ignore'))
	for x in vcount:
		counts = counts + x.title.split(' ')
		titles.append((x.title).encode('ascii','ignore'))
	for x in scount:
		counts = counts + x.title.split(' ')
		titles.append((x.title).encode('ascii','ignore'))
	cfdict = Counter(counts)
	print 'd'
	q = np.zeros((60870,len(cfdict)))
	documents = titles
	print 'h'
	for x in range(len(documents)):
		for y in range(len(cfdict)):
				if cfdict.keys()[y] in documents[x].split(' '):
					q[x][y] = 0.6*(1/len(documents[x])) + 0.4*cfdict.values()[y]
				else:
					q[x][y] = 0.4*cfdict.values()[y]
	print 'e'
	return q

def tfidf_talk():
	add_stopwords = ['The', 'of', 'for', 'from', 'at', 'and', 'over', 'in', 'i','School','lists', 'talks', '(aka','All', 'list)','(Computer', 'Computer', 'Laboratory)', 'Laboratory','speaker', 'venue','to', 'be','beyond', 'a', 'A','on','with','an', 'its', "An"
	, "How", "needed", "understanding", "between", "list", "Featured", "open", "Open", "meeting", 'Meeting', "meetings"]
	stop_words = text.ENGLISH_STOP_WORDS.union(add_stopwords)
	talks = Talk.objects.all()
	corpus_talk = [x.title for x in talks]
	

	vectorizer = TfidfVectorizer(min_df=1,stop_words=stop_words,  lowercase=False)
	a = vectorizer.fit_transform(corpus_talk)
	#tidf = vectorizer._tfidf.idf_
	#talk_tfidf = dict(zip(vectorizer.get_feature_names(), tidf))
	#return t_mat, corpus_talk
	for t in talks:
		try:
			print t.id
			x = cosine_similarity(a[t.id-1], a)[0]
			arr = np.nonzero(x)[0]
			rel=[]

			for y in np.nditer(arr, op_flags=['readwrite']):
				if x[y]>0.2:
					rel.append(corpus_talk[y])
			t.rec=rel
			t.save()
		except:
			pass

def tfidf_list():
	add_stopwords = ['The', 'of', 'for', 'from', 'at', 'and', 'over', 'in', 'i','School','lists', 'talks', '(aka','All', 'list)','(Computer', 'Computer', 'Laboratory)', 'Laboratory','speaker', 'venue','to', 'be','beyond', 'a', 'A','on','with','an', 'its', "An"
	, "How", "needed", "understanding", "between", "list", "Featured", "open", "Open", "meeting", 'Meeting', "meetings"]
	stop_words = text.ENGLISH_STOP_WORDS.union(add_stopwords)
	lists = List.objects.all()
	corpus_list = [y.title for y in lists]

	a = vectorizer.fit_transform(corpus_list)
	#lidf = vectorizer._tfidf.idf_
	#list_tfidf = dict(zip(vectorizer.get_feature_names(), lidf))
	for t in lists:
		try:
			print t.id
			x = cosine_similarity(a[t.id-1], a)[0]
			arr = np.nonzero(x)[0]
			rel=[]

			for y in np.nditer(arr, op_flags=['readwrite']):
				if x[y]>0.2:
					rel.append(corpus_list[y])
			t.rec=rel
			t.save()
		except:
			pass

def rw(node):
	fails = []
	try:
		edges = json.loads(node.edges)
		traj=[]
		halt = random.uniform(0,1)
		if edges:
			if(halt<=0.6):
				randnum = random.uniform(0,1)
				for e in edges:
					if randnum<=e['p']:
						#print e['to']
						traj.append(e['to'])
						if List.objects.filter(id=e['to']):
							next =  List.objects.get(id=e['to'])
						elif Speaker.objects.filter(id=e['to']):
							next =  Speaker.objects.get(id=e['to'])
						elif Venue.objects.filter(id=e['to']):
							next =  Venue.objects.get(id=e['to'])
						else:
							next = Talk.objects.get(id=e['to'])
						break
				traj = traj+ rw(next)
		return traj
	except TypeError, UnboundLocalError:
		fails.append(node)

def rw_venue(node):
	edges=[]
	edge_weights={}
	weight=0
	talks = node.talk_set.all()
	for talk in talks:
		d={}
		d['id'] = talk.id
		d['label'] = talk.title
		d['group'] = 'dotsWithLabel'
		if not any (e['to']==talk.id for e in edges):
			edges.append({'from':node.id, 'to':talk.id, 'type':'V-T'})
			weight+=5
	speakers = node.speakers.all()
	for s in speakers:
		e = {}
		e['id'] = s.id
		e['label'] = s.title
		e['group'] = 'diamonds'
		if not any (e['to']==s.id for e in edges):
			edges.append({'from':node.id, 'to':s.id, 'type':'V-S'})
			weight+=1
	lists = node.lists.all()
	for l in lists:
		f={}
		f['id'] = l.id
		f['label'] = l.title
		f['group'] = 'mints'
		if not any (e['to']==l.id for e in edges):
			edges.append({'from':node.id, 'to':l.id, 'type':'V-L'})
			weight+=3
	edge_weights[node.id]=weight
	return edges, edge_weights

def rw_talk(node):
	edges=[]
	edge_weights={}
	weight=0
	v = node.venue
	s = node.speaker
	lists = node.listos.all()
	if v:
		d={}
		d['id']=v.id
		d['label']=v.title
		d['group']='icons'
		if not any (e['to']==v.id for e in edges):
			edges.append({'from':node.id, 'to':v.id, 'type':'T-V'})
			weight+=5
	if s:
		e={}
		e['id']=s.id
		e['label']=s.title
		e['group']='diamonds'
		if not any (e['to']==s.id for e in edges):
			edges.append({'from':node.id, 'to':s.id,'type':'T-S'})
			weight+=5
	if lists:
		for l in lists:
			a = {}
			a['id'] = l.id
			a['label'] = l.title
			a['group'] = 'mints'
			if not any (e['to']==l.id for e in edges):
				edges.append({'from':node.id, 'to':l.id,'type':'T-L'})
				weight+=5
	edge_weights[node.id]=weight
	return edges, edge_weights

def rw_list(l):
	edges=[]
	edge_weights={}
	weight=0
	talks = l.talk_set.all()
	venues = l.venue_set.all()
	speakers = l.speaker_set.all()
	if talks:
		for talk in talks:
			d={}
			d['id'] = talk.id
			d['label'] = talk.title
			d['group'] = 'dotsWithLabel'
			if not any (e['to']==talk.id for e in edges):
				edges.append({'from':l.id, 'to':talk.id, 'type':'L-T'})
				weight+=5
	for venue in venues:
		e = {}
		e['id'] = venue.id
		e['label'] = venue.title
		e['group'] = 'icons'
		if not any (e['to']==venue.id for e in edges):
			edges.append({'from':l.id, 'to':venue.id, 'type':'L-V'})
			weight+=3
	for speaker in speakers:
		f = {}
		f['id'] = speaker.id
		f['label'] = speaker.title
		f['group'] = 'diamonds'
		if not any (e['to']==speaker.id for e in edges):
			edges.append({'from':l.id, 'to':speaker.id,'type':'L-S'})
			weight+=2
	edge_weights[l.id]=weight
	return edges, edge_weights

def rw_speaker(node):
	edges=[]
	edge_weights={}
	weight=0
	talks = node.talk_set.all()
	venues = node.venue_set.all()
	lists = node.lists.all()

	for talk in talks:
		d={}
		d['id'] = talk.id
		d['label'] = talk.title
		d['group'] = 'dotsWithLabel'
		if not any (e['to']==talk.id for e in edges):
			edges.append({'from':node.id, 'to':talk.id, 'type':'S-T'})
			weight+=5
	for venue in venues:
		e = {}
		e['id'] = venue.id
		e['label'] = venue.title
		e['group'] = 'icons'
		if not any (e['to']==venue.id for e in edges):
			edges.append({'from':node.id, 'to':venue.id, 'type':'S-V'})
			weight+=1
	for l in lists:
		f={}
		f['id'] = l.id
		f['label'] = l.title
		f['group'] = 'mints'
		if not any (e['to']==l.id for e in edges):
			edges.append({'from':node.id, 'to':l.id, 'type':'S-L'})
			weight+=2
	edge_weights[node.id]=weight
	return edges, edge_weights


class List(models.Model):
	title = models.CharField(max_length=200)
	upcoming = models.CharField(max_length=50)
	past = models.CharField(max_length=50)
	talks = models.CharField(max_length=400)
	cache = models.CharField(max_length=500)
	edges = models.CharField(max_length=500)
	rec = models.CharField(max_length=1000, blank=True)

	def populate_cache(self):
		fins = []
		for j in range(0, 500):
			traj = rw(self)
			if traj:
				fins.append(traj[len(traj)-1])
		counter = collections.Counter(fins).most_common(5)
		print counter
		top_5 = [x[0] for x in counter]
		self.cache = top_5
		print self.cache
		self.save()

	def populate_edges(self):
		edges=json.loads(self.edges)
		weight=0

		talks = self.talk_set.all()
		venues = self.venue_set.all()
		speakers = self.speaker_set.all()
		if talks:
			for talk in talks:
				d={}
				d['id'] = talk.id
				d['label'] = talk.title
				d['group'] = 'dotsWithLabel'
				edges.append({'from':self.id, 'to':talk.id, 'type':'L-T'})
				weight+=5
		for venue in venues:
			e = {}
			e['id'] = venue.id
			e['label'] = venue.title
			e['group'] = 'icons'
			edges.append({'from':self.id, 'to':venue.id, 'type':'L-V'})
			weight+=3
		for speaker in speakers:
			f = {}
			f['id'] = speaker.id
			f['label'] = speaker.title
			f['group'] = 'diamonds'
			edges.append({'from':self.id, 'to':speaker.id,'type':'L-S'})
			weight+=2
		self.edge_weight=weight
		self.save()

		for edge in edges:
			if(edge['type']=='L-V'):
				edge['p'] = 3.0/self.edge_weight
			elif(edge['type']=='L-S'):
				edge['p'] = 2.0/self.edge_weight
			elif(edge['type']=='L-T'):
				edge['p'] = 5.0/self.edge_weight
			else:
				pass

		for i in xrange(1, len(edges)):
			edges[i]['p'] = edges[i]['p'] + edges[i-1]['p']
		self.edges = json.dumps(edges)
		self.save()


class Speaker(models.Model):
	title = models.CharField(max_length=200)
	no_of_talks = models.CharField(max_length=50)
	lists = models.ManyToManyField(List)
	cache = models.CharField(max_length=500)
	edges = models.CharField(max_length=500)

	def populate_list(self):
		talks = self.talk_set.all()
		for talk in talks:
			l = talk.listos.all()
			for x in l:
				self.lists.add(x)
				self.save()

	def populate_cache(self):
		fins = []
		for j in range(0, 500):
			traj = rw(self)
			if traj:
				fins.append(traj[len(traj)-1])
		counter = collections.Counter(fins).most_common(5)
		print counter
		top_5 = [x[0] for x in counter]
		self.cache = top_5
		print self.cache
		self.save()

	def populate_edges(self):
		edges=json.loads(self.edges)
		weight=0

		talks = self.talk_set.all()
		venues = self.venue_set.all()
		lists = self.lists.all()

		for talk in talks:
			d={}
			d['id'] = talk.id
			d['label'] = talk.title
			d['group'] = 'dotsWithLabel'
			edges.append({'from':self.id, 'to':talk.id, 'type':'S-T'})
			weight+=5
		for venue in venues:
			e = {}
			e['id'] = venue.id
			e['label'] = venue.title
			e['group'] = 'icons'
			edges.append({'from':self.id, 'to':venue.id, 'type':'S-V'})
			weight+=1
		for l in lists:
			f={}
			f['id'] = l.id
			f['label'] = l.title
			f['group'] = 'mints'
			edges.append({'from':self.id, 'to':l.id, 'type':'S-L'})
			weight+=2
		self.edge_weight=weight
		self.save()

		for edge in edges:
			if(edge['type']=='S-V'):
				edge['p'] = 1.0/self.edge_weight
			elif(edge['type']=='S-L'):
				edge['p'] = 2.0/self.edge_weight
			elif(edge['type']=='S-T'):
				edge['p'] = 5.0/self.edge_weight
			else:
				pass

		for i in xrange(1, len(edges)):
			edges[i]['p'] = edges[i]['p'] + edges[i-1]['p']
		self.edges = json.dumps(edges)
		self.save()

class Venue(models.Model):
	title = models.CharField(max_length=200)
	upcoming = models.CharField(max_length=50)
	past = models.CharField(max_length=50)
	lists = models.ManyToManyField(List)
	cache = models.CharField(max_length=500)
	speakers = models.ManyToManyField(Speaker, blank = True, null = True)
	edges = models.CharField(max_length=500)

	def populate_list(self):
		talks = self.talk_set.all()
		for talk in talks:
			l = talk.listos.all()
			for x in l:
				self.lists.add(x)
				self.save()

	def populate_speaker(self):
		talks = self.talk_set.all()
		for talk in talks:
			s = talk.speaker
			if s:
				self.speakers.add(s)
				self.save()

	def populate_cache(self):
		fins = []
		for j in range(0, 500):
			traj = rw(self)
			if traj:
				fins.append(traj[len(traj)-1])
		counter = collections.Counter(fins).most_common(5)
		print counter
		top_5 = [x[0] for x in counter]
		self.cache = top_5
		print self.cache
		self.save()

	def populate_edges(self):
		edges=json.loads(self.edges)
		weight=0
		talks = self.talk_set.all()
		for talk in talks:
			print talk
			d={}
			d['id'] = talk.id
			d['label'] = talk.title
			d['group'] = 'dotsWithLabel'
			edges.append({'from':self.id, 'to':talk.id, 'type':'V-T'})
			weight+=5
			print weight

		speakers = self.speakers.all()
		for s in speakers:
			e = {}
			e['id'] = s.id
			e['label'] = s.title
			e['group'] = 'diamonds'
			edges.append({'from':self.id, 'to':s.id, 'type':'V-S'})
			weight+=1
			print weight

		lists = self.lists.all()
		for l in lists:
			f={}
			f['id'] = l.id
			f['label'] = l.title
			f['group'] = 'mints'
			edges.append({'from':self.id, 'to':l.id, 'type':'V-L'})
			weight+=3
			print weight
		print weight
		for edge in edges:
			if(edge['type']=='V-S'):
				edge['p'] = 1.0/weight
			elif(edge['type']=='V-L'):
				edge['p'] = 3.0/weight
			elif(edge['type']=='V-T' ):
				edge['p'] = 5.0/weight
			else:
				pass

		for i in xrange(1, len(edges)):
			edges[i]['p'] = edges[i]['p'] + edges[i-1]['p']
		self.edges = json.dumps(edges)
		self.save()


class Talk(models.Model):
	title = models.CharField(max_length=200)
	date = models.DateTimeField(blank=True, null=True)
	talker = models.CharField(max_length=200)
	lists = models.CharField(max_length=400)
	abstract = models.TextField()
	place = models.CharField(max_length=200)
	venue = models.ForeignKey(Venue, blank = True, null = True)
	speaker = models.ForeignKey(Speaker, blank = True, null = True)
	listos = models.ManyToManyField(List)
	cache = models.CharField(max_length=500)
	edges = models.CharField(max_length=500)
	rec = models.CharField(max_length=1000, blank=True)

	def populate_rec(self):
		a = tfidf_talk()[0]
		titles = tfidf_talk()[1]

		x = cosine_similarity(a[self.id-1], a)[0]
		arr = np.nonzero(x)[0]
		rel=[]
		for y in np.nditer(arr, op_flags=['readwrite']):
			if x[y]>0.2:
				rel.append(titles[y])
		print self.id
		self.rec=rel
		self.save()
				
	def populate_venue(self):
		if Venue.objects.filter(title = self.place):
			v = Venue.objects.filter(title = self.place)[0]
			v.save()
			self.venue = v
			self.save()

	def populate_speaker(self):
		if Speaker.objects.filter(title__icontains=self.talker[:15]):
			s = Speaker.objects.filter(title__icontains = self.talker[:15])[0]
			s.save()
			self.speaker = s
			self.save() 

	def populate_list(self):
		lists = [List.objects.filter(title=y)[0] for y in json.loads(self.lists) if List.objects.filter(title=y)]
		for l in lists:
			self.listos.add(l)
			self.save()


	def populate_cache(self):
		fins = []
		for j in range(0, 500):
			traj = rw(self)
			if traj:
				fins.append(traj[len(traj)-1])
		counter = collections.Counter(fins).most_common(5)
		print counter
		top_5 = [x[0] for x in counter]
		self.cache = top_5
		print self.cache
		self.save()

	def populate_edges(self):
		edges=json.loads(self.edges)
		weight=0

		v = self.venue
		s = self.speaker
		lists = self.listos.all()
		if v:
			d={}
			d['id']=v.id
			d['label']=v.title
			d['group']='icons'
			edges.append({'from':self.id, 'to':v.id, 'type':'T-V'})
			weight+=5
		if s:
			e={}
			e['id']=s.id
			e['label']=s.title
			e['group']='diamonds'
			edges.append({'from':self.id, 'to':s.id,'type':'T-S'})
			weight+=5
		if lists:
			for l in lists:
				a = {}
				a['id'] = l.id
				a['label'] = l.title
				a['group'] = 'mints'
				edges.append({'from':self.id, 'to':l.id,'type':'T-L'})
				n = int(l.upcoming) + int(l.past)
				if(n>10000):
					weight+=3.5
				else:
					weight+=5
		self.edge_weight=weight
		self.save()

		for edge in edges:
			edge['p'] = 5.0/self.edge_weight

		for i in xrange(1, len(edges)):
			edges[i]['p'] = edges[i]['p'] + edges[i-1]['p']
		self.edges = json.dumps(edges)
		self.save()

class Session(models.Model):
	name = models.CharField(max_length=400, default='')
	nodes = models.CharField(max_length=400)
	edges = models.CharField(max_length=400)


		




