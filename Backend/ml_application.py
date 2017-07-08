from __future__ import print_function

import pandas as pd

from sklearn import preprocessing
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split

# importing in the CSV
data = pd.read_csv("survey_results_public.csv", index_col=0)

# print(type(data))


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

# Remove rows with invalid job types
clean_data = clean_data[~(clean_data['DeveloperType'] != 'Other' or 'Web Developer' or
                          'Embedded applications/devices developer' or 'Mobile developer' or
                          'Desktop applications developer' or 'DevOps specialist' or 'Quality assurance engineer' or
                          'Machine learning specialist' or 'Desktop applications developer' or 'Graphics programming' or
                          'Database administrator' or 'Systems administrator').any(axis=1)]

print(clean_data.head(30))

# Create Array of Unique Jobs
unique_jobs = clean_data['DeveloperType'].unique()
print(unique_jobs[:100])

# Create Job Dictionary to associate job with id
job_dict = {}
counter = len(unique_jobs) - 1
while counter >=0:
    job_dict[counter] = unique_jobs[counter]
    counter = counter - 1

# Replace all values in DeveloperType with dictionary key



# One Hot Encoding
# Find all categorical data
categoricals = clean_data.select_dtypes(include=[object])

# Create a LabelEncoder object and fit it to each feature
le = preprocessing.LabelEncoder()

# apply le.fit_transform to all columns
clean_data = clean_data.apply(le.fit_transform)

# # Split into training + Testing

values = clean_data.values

# # gets the feature values - all except the Developer Types
X = values[:, [0, 1, 2, 3, 4, 5]]

# # Gets the labels - gets tuple sliced from structure, column 4 only
Y = values[:, 6]


validation_size = 0.20
seed = 7
X_train, X_validation, Y_train, Y_validation = train_test_split(X, Y, test_size=validation_size, random_state=seed)

# Build the model - svm (students should not use on vm)
classifier = SGDClassifier()
classifier.fit(X_train, Y_train)

# Predict the results
me = [1, 2, 3, 4, 5, 6]

predicted = classifier.predict(me)
# print(clean_data['DeveloperType'].unique())
