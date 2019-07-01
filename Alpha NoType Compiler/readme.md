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

"Correct Functions" will make sure to indicate return values ex:  `def returnsInt() -> int {`, but since this isnt a typed compiler, dont bother.  

returning the code is extremely simple, we utilize the 'return' like a standard language.  If you call a function and fail to provide a return pointer i.e call `myfunc` which returns int, but dont supply a variable to catch it, the compiler will warn you that it cannot find a return pointer.

Returning works in any control flow ex: `return` in a while loop wont start executing things after.
# Parameters and Pointers
Parameters can either be passed by reference or by copy.  Since parameters may be modified once in the function, it is standard to have all parameters be passed by copy, but this of course will create overhead and extra memory usage.  

A good example of Pointer usage is `getLocation(&cx,&cz)` which provides the player's location on the XZ plane with just 1 line call.  You can see within `navigation-latest` (a library), the code for this is as follows: 
```
func getLocation(x,z){
        native{
        !x! = %XPOS%
        !z! = %ZPOS%
        }
}
```
(Luckily the compiler does reuse memory which hits end-of-life)  

If you want to pass a value by reference, utilze the `&` token in front of a varaible.  This will overall eliminate overhead and can be used for returning more values, etc.

# Control Flow
Control Flow for Alpha NoType extends past the macromod controlflow. At the moment, we support traditional `for` `while` `if` and `if-else` statements.  The statements all support returning and adapt to macromod code.

## For Loop Syntax
The for loop is structured as so:
```
for ( intialization statement ; check statement; incrementor statement ) {
 // code
}
```
there should be exactly two semicolons, and as per usual, the variable intialized in the intialization statement will be deconstructed by the end of the loop.    

For reference, the macromod itself only supports integer counting for loops, and only work between upper and lower bounds. 

## while Loop Syntax
Another grievance of the macromod is the `do-while` only paradigm.  The `while` loop is an adapted version of the `do-while` which is encapsulated in a precheck `if` statement to prevent mandatory running. 
```
while(condition){
  // code
 }
 ```

I should make it clear that conditions do not need to be simple! You may call functions, do complex boolean exprs , define your own operators, or compare using standard operators within the conditions!

## If else syntax
This is a standard translation of the if-else syntax from macromod but we have removed the `endif` requirement.  To be consistent with the rest, we utilize `{` and `}` to indicate new scopes:
```
if(condition){
  // positive code
}
else{
  //optional code.
}
```
As of 7/1/2019, there is no support for `elif` / `elseif` but they are implemented in macromod and will transfer shortly.

## Native Blocks
Working with pure Alpha No-Type is pretty useless.  You can do extremely elaborate computational work, but at the end of the day, the point is to utilize sophisticated frameworks in order to create reliable actuation.  By mixing snippits of Alpha NoType and encoded actions from the Macromod itself, we can produce extremely powerful scripts.

The `native` block indicates that you want to inject pure Macromod code into the program.  Of course, we would want to transfer computed values from Alpha NoType, so we can utilize the `!` symbol to ask for a native-reference to a Alpha NoType Variable.   

For example in the code: (assume the compiler assigns variable `a` to `@tempvariable`
```
  func main(){
  a = 1
  native{
    log("wow the value of a is %!a!% ?")
  }
}
```
will compile to 
```
@tempvariable = 1
log("wow the value of a is %@tempvariable% ?");
```
by surrounding `a` in `!` we have asked the compiler to reference the abstract variable `a`'s memory location in the native block.

Native blocks can be used for movement or other kinds of control, but dont forget most `native` blocks should be in libraries to prevent users from having to actually deal with macromod code.   

Also don't forget, since booleans are essentially integers, we can test conditions in a native block and extrace the output in either a 1 or 0.

For example
```
func waitForApple(){
        mark = 0
        native{
                getslotitem(1,&out)
                !mark! = &out == "apple"
        }
        return mark
}
```
will return `1` if item slot 1 is an apple and `0` if not.  You can see that since we are working with pointers like `&out` (these are macromod pointers), we can't cast it to an integer and need to compute on it within the `native` scope. But once we test our booleans, we can extract the boolean `mark` and return it.
