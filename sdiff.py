# -*- coding: utf-8 -*-
# Semantic diff between C header files
# ------------------------------------
#
# This tool parses two sets of C header files to locate all
# declarations: variables, functions, defines, macros, and
# typedefs. It produces in output:
# - Symbols defined in one set and not the other
# - Symbols with a different definition in both sets
#
# All the parsing is done using `ctags`.
#
import os
import sys
import glob

class Symbol:
    '''
    Parse the output of:
    ctags-universal --kinds-c=+pLl --fields=Sk -f- filename.h
    and store it as named fields.
    Useful to store a list of symbols found in a file to compare it against
    another list of symbols to find diffs.
    '''
    def __init__(self, line):
        toks=[x.strip() for x in line.split('\t')]
        self.name=toks[0]
        self.file=toks[1]
        self.type=toks[3]
        self.sig=None
        if len(toks)>4:
            self.sig = toks[4][10:]
        self.found=0

    def __str__(self):
        s='[%s][%s][%s]' % (self.file, self.type, self.name)
        if self.sig:
            s+='%s' % self.sig
        return s

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.name==other.name and \
               self.type==other.type and \
               self.sig==other.sig

def tagfile(filename):
    syms=[]
    p=os.popen('ctags-universal --kinds-c=+pLl --fields=Sk -f- '+filename, 'r')
    for line in p.readlines():
        s=Symbol(line)
        syms.append(s)
    p.close()
    return syms

def tagdir(dirname):
    symbols=[]
    candidates=glob.glob(dirname+'/*.h')
    candidates.sort()
    for c in candidates:
        symbols.extend(tagfile(c))
    return symbols

def tag(name):
    if not os.path.exists(name):
        print('error: cannot find '+name)
        return None
    if os.path.isdir(name):
        return tagdir(name)
    if os.path.isfile(name):
        return tagfile(name)
    return None

if __name__=="__main__":
    if len(sys.argv)!=3:
        print(f'''

    use: {sys.argv[0]} reference candidate

    reference and candidate can either be a single
    header file, or a directory containing header files.
    No recursive sub-directory search is performed.

''')
        raise SystemExit

    # Parse reference headers
    ref=tag(sys.argv[1])
    print('-- reference: %d symbols' % len(ref))
    #for s in ref: print(s)

    # Parse candidate headers
    cand=tag(sys.argv[2])
    print('-- candidate: %d symbols' % len(cand))
    # for s in cand: print(s)
    
    # Loop on all symbols defined in ref
    for s_ref in ref:
        #print('looking for:', s_ref.name)
        for s_can in cand:
            if s_ref==s_can:
                s_ref.found+=1
                #print('\tfound:', s_can.file)

    print('-- symbols not defined anywhere')
    for s_ref in ref:
        if s_ref.found<1:
            print('\t', s_ref)
    print('-- symbols multiply defined')
    for s_ref in ref:
        if s_ref.found>1:
            print('\t', s_ref)

