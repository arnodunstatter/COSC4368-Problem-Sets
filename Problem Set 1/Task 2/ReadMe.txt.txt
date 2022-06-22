Two methods of testing the program follow:
	1. 	a. Install python 3.9 or higher
		b. Download and colocate both the main.py and the csp.py files. 
		c. Navigate to the directory in your terminal and run "python main.py".
		d. Follow the prompts to execute either the predefined problems or custom problems.

	2. 	a. Download and colocate the csp.py and the test.ipynb files and open the test.ipynb file with jupyter notebook.
			Alternatively you could make your own .py or .ipynb files in the same directory as the csp.py file and 
			therein call `import csp`.
		b. The csp.problem() constructor takes three arguments:
			i. variables: a list of single character alphabetic strings
			ii. constraints: a list of python evaluable strings
			iii. domains: a dictionary whose keys are the variables and whose values are lists of integers
		c. Call the problem.backtrackV4() function to solve the problem.