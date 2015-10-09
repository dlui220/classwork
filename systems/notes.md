#Notes

*10/9/15*
**Aim: **

1. Dynamic Memory Allocation
  - Normal memory allocation happens on the stack
  - Stack memory gets released as function pops off
  - Dynamic memory is located on the heap, it persists even after the function that created it pops off the stack
  - You must manually release dynamically allocated memory from the heap
2. free
  - Releases dynamically allocated memory
  - Takes one parameter, a pointer to the beginning of a dynamically allocated block of memory
  - EVery call to malloc/calloc should have a corresponding call to free

```C
int *p;
p = (int *(malloc(20));
free(p);
```

3. Typedef
  - PRovide a new name for an existing data type

```C
typedef <real type> <new name>;

ex:
   typedef unsigned int size_t;
   size_t x = 139; // x is really an unsigned int;
```

4. Struct
  - A collection of values in a single data type

```C

struct { int a; char x; } s;

```

---

*10/8/15*
**Aim: If you can't (al)locate your memory...I forget**

File dependencies for compiling:

    dwstring.c   dwstring.h   main.c
          \       /    \     /     
         dwstring.o     main.o
                  \    /
                   a.out

1. More stuff with "make"

- Running "make" runs the "makefile" file, no extensions

- Instead of writing a.out in the makefile, you can use "all" to always run
the command.

- You can also specify a target: "make dwstring.o"  to run the line dwstring.o

- "touch" - if it doesn't exist, file is made, and if it does, modifies
the timestamp (updated)

- You can have a "clean" function, to remove pesky files like ~ files.

- In the "all" function, you can have "gcc -o string_test dwstring.o main.o"
  in order to customize the filename.

- Now that we know how to use "make" files, our work should now include it.

- Can choose separate functions in terminal by running "make run", "make clean", etc

2. Dynamic Memory Allocation
   
- malloc( int x )
   - Allocates x bytes of memory (from the heap)
   - Returns the address at the beginning of the allocation
   - Returns a void *, always typecast to the correct pointer type.
    
```C
int *p;
p = (int *)malloc( 5 * sizeof(int) );
```

- calloc(int n, int x)
   - Allocates n * x bytes of memory
   - Ensures that each bit is set to 0
   - Works like malloc in all other ways

```C
int *p;
p = (int *)calloc(5, sizeof(int));
```

- realloc(void *p, int x)
   - Changes the amount of memory allocated to a given block
   - p must be a pointer to the beginning of an allocated block of memory, but it does not have to be the original pointer
   - If x is smaller than the original size of the allocation, the extra bytes will be released.

```C
int *p;
p = (int *)malloc(20);
p = (int *)realloc(p,40);
```

---

*//SOTD: Fake Plastic Trees - Radiohead*

*SOTD: Rearviewmirror - Pearl Jam*

**Aim: Make it so**

1. Seperate compilation
   
   - You can combine multiple C files into a C program by including them all
     in one gcc command

   - You cannot have duplicate function or global variable names across 
     those files, including the int main() function

```C
gcc -c
//This will compile a C file into an .o file. It's not a fully functional
//program, but it's compiled. Do this to compile .c files that don't have a
//main() function
```

- You can compile faster if you want to compile a c file and an o file because 
  o files won't be recompiled. The general format is to gcc -c the library files
  and then gcc the main.c and the .o files at the same time. This way, if any
  changes are made to your main.c file, you don't need to change any other files

Ex: dwstring.h, dwstring.c, main.c, dwstring.o, and a.out

- dwstring.c changes = dwstring.o and a.out change 
  (a.out is dependent on dwstring.o)

- main.c changes = a.out changes
  (a.out dependent on main.c)

- dwstring.h changes = everything changes  
    

2. Make

   - Create compiling instructions and setup dependencies
   
   - Standard name for the file is makefile

   - Syntax:

    ```C
    <TARGET>: <DEPENDENCIES>
    [TAB]<RULES>
    //Has to be a single tab, not 4 spaces
    ```

---

**10/1/15**
*SOTD: Tom Sawyer - Rush*

**Aim: How to write function code(2)**

asdf.h contains header files
```C
#include "customlib.h"
```

You can rename types (type definitions)

```C
//Useful Ctring commands
int strcmp(char *s1, char *s2)

char * strcpy(char *dest, char *source)

char * strcat(char *s1, char *s2)
```

---

**9/30/15**

*SOTD: One Headlight - The Wallflowers*

**Aim: How to write functioning code**

1. DN: Write a c program that does the following

- Create a string and set it to some value.
- Write code to find the length of the string and then print it. (Do not write a function for this)

```C
#include <stdio.h>
char s[256] = "swaggy"; 

int main(){
   printf("%s", s);
   return 0;
}
```
---

**9.29.2015**

Aim: Time to stop stringing you along.

The variable containing the array name is a pointer. No need to use ampersand when assigning a pointer to an array.

```C	     
float fray[5];
float *fp = fray;
//pointer fp now refers to the same place as fray.
//fp - > 824
//*fp - > 2.3
```

```C	
*(ray + 2) = *(2 + ray);
//however, a[b] is simply shorthand for *(a + b)
//this means that
ray[2] = 2[ray];
```

Array variables CANNOT BE MODIFIED:
```C
ray++;
//DOES NOT COMPILE
```

C Strings (ctrings)
Strings are character arrays that end with a null character (either ‘ ‘ or 0 or ‘\0’)

The terminating null character is a convention, string functions will not work correctly without it. 
The follow are ways to declare strings:
```C
char s[256];
    //Normal array declaration, 256 bytes allocated, nothing is set 
    //automatically. There’s no guarantee of a terminating null.
char s[256] = “Imagine”;
    //Allocates 256 bytes, puts “Imagine” in the first 7 bytes 
    //AND adds a null at the 8th byte.
char s[] = “Tuesday”;
    //Allocates 8 bytes, puts “Tuesday” in the first 7 bytes 
    //AND adds a null to the 8th byte.
char *s = “Mankind”;
    //Allocates 8 bytes, puts “Mankind” in the first 7 bytes 
    //AND adds a null at the 8th byte. s is a pointer variable instead of an array
    ```
		
You can only assign strings with = at declaration.
```C
char s[] = “Zero”; // ok
s = “seven” //NOT ok
```
This is the only time you can assign something to a String literal.
