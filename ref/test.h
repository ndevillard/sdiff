

/* Constants and macros */
#define CONSTANT1   42
#define CONSTANT2   3.14
#define ARRAY_SZ    (2*CONSTANT1)

/* Typedefs */
typedef unsigned char byte ;

/* Typedef struct */
typedef struct _point_ {
    double x, y ;
    double dist ;
    char * name ;
} point ;

/* Function prototypes */
point * point_new(double x, double y);
void point_del(point * p);

/* Variables */
size_t big_size ;

    
