# Author: Izaak Neutelings (May 2020)
import re


def convertstr(string):
  """Convert a string to a boolean, float or int if possible."""
  if isinstance(string,str):
    if string.isdigit():
      string = int(string)
    elif string=='True':
      string = True
    elif string=='False':
      string = False
    elif string.count('.')==1 and re.match(r"^[-+]?[\d.]+\d*$",string):
      string = float(string)
  return string
  

def quotestrs(strings):
  """Make summation of quoted strings."""
  return ", ".join(repr(s) for s in strings if s)
  

def isglob(string):
  """Return if string is likely a glob pattern."""
  return '*' in string or '?' in string or ('[' in string and ']' in string)
  

def repkey(string,**kwargs):
  """Replace keys with '$'."""
  for key, value in sorted(kwargs.items(),key=lambda x: -len(x[0])):
    if '${'+key in string: # BASH variable expansions
      matches = re.findall(r"\$\{%s:(\d*):(\d+)\}"%(key),string)
      for a, b in matches:
        substr = value[int(a or 0):int(b)]
        string = re.sub(r"\$\{%s:%s:%s\}"%(key,a,b),substr,string)
    string = string.replace('$'+key,str(value))
  return string
  

def rreplace(string,old,new='',count=-1):
  """Replace occurrences substring from right to left."""
  parts = string.rsplit(old,count)
  return new.join(parts)
  

def lreplace(string,old,new='',count=-1):
  """Replace occurrences substring from left to right."""
  parts = string.split(old,count)
  return new.join(parts)
  

def alphanum_key(string):
  """Turn a string into a list of string and number chunks,
  e.g. "z23a" -> ["z", 23, "a"]
  Useful for sorting a list of strings containing numbers 'naturally'/'alphanumerically',
  e.g. sorted(['z10','z1','z2','z20'],key=alphanum_key)"""
  # https://nedbatchelder.com/blog/200712/human_sorting.html
  return [ tryint(x) for x in re.split("([0-9]+)",string) ]
  

def getyear(string):
  """Recognize year from era string."""
  year = string
  if isinstance(string,str):
    # match either 2 digits ('18','22'), or 4 digits starting with '20' ('2018')
    matches = re.findall(r"(?<!\d)(?:20)?[0-4]\d(?!\d)",string)
    if matches:
      matches.sort(key=lambda x: len(x),reverse=True)
      year = int(matches[0])
      if year<100: # e.g. to map 18->2018, 22->2022, etc.
        year += 2000
  return year
  

def tryint(x):
  """Convert to integer, if it is possible."""
  try:
    return int(x)
  except ValueError:
    return x
  

def took(wall,cpu=None,pre=""):
  """Convert time to minutes/seconds."""
  import time
  time_wall = time.time() - wall # wall clock time via wall=time.time()
  time_cpu  = (time.process_time() - cpu) if cpu!=None else None # CPU time via cpu=time.process_time()
  if time_wall>60:
    string = pre+"%d min %.1f sec"%divmod(time_wall,60)
  else:
    string = pre+"%.1f sec"%time_wall
  if cpu!=None:
    if time_cpu>60:
      string += " (CPU: %d min %.1f sec)"%divmod(time_cpu,60)
    else:
      string += " (CPU: %.1f sec)"%time_cpu
  return string
  
