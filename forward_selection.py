import pandas as pd
import statsmodels.api as sm

def forward_selection(yhat, xvars, alpha=.05, by_pvalue=True) :

    """ Create a forward selection stepwise linear regression model. This requires building a simple linear model 
    for each variable individually. The function takes the variable that has the smallest t-test p-value and puts 
    that variable in the model. It then creates two variable models using the first selected variable and one of the 
    remaining variables. It then picks the second variable from the model with the lowest p-value. This process continues
    until the R-squared adjusted value stops increasing or it runs out of variables. yhat is the dependent variable, 
    xvars are all the independent variables. modelVars are the independent variables selected for the final model.
    The function returns the final model plus the result of each step in the selection process. """

    modelstats = []
    midx = 1
    modelVars = pd.DataFrame()
    max_rsq_adj = 0
    model_steps = pd.DataFrame()
    model_steps[['risk']] = ""
    model_steps[['RsqAdj']] = ""
    
    for i in range(len(xvars)):
        modelstats = []

        for column in xvars:
            xs=pd.concat([modelVars,xvars[column]],axis=1)

            # Add a constant to the dependent variables first
            xs = sm.add_constant(xs)

            # Build the model
            model = sm.OLS(yhat, xs).fit()

            data = {'risk' : column, 'B0' : model.pvalues[0], 'B1' : model.pvalues[midx],  'RsqAdj' : model.rsquared_adj}

            modelstats.append(data)

        midx += 1
        df_modelstats = pd.DataFrame(modelstats)
        idx = df_modelstats['B1'].idxmin()
        rsq = df_modelstats['RsqAdj'].iloc[idx]
        lowest_pvalue = df_modelstats['B1'].iloc[idx]
    
        if by_pvalue :
            if lowest_pvalue <= alpha :
                modelVars = pd.concat([modelVars,xvars.iloc[:,idx]],axis=1)
                xvars=xvars.drop(xvars.columns[idx],axis=1)
                max_rsq_adj = rsq
                model_steps.loc[len(model_steps.index)] = df_modelstats.iloc[idx,[0,3]]
            else :
                break

        else :
            if rsq > max_rsq_adj :
                modelVars = pd.concat([modelVars,xvars.iloc[:,idx]],axis=1)
                xvars=xvars.drop(xvars.columns[idx],axis=1)
                max_rsq_adj = rsq
                model_steps.loc[len(model_steps.index)] = df_modelstats.iloc[idx,[0,3]]
            else :
                break

    # Add a constant to the dependent variables first
    modelVars = sm.add_constant(modelVars)

    # Build the model
    model = sm.OLS(yhat, modelVars).fit()

    return model, model_steps