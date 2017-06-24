import tkinter as tk
import datetime
import os
import pickle


#add all the frames...
from mistypeCreateFrame import mistypeCreateFrame
from startFrame import startFrame
from retrieveDataFrame import retrieveDataFrame
from mainMenuFrame import mainMenuFrame
from addDailyWeightFrame import addDailyWeightFrame
from addDailyCaloriesFrame import addDailyCaloriesFrame
from visualizeProgressFrame import visualizeProgressFrame
from profileUpdateFrame import profileUpdateFrame

from calorieSubMenuFrame import calorieSubMenuFrame
from modifyCalorieFrame import modifyCalorieFrame

from Profile import Profile

"""
Made by Zachary Kim
email: zkim2@illinois.edu

IMPORTANT: THIS IS CONSIDERED TO BE THE CONTROLLER OF THE PROGRAM.

Will change the file name to something more specific after all is finished.


To do:

1. Create the different frames that will be used
2. Stack and link the frames together
3. Combine the GUI with the command line logic 
4. Make a better design
5. Make executable for easy access and use

"""

class ProfileWindow(tk.Tk): #this is inheriting from the top most level and will be "controller" of other frame instances

	def __init__(self, *args, **kwargs):

		tk.Tk.__init__(self, *args, **kwargs)

		#self.geometry("500x500+300+300")
		self.mainFrame = tk.Frame(self) #all other frames will have this as the parent.

		#self.mainFrame.grid_columnconfigure(0, weight=1)
		#self.mainFrame.grid_rowconfigure(0,weight=1)

		self.mainFrame.grid(row=0, column=0, sticky="nsew")

		self.subFrames = {}

		self.setUpWidgets()

		self.todaysDate = datetime.date.today() #in this class because an instance is created everytime the user logs in so the datetime will be updated.

	def setUpWidgets(self):

		frameBegin = startFrame(self.mainFrame, self)
		
		frameOops = mistypeCreateFrame(self.mainFrame, self)

		frameInfo = retrieveDataFrame(self.mainFrame,self)

		frameMenu = mainMenuFrame(self.mainFrame,self)

		frameDailyWeight = addDailyWeightFrame(self.mainFrame,self)

		frameDailyCalories = addDailyCaloriesFrame(self.mainFrame,self)

		frameVisualize = visualizeProgressFrame(self.mainFrame,self)

		frameUpdateInfo = profileUpdateFrame(self.mainFrame,self)

		frameCalorieMenu = calorieSubMenuFrame(self.mainFrame,self)

		frameCalorieModify = modifyCalorieFrame(self.mainFrame,self)
		
		self.subFrames[startFrame.__name__] = frameBegin
		self.subFrames[mistypeCreateFrame.__name__] = frameOops
		self.subFrames[retrieveDataFrame.__name__] = frameInfo
		self.subFrames[mainMenuFrame.__name__] = frameMenu
		self.subFrames[addDailyWeightFrame.__name__] = frameDailyWeight
		self.subFrames[addDailyCaloriesFrame.__name__] = frameDailyCalories
		self.subFrames[visualizeProgressFrame.__name__] = frameVisualize
		self.subFrames[profileUpdateFrame.__name__] = frameUpdateInfo

		self.subFrames[calorieSubMenuFrame.__name__] = frameCalorieMenu

		self.subFrames[modifyCalorieFrame.__name__] = frameCalorieModify
	
		frameBegin.grid(row=0, column=0,sticky="nsew")

		frameOops.grid(row=0, column=0,sticky="nsew")

		frameInfo.grid(row=0,column=0,sticky="nsew")

		frameMenu.grid(row=0,column=0,sticky="nsew")

		frameDailyWeight.grid(row=0,column=0,sticky="nsew")

		frameDailyCalories.grid(row=0,column=0,sticky="nsew")

		frameVisualize.grid(row=0,column=0,sticky="nsew")

		frameUpdateInfo.grid(row=0,column=0,sticky="nsew")

		frameCalorieMenu.grid(row=0,column=0,sticky="nsew")

		frameCalorieModify.grid(row=0,column=0,sticky="nsew")

		self.raiseWidget("startFrame")
		
		
	def raiseWidget(self, name):

		self.subFrames[name].tkraise()
		


	#THIS SECTION CONTROLS IF USER INPUTS A PROFILE THAT IS NOT IN THE CURRENT DIRECTORY
	def submitProfileValid(self,event): 

		#checks current directory to see if a profile is created under this user. supposed to be in the model but it's easier to load object in the controller
		#in the profile model i would be doing self = pickle.load() which doesn't work.

		potentialProfileName = self.subFrames["startFrame"].loginEntry.get()

		potentialProfileName = potentialProfileName.replace(' ' , '')

		potentialProfileName= potentialProfileName.lower()

		file_name = potentialProfileName + '.pickle'

		cur_dir = os.getcwd()

		inSystem = False

		file_list = os.listdir(cur_dir)

		for file in file_list:

			if(file == file_name):

				inSystem = True
				break

		if(inSystem == False):

			self.userProfile = Profile(name=potentialProfileName) #normal constructor
			self.raiseWidget("mistypeCreateFrame")

		else:
			
			pickle_inProfile = open(potentialProfileName + ".pickle", "rb")

			self.userProfile = pickle.load(pickle_inProfile) #previous object


			self.raiseWidget("mainMenuFrame")

	
	#this button sends to the frame that gets user data
	def infoInput(self,event):

		self.subFrames["retrieveDataFrame"].clearFrame() #always clear it before next input
		self.raiseWidget("retrieveDataFrame")


	def backToStart(self,event):

		self.subFrames["startFrame"].clearFrame()
		self.raiseWidget("startFrame")
			
	def backToProfileValid(self,event):

		self.raiseWidget("mistypeCreateFrame")

	#show mainMenu if going back 

	def backToMainMenu(self,event):

		self.raiseWidget("mainMenuFrame")
			
	def exit(self,event): #have to exit throught quit button to save.

		pickle_Save = open(self.userProfile.name + ".pickle", "wb")
		pickle.dump(self.userProfile, pickle_Save)
		pickle_Save.close()

		#add saveFeature
		exit()
	

	#submit on retrieveDataFrame checks the info.

	def submitInputValid(self,event): 

		inputAge = self.subFrames["retrieveDataFrame"].ageVar.get() #getting info from the view 
		inputWeight = self.subFrames["retrieveDataFrame"].weightVar.get()
		inputHeight = self.subFrames["retrieveDataFrame"].heightVar.get()
		inputGoalWeight = self.subFrames["retrieveDataFrame"].goalWeightVar.get()
		inputActLvl = self.subFrames["retrieveDataFrame"].activityLvlVar.get()
		inputIntensity = self.subFrames["retrieveDataFrame"].intensityVar.get()

		passed = True

		#makes sure input is valid before updating model

		if(inputAge <= 0 or inputAge >=130):
	
			self.subFrames["retrieveDataFrame"].fieldInvalid(1)
			passed=False

		if(inputWeight <=0 or inputWeight >= 1000):
		
			self.subFrames["retrieveDataFrame"].fieldInvalid(2)
			passed=False

		if(inputHeight <= 0 or inputHeight >= 84):

			self.subFrames["retrieveDataFrame"].fieldInvalid(3)
			passed=False

		if(inputGoalWeight >= inputWeight or inputGoalWeight <=0 or inputGoalWeight >= 1000):

			self.subFrames["retrieveDataFrame"].fieldInvalid(4)
			passed=False

		if(inputActLvl < 1 or inputActLvl > 5):

			self.subFrames["retrieveDataFrame"].fieldInvalid(5)
			passed=False

		if(inputIntensity != 500 and inputIntensity != 750 and inputIntensity != 1000):

			self.subFrames["retrieveDataFrame"].fieldInvalid(6)
			passed=False

	
		if(passed):

			#update the model aka profile object
			self.userProfile.age = inputAge
			self.userProfile.currentWeight = inputWeight
			self.userProfile.currentHeight = inputHeight
			self.userProfile.goalWeight = inputGoalWeight
			self.userProfile.actLvl = inputActLvl
			self.userProfile.intensity = inputIntensity

			#save and pickle it
			pickle_Save = open(self.userProfile.name + ".pickle", "wb")
			pickle.dump(self.userProfile, pickle_Save)
			pickle_Save.close()

			print("Success!!!")

			#go to mainMenu
			self.raiseWidget("mainMenuFrame") 


	#Main menu button actions

	def addDailyWeight(self,event):

		self.subFrames["addDailyWeightFrame"].clearFrame()
		self.raiseWidget("addDailyWeightFrame")

	def addDailyCalories(self,event):

		self.subFrames["addDailyCaloriesFrame"].clearFrame()
		self.raiseWidget("addDailyCaloriesFrame")

	def visualizeProgress(self,event):

		self.raiseWidget("visualizeProgressFrame")

	def updateProfileInfo(self,event):

		self.raiseWidget("profileUpdateFrame")


	#profile update button actions

	def sendToCalorieMenu(self,event):

		self.raiseWidget("calorieSubMenuFrame")

	def sendToModifyCalories(self,event):

		self.subFrames["modifyCalorieFrame"].clearFrame()
		self.raiseWidget("modifyCalorieFrame")

	#addDaillyWeightFrame submit action which will update model.

	def submitDailyWeight(self,event):

		userDailyWeight = self.subFrames["addDailyWeightFrame"].weightVar.get()

		self.userProfile.weightData[self.todaysDate] = userDailyWeight

		#add feature that warns user about adding multiple entries on the same day.

		self.subFrames["addDailyWeightFrame"].displaySuccess()


	#addDailyWeightFrame submit action which will update model.

	def submitDailyCalories(self,event):

		userDailyCalories = self.subFrames["addDailyCaloriesFrame"].caloriesVar.get()

		self.userProfile.caloricData[self.todaysDate] = userDailyCalories

		#add feature that warns user about adding multiple entries on the same day.
		
		self.subFrames["addDailyCaloriesFrame"].displaySuccess()


	def submitModifyCalories(self,event):

		dateOfCalories = self.subFrames["modifyCalorieFrame"].dateString.get()

		dateOfCalories = datetime.datetime.strptime(dateOfCalories, '%m/%d/%y') #changes to datetime object

		caloriesToChange = self.subFrames["modifyCalorieFrame"].calorieVar.get()

		self.userProfile.caloricData[dateOfCalories] = caloriesToChange

		print(self.userProfile.caloricData)

		self.subFrames["modifyCalorieFrame"].displaySuccess()


runningApp = ProfileWindow()

runningApp.mainloop()