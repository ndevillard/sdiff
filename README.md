# sdiff

Semantic diff between C header files

This tool piggybacks on the output of `ctags` to build a list of declared
symbols: constants, macros, typedefs, global variables, function
prototypes, and function definitions. Each symbol is registered by name,
file name, type, and function signature where applicable.

## Use case

One header file is the reference, it contains all symbols that must be
defined by a candidate.

The other header file (or set of header files) is the candidate.

`sdiff` compares the two header files to see if all the symbols declared in
the reference also appear in the candidate. It will also detect symbols
multiply defined, symbols that fail to appear, or symbols that are in the
candidate and not in the reference.

Hope that's useful
Nicolas



