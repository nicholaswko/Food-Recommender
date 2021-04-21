from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QInputDialog, QFileDialog, QMessageBox, QTableWidgetItem

def get_thresh( userId): 
    '''
    Returns the threshold for recommendation for that user based on that user's character.
    '''
    global users
    character = users[users['userId'] == userId]['character'].values[0]
    thresh = (character-0.5)*0.5 + 4
    return thresh 

def get_place_info( placeId, metadata): 
    
    """
    Returns some basic information about the stall given the placeId and the metadata dataframe.
    """
    
    place_info = metadata[metadata.index == placeId][['Stall Name', 
                                                    'Cuisine', 'Shop Type', 'Address']]
    return place_info.to_dict(orient='records')

def predict_review( userId, placeId, model, metadata):

    """
    Predicts the rating (on a scale of 0-5) that a user would assign to a stall. 
    """
    
    review_prediction = model.predict(uid = userId, iid = placeId)
    return review_prediction.est

def generate_recommendation(userId, model, metadata, numTrail):
    
    """
    Generates a stall recommendation for a user based on a rating threshold. Only
    stalls with a predicted rating at or above the threshold will be recommended.
    """
    global reviews
    
    # Get a list of all placeIds
    placeId_list = list(metadata.index)
    
    # Get a list of placeIds that userId has reviewed
    reviewed_list = reviews.loc[reviews['UserId'] == userId, 'StallId']
    
    # Remove the placeIds that userId has review from list of all placeIds
    placeId_list = np.setdiff1d(placeId_list, reviewed_list)
    
    thresh = get_thresh(userId)

    # Create empty list for storage of placeIds
    placeList = list()
    # Storage for info on placeIds in placeList
    placeDict = dict()
    
    for trail in range(numTrail):
        # Remove the placeIds in placeList
        placeId_list = np.setdiff1d(placeId_list, placeList)
        random.shuffle(placeId_list)
        for placeId in placeId_list:
            rating = predict_review(userId, placeId, model, metadata)
            if rating >= thresh:
                placeList.extend([placeId])
                placeDict[trail] = get_place_info(placeId, metadata)
                break
    return placeList, placeDict

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 720)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.BackgroundImage = QtWidgets.QLabel(self.centralwidget)
        self.BackgroundImage.setGeometry(QtCore.QRect(0, 0, 481, 720))
        self.BackgroundImage.setAutoFillBackground(False)
        self.BackgroundImage.setScaledContents(True)
        self.BackgroundImage.setIndent(0)
        self.BackgroundImage.setObjectName("BackgroundImage")
##############################LOGIN GROUP#############################################
        self.LoginGrp = QtWidgets.QGroupBox(self.centralwidget)
        self.LoginGrp.setGeometry(QtCore.QRect(0, 0, 480, 720))
        font = QtGui.QFont()
        font.setKerning(False)
        self.LoginGrp.setFont(font)
        self.LoginGrp.setTitle("")
        self.LoginGrp.setObjectName("LoginGrp")
        self.Title = QtWidgets.QLabel(self.LoginGrp)
        self.Title.setGeometry(QtCore.QRect(50, 60, 391, 61))
        font = QtGui.QFont()
        font.setFamily("Ebrima")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.Title.setFont(font)
        self.Title.setAlignment(QtCore.Qt.AlignCenter)
        self.Title.setObjectName("Title")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.LoginGrp)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(60, 230, 361, 121))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.UserID = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.UserID.setContentsMargins(0, 0, 0, 0)
        self.UserID.setSpacing(27)
        self.UserID.setObjectName("UserID")
        self.UserID_label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.UserID_label.setFont(font)
        self.UserID_label.setObjectName("UserID_label")
        self.UserID.addWidget(self.UserID_label)
        self.UserID_input = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.UserID_input.sizePolicy().hasHeightForWidth())
        self.UserID_input.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.UserID_input.setFont(font)
        self.UserID_input.setText("")
        self.UserID_input.setFrame(False)
        self.UserID_input.setClearButtonEnabled(True)
        self.UserID_input.setObjectName("UserID_input")
        self.UserID.addWidget(self.UserID_input)
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.LoginGrp)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(60, 320, 361, 121))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.Password = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.Password.setContentsMargins(0, 0, 0, 0)
        self.Password.setObjectName("Password")
        self.Password_label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.Password_label.setFont(font)
        self.Password_label.setObjectName("Password_label")
        self.Password.addWidget(self.Password_label)
        self.Password_input = QtWidgets.QLineEdit(self.horizontalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Password_input.sizePolicy().hasHeightForWidth())
        self.Password_input.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Password_input.setFont(font)
        self.Password_input.setText("")
        self.Password_input.setFrame(False)
        self.Password_input.setClearButtonEnabled(True)
        self.Password_input.setObjectName("Password_input")
        self.Password.addWidget(self.Password_input)
        self.Recommend_button = QtWidgets.QPushButton(self.LoginGrp)
        self.Recommend_button.setGeometry(QtCore.QRect(150, 500, 171, 34))
        font = QtGui.QFont()
        font.setFamily("Ebrima")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.Recommend_button.setFont(font)
        self.Recommend_button.setObjectName("Recommend_button")
        self.Recommend_button.clicked.connect(self.login)
