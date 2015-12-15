#Notes
**12/15/15**

*Aim: A pipe by any other name...*

1. Named Pipes
  - mkfifo - &lt;sys/types.h&gt; &lt;sys/stat.h&gt;
    - C function to create a FIFO
	- Returns 0 on success and -1 on failure
	- Once created, the FIFO acts like a regular file, and we can use open, read, write, and close on it
	- mkfifo( &lt;name&gt;, &lt;permissions&gt; )

```C
int main() {
   int from_client;
   int e;
   char line[100];

   e = mkfifo("mario",0644);
   printf("<server> Pipe created: %d\n",e);

   from_client = open( "mario", O_RDONLY);
   printf("<server> connection open\n");

   read( from_client, line, sizeof( line ) );
   printf( "<server> read: [%s]\n", line );
   //reading doesn't care about terminating null

   close(from_client);
   return 0

}
```

```C
int main() {
   int to_server;
   char line[100];
   
   to_server = open( "mario", O_WRONLY );
   printf("<client> connection opened\n");

   printf("<client> enter stuff: ");
   fgets( line, sizeof(line), stdin );

   write( to_server, line, sizeof(line) );
   close( to_server );
   
   return 0;
}
```
**12/14/15**

*Aim: Ceci n'est pas une pipe*

1. Pipe
  - A conduit between 2 seperate processes
  - Pipes have 2 ends, a read end and a write end
  - Pipes are unidirectional (a single pipe must be either read or write only in a  process)
  - Pipes act just like files.
  - You can transfer any data you like through a pipe using read/write
  - Unnamed pipes have no external identification (like a descriptor or name)
  - pipe - &lt;unistd.h&gt;
    - Creates an unnamed pipe.
	- Returns 0 if the pipe was created, -1 if not.
	- Opens both ends of pipe as files.
	- pipe( int descriptors[2] )
	  - descriptors
	     - array that will contain the descriptors for each end of the pipe

```C
int main(){

   int fds[2];
   int f;
   
   pipe(fds);
   f = fork();
   if ( f == 0 ) { //if f is 0 it is the child
      close( fds[0] );
	  //sets child to write end by closing other end
	  float p = 123.347;
	  write( fds[1], &p. sizeof(p) );
	  close( fds[1] );
   }

   else {
      close( fds[1] );
	  //close writing end
	  float q;
	  read( fds[0], &q, sizeof(q) );
	  printf("parent read: %f\n", q);
   }

   return 0;

}
```
- Alternatively:

```C
int main(){

   int fds[2];
   int f;
   char line[100];
   
   pipe(fds);
   f = fork();
   if ( f == 0 ) { //if f is 0 it is the child
      close( fds[0] );
	  //sets child to write end by closing other end
	  printf("Enter some text");
      fgets( line, sizeof(line), stdin );
	  write( fds[1], line, sizeof(line) );
	  close( fds[1] );
   }

   else {
      close( fds[1] );
	  //close writing end
	  read( fds[0], line, sizeof(line) );
	  printf("parent read: [%s]\n", line);
   }

   return 0;

}

//Example of usage:
//Have child take data from user, send to parent, and then back to child->user
```

2. Named Pipes
  - Also known as FIFOs.
  - Same as unnamed pipes except FIFOs have a name that can be used to identify them via different programs.
  - Unidirectional, like unnamed pipes.
  - mkfifo
    - Shell command to make a FIFO
	- $ mkfifo &lt;pipe name&gt;
  - Named pipes look like files when created, and can be treated like files



---

**12/9/15**

*Aim: more semaphore code*

1. semop
   - Perform semaphore operations (like Up/Down)
   - All operations performed via semop are atomic!
   - semop(*DESCRIPTOR,OPERATION,AMOUNT*)
      - DESCRIPTOR:
	     - you know what this is...
	  - AMOUNT:
	     - The amount of semaphores you want to operate on in the semaphore set
		 - For a single semaphore set, 1.
	  - OPERATION:
	     - A pointer to a struct sembuf value:
		 ```C
		 struct sembuf {
		    short sem_op;
			short sem_num;
			short sem_flg;
		 }
		 ```

         - **sem_num:**
		    - The index of the semaphore you want to work on
		 - **sem_op:**
		    - -1: Down(S)
			- 1: Up(S)
			   - Any -/+ number will work, you will be requesting/releasing that value from the semaphore.
	     - **sem_flg:**
		    - Provide further options:
			- SEM_UNDO:
			   - Allow the OS to undo the given operation. Useful in the event that a program exits before it could release a semaphore.
			- IPC_NOWAIT:
			   - Instead of waiting for the semaphore to be available, return an error
			   
