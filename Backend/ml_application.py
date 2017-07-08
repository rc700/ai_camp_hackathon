from __future__ import print_function

import pandas as pd

from sklearn import preprocessing
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split


def predict(aList):
    # importing in the CSV
    data = pd.read_csv("survey_results_public.csv", index_col=0)


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
    keep = ['Other', 'Web Developer', 'Embedded applications/devices developer', 'Mobile developer',
            'Desktop applications developer', 'DevOps specialist', 'Quality assurance engineer',
            'Machine learning specialist', 'Desktop applications developer', 'Graphics programming',
            'Database administrator', 'Systems administrator']

    clean_data = clean_data[clean_data['DeveloperType'].isin(['Other', 'Web Developer',
                                                              'Embedded applications/devices developer',
                                                              'Mobile developer', 'Desktop applications developer',
                                                              'DevOps specialist', 'Quality assurance engineer',
                                                              'Machine learning specialist',
                                                              'Desktop applications developer', 'Graphics programming',
                                                              'Database administrator', 'Systems administrator'])]


    # Create Array of Unique Jobs
    unique_jobs = clean_data['DeveloperType'].unique()

    # Create Job Dictionary to associate job with id
    job_dict = {}
    counter = len(unique_jobs) - 1
    while counter >=0:
        job_dict[counter] = unique_jobs[counter]
        counter = counter - 1

    # Replace all values in DeveloperType with dictionary key
    clean_data['DeveloperType'].replace('Other', '0', inplace=True)
    clean_data['DeveloperType'].replace('Embedded applications/devices developer', '1', inplace=True)
    clean_data['DeveloperType'].replace('Mobile developer', '2', inplace=True)
    clean_data['DeveloperType'].replace('Desktop applications developer', '3', inplace=True)
    clean_data['DeveloperType'].replace('DevOps specialist', '4', inplace=True)
    clean_data['DeveloperType'].replace('Machine learning specialist', '5', inplace=True)
    clean_data['DeveloperType'].replace('Graphics programming', '6', inplace=True)
    clean_data['DeveloperType'].replace('Quality assurance engineer', '7', inplace=True)
    clean_data['DeveloperType'].replace('Database administrator', '8', inplace=True)
    clean_data['DeveloperType'].replace('Systems administratorr', '9', inplace=True)

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

    predicted = classifier.predict(aList)
    job_prediction = job_dict.get(predicted[0])

    return job_prediction
