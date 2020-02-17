from tkinter import *
from tkinter import ttk
from tkinter.ttk import * 
import joblib
import numpy as np


# ROOT WINDOW 
root= Tk()
root.geometry('1100x800')
root.title("MENTAL HEALTH DISORDERS PREDICTOR")
root.configure (background = '#f5f5b5')

# HEADING 
lbl = ttk.Label(root, text="MENTAL HEALTH DISORDERS PREDICTOR" ,font=("Arial Bold", 25), background='#f5f5b5')
lbl.pack(pady=20)

# INSTRUCTION 
lbl = ttk.Label(root, text="How to use?", font=("Arial Bold", 18), background='#f5f5b5')
lbl.pack(pady=5)

lbl = ttk.Label(root, background='#f5f5b5', text="1. Answer ALL questions and click ANALYZE button.", font=("Arial", 11))
lbl.pack()
lbl = ttk.Label(root, background='#f5f5b5', text="2. There are two diseases to choose from: Depression and Seizure Disorder. Choose the correct tab below.", font=("Arial", 11))
lbl.pack()
lbl = ttk.Label(root, background='#f5f5b5', text="3. All questions are tailored to the appropriate model and related to the patient's lifestyle.", font=("Arial", 11))
lbl.pack()
lbl = ttk.Label(root, background='#f5f5b5', text="4. Based on historical data, the model predicts whether the patient may or may not have the selected disorder.", font=("Arial", 11))
lbl.pack(pady=(0, 10))

notebook = ttk.Notebook(root, width=1000, height=550)
notebook.pack()
                
                
# DEPRESSION TAB
panedwindow1 = ttk.Panedwindow(notebook, orient = HORIZONTAL)
panedwindow1.pack(fill = BOTH, expand = True)
notebook.add(panedwindow1, text='DEPRESSION')


frame = ttk.Frame(panedwindow1, width = 400, height = 300, relief = SUNKEN, )
frame2 = ttk.Frame(panedwindow1, width = 400, height = 300, relief = SUNKEN)
panedwindow1.add(frame, weight = 1)
panedwindow1.add(frame2, weight = 1)


# seizuredisorder TAB

panedwindow2 = ttk.Panedwindow(notebook, orient = HORIZONTAL)
panedwindow2.pack(fill = BOTH, expand = True)
notebook.add(panedwindow2, text='SEIZURE DISORDER')


frame3 = ttk.Frame(panedwindow2, width = 400, height = 300, relief = SUNKEN)
frame4 = ttk.Frame(panedwindow2, width = 400, height = 300, relief = SUNKEN)
panedwindow2.add(frame3, weight = 1)
panedwindow2.add(frame4, weight = 1)



# Define functions for "Depression" Part 
def predictdepression (x):
    # Load the model from file
    SVC = joblib.load('SVM_model1.pkl')
    print (SVC)
    test_patient = np.array(x).reshape(1,-1)
    #predict
    prediction = SVC.predict(test_patient)
    print (prediction)
    result = prediction[0]
    #print results
    print (result)
    
    if result == 0:
        messagebox.showinfo("Title", "The model prediction: NO DEPRESSION")
    elif result == 1:
         messagebox.showinfo("Title", "The model prediction: DEPRESSION")
    
    
def callback ():
    sex1 =sex.get()
    married = marr.get()
    livin = living.get()
    past_d1 = pastd.get()
    db = diab.get()
    mobile1 = mobile.get()
    age_gr = agegroup.get()
   
    sales = jsands.get()
    mp = managment.get()
    hbp1 = hbp.get()
    stud = st.get()
    he1 = he.get()
    suicide1 = suicide.get()
    stype1 = stype.get()
    subM = submar.get()
    par = parentss.get()
    arrest = arrested.get()
    empl_stat= employm.get()

    age_group = 0
    mobileu = 0
    edul = 0
    suidF = 0
    suidE = 0
    fd = 0
    md = 0
    employment = 0
    selfe = 0
    
#Set values for employment status

    if empl_stat == 'Unemployed':
        employment = 0
        selfe = 0
    elif empl_stat =='Employed' :
        employment = 1
        selfe = 0
    elif empl_stat == 'Self-Employed' :
        employment = 0
        selfe = 1

