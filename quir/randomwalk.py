from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import Context,RequestContext
import json
from quir.models import Venue, Talk, List, Speaker
from django.core.context_processors import csrf
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import View
import unicodedata
from operator import itemgetter
import random
import collections





def rw(node):
	fails = []
	try:
		if type(node).__name__=='List':
			edges, edge_weights = rw_list(node)
		elif type(node).__name__=='Speaker':
			edges, edge_weights = rw_speaker(node)
		elif type(node).__name__=='Venue':
			edges, edge_weights = rw_venue(node)
		else:
			edges, edge_weights = rw_talk(node)

		for edge in edges:
			if(edge['type']=='V-S' or edge['type']=='S-V'):
				edge['p'] = 1.0/edge_weights[edge['from']]
			elif(edge['type']=='V-L' or edge['type']=='L-V'):
				edge['p'] = 3.0/edge_weights[edge['from']]
			elif(edge['type']=='V-T' or edge['type']=='T-V'):
				edge['p'] = 5.0/edge_weights[edge['from']]
			elif(edge['type']=='S-L' or edge['type']=='L-S'):
				edge['p'] = 2.0/edge_weights[edge['from']]
			elif(edge['type']=='S-T' or edge['type']=='T-S'):
				edge['p'] = 5.0/edge_weights[edge['from']]
			elif(edge['type']=='L-T' or edge['type']=='T-L'):
				edge['p'] = 5.0/edge_weights[edge['from']]
			else:
				pass

		for i in xrange(1, len(edges)):
			edges[i]['p'] = edges[i]['p'] + edges[i-1]['p']

		traj=[]
		halt = random.uniform(0,1)
		if(halt<=0.4):
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
	except TypeError:
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
		if Speaker.objects.filter(title = talk.talker):
			speaker = Speaker.objects.filter(title = talk.talker)
			e = {}
			e['id'] = speaker[0].id
			e['label'] = speaker[0].title
			e['group'] = 'diamonds'
			if not any (e['to']==speaker[0].id for e in edges):
				edges.append({'from':node.id, 'to':speaker[0].id, 'type':'V-S'})
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
	lists = node.listos.all()
	if v:
		d={}
		d['id']=v.id
		d['label']=v.title
		d['group']='icons'
		if not any (e['to']==v.id for e in edges):
			edges.append({'from':node.id, 'to':v.id, 'type':'T-V'})
			weight+=5
	if Speaker.objects.filter(title=node.talker):
		s = Speaker.objects.filter(title=node.talker)[0]
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
	speakers = [Speaker.objects.filter(title=t.talker)[0] for t in talks if Speaker.objects.filter(title = t.talker)]
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
	talks = Talk.objects.filter(talker=node.title)
	for talk in talks:
		d={}
		d['id'] = talk.id
		d['label'] = talk.title
		d['group'] = 'dotsWithLabel'
		if not any (e['to']==talk.id for e in edges):
			edges.append({'from':node.id, 'to':talk.id, 'type':'S-T'})
			weight+=5
		venue = talk.venue
		if venue:
			e = {}
			e['id'] = venue.id
			e['label'] = venue.title
			e['group'] = 'icons'
			if not any (e['to']==venue.id for e in edges):
				edges.append({'from':node.id, 'to':venue.id, 'type':'S-V'})
				weight+=1
		lists = [List.objects.filter(title=y)[0] for y in json.loads(talk.lists) if List.objects.filter(title=y)]
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
