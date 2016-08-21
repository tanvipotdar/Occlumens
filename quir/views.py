from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import Context,RequestContext
from sklearn.feature_extraction.text import TfidfVectorizer
from quir.models import Venue, Talk, List, Speaker, Session
from django.core.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth import authenticate, login
from django.views.generic import View
from django.contrib.auth.decorators import login_required
from sklearn.feature_extraction import text
from collections import Counter
from operator import itemgetter
import operator
import unicodedata
import random
import collections
import re
import itertools
import json
import ast
import logging
logger = logging.getLogger(__name__)
 

@login_required(login_url='/login/')
def search_screen(request):
	logger.info("Opened the search page")
	return render(request, 'quir/search_screen.html', {})

def load_data(request):
	results = []
	if 'term' in request.GET:
		t = str(request.GET['term'])
		print type(t)
		print t.split(' ')[0]
		d = t.split(' ')
		print d
		# d is a list of terms in the query
		counts = []
		titles = []
		tcount = Talk.objects.all()
		lcount = List.objects.all()
		vcount = Venue.objects.all()
		scount = Speaker.objects.all()
		for x in tcount:
			print 'k'
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
		
		resdict = {}
		for t in titles:
			print 'hi'
			rank=1
			for x in d:
				p = 0.6*(1/len(d)) + 0.4*cfdict[x]
				rank=rank*p
			resdict[t]=rank
			if len(resdict)>15:
				break
		print resdict
		'''
		venues=[]
		lists=[]
		speakers=[]
		talks=[]
		for x in d:
			print 'a'
			venues += list(Venue.objects.filter(title__icontains=x))
			
			speakers += list(Speaker.objects.filter(title__icontains=x))
			lists += list(List.objects.filter(title__icontains=x))
		print venues
		print 'hello'
		'''
		#talks = talks + list(Talk.objects.filter(title__icontains=x))
		venues = Venue.objects.filter(title__icontains=request.GET['term'])
		lists = List.objects.filter(title__icontains=request.GET['term'])
		speakers = Speaker.objects.filter(title__icontains=request.GET['term'])
		talks = Talk.objects.filter(title__icontains=request.GET['term'])
		for venue in venues:
			d={}
			d['label'] = venue.title
			d['category'] = 'Venue'
			results.append(d)
		for list1 in lists:
			d={}
			d['label'] = list1.title
			d['category'] = 'Lists'
			results.append(d)
		for speaker in speakers:
			d={}
			d['label'] = speaker.title
			d['category'] = 'Speaker'
			results.append(d)
		for talk in talks:
			d={}
			d['label'] = talk.title
			d['category'] = 'Talk'
			results.append(d)

		return HttpResponse(json.dumps(results))
	return HttpResponse()

def create_network(request):
	c={}
	c.update(csrf(request))
	r=[]
	request.session.set_expiry(0)
	#request.session.flush()
	if request.method == "POST":
		if 'query' in request.POST:
			query = request.POST['query']
			print query
			l = request.POST['resp']
			request.session["query"] = query
			request.session["resp"] = l
	print request.session.keys()
	q = request.session.get("query")
	print q
	responses = eval((request.session["resp"]))

	if Venue.objects.filter(title=q):
		ide = Venue.objects.filter(title=q)[0].id
		group = 'icons'
	elif Speaker.objects.filter(title=q):
		ide = Speaker.objects.filter(title=q)[0].id
		group = 'diamonds'
	elif List.objects.filter(title=q):
		ide = List.objects.filter(title=q)[0].id
		group = 'mints'
	elif Talk.objects.filter(title=q):
		ide = Talk.objects.filter(title=q)[0].id
		group = 'dotsWithLabel'
	else:
		ide = 1
		group=''
	r.append({'id':ide, 'label':q, 'source':'source','group':group})

	n = len(responses) if len(responses)<15 else 15
	rex = random.sample(responses, n) if responses[0]['label']!='Output goes here:<br><ul></ul>' else responses[:15]

	for i in range(len(rex)):
		d={}
		name = rex[i]['label']

		if name:
			if Venue.objects.filter(title=name):
				venue = Venue.objects.filter(title=name)
				d['id'] = venue[0].id
				d['label'] = venue[0].title
				d['group'] = 'icons'
				r.append(d)
			elif Speaker.objects.filter(title=name):
				speaker = Speaker.objects.filter(title=name)
				d['id'] = speaker[0].id
				d['label'] = speaker[0].title
				d['group'] = 'diamonds'
				r.append(d)
			elif List.objects.filter(title=name):
				lis = List.objects.filter(title=name)
				d['id'] = lis[0].id
				d['label'] = lis[0].title
				d['group'] = 'mints'	
				r.append(d)
			elif Talk.objects.filter(title=name):
				talk = Talk.objects.filter(title=name)
				d['id'] = talk[0].id
				d['label'] = talk[0].title
				d['group'] = 'dotsWithLabel'	
				r.append(d)	

	r_new = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in r)]

	data = json.dumps(r_new)

	edges=[]
	for i in range(len(r_new)):
		edges.append({'from':1, 'to':r_new[i]['id']})
	
	#edges.remove({'to':1,'from':1})
	data_e = json.dumps(edges)


	con = RequestContext(request, {"nodes":data, "edges":data_e})
	response  = render_to_response('quir/network.html', c, con)
	logger.info("Created network with query "+q)
	return response