#Set values for age groups

    if age_gr == '0-20':
        age_group  =1
    elif age_gr =='21-30' :
        age_group  = 2
    elif age_gr == '31-40' :
        age_group  = 3
    elif age_gr == '41-60' :
        age_group  = 4
    elif age_gr == '60+':
        age_group  = 5
#Set values for mobile use

    if mobile1 == 'None':
        mobileu = 1
    elif mobile1 =='Low' :
        mobileu = 2
    elif mobile1 == 'Medium' :
        mobileu = 3
    elif mobile1 == 'High' :
        mobileu = 4
    elif mobile1 == 'Very High':
        mobileu = 5

#Set values for education level
    if he1 == 'Uneducated':
        edul =1
    elif he1 =='Primary' :
        edul = 2
    elif he1 == 'Secondary' :
        edul = 3
    elif he1 == 'Higher Education' :
        edul = 4


#Set values for suicide type
    if stype1 == 'Fatalistic':
        suidF = 1
        suidE = 0
    elif stype1 =='Egoistic' :
        suidF = 0
        suidE = 1
    elif stype1 == 'Other' :
        suidF = 0
        suidE = 0
   
#Set values for father and mother deceased or alive
    if par  == 'Yes':
        fd = 0
        md = 0
    elif par =='No' :
        fd = 1
        md = 1
    elif par == 'Only Mother' :
        fd = 1
        md = 0
    elif par == 'Only Father' :
        fd = 0
        md = 1

    if suicide1 == 0:
        suidF = 0
        suidE = 0

    # create the list of values in the right order 
    patient2 = [int(married), int(past_d1), int(age_group), int(stud),int(selfe),int(sex1),int(employment), int(subM),int(fd), int(suidE), int(hbp1), int(mobileu), int(edul),int(md),int(sales), int(livin), int(mp),int(arrest), int(suidF), int(db)]
    print (patient2)
    
    #call function predictdepression - a list to sent as an argument 
    return predictdepression(patient2)

## !!!! DEPRESSION PART  - QUESTIONS !!!!

# Q1
label = ttk.Label(frame, text="1. Sex : ")
label.pack(pady=5)
sex = StringVar()
ttk.Radiobutton(frame, text='male', variable=sex, value='1').pack()
ttk.Radiobutton(frame, text='female', variable=sex, value='0').pack()

#Q2
label = ttk.Label(frame, text="2. What is the patient's age group?")
label.pack()
agegroup = StringVar()
combobox = ttk.Combobox(frame, textvariable= agegroup)
combobox.pack()
combobox.config(values = ('0-20', '21-30' , '31-40' , '41-60' , '60+'))

#Q3
label = ttk.Label(frame, text="3. Is the patient married?")
label.pack()
marr = StringVar()
ttk.Radiobutton(frame, text='Yes', variable=marr, value='1').pack()
ttk.Radiobutton(frame, text='No', variable=marr, value='0').pack()


#Q4

label = ttk.Label(frame, text="4. Does the patient live with the partner?")
label.pack()
living = StringVar()
ttk.Radiobutton(frame, text='Yes', variable=living, value='1').pack()
ttk.Radiobutton(frame, text='No', variable=living, value='0').pack()

#Q5
label = ttk.Label(frame, text="5. Are the patient's parents alive??")
label.pack()
parentss = StringVar()
combobox = ttk.Combobox(frame, textvariable= parentss)
combobox.pack()
combobox.config(values = ('Yes', 'Only Mother' , 'Only Father' , 'No'))


#Q6
label = ttk.Label(frame, text="6. Has the patient been diagnosed with depression in the past?")
label.pack()
pastd = StringVar()
ttk.Radiobutton(frame, text='Yes', variable=pastd, value='1').pack()
ttk.Radiobutton(frame, text='No', variable=pastd, value='0').pack()

#Q7

label = ttk.Label(frame, text="7. Has the patient been diagnosed with chronic disease: High Blood Pressure?'?")
label.pack()
hbp = StringVar()
ttk.Radiobutton(frame, text='Yes', variable=hbp, value='1').pack()
ttk.Radiobutton(frame, text='No', variable=hbp, value='0').pack()

