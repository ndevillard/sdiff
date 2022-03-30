

#define CONSTANT1   42
#define CONSTANT2   3.14
#define ARRAY_SZ    (2*CONSTANT1)

typedef unsigned char byte ;

typedef struct _point_ {
    double x, y ;
    double dist ;
    char * name ;
} point ;

point * point_new(double x, double y);
void point_del(point * p);

    
