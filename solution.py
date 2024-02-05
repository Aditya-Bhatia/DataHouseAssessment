import json     # importing json for .json file handling
import os       # importing os to check for valid file paths


# Function to read team and applicant data from provided json file
def ReadInputData(fileName):
    # check to see if file can be opened. Returns None if file is not found
    try:
        inputData = open(fileName, 'r')
    except FileNotFoundError:
        return None

    # if file is found, returns team and applicant data separately
    data = json.load(inputData)
    inputData.close()
    return data["team"], data["applicants"]


# Function to calculate the average of each attribute across all team members
def TeamAttributeAverages(teamMembers):
    sumIntelligence, sumStrength, sumEndurance, sumSpicyFoodTolerance = 0, 0, 0, 0
    # loops through each team member and adds their attribute to a sum
    for teamMember in teamMembers:
        sumIntelligence += teamMember["attributes"]["intelligence"]
        sumStrength += teamMember["attributes"]["strength"]
        sumEndurance += teamMember["attributes"]["endurance"]
        sumSpicyFoodTolerance += teamMember["attributes"]["spicyFoodTolerance"]

    # returns the average by dividing the sum of each attribute by the total number of team members
    return sumIntelligence / len(teamMembers), sumStrength / len(teamMembers), sumEndurance / len(teamMembers), sumSpicyFoodTolerance / len(teamMembers)


# Function to calculate the applicant compatibility score
def CalculateCompatibility(applicantInformation, averages):
    # multipliers given to add different weightage to each category. I prioritized itelligence, gave equal value to strength and endurance, and gave least priority to spice tolerance
    intelligenceMultiplier = 0.35
    strengthMultiplier = 0.25
    enduranceMultiplier = 0.25
    spicyFoodToleranceMultiplier = 0.15

    # loops through each applicant and creates a base score
    applicantScore = []
    for applicant in applicantInformation:
        # calculates base score by subtarcting the team members' respective attribute's average from the applicant's attribute and then applies the multiplier
        # all attributes are then added up to create the base score
        # this method can create negative score since the multiplier will punish having an attribute below the team average
        # yes, this line is too long, but python does not like random indents
        score = ((applicant["attributes"]["intelligence"] - averages[0]) * intelligenceMultiplier) + ((applicant["attributes"]["strength"] - averages[1]) * strengthMultiplier) + ((applicant["attributes"]["endurance"] - averages[2]) * enduranceMultiplier) + ((applicant["attributes"]["spicyFoodTolerance"] - averages[3]) * spicyFoodToleranceMultiplier)
        applicantScore.append(score)
    
    normalizedScore = []
    # loop to normalize the base scores
    # normalization is done with respect to the base scores of all the applicants
    # the applicant with the lowest base score will always have a compatibility of 0
    # and the applicant with the highest base score will always have a compatibility of 1
    for score in applicantScore:
        nscore = (score - min(applicantScore)) / (max(applicantScore) - min(applicantScore))
        # rounds the score to 2 places after the decimal before appending it to the list
        normalizedScore.append(round(nscore, 2))

    # returns the normalized scores in a list
    return normalizedScore



#---main---
# default file name expected in the same folder as the program
defaultFileName = "input.json"
# loop to check validity of file or to keep asking for a valid file path if given path is invalid
while True:
    # asks for custom file path or the use of default path by pressing Enter
    fileNameInput = input(f"Enter file path (press Enter to use default '{defaultFileName}'): ")
    # if the user pressed Enter use the default file name/path
    if not fileNameInput:
        fileNameInput = defaultFileName
    # check if the user specified path exists. If it doesn't, print an error message and loop back to input statement
    if os.path.exists(fileNameInput):
        # if file does exist, call the ReadInputData function and store the two returns in the processedData tuple
        processedData = ReadInputData(fileNameInput)
        # if the function sucessfully returns the data, we can exit the loop. Otherwise, we print an error message and loop back to the input command
        if processedData is not None:
            break
        else:
             print("Error: The file exists but could not be read.")
    else:
        print("Error: Invalid file. Please try again.")


# assigning the processed data to more appropriate labels
teamMembers, applicantData = processedData[0], processedData[1]

# function call to calculate and store the averages of the team member attributes
attributeAverages = TeamAttributeAverages(teamMembers)

# function call to calculate the final score
finalScores = CalculateCompatibility(applicantData, attributeAverages)

# creates an ouptut file 
with open("scored_applicants.json", 'w') as outputFile:
    # formats the ouput data to a json format
    outputData = {"scoredApplicants" : []}
    # adds all the scores in the format specified by the instructions
    for i in range(len(finalScores)):
        outputData["scoredApplicants"].append({"name" : applicantData[i]["name"], "score" : finalScores[i]})

    # writes the data to the json output file. Uses tab-spacing of 4.
    json.dump(outputData, outputFile, indent=4)