def node_click(request):
	c={}
	c.update(csrf(request))
	if 'iden' in request.GET:
		i = request.GET['iden']
		#color = request.GET['color']
		group = request.GET['group']
		print i
		#print color
		print group
		fin_edges=[]
		r=[]
		if group=="icons" or group=="iconsr" or group=="iconso" or group=="iconsg":
			v = Venue.objects.get(id=i)
		elif group=="diamonds" or group=="diamondsr" or group=="diamondsg" or group=="diamondso":
			v = Speaker.objects.get(id=i)
		elif group=="mints" or group=="mintsr" or group=="mintso" or group=="mintsg":
			v = List.objects.get(id=i)
		else:
			v = Talk.objects.get(id=i)

		cache = json.loads(v.cache)
		#c = [x['to'] for x in json.loads(v.edges)]
		#n = len(c) if len(c)<9 else 9
		#cache = random.sample(c,n) 
		for y in cache:
			d={}
			#if str(color)=="red" or str(color)=='orange' or str(color)=='rgb(0,204,51)':
				#print 'TRUE'
				#d['color'] = color

			if Speaker.objects.filter(id=y):
				node = Speaker.objects.get(id=y)
				#c = group[-1]
				d['group'] = "diamonds"

			elif List.objects.filter(id=y):
				node = List.objects.get(id=y)
				#c = group[-1]
				d['group'] = "mints"

			elif Venue.objects.filter(id=y):
				node = Venue.objects.get(id=y)
				#c = group[-1]
				#d['group'] = 'icons'+c if c=='r' or c=='o' or c=='g' else "icons"
				d['group'] = 'icons'
			else:
				node = Talk.objects.get(id=y)
				#c = group[-1]
				d['group'] = 'dotsWithLabel'
			print node
			d['label'] = node.title
			d['id'] = node.id
			fin_edges.append({'from':i, 'to':node.id})
			r.append(d)
		node_new = json.dumps(r)
		edge_new = json.dumps(fin_edges)
		print node_new, edge_new
		#return node_new, edge_new
		return HttpResponse(json.dumps({"node_new":node_new, "edge_new": edge_new}))
	else:
		logger.error("Expand didnt work")
		return HttpResponse()



def information(request):
	logger.info("Got information")
	r=[]
	if 'nid' in request.GET:
		print request.GET['nid']
		#print request.GET['g']
		if 'g' in request.GET:
			if request.GET['g'][:5]=="icons" and Venue.objects.filter(id=request.GET['nid']):
				d={}
				d['past'] = Venue.objects.get(id=request.GET['nid']).past
				d['upcoming'] = Venue.objects.get(id=request.GET['nid']).upcoming
				r.append(d)
			elif request.GET['g'][:13]=="dotsWithLabel" and Talk.objects.filter(id=request.GET['nid']):
				d={}
				d['venue'] = Talk.objects.get(id=request.GET['nid']).venue.title if Talk.objects.get(id=request.GET['nid']).venue else None 
				d['speaker'] = Talk.objects.get(id=request.GET['nid']).talker
				d['date'] = str(Talk.objects.get(id=request.GET['nid']).date)
				d['abstract'] = Talk.objects.get(id=request.GET['nid']).abstract[:3000]
				r.append(d)
			elif request.GET['g'][:8]=="diamonds" and Speaker.objects.filter(id=request.GET['nid']):
				d={}
				d['no_of_talks'] = Speaker.objects.get(id=request.GET['nid']).no_of_talks
				r.append(d)
			elif request.GET['g'][:5]=="mints" and List.objects.filter(id=request.GET['nid']):
				d={}
				d['past'] = List.objects.get(id=request.GET['nid']).past
				d['upcoming'] = List.objects.get(id=request.GET['nid']).upcoming
				r.append(d)
			else:
				pass
		return HttpResponse(json.dumps(r))

	return HttpResponse()


