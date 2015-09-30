#Notes

9/30/15

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
    //Normal array declaration, 256 bytes allocated, nothing is set automatically. There’s no guarantee of a terminating null.
    char s[256] = “Imagine”;
    //Allocates 256 bytes, puts “Imagine” in the first 7 bytes AND adds a null at the 8th byte.
    char s[] = “Tuesday”;
    //Allocates 8 bytes, puts “Tuesday” in the first 7 bytes AND adds a null to the 8th byte.
    char *s = “Mankind”;
    //Allocates 8 bytes, puts “Mankind” in the first 7 bytes AND adds a null at the 8th byte. s is a pointer variable instead of an array
    ```
		
You can only assign strings with = at declaration.
    ```C
char s[] = “Zero”; // ok
s = “seven” //NOT ok
    ```
This is the only time you can assign something to a String literal.
