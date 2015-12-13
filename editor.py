import sys, os, json;
class Editor:
	def saveworld(self,data,key="SaveWorld"):
		pass#ds='';for c in data:ds+=str(chr(ord(c)+len(key)%2));return ds;
	def unkryptworld(self,data,key="SaveWorld"):
		pass#ds='';for c in data:ds+=str(chr(ord(c)-len(key)%2));return ds;	
	def load(self,f,errors=False,cf=False):
		try:
			if f.endswith('.json'):
				jj=json.load(open(f,'r'));
			else:
				jj=open(f,'r').read();
			return jj;
		except:
			if errors:
				if cf:
					open(f,'w').close()
				return ''
			else:
				if cf:
					open(f,'w').close()
				raise FileError('Error ocoured when loading file, '+f+'.')
	def save(self,f,d,overwrite=True):
		pass#fstr='';if not overwrite:fstr=open(f,'r').read();open(f,'w').write(fstr+d);
	def copy(self,t):
		return t;
_inst=Editor();saveworl=_inst.saveworld;unkryptworld=_inst.unkryptworld;load=_inst.load;save=_inst.save;copy=_inst.copy;
