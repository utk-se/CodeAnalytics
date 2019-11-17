# Code Analytics

A spiritual successor to Adam's code size short paper. Extending his script to look at many many more github repos to analyze...

 - How many code files?
   - Can be implemented with the current code
 - How many classes?
 - How many methods?
   - Can be implemented with the current code (?)
 - How many lines are each file, class, method? How many characters wide are each method?
 - How many lines of code? Comments only? Both?
 - How many variable declarations?
 - How many conditionals?
 - How many loops?
 - How many tokens per line?
 - How many literals, number and string?
 
Ways to split the data... 

 - Language
 - Project size 
 - Solo contributor vs a few vs many
   - What are we considering a contributor?
 - Many stars vs a few
 - How old is the project
   - Are we determining from the last commit or when the project started?
 
 ## Running the Code

 Please make sure your GitHub keys are in `keys.json`. They can be created [here](https://github.com/settings/developers) under OAuth Apps.

 Create a virtual environment for python 3 by typing `python3 -m venv env`. Then, activate the virtual environment by typing `source env/bin/activate`. Finally, install all the requirements by typing `pip install -r requirements.txt`.