##############################RATING GROUP############################################
        self.RatingGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.RatingGroup.setEnabled(True)
        self.RatingGroup.setGeometry(QtCore.QRect(0, 0, 480, 720))
        font = QtGui.QFont()
        font.setKerning(False)
        self.RatingGroup.setFont(font)
        self.RatingGroup.setTitle("")
        self.RatingGroup.setObjectName("RatingGroup")
        self.RatingGroup.hide()
        self.Recommnedation_Label = QtWidgets.QLabel(self.RatingGroup)
        self.Recommnedation_Label.setGeometry(QtCore.QRect(40, 60, 391, 61))
        font = QtGui.QFont()
        font.setFamily("Ebrima")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.Recommnedation_Label.setFont(font)
        self.Recommnedation_Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Recommnedation_Label.setObjectName("Recommnedation_Label")
        self.AskingReviewLabel = QtWidgets.QLabel(self.RatingGroup)
        self.AskingReviewLabel.setGeometry(QtCore.QRect(60, 150, 361, 231))
        font = QtGui.QFont()
        font.setFamily("Ebrima")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.AskingReviewLabel.setFont(font)
        self.AskingReviewLabel.setTextFormat(QtCore.Qt.AutoText)
        self.AskingReviewLabel.setWordWrap(True)
        self.AskingReviewLabel.setObjectName("AskingReviewLabel")
        self.Score = QtWidgets.QDoubleSpinBox(self.RatingGroup)
        self.Score.setGeometry(QtCore.QRect(180, 400, 112, 34))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.Score.setFont(font)
        self.Score.setDecimals(1)
        self.Score.setMaximum(5.0)
        self.Score.setSingleStep(0.5)
        self.Score.setObjectName("Score")
        self.pushButton = QtWidgets.QPushButton(self.RatingGroup)
        self.pushButton.setGeometry(QtCore.QRect(180, 470, 112, 34))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.rate)
