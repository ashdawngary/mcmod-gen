#Legacy mcmod-gen

This is Legacy mcmod-gen.  There is only 1 important file namely `compiler.py`.   
Essentially, legacy mcmod gen is just a cut and paste job.  It was written a very long time ago, and was only meant to simulate void no input functions i.e action only code.  
I was able to finese many different bots as you can see by clicking around.  They were mostly for cosmic-prisons  and saico-sky.  

Here is a video of someone who happened to capture on of the miners in action  
https://www.youtube.com/watch?v=O1Ysamct04M  
https://www.youtube.com/watch?v=FSL74QRURnU   
https://www.youtube.com/watch?v=duBto6rjFwg 

Ironically none of these videos provided "sufficent evidence" to even blacklist it, so it shows how powerful bots can be if they arent just taping your mouse.    
Here is the code for those videos: https://github.com/ashdawngary/mcmod-gen/tree/master/legacy%20compiler/new%20redstone%20code  

If you are really well-versed in mcmod-gen and are just looking for a cut paste void procedure compiler, then this is your best bet.  

#How to use

Legacy is a very simple system.  You pass in an input file, run the compiler with a bunch of helper functions in their own files, and just compile into a new file.  For example, 
In order to call a void function, we use the `%%` operator and enclose a file within.  
```
    
do
	%%eastmovement.txt%%
	%%westmovement.txt%%

while(true)

```

in normal macromod code would just loop.  Now we can define void procedures within eastmovement.txt and westmovement.txt and it works!.

Furthermore we can also set up recursive void procedures for example `eastmovement.txt` may contain:   

```
%%lookeastapprox.txt%%
looks(90,0,500ms)
%%east.scanrow.low.txt%%
```
This procedure invokes another void procedure that looks approx east, and then it initalizes a `east.scanrow.low` procedure. Looking into scanrow, we can see that it has:

https://github.com/ashdawngary/mcmod-gen/blob/master/legacy%20compiler/new%20redstone%20code/east.scanrow.low%20(2018_12_10%2023_00_25%20UTC).txt

This is some extremely bulky code, but even it has some dependencies.  Eventually we reach very fine small macromod procedures such as: 
(moveleft.txt)
```
keydown(left)
wait(50ms)
keyup(left)
```
These smaller scripts eventually allow us to build very powerful scripts at the top (i.e. a bot frame)


#How to execute given dependencies.   
Run `python -i` or some equivalent such as idle with `compiler.py` which will open up an interactive shell.  
There is only 1 function: `force_compile(filename,fle = False,tabtype = '\t')` where:  
`filename` is filename to input
`fle` is `False` if you want to return a string program to `python -i` or an outputfile if not of type `bool`
`tabtype` is the character for tabs

We can run `force_compile('botframe.txt',fle='outputfile.txt',tabtype='\t') and the rest is done.

The resst of the syntax is all Mumfrey's macromod so have fun!
