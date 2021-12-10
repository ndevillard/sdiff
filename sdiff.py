# -*- coding: utf-8 -*-
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

def tag(filename):
    syms=[]
    p=os.popen('ctags-universal --kinds-c=+pLl --fields=Sk -f- '+filename, 'r')
    for line in p.readlines():
        s=Symbol(line)
        syms.append(s)
    p.close()
    return syms

if __name__=="__main__":
    if len(sys.argv)!=3:
        print("use: %s ref dir" % os.path.basename(sys.argv[0]))
        raise SystemExit

    # Parse reference header
    ref=tag(sys.argv[1])
    print('-- reference: %d symbols' % len(ref))

    # Parse every header file in directory
    srcs=[]
    candidates=glob.glob(sys.argv[2]+'/*.h')
    candidates.sort()
    print('-- files to check:')
    for c in candidates:
        print('\t'+c)
        srcs.append(tag(c))

    # Loop on all symbols defined in ref
    for s_ref in ref:
        print('looking for:', s_ref.name)
        for src in srcs:
            for s in src:
                if s_ref==s:
                    s_ref.found+=1
                    print('\tfound:', s.file)

    print('-- symbols not defined anywhere')
    for s_ref in ref:
        if s_ref.found<1:
            print('\t', s_ref)
    print('-- symbols multiply defined')
    for s_ref in ref:
        if s_ref.found>1:
            print('\t', s_ref)
        
        

