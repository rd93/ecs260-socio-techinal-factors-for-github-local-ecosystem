#use install.packages() to install these 
#load libraries
library(ggplot2)
library(reshape2)
library(corrplot)
library(scales)

#read in the data
op2 <- read.csv("/Users/aabhastonwer/ucdavis/software/ecs260-socio-techinal-factors-for-github-local-ecosystem/op2.csv")
names(op2) = gsub('\\.',' ',names(op2))


#============================================
#Exploration
#============================================

#check for collinearity - PR Count and Average Comments are collinear
corrplot(cor(op2),type='lower')

#reshape the data to make it easier for plotting
op2melt = melt(op2)
op2melt$logvalue = log(op2melt$value)

#make a grid of histograms -- none of these are normally distributed
ggplot(op2melt,mapping=aes(x=value)) +
  geom_histogram(bins = 10) +
  facet_wrap(vars(variable),nrow=3) +
  scale_x_continuous(labels = comma) +
  theme_classic() +
  ggtitle('Parameter Histograms',subtitle='Untransformed')+
  labs(y='Frequency',x='Value') 

#logged values
ggplot(op2melt,mapping=aes(x=logvalue)) +
  geom_histogram(bins = 100) +
  facet_wrap(vars(variable),nrow=3)  +
  scale_x_continuous(labels = comma) +
  theme_classic() +
  ggtitle('Parameter Histograms',subtitle='Log transformed')+
  labs(y='Frequency',x='Logged Value') 


#============================================
#Fit a linear model with the logged values
#============================================

#log the original dataframe
logop2 = log(op2)
#replace infinities produced from logs with NA to prevent errors down the line
logop2 = do.call(data.frame,lapply(logop2,function(x) replace(x, is.infinite(x), NA)))
names(logop2) = gsub('\\.',' ',names(logop2))

#fit the 3 individual models at the same time
model.all = lm(cbind(`Average Latency`,`Release Count`,`Commit Count`)~
              `PR Count` + `Average Comments` + Contributors,
            logop2)

#check the results of each individual model
summary(model.all)

#separate the models

#################
#latency model
#################

mod.latency = lm(`Average Latency` ~ `PR Count` + `Average Comments` + Contributors,
                 logop2)
plot(mod.latency)
#not normally distributed residuals, partially due to the outlier, everything else good

#plot scatterplots individually to assess linearity visually
ggplot(logop2,mapping=aes(y=`Average Latency`,x=`PR Count`)) +
  geom_point() +
  geom_smooth(method = 'lm') +
  theme_classic() +
  ggtitle('Contributors vs Average Latency') +
  labs(x='log(PR Count)',y='log(Average Latency)')

ggplot(logop2,mapping=aes(y=`Average Latency`,x=`Average Comments`)) +
  geom_point() +
  geom_smooth(method = 'lm') +
  theme_classic() +
  ggtitle('Contributors vs Average Latency') +
  labs(x='log(PR Count)',y='log(Average Latency)')

ggplot(logop2,mapping=aes(y=`Average Latency`,x=Contributors)) +
  geom_point() +
  geom_smooth(method = 'lm') +
  theme_classic() +
  ggtitle('Contributors vs Average Latency') +
  labs(x='log(Contributors)',y='log(Average Latency)')


#separate the models
#Only average comments seems to have a significant effect on average latency
#reduce the model to just these parameters
mod.latency.red = lm(`Average Latency` ~ `Average Comments`,
                 logop2)
summary(mod.latency.red)
plot(mod.latency.red)

#write model results to csv
write.csv(summary(mod.latency.red)$coefficients,'mod_latency_red.csv')

######################
#commit model
######################

#only contributors has effect on commit count -- remove other params
mod.commits = lm(`Commit Count`~ Contributors, logop2)
summary(mod.commits)
plot(mod.commits)
#pretty good looking graphs -- regression assumptions are met

#make scatter plot
ggplot(logop2,mapping=aes(y=`Commit Count`,x=Contributors)) +
  geom_point() +
  geom_smooth(method = 'lm') +
  theme_classic() +
  ggtitle('Contributors vs Commits') +
  labs(x='log(Contributors)',y='log(Commits)')

#write model results to csv
write.csv(summary(mod.commits)$coefficients,'mod_commits.csv')

################
#interaction effects
#################

model.interaction = lm(cbind(`Average Latency`,`Release Count`,`Commit Count`)~
                         `PR Count` * `Average Comments` * Contributors,
                       logop2)
summary(model.interaction)
