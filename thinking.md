# Question 1

from where to extract claim : <br>
a) user's query < br>
b) LLM's answer

# Question 2

what is hallucination, how it develops?

# Blind Spot

<pre>
1. any failure -> refuse everything is too rigid in production
fix: depending on the professional category where this is being used we will chose the threshold for the answer verification.

2. entailment model themselves hallucinate confidence.
fix: since entailment itself is the problem, therefore we can avoid using it or just use it but the types of nli entailment will be chose according to the query and data.

3. we have assumed claim extraction is perfect.(claim extraction can be wrong)
fix: claim extraction is the only way and is used in the market, we can improve it using prompt. or accept it as tradeoff.

4. no re-ask or repair loop.
fix: have to implemenet loop , its must.

5. current algo: if answer is correct, but chunk ID is wrong, that's a problem.
   best algo: correct answer + wrong evidence = incorrect answer.
</pre>

# Question 4

since many types of files exist, how can i load document and chunking or vector storing , do i need to separate each file separatelly or is there any single common way to do this

# Question 5

like here we are providing the document itself, is ther any way that we provide the website link and then we convert the website page content in document then chunking and further

# Question 6

but why need to define class , we can simply doit by using function without class

# Question 7

how by using class, it enforces same format of metadata

# Statement 1

If the child has to call the method, enforcement is optional.
Optional enforcement = broken system.
The parent must call the child — not the other way around.
You do not create a “utility parent” that children call.

You create a controller parent that children cannot bypass.
This is called the Template Method pattern.

# Queston 8

why child call parent's method is wrong?
:- it's wrong because, The child can forget to call it, The child can call it incorrectly. that fails at large scale,
correction : The parent must call the child

# Question 9

when to use class?
a) You must enforce invariants
b) There are multiple implementations of the same role
c) The algorithm is fixed, but one step varies
d) Order of operations matters
e) You want correctness to be structural

# Statement 2

❌ “Every document must have a file name”
✅ Every document must have a stable, human-readable origin identifier

# Question 10

in inheritance parent class dont have the access to child class then why in parent class self.f() is called

# Statement 3

self.f() means:
“Call method f on the object instance that self refers to,
resolving it by searching the object’s class first, then its parents, then further up.”
