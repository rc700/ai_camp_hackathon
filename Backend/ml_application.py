from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from pandas.plotting import scatter_matrix, andrews_curves

from sklearn import preprocessing, metrics
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# importing in the CSV
data = pd.read_csv("survey_results_public.csv", index_col=0)

print(type(data))


# cleaning the CSV
clean_data = data.drop(['Professional', 'ProgramHobby', 'University', 'EmploymentStatus', 'CompanySize', 'CompanyType',
                        'YearsCodedJobPast', 'WebDeveloperType', 'MobileDeveloperType', 'NonDeveloperType',
                        'ExCoderReturn', 'ExCoderNotForMe', 'ExCoderBalance', 'ExCoder10Years', 'ExCoderBelonged',
                        'ExCoderSkills',	'ExCoderWillNotCode', 'ExCoderActive', 'PronounceGIF', 'ProblemSolving',
                        'BuildingThings', 'LearningNewTech', 'BoringDetails', 'JobSecurity', 'DiversityImportant',
                        'AnnoyingUI', 'FriendsDevelopers', 'RightWrongWay', 'UnderstandComputers', 'SeriousWork',
                        'InvestTimeTools', 'WorkPayCare', 'KinshipDevelopers', 'ChallengeMyself', 'CompetePeers',
                        'ChangeWorld', 'JobSeekingStatus',	'HoursPerWeek',	'LastNewJob', 'AssessJobIndustry',
                        'AssessJobRole', 'AssessJobExp',	'AssessJobDept', 'AssessJobTech', 'AssessJobProjects',
                        'AssessJobCompensation',	'AssessJobOffice', 'AssessJobCommute',	'AssessJobRemote',
                        'AssessJobLeaders', 'AssessJobProfDevel', 'AssessJobDiversity', 'AssessJobProduct',
                        'AssessJobFinances', 'ImportantBenefits', 'ClickyKeys', 'JobProfile', 'ResumePrompted',
                        'LearnedHiring', 'ImportantHiringAlgorithms', 'ImportantHiringTechExp',
                        'ImportantHiringCommunication', 'ImportantHiringOpenSource', 'ImportantHiringPMExp',
                        'ImportantHiringCompanies',	'ImportantHiringTitles', 'ImportantHiringEducation',
                        'ImportantHiringRep', 'ImportantHiringGettingThingsDone', 'Currency', 'Overpaid', 'TabsSpaces',
                        'EducationImportant', 'EducationTypes', 'SelfTaughtTypes', 'TimeAfterBootcamp',
                        'CousinEducation', 'WorkStart', 'HaveWorkedLanguage', 'WantWorkLanguage', 'HaveWorkedFramework',
                        'WantWorkFramework', 'HaveWorkedDatabase', 'WantWorkDatabase', 'HaveWorkedPlatform',
                        'WantWorkPlatform', 'IDE', 'AuditoryEnvironment', 'Methodology', 'VersionControl',
                        'CheckInCode', 'ShipIt', 'OtherPeoplesCode', 'ProjectManagement', 'EnjoyDebugging', 'InTheZone',
                        'DifficultCommunication', 'CollaborateRemote', 'MetricAssess', 'EquipmentSatisfiedMonitors',
                        'EquipmentSatisfiedCPU', 'EquipmentSatisfiedRAM', 'EquipmentSatisfiedStorage',
                        'EquipmentSatisfiedRW', 'InfluenceInternet', 'InfluenceWorkstation', 'InfluenceHardware',
                        'InfluenceServers', 'InfluenceTechStack', 'InfluenceDeptTech', 'InfluenceVizTools',
                        'InfluenceDatabase', 'InfluenceCloud', 'InfluenceConsultants', 'InfluenceRecruitment',
                        'InfluenceCommunication', 'StackOverflowDescribes', 'StackOverflowSatisfaction',
                        'StackOverflowDevices', 'StackOverflowFoundAnswer',	'StackOverflowCopiedCode',
                        'StackOverflowJobListing', 'StackOverflowCompanyPage', 'StackOverflowJobSearch',
                        'StackOverflowNewQuestion', 'StackOverflowAnswer', 'StackOverflowMetaChat',
                        'StackOverflowAdsRelevant',	'StackOverflowAdsDistracting',	'StackOverflowModeration',
                        'StackOverflowCommunity',	'StackOverflowHelpful',	'StackOverflowBetter',
                        'StackOverflowWhatDo',	'StackOverflowMakeMoney', 'HighestEducationParents', 'Race',
                        'SurveyLong', 'QuestionsInteresting', 'QuestionsConfusing', 'InterestedAnswers', 'Salary',
                        'ExpectedSalary'], axis=1)


# Remove null/NA values
clean_data.fillna("NaN")
clean_data = clean_data.dropna(axis='rows', how='any')
print('before', clean_data.head())

# One Hot Encoding
# Find all categorical data
categoricals = clean_data.select_dtypes(include=[object])
print(categoricals.columns)

# 'Country', 'FormalEducation', 'MajorUndergrad', 'HomeRemote', 'YearsProgram',
# 'YearsCodedJob', 'DeveloperType', 'Gender' need one hot encoded
# Create a LabelEncoder object and fit it to each feature in X
# 1. INSTANTIATE
# encode labels with value between 0 and n_classes-1.
le = preprocessing.LabelEncoder()
# 2/3. FIT AND TRANSFORM
# use df.apply() to apply le.fit_transform to all columns
clean_data = clean_data.apply(le.fit_transform)
print('after', clean_data.head())





# All headers/features
# print('There are this many features: ', len((list(clean_data))))

# All unique job types
# print("Job Types: ", clean_data["DeveloperType"].unique(), sep="\n")

# # Split into training + Testing

values = clean_data.values

# # gets the feature values - all except the Developer Types
X = values[:, [0, 1, 2, 3, 4, 5, 7, 8, 9]]

# # Gets the labels - gets tuple sliced from structure, column 4 only
Y = values[:, 6]


validation_size = 0.20
seed = 7
X_train, X_validation, Y_train, Y_validation = train_test_split(X, Y, test_size=validation_size, random_state=seed)

print(X_validation[:5])
print(Y_validation[:5])

# Build the model - svm (students should not use on vm)


classifier = SGDClassifier()
classifier.fit(X_train, Y_train)

# Predict the results

predicted = classifier.predict(X_validation)
print(predicted)

# Get Results


#manual
num_correct = 0
for i in range(0, len(Y_validation)):
    if Y_validation[i] == predicted[i]:
        num_correct = num_correct + 1

print("Accuracy:\n%s" % str(float(num_correct) / float(len(Y_validation))))

# use report
print("Accuracy:\n%s" % metrics.accuracy_score(Y_validation, predicted))
# print("Classification report for classifier %s:\n%s\n"
#       % (classifier, metrics.classification_report(Y_validation, predicted)))
print("Confusion matrix:\n%s" % metrics.confusion_matrix(Y_validation, predicted))