# mcmod-gen Alpha Compiler
Welcome to the Alpha NoType Compiler, a first try at actual abstraction for macromod.    
Why someone would choose Alpha-Compiler: 
* You like scopes
* You like libraries
* You like actually returning things
* You want to reuse functions like a normal language
* You like passing by references
* You want to have an easier syntax

Whatever may be the case, Alpha Compiler is the newest tool for mcmod-gen and will probably fit your needs.  Programs are even simpler on mcmod gen.

# variables
There is only 1 kind of variable: integers.  Booleans are integers, but for our cases, you want to test `int` op `int` for any boolean evaluations.   
Variables stick to their scope. Unless you pass a variable by parameter it will not copy over.  When you exit a function, the variables essentially dissapear.  
One of the amazing things about macromod is that there is good garbage collection.  Essentially all variables who's memory is freed may be reused by another function as long as the code execution segments are mutually exclusive.  This property is verified at compiletime.

# Functions
All programs are just functions.  All Runnable programs have `main` functions and libraries will just have functions.  Functions may start with `def` or `func` (interchangable) 
Here is an example function(program)
``` 
def main(){

a = 1
cout << "The Answer to the question is:" << a
}
```
This program just prints `The Answer to the question is: 1`
