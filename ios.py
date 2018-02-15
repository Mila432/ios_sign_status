import requests
import plistlib

ioses={}
major_ver=11

def ios_ipsw():
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

def ios_ota():
	r=requests.get('https://mesu.apple.com/assets/com_apple_MobileAsset_SoftwareUpdate/com_apple_MobileAsset_SoftwareUpdate.xml')
	p=plistlib.readPlistFromString(r.content)
	for i in p:
		if i =='Assets':
			versions=p[i]
			for v in versions:
				ver=v['OSVersion'].replace('9.9.','')
				for t in v['SupportedDevices']:
					if t in ioses:
						if ver not in ioses[t]:
							ioses[t].append(ver)
					else:
						ioses[t]=[]
						ioses[t].append(ver)

def ios_beta():
	r=requests.get('https://mesu.apple.com/assets/iOS%sDeveloperSeed/com_apple_MobileAsset_SoftwareUpdate/com_apple_MobileAsset_SoftwareUpdate.xml'%(major_ver))
	p=plistlib.readPlistFromString(r.content)
	for i in p:
		if i =='Assets':
			versions=p[i]
			for v in versions:
				ver=v['OSVersion'].replace('9.9.','')
				for t in v['SupportedDevices']:
					if t in ioses:
						if ver not in ioses[t]:
							ioses[t].append(ver)
					else:
						ioses[t]=[]
						ioses[t].append(ver)

def ml(l):
	tmp=[]
	tt=[]
	for idx, i in enumerate(l):
		j=i.replace('.','')
		if len(i)==3:
			j=j+'0'*(4-len(i))
		elif len(i)==6 and i.split('.')[0]=='4':
			j=j[:3]
		else:
			j=j+'0'*(5-len(i))
		i=int(j)
		tmp.append((i,l[idx]))
	for x in sorted(tmp,key=lambda x: x[0]):
		tt.append(x[1])
	return tt

ios_ipsw()
ios_ota()
ios_beta()

tmp=[]							
for de in ioses:
	_t=ml([x for x in ioses[de]])
	tmp.append('Device:%s Versions:%s'%(de,'->'.join(_t)))
print '\n'.join(sorted(tmp))