#Q8

label = ttk.Label(frame, text="8. Is the patient diabetic?")
label.pack()
diab = StringVar()
ttk.Radiobutton(frame, text='Yes', variable=diab , value='1').pack()
ttk.Radiobutton(frame, text='No', variable=diab , value='0').pack()    
   
#Q9
label = ttk.Label(frame, text="9. How often does the patient use a mobile phone?")
label.pack()
mobile = StringVar()
combobox = ttk.Combobox(frame, textvariable= mobile)
combobox.pack()
combobox.config(values = ('None', 'Low' , 'Medium' , 'High' , 'Very High'))


#Q10
label = ttk.Label(frame2, text="10. Patient's employment status:")
label.pack(pady=5)
employm = StringVar()
combobox = ttk.Combobox(frame2, textvariable= employm)
combobox.pack()
combobox.config(values = ('Self-Employed', 'Employed' , 'Unemployed'))

#Q11
label = ttk.Label(frame2, text="11. If NOT unemployed: Does the patient work in the sector Sales and service?")
label.pack()
jsands = StringVar()
ttk.Radiobutton(frame2, text='Yes', variable=jsands, value='1').pack()
ttk.Radiobutton(frame2, text='No', variable=jsands, value='0').pack()

#Q12

label = ttk.Label(frame2, text="12. If NOT unemployed: Is it management position?")
label.pack()
managment = StringVar()
ttk.Radiobutton(frame2, text='Yes', variable=managment, value='1').pack()
ttk.Radiobutton(frame2, text='No', variable=managment, value='0').pack()


#Q13
label = ttk.Label(frame2, text="13. Is the patient a student?")
label.pack()
st = StringVar()
ttk.Radiobutton(frame2, text='Yes', variable=st, value='1').pack()
ttk.Radiobutton(frame2, text='No', variable=st, value='0').pack()


#Q14

label = ttk.Label(frame2, text="14. What's the highest education level?")
label.pack()
he = StringVar()
combobox = ttk.Combobox(frame2, textvariable= he)
combobox.pack()
combobox.config(values = ('Uneducated', 'Primary' , 'Secondary' , 'Higher Education'))


#Q15
 
label = ttk.Label(frame2, text="15. Any suicide attempts?")
label.pack()
suicide = StringVar()
ttk.Radiobutton(frame2, text='Yes', variable=suicide, value='1').pack()
ttk.Radiobutton(frame2, text='No', variable=suicide, value='0').pack()


#Q16
label = ttk.Label(frame2, text="16. If YES: What type of suicide attempt was this?")
label.pack()
stype = StringVar()
combobox = ttk.Combobox(frame2, textvariable= stype)
combobox.pack()
combobox.config(values = ('Egoistic', 'Fatalistic' , 'Other'))


#Q17

label = ttk.Label(frame2, text="17. Has patient used a psychoactive substances? Specifically Marijuana?")
label.pack()
submar = StringVar()
ttk.Radiobutton(frame2, text='Yes', variable=submar, value='1').pack()
ttk.Radiobutton(frame2, text='No', variable=submar, value='0').pack()



#Q18
label = ttk.Label(frame2, text="18. Has the patient been arrested in the past?")
label.pack()
arrested = StringVar()
ttk.Radiobutton(frame2, text='Yes', variable=arrested, value='1').pack()
ttk.Radiobutton(frame2, text='No', variable=arrested, value='0').pack()


# Button with callback function 
ttk.Button(frame2, text= 'Analyze!', command = lambda: callback()).pack()

# Define functions for SEIZURE DISORDER part
def predictsd (x):
    # Load the model from file
    LR = joblib.load('LR_modelsd.pkl')
    print (LR)
    test_patient = np.array(x).reshape(1,-1)
    #make prediction
    prediction = LR.predict(test_patient)
    print (prediction)
    result = prediction[0]
    #print the result of prediction in a user-friendly way
    print (result)
    
    if result == 0:
        messagebox.showinfo("Title", "The model prediction: NO SEIZURE DISORDER")
    elif result == 1:
         messagebox.showinfo("Title", "The model prediction: SEIZURE DISORDER")

    
    