###########################Recommendation Group#######################################
        self.Recommendations_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.Recommendations_2.setGeometry(QtCore.QRect(0, 0, 480, 720))
        self.Recommendations_2.setTitle("")
        self.Recommendations_2.setObjectName("Recommendations_2")
        self.Recommendations_2.hide()
        self.Recommnedation_Label_3 = QtWidgets.QLabel(self.Recommendations_2)
        self.Recommnedation_Label_3.setGeometry(QtCore.QRect(50, 60, 391, 61))
        font = QtGui.QFont()
        font.setFamily("Ebrima")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.Recommnedation_Label_3.setFont(font)
        self.Recommnedation_Label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.Recommnedation_Label_3.setObjectName("Recommnedation_Label_3")
        self.Stall_Label_2 = QtWidgets.QLabel(self.Recommendations_2)
        self.Stall_Label_2.setGeometry(QtCore.QRect(30, 180, 71, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.Stall_Label_2.setFont(font)
        self.Stall_Label_2.setObjectName("Stall_Label_2")
        self.StallName_2 = QtWidgets.QLabel(self.Recommendations_2)
        self.StallName_2.setGeometry(QtCore.QRect(130, 170, 341, 70))
        font = QtGui.QFont()
        font.setFamily("Ebrima")
        font.setBold(True)
        font.setPointSize(14)
        self.StallName_2.setFont(font)
        self.StallName_2.setScaledContents(True)
        self.StallName_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.StallName_2.setWordWrap(True)
        self.StallName_2.setObjectName("StallName_2")
        self.Rating_Label_2 = QtWidgets.QLabel(self.Recommendations_2)
        self.Rating_Label_2.setGeometry(QtCore.QRect(30, 250, 101, 51))
        font = QtGui.QFont()
        font.setFamily("Ebrima")
        font.setBold(True)
        font.setPointSize(14)
        self.Rating_Label_2.setFont(font)
        self.Rating_Label_2.setObjectName("Rating_Label_2")
        self.Score_3 = QtWidgets.QLabel(self.Recommendations_2)
        self.Score_3.setGeometry(QtCore.QRect(130, 250, 341, 51))
        font = QtGui.QFont()
        font.setFamily("Ebrima")
        font.setBold(True)
        font.setPointSize(14)
        self.Score_3.setFont(font)
        self.Score_3.setScaledContents(True)
        self.Score_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.Score_3.setWordWrap(True)
        self.Score_3.setObjectName("Score_3")
        self.Location_Label_2 = QtWidgets.QLabel(self.Recommendations_2)
        self.Location_Label_2.setGeometry(QtCore.QRect(30, 330, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Ebrima")
        font.setBold(True)
        font.setPointSize(14)
        self.Location_Label_2.setFont(font)
        self.Location_Label_2.setObjectName("Location_Label_2")
        self.Location_2 = QtWidgets.QLabel(self.Recommendations_2)
        self.Location_2.setGeometry(QtCore.QRect(130, 330, 341, 171))
        font = QtGui.QFont()
        font.setFamily("Ebrima")
        font.setBold(True)
        font.setPointSize(14)
        self.Location_2.setFont(font)
        self.Location_2.setScaledContents(True)
        self.Location_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.Location_2.setWordWrap(True)
        self.Location_2.setObjectName("Location_2")

        self.link_label = QtWidgets.QLabel(self.Recommendations_2)
        self.link_label.setGeometry(QtCore.QRect(30, 450, 121, 31))
        font = QtGui.QFont()
        font.setFamily("Ebrima")
        font.setBold(True)
        font.setPointSize(14)
        self.link_label.setFont(font)
        self.link_label.setObjectName("linklabel")
        self.link = QtWidgets.QLabel(self.Recommendations_2)
        self.link.setGeometry(QtCore.QRect(130, 450, 300, 200))
        font = QtGui.QFont()
        font.setFamily("Ebrima")
        font.setBold(True)
        font.setPointSize(14)
        self.link.setFont(font)
        self.link.setScaledContents(True)
        self.link.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.link.setWordWrap(True)
        self.link.setObjectName("link")
        self.link.setOpenExternalLinks(True)


        self.pushButton_4 = QtWidgets.QPushButton(self.Recommendations_2)
        self.pushButton_4.setGeometry(QtCore.QRect(60, 510, 180, 40))
        font = QtGui.QFont()
        font.setFamily("Ebrima")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.new_location)
        self.pushButton_5 = QtWidgets.QPushButton(self.Recommendations_2)
        self.pushButton_5.setGeometry(QtCore.QRect(250, 510, 180, 40))
        font = QtGui.QFont()
        font.setFamily("Ebrima")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.selected_restaurant)
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 480, 31))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
#################################UI Looks#############################################
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        pixmap = QPixmap("files/blurred_background.jpg")
        self.BackgroundImage.setPixmap(pixmap)
        self.Title.setText(_translate("MainWindow", "SG Food Recommneder"))
        self.UserID_label.setText(_translate("MainWindow", "User ID:"))
        self.Password_label.setText(_translate("MainWindow", "Password:"))
        self.Recommend_button.setText(_translate("MainWindow", "Recommend Me!"))
        self.Recommnedation_Label.setText(_translate("MainWindow", "Rate Your Meal!"))
        self.AskingReviewLabel.setText(_translate("MainWindow", "How did you enjoy the food at Pastamania West Mall"))
        self.pushButton.setText(_translate("MainWindow", "Rate"))
        self.Recommnedation_Label_3.setText(_translate("MainWindow", "Recommendations"))
        self.Stall_Label_2.setText(_translate("MainWindow", "Stall:"))
        self.StallName_2.setText(_translate("MainWindow", "Stall Name"))
        self.Rating_Label_2.setText(_translate("MainWindow", "Rating:"))
        self.Score_3.setText(_translate("MainWindow", "score"))
        self.Location_Label_2.setText(_translate("MainWindow", "Location:"))
        self.Location_2.setText(_translate("MainWindow", "Location test test test test test test test test test test"))
        self.link_label.setText("Google:")
        self.pushButton_4.setText(_translate("MainWindow", "NAH!"))
        self.pushButton_5.setText(_translate("MainWindow", "LOOKS GOOD!"))
