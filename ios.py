import requests
import plistlib

ioses={}

r=requests.get('https://s.mzstatic.com/version')
p=plistlib.readPlistFromString(r.content)
for i in p:
	if i =='MobileDeviceSoftwareVersionsByVersion':
		versions=p[i]
		for v in versions:
			for z in versions[v]:
				if z =='MobileDeviceSoftwareVersions':
					for t in versions[v][z]:
						for mv in versions[v][z][t]:
							if 'SameAs' in versions[v][z][t][mv] or 'Universal' in versions[v][z][t][mv] or 'Restore' not in versions[v][z][t][mv]:
								continue
							if t in ioses:
								if versions[v][z][t][mv]['Restore']['ProductVersion'] not in ioses[t]:
									ioses[t].append(versions[v][z][t][mv]['Restore']['ProductVersion'])
							else:
								ioses[t]=[]
								ioses[t].append(versions[v][z][t][mv]['Restore']['ProductVersion'])
							#print versions[v][z][t][mv]['Restore']['ProductVersion'],t
def ml(l):
	tmp=[]
	tt=[]
	for idx, i in enumerate(l):
		j=i.replace('.','')
		if i.split('.')[0]=='9':
			j=j+'0'*(4-len(i))
		elif i.split('.')[0]=='10':
			j=j+'0'*(5-len(i))
		elif i.split('.')[0]=='5':
			j=j+'0'*(4-len(i))
		i=int(j)
		tmp.append((i,l[idx]))
	for x in sorted(tmp,key=lambda x: x[0]):
		tt.append(x[1])
	return tt
tmp=[]							
for de in ioses:
	_t=ml([x for x in ioses[de]])
	tmp.append('Device:%s Versions:%s'%(de,'->'.join(_t)))
print '\n'.join(sorted(tmp))