def callback1 ():
    igbo1 =igbo.get()
    age1 = age.get()
    married1 = married.get()
    living1 = liv.get()
    parents1 = parents.get()
    fam1 = fam.get()
    mobile1 = mobile.get()
    emplstat= employment.get()
    js1 = js.get()
    mp1 = mp.get()
    student1 = student.get()
    he1 = he.get()
    prsch1 = prsch.get()
    sch1 = sch.get()
    subPS1 = subPS.get()
    arr1 = arr.get()


    agegr = 0
    mobileu = 0
    edul = 0
    fathd = 0
    motd = 0
    empl = 0
    selfe = 0
    prpub = 0
    prpriv = 0
    
#Set values for employment status

    if emplstat == 'Unemployed':
        empl = 0
        selfe = 0
        js1 = 0
        mp1 = 0
    elif emplstat =='Employed' :
        empl = 1
        selfe = 0
    elif emplstat == 'Self-Employed' :
        empl = 0
        selfe = 1

#Set values for age groups

    if age1 == '0-20':
        agegr =1
    elif age1 =='21-30' :
        agegr = 2
    elif age1 == '31-40' :
        agegr = 3
    elif age1 == '41-60' :
        agegr = 4
    elif age == '60+':
        agegr = 5
#Set values for mobile use

    if mobile1 == 'None':
        mobileu =1
    elif mobile1 =='Low' :
        mobileu = 2
    elif mobile1 == 'Medium' :
        mobileu = 3
    elif mobile1 == 'High' :
        mobileu = 4
    elif mobile1 == 'Very High':
        mobileu = 5

#Set values for education level
    if he1 == 'Uneducated':
        edul =1
        prpub = 0
        prpriv = 0
    elif he1 =='Primary' :
        edul = 2
    elif he1 == 'Secondary' :
        edul = 3
    elif he1 == 'Higher Education' :
        edul = 4

#Set values for father and mother deceased or alive
    if parents1  == 'Yes':
        fathd = 0
        motd = 0
    elif parents1 =='No' :
        fathd = 1
        motd = 1
    elif parents1 == 'Only Mother' :
        fathd = 1
        motd = 0
    elif parents1 == 'Only Father' :
        fathd = 0
        motd = 1


# Set values for primaryschool 
        
    if prsch1 == 'Public':
        prpub = 1
        prpriv = 0
    elif prsch1 == 'Private':
        prpub = 0
        prpriv = 1
        
    patient = [int(agegr),int(student1),int(married1), int(fathd),int(edul),int(mobileu), int(selfe), int(motd), int(prpub), int(empl),int(subPS1), int(prpriv),int(arr1), int(sch1), int(mp1), int(igbo1), int(fam1), int(living1), int(js1) ]
    #patient = [(agegr),(student1),(married1), (fathd),(edul),(mobileu), (selfe),(motd), (prpub), (empl),(subPS1), (prpriv),(arr1), (sch1), (mp1), (igbo1), (fam1), (living1), (js1) ]
    print (patient)
    # call function predictsd
    return predictsd(patient)


# !!!! SCHEIZURE DISORDER PART - QUESTIONS !!!!

# Q1
label = ttk.Label(frame3, text="1. Is the patient from an Igbo tribe?")
label.pack(pady=5)
igbo = StringVar()
ttk.Radiobutton(frame3, text='Yes', variable=igbo, value='1').pack()
ttk.Radiobutton(frame3, text='No', variable=igbo, value='0').pack()

#Q2
label = ttk.Label(frame3, text="2. What is the patient's age group?")
label.pack()
age = StringVar()
combobox = ttk.Combobox(frame3, textvariable= age)
combobox.pack()
combobox.config(values = ('0-20', '21-30' , '31-40' , '41-60' , '60+'))

#Q3
label = ttk.Label(frame3, text="3. Is the patient married?")
label.pack()
married = StringVar()
ttk.Radiobutton(frame3, text='Yes', variable=married, value='1').pack()
ttk.Radiobutton(frame3, text='No', variable=married, value='0').pack()