#############################BUTTON FUNCTIONS#########################################    
    def login(self):
        global users
        global user_id
        global locations
        global reclist

        new_id = (self.UserID_input.text())
        
        if(new_id == "" or int(new_id) not in users.index):
            msg = QMessageBox()
            missing_fields = msg.setWindowTitle("Invalid Id")
            warning = msg.setIcon(QMessageBox.Warning)
            missing_fields
            warning
            msg.setText("Enter a valid ID")
            x = msg.exec_()
        else:
            self.LoginGrp.hide()
            user_id = int(new_id)

            reclist, adict = generate_recommendation(user_id, svd_model, locations, 1)
            self.StallName_2.setText(locations.loc[reclist[0], "Stall Name"])
            self.Score_3.setText(str(locations.loc[reclist[0], "Average Review"]))
            self.Location_2.setText(locations.loc[reclist[0], "Address"])
            self.link.setText(f"<a href=\"https://www.google.com/search?source=hp&ei=RMtRYMaDCML69QPxvYzQBQ&iflsig=AINFCbYAAAAAYFHZVCGjKdQ7SCTBw9cWYUrAyDMsHWCs&q={locations.loc[reclist[0], 'Stall Name']}\">Find Out More!</a>")#)
            self.Recommendations_2.show()

    def new_location(self):
        if swapper % 2 == 0:
            reclist, adict = generate_recommendation(user_id, svd_model, locations, 1)
            self.StallName_2.setText(locations.loc[reclist[0], "Stall Name"])
            self.Score_3.setText(str(locations.loc[reclist[0], "Average Review"]))
            self.Location_2.setText(locations.loc[reclist[0], "Address"])
            self.link.setText(f"<a href=\"https://www.google.com/search?source=hp&ei=RMtRYMaDCML69QPxvYzQBQ&iflsig=AINFCbYAAAAAYFHZVCGjKdQ7SCTBw9cWYUrAyDMsHWCs&q={locations.loc[reclist[0], 'Stall Name']}\">Find Out More!</a>")#)
            # self.Recommendations_2.show()
        else:
            reclist, adict = generate_recommendation(user_id, knn_model, locations, 1)
            self.StallName_2.setText(locations.loc[reclist[0], "Stall Name"])
            self.Score_3.setText(str(locations.loc[reclist[0], "Average Review"]))
            self.Location_2.setText(locations.loc[reclist[0], "Address"])
            self.link.setText(f"<a href=\"https://www.google.com/search?source=hp&ei=RMtRYMaDCML69QPxvYzQBQ&iflsig=AINFCbYAAAAAYFHZVCGjKdQ7SCTBw9cWYUrAyDMsHWCs&q={locations.loc[reclist[0], 'Stall Name']}\">Find Out More!</a>")#)
            # self.Recommendations_2.show()

    def selected_restaurant(self):
        location = self.StallName_2.text()
        self.AskingReviewLabel.setText(f"How did you enjoy the food at {location}")
        self.Recommendations_2.hide()
        self.RatingGroup.show()

    def rate(self):
        self.Recommnedation_Label.hide()
        self.Score.hide()
        self.pushButton.hide()
        self.AskingReviewLabel.setAlignment(Qt.AlignCenter)
        self.AskingReviewLabel.setText("Thank You For Using The App! Expect better recommendations over time!")
        
if __name__ == "__main__":
    import sys
    import pandas as pd
    import pickle
    import difflib
    import random
    import numpy as np

    user_id = -1
    swapper = 1

    users = pd.read_csv("files/userDf_new_V2.csv")
    locations = pd.read_csv("files/Final_list.csv")
    reviews = pd.read_csv("files/User Reviews Final.csv")

    model_file = open("files/svd_model.pkl", "rb")
    svd_model = pickle.load(model_file)
    model_file.close()

    model_file = open("files/knn_model.pkl", "rb")
    knn_model = pickle.load(model_file)
    model_file.close()
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
