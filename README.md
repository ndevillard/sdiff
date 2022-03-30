# sdiff

Semantic diff between C header files

This tool piggybacks on the output of `ctags` to build a list of declared
symbols: constants, macros, typedefs, global variables, function
prototypes, and function definitions. Each symbol is registered by name,
file name, type, and function signature where applicable.

## Use

The program expects two names. Those names can either be a C header file
or a directory containing C header files. For directories, no recursive
search is performed, they must contain a flat structure with all header
files at the same level.

The first provided name is the reference: it contains all symbols that
need to be defined.

The second provided name is a candidate. All header files will be parsed
and searched for symbols present in the reference.

The program output describes:

- What symbols are declared in both reference and candidate.
- What symbols differ between reference and candidate.

Differing symbols can be:

- Symbols declared differently: one could be a function and another a macro
- Structs that do not have identical members
- Functions that do not have identical prototypes
- Typedefs that have the same name but different definitions

The program does not parse defines and macros, so they could have different
values between reference and candidate.

Run with `-v` to get more a verbose output.

