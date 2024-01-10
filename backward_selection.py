
import pandas as pd
import statsmodels.api as sm

def backward_selection (yhat, xvars, alpha) :
    """ In order to create a first order linear model I will perform a forward selection stepwise linear regression. 
    This means I will create a simple linear model for each variable individually. I will take the model whose variable 
    has the smallest t-test p-value and put that variable in my model. I will then create two variable models using my 
    first selected variable and add each of the remaining variables. I then pick the second variable from the model with 
    the lowest p-value. This will process continue until the R-squared adjusted value stops increasing or I run out of variables. 
    yhat is the dependent variable, GNI. xvars are all the independent variables. modelVars are the independent variables 
    selected for the model. """

    # Initialize variables
    modelstats = []
    modelVars = xvars
    removed_column = []
    highest_pvalue = 0

    # remove x variables whose p-values are >  alpha
    for i in range(len(xvars)-1) :
        xs = modelVars

        # Add a constant to the dependent variables first
        xs = sm.add_constant(xs)

        # Build the model
        model = sm.OLS(yhat, xs).fit()

        # Record the model Adjusted R-squared and the x variable with highest pvalue from previous iteration
        data = {'removed_column' : removed_column, 'highest_pvalue' : highest_pvalue, 'RsqAdj' : model.rsquared_adj}
        modelstats.append(data)

        # Find the x variable with the highest pvalue
        idx = model.pvalues.idxmax()
        highest_pvalue = model.pvalues[idx]
        
        if highest_pvalue > alpha :
            removed_column = idx
            modelVars = modelVars.drop(columns=idx)
        else :
            break

    return(model, modelVars)

"""I started with a model consisting of all the x variables. The for loop removes from the model the x variable with the 
highest p-value, until the highest p-value is less than alpha. At that point it stops. The function returns the model anf
the list of model variables"""