```C
int main(){
   int key = ftok("makefile",'a');
   int semid;

   semid = semget(key,1,0644);
   printf("Before access...\n");

   //the key is to create this struct and then call semop
   struct sembuf sb;
   sb.sem_num = 0;
   sb.sem_flg = SEM_UNDO;
   sb.sem_op = -1;

   semop( semid, &sb, 1 );
   int i = 10;
   while( i-- ) {
      printf("I'm in!\n");
	  sleep(1);
   }
   
   sb.sem_op = 1;
   //just change the value in the struct and return the operation
   semop( semid, &sb, 1 );
   
   return 0;
}
```
  - Use the amount of bytes in shared memory to know how much to read from the last file

---

**12/8/15**
*Aim: What's a semaphore?*


1.semctl
   - control the semaphore, including:
      - setting the semaphore value
      - removing the semaphore
      - getting the current value
      - getting info about the semaphore
   - semctl(DESCRIPTOR,INDEX,OPERATION,DATA)
      - DESCRIPTOR: the return value of semget
      - INDEX: the index of the semaphore you want to control in the semaphore set identified by the descriptor
         - for a single semaphore set, 0.
      - OPERATION: one of the following constants (there are others as well)
         - IPC_RMID: remove the semaphore
	 - SETVAL: set the value (requires DATA)
	 - SETALL: set the value of every semaphore in the set (requires DATA)
	 - GETVAL: return the value
	 - IPC_STAT: populate buffer with information about the semaphore (requires DATA)
      - DATA:
      	 - variable for setting/storing information about the semaphore (data type: union semun)
	 - a union is only as large as the largest data member inside


```C
union semun {
  int val;
  struct semid_ds *buf;
  unsigned short  *array;
  struct seminfo  *__buf;
};
```

```C
int main(int argc, char **argv){
    int key = ftok("makefile",'b');
    int semid;

    if (strcmp( argv[0], "-c")==0){
       semid = semget(key, 1, 0644 | IPC_CREAT);
       union semun su;
       su.val = 3;
       semctl(semid,0,SETVAL,su);
       printf("semaphore created: %d\n",semid);
    }

    if(strcmp(argv[0],"-v") == 0){
       semid = semget(key,1,0644);
       int v = semctl(semid,0,GETVAL);
       printf("current value: %d\n",v);
    }      
    
    if(strcmp(argv[0],"-r) == 0){
       semid = semget(key,1,0644);
       int r = semctl(semid,0,IPC_RMID);
       printf("semaphore created:%d\n",v);
    }      
        
```

	 
      
---