#Q4

label = ttk.Label(frame3, text="4. Does the patient live with the Relatives?")
label.pack()
liv = StringVar()
ttk.Radiobutton(frame3, text='Yes', variable=liv, value='1').pack()
ttk.Radiobutton(frame3, text='No', variable=liv, value='0').pack()

#Q5
label = ttk.Label(frame3, text="5. Are the patient's parents alive?")
label.pack()
parents = StringVar()
combobox = ttk.Combobox(frame3, textvariable= parents)
combobox.pack()
combobox.config(values = ('Yes', 'Only Mother' , 'Only Father' , 'No'))


#Q6
label = ttk.Label(frame3, text="6. Is the patient from a monogamous family?")
label.pack()
fam = StringVar()
ttk.Radiobutton(frame3, text='Yes', variable=fam, value='1').pack()
ttk.Radiobutton(frame3, text='No', variable=fam, value='0').pack()


   
#Q7 
label = ttk.Label(frame3, text="7. How often does the patient use a mobile phone?")
label.pack()
mobile = StringVar()
combobox = ttk.Combobox(frame3, textvariable= mobile)
combobox.pack()
combobox.config(values = ('None', 'Low' , 'Medium' , 'High' , 'Very High'))


#Q8
label = ttk.Label(frame3, text="8. Patient's employment status:")
label.pack()
employment = StringVar()
combobox = ttk.Combobox(frame3, textvariable= employment)
combobox.pack()
combobox.config(values = ('Self-Employed', 'Employed' , 'Unemployed'))

#Q9
label = ttk.Label(frame4, text="9. If NOT unemployed: Does the patient work in the sector Sales and service?")
label.pack(pady=5)
js = StringVar()
ttk.Radiobutton(frame4, text='Yes', variable=js, value='1').pack()
ttk.Radiobutton(frame4, text='No', variable=js, value='0').pack()

#Q10

label = ttk.Label(frame4, text="10. If NOT unemployed: Is it management position?")
label.pack()
mp = StringVar()
ttk.Radiobutton(frame4, text='Yes', variable=mp, value='1').pack()
ttk.Radiobutton(frame4, text='No', variable=mp, value='0').pack()



#Q11
label = ttk.Label(frame4, text="11. Is the patient a student?")
label.pack()
student = StringVar()
ttk.Radiobutton(frame4, text='Yes', variable=student, value='1').pack()
ttk.Radiobutton(frame4, text='No', variable=student, value='0').pack()


#Q12

label = ttk.Label(frame4, text="12. What's the highest education level?")
label.pack()
he = StringVar()
combobox = ttk.Combobox(frame4, textvariable= he)
combobox.pack()
combobox.config(values = ('Uneducated', 'Primary' , 'Secondary' , 'Higher Education'))



#Q13
label = ttk.Label(frame4, text="13. If UNEDUCATED leave blank* Type of Primary School?")
label.pack()
prsch = StringVar()
combobox = ttk.Combobox(frame4, textvariable= prsch)
combobox.pack()
combobox.config(values = ('Public', 'Private' ))


#Q14
label = ttk.Label(frame4, text="14. Did the patient have any seizure attacks?")
label.pack()
sch = StringVar()
ttk.Radiobutton(frame4, text='Yes', variable=sch, value='1').pack()
ttk.Radiobutton(frame4, text='No', variable=sch, value='0').pack()


#Q15

label = ttk.Label(frame4, text="15. Has patient used a psychoactive substances? Specifically Marijuana?")
label.pack()
subPS = StringVar()
ttk.Radiobutton(frame4, text='Yes', variable=subPS, value='1').pack()
ttk.Radiobutton(frame4, text='No', variable=subPS, value='0').pack()



#Q16
label = ttk.Label(frame4, text="16. Has the patient been arrested in the past?")
label.pack()
arr = StringVar()
ttk.Radiobutton(frame4, text='Yes', variable=arr, value='1').pack()
ttk.Radiobutton(frame4, text='No', variable=arr, value='0').pack()


# Button with the callback1 function
ttk.Button(frame4, text= 'Analyze!', command = lambda: callback1()).pack()




root.mainloop()
