# Stepwise-Regression-Algorithms
Contains forward and backward stepwise selection algorithms
!![Model_Summary](https://github.com/jeg-msba/Stepwise-Regression-Algorithms/assets/111711622/bb4c26a1-67e5-427e-853d-41961230eeb0)

This repository contains two algorithms for doing stepwise regression: foward selection and backward selection
The forward selection algorith creates a model by adding variables, one at a time, measuring either the Adjusted R-squared value or the p-value.
If you select by_pvalue == True, the model keeps adding variables as long as their p-value is less than alpha. While building this model 
it is possible that previously selected variables will have their p-value change such that they are no longer less than alpha. If you 
select by_pvalue == False, the algorithm keeps adding variables to the model until the AdjRsq score stops increasing. The individual
p-values are not considered.

The backward selection algorithm creates a model using all variables, then removes them, one at a time, if their p-value is greater than
alpha. An advantage of the backward algorithm is that the final model will have all variable p-values < alpha

I included two data files which the wrapper reads in to test the algorithm. You can of course use your own data files. xVars is a 
data file of 28 risk factors leading to death among countries with a Gross National Income less than the mean.
yhat is the Gross National Income of those countries. The data files have been taken from

Sources
# https://ourworldindata.org/grapher/number-of-deaths-by-risk-factor
# https://databank.worldbank.org/reports.aspx?source=2&series=NY.GNP.PCAP.CD&country=
# https://databank.worldbank.org/reports.aspx?source=2&series=SP.POP.TOTL&country=
