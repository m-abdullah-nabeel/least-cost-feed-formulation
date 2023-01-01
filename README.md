"# least-cost-feed-formulation" 

The response variable "available" tells if the calculation by scipy.optimize.linprog has been processed or not.
Though the calculation may not end as planned. 
The available will still return 1.
along with results in case of correct computation.
Or with error message otherwise.
The error if unhandled is dealt by plain text.

The status can be used to identify if the problem is feasible, infeasible, in bound or out of bound etc.
and is in accordance with the scipy.optimize.linprog docs