def findWholeWord(w):
	if w:
		w = w.strip('(')
		w = w.strip(')')
		w = w.strip('.')
		return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search

 
def get_recs(request):
	print request.session.keys()
	'''
	add_stopwords = ['The', 'of', 'for', 'from', 'at', 'and', 'over', 'in', 'i','School','lists', 'talks', '(aka','All', 'list)','(Computer', 'Computer', 'Laboratory)', 'Laboratory','speaker', 'venue','to', 'be','beyond', 'a', 'A','on','with','an', 'its', "An"
	, "How", "needed", "understanding", "between", "list", "Featured", "open", "Open", "meeting", 'Meeting', "meetings"]
	stop_words = text.ENGLISH_STOP_WORDS.union(add_stopwords)
	corpus_talk = [x.title for x in Talk.objects.all()]
	corpus_list = [y.title for y in List.objects.all()]

	vectorizer = TfidfVectorizer(min_df=1,stop_words=stop_words,  lowercase=False)
	vectorizer.fit_transform(corpus_talk)
	tidf = vectorizer._tfidf.idf_
	talk_tfidf = dict(zip(vectorizer.get_feature_names(), tidf))

	vectorizer.fit_transform(corpus_list)
	lidf = vectorizer._tfidf.idf_
	list_tfidf = dict(zip(vectorizer.get_feature_names(), lidf))
	'''

	if 'rid' in request.GET:
		rid = request.GET['rid']
		rcolor = request.GET['rcolor']
		rlist = json.loads(request.GET['rlist'])
		print rlist
		rlist = [x.encode('ascii','ignore') for x in rlist]


		rnodes=[]
		redges=[]
		rec_list=[]
		for x in rlist:
			print x
			t = Talk.objects.filter(title=x)[0] if Talk.objects.filter(title=x) else None
			print t
			if t:
				print t.rec
				y = [ item.encode('ascii','ignore') for item in eval(t.rec) ]
				print y
				for item in y:
					print item
					if item!=x:
						d = Talk.objects.filter(title=item)[0] if Talk.objects.filter(title=item) else None
						print d
						if d:
							rec_list.append(item)
							print rec_list
							rnodes.append({'label':d.title, 'group':'dotsWithLabel','id':d.id})
							print rnodes
		print rnodes

		nodes = random.sample(rnodes,5) if len(rnodes)>5 else rnodes
		recnodes = json.dumps(nodes)
		for item in nodes:
			redges.append({'to':item['id'], 'from':rid, 'dashes':'true', 'color':rcolor, 'width':'10'})
		recedges = json.dumps(redges)
		print recedges
		
		return HttpResponse(json.dumps({"recnodes":recnodes, "recedges": recedges}))
	else:
		print 'wtf'

def saveToDB(request):
	print 'HI'
	if 'date' and 'nodes' and 'edges' in request.POST:
		print 'IN'
		d = request.POST['date']
		print request.POST['nodes']
		n = request.POST['nodes']
		e = request.POST['edges']
		print d
		print n
		print e
		s = Session(name=d, nodes=n, edges=e)
		print s
		s.save()
		return HttpResponse()

def retreive_session(request):
	if 'date' in request.GET:
		print 'df'
		d = request.GET['date']
		print d
		s = Session.objects.get(name=d)
		nodes = s.nodes
		edges = s.edges
		print nodes
		return HttpResponse(json.dumps({"n":nodes, "e": edges}))
	else:
		return HttpResponse()











	
	










