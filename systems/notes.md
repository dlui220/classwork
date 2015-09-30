*Systems Level Programming Notes*

**Aim: How to write functioning code**

*Do Now:* Write a C program that does the following:
    
	1) Create a string and set it to some value

    	2) Write code to find the length of the string and then print it. (do not write a function for this)

	```C
	

**9.29.2015

Aim: Time to stop stringing you along.

The variable containing the array name is a pointer. No need to use ampersand when assigning a pointer to an array.

    ```C	     
    float fray[5];
    float *fp = fray;
    //pointer fp now refers to the same place as fray.
    //fp - > 824
    //*fp - > 2.3
    ```C

    ```C	
    *(ray + 2) = *(2 + ray);
    //however, a[b] is simply shorthand for *(a + b)
    //this means that
    ray[2] = 2[ray];
   ```C

   Array variables CANNOT BE MODIFIED:
	```C
	ray++;
	//DOES NOT COMPILE
	```C

C Strings (ctrings)
Strings are character arrays that end with a null character (either ‘ ‘ or 0 or ‘\0’)

The terminating null character is a convention, string functions will not work correctly without it. 
The follow are ways to declare strings:
    ```C
    char s[256];
    //Normal array declaration, 256 bytes allocated, nothing is set automatically. There’s no guarantee of a terminating null.
    char s[256] = “Imagine”;
    //Allocates 256 bytes, puts “Imagine” in the first 7 bytes AND adds a null at the 8th byte.
    char s[] = “Tuesday”;
    //Allocates 8 bytes, puts “Tuesday” in the first 7 bytes AND adds a null to the 8th byte.
    char *s = “Mankind”;
    //Allocates 8 bytes, puts “Mankind” in the first 7 bytes AND adds a null at the 8th byte. s is a pointer variable instead of an array
    ```C
		
You can only assign strings with = at declaration.
    ```C
char s[] = “Zero”; // ok
s = “seven” //NOT ok
  ```C
This is the only time you can assign something to a String literal.