**10/28/15**
**Aim: I need information, stat!**
1. Metadata - information provided to you about files (data about data, not contained within the data
   - stat - <sys/stat.h>
      - Get information about a file (metadata)
	  - stat(<PATH>,<STAT BUFFER>)
	  - Buffer has to be a pointer so it can be modified
	  
	  ```C
	  struct stat sb; //sb for stat buffer
	  stat("foo",&sb);
	  ```

      - STAT BUFFER
	     - must be a pointer to a struct stat
		 - all the file information gets put into the stat buffer
		 - some of the fields in struct stat:
		 ```C
		 st_size // file size in bytes
		 st_uid, st_gid // user id, group id
		 st_mode // file permissions
		 
		 st_atime, st_mtime //last access, last modification
	 	 ```
		 - These are struct time_t variables. We can use functions in time.h to ake sense of them
		 - ctime(<struct time_t *>
		    - returns time as a string
	     - time(<struct time_t *>)
		    - sets the parameter to the current time


---


**10/22/15**

*~a brief interlude~*

1. bitwise operators
  - &: bitwise and
  - |: bitwise or
  - ~: bitwise not
  - ^: bitwise xor

  - Logical operators work on each bit of a value
     - char c = 13; // 0000101
	 - char x = ~c; // 1111010

2. Flags
  - Each flag is a number, to combine flags we use bitwise or
```C
O_WRONLY = 1           00000001
O_APPEND = 8           00001000
O_WRONLY | O _APPEND   00001001
```
  - Note we're using bitwise or. It checks the 0's and 1's of each statement to get the final representation


3. close - <unistd.h>
  - Remove a file from the file table
  - Returns 0 if successful, returns -1 and sets errno if unsuccessful.
  - close(<file descriptor>)


4. read - <unistd.h>
  - reads in data from a file
  - read( <file descriptor>, <buffer>, <amount> )
  - read (fd, buff, n)
  - read n bytes from the fd's file and put that data into buff
  - returns the number of bytes actually read. Returns -1 and sets errno if unsuccessful
  - buff has to be a pointer otherwise it can't be modified

```C
char b1[100];
fd1 = open("foo", O_RDONLY);
b = read (fd1, b1, 5);
fd2 = open( "goo", O_CREAT | O_WRONLY | O_TRUNC, 0644);
b = write (fd2, b2, sizeof(b2));

```
---

**10/21/15**

**Aim: Opening up a whole new world of possibilities**

*Note: Don't compile .h files!*

1. File Table
   - A list of all files used by a program while it is running
   - Contains basic information like the file's location and size
   - The file table has a limited size, which is a power of 2 and commonly 256.
   - getdtablesize() will return this value
   - Each file is given an integer index, starting at 0, this is referred to as the file descriptor
   - There are 3 files always open in the table
     - 0 or STDIN_FILENO: stdin
	 - 1 or STDOUT_FILENO: stdout
	 - 2 or STDERR_FILENO: stderr
	 
   - open - <fcntl.h>
     - Add a file to the file table and return its file descriptor
	 - If open fails, -1 is returned, extra error information can be found in errno
	   - errno is an int variable tha can be found in <errno.h>, using strerror (in string.h) on errno will return a string description of the error

   - open( <PATH>, <FLAGS>, <MODE> )
     - mode
	   - Only used when creating a file. Set the new file's permissions using a 3 digit octal #
	   - Octal #s have a leading 0
	     - 0644, 0777 ...
	 - flags
	   - determine what you plan to do with the file
	   - user the following constants:
	     - O_RDONLY
		 - O_WRONLY
		 - O_RDWR
		 - O_APPEND
		 - O_TRUNC
		 - O_CREAT
		 - O_EXCL : When combined with CREAT, will return an error if the file exists.


---

*10/15/15*
**Common problems we may encounter on project**

```C
//link_list.h

typedef struct n{

// ...

} song_node;
//...

//library.h
#include "link_list.h"
void print_artist(song_node *);

//main.c
#include "link_list.h"
#include "library.h"
//If we include library.h, it recopies all of the linked list stuff
//will give an ERROR, due to duplicate functions (caused by adding link_list.h
//to library.h)
```

- Redeclaring things is NOT something we want to do.
- "#" is a preprocessor instruction
   - before your code is properly compiled, THESE things will happen

- "#define FOO value"
   - we don't have to give it a value
   - if you think of include as a copy/paste
   - #define is a replacement
   - ex:
   ```C
   #define FOO 27
   ```
       - ex, all instances of FOO will be replaced with 27
   - you can put a chunk of C code in the define if you want 

- "#ifndef FOO"
   - if not defined, do all of the actions in between until #endif
   - ex:
```C
//link_list.h
#ifndef LINK_LIST_H
#define LINK_LIST_H
typedef struct n{
} song_node;
#endif
```
- If LINK_LIST_H is not defined, then define it.
   - Since LINK_LIST_H is already defined after importing it from linklist.h in the main , it won't be redefined again after importing library.h
   - Order of #include in main file doesn't matter
   - We don't have to include a value, we just use it to determine whether or not a group of things has been defined already
   
---


*10/13/15*
**Aim: Zelda's in trouble, get Link!**

1. Do Now:
   - What's wrong with this function? (assume node has been declared correctly)

```C
node * insert_front( node * front, int i ) {

   node new; //new is not a pointer, but an actual struct
   new.i = i;
   new.next = front;

   return &new;
}
//Leads to Segmentation Fault, accessing data we aren't supposed to
```

2. Once Stack memory (statically allocated memory) is popped off, the memory allocated is released, hence we are left with a Seg Fault

3. We have to Dynamically allocate memory so it'll persist after stack is popped off.

```C
//Working Code
node * insert_front( node * front, int i){
    node *new;
    new = (node *)malloc( sizeof(node) );

    new->i = i;
    new->next=front;

    return new;
}
```

```C
//Creating a linked list in main

int main(){
   node *n = 0; //like creating a null leading node

   n = insert_front( n,0 );
   n = insert_front( n,1 );
   n = insert_front( n,2 );
   n = insert_front( n,3 );

   print_list(n);

   return 0;
}
```

---

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
  - Provide a new name for an existing data type

```C
typedef <real type> <new name>;

ex:
   typedef unsigned int size_t;
   size_t x = 139; // x is really an unsigned int;
```

4. Struct
  - A collection of values in a single data type

```C
//Regular Struct
struct { int a; char x; } s;\

//Like a template for struct
struct foo {int a; char c; };
struct foo s;

//Integrating typedef
typedef struct {int a; char c;} fool
foo *t;
t = (foo *)malloc( sizeof(foo) ); //Similar to constructor in Java

(*t).a = 97;
t->c = '@';
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
