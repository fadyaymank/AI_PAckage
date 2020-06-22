from pyknow import *


class Patient(Fact):
    pass


class MedicalES(KnowledgeEngine):
    low_sugar_symptoms = ["shakiness", "hunger", "sweating", "headache", "pale"]
    high_sugar_symptoms = ["thirst", "blurred vision", "headache", "dry mouth", "smelling breath",
                           "shortness of breath"]

    # If the patient is a child (less than or equal 5 years old) and
    # have more than two symptoms of following list (shakiness, hunger, sweating, headache or pale)
    # then he/she has signs of low sugar.
    @Rule(AND(Patient(maturity="child"), Patient(low_sugar_symptoms_count=MATCH.count)))
    def signs_of_low_sugar(self, count):
        if count >= 3:
            print("\n\t\tYou have signs of low sugar.\n")
            self.declare(Patient(signs="low sugar"))
            self.declare(Patient(diabetic_parents=input("Do you have diabetic parents, yes or no? ")))

    # If the patient is a child and
    # has more than two symptoms of the following list (thirst, blurred vision,
    # headache, dry mouth, smelling breath, shortness of breath),
    # then the patient has signs of high sugar.
    @Rule(AND(Patient(maturity="child"), Patient(high_sugar_symptoms_count=MATCH.count)))
    def signs_of_high_sugar(self, count):
        if count >= 3:
            print("\n\t\tYou have signs of high sugar.\n")
            self.declare(Patient(signs="high sugar"))

    # If the patient has runny nose and harsh cough,
    # then the patient has signs of cold.
    @Rule(AND(Patient(symptom="runny nose"), Patient(symptom="harsh cough")))
    def signs_of_cold(self):
        print("\n\t\tYou have signs of cold.\n")
        self.declare(Patient(signs="cold"))
        print("----------------------------------------------------")
        user_answer = input("Do you wish to check if you have measles, yes or no? ")
        if user_answer == "yes":
            self.declare(Patient(rash=input("Do you have a brownish-pink rash, yes or no? ")))
            self.declare(Patient(eyes_state=input("Do you have bloodshot eyes, yes or no? ")))
            self.declare(Patient(fast_temp=input("Is your temperature rising fast, yes or no? ")))
            self.declare(Patient(cheek_spots=input("Is there any white spots inside your cheeks, yes or no? ")))
        print("----------------------------------------------------")
        user_answer = input("Do you wish to check if you have a flu, yes or no? ")
        if user_answer == "yes":
            self.check_for_flu()

    def check_for_flu(self):
        self.declare(Patient(conjunctive=input("Are you conjunctive, yes or no? ")))
        self.declare(Patient(body_ache=input("If you feel any body ache what's it's level (strong, mild, none)? ")))
        self.declare(Patient(weakness=input("Do you feel any weakness in your body, yes or no? ")))
        self.declare(Patient(vomiting=input("Is there any case of vomiting, yes or no? ")))
        self.declare(Patient(sneezing=input("Is there any case of sneezing, yes or no? ")))
        self.declare(Patient(sore_throat=input("Is your throat sore, yes or no? ")))

    # If the patient has signs of low sugar and has diabetic parents,
    # then the patient could be diabetic.
    @Rule(AND(Patient(signs="low sugar"), Patient(diabetic_parents="yes")))
    def diabetic(self):
        print("\n\t\tYou could be diabetic.\n")

    def check_for_mumps(self):
        self.declare(Patient(saliva=input("what's the state of your saliva, normal or not normal? ")))
        self.declare(Patient(lymph_nodes_in_neck=input("Do you have swollen lymph nodes in your neck, yes or no? ")))
        self.declare(Patient(dry_mouth=input("Is your mouth dry, yes or no? ")))

    # If the patient is a child and has moderate temperature, saliva is not normal,
    # swollen lymph nodes in neck, mouth dry
    # then he/she has mumps.
    @Rule(AND(Patient(saliva="not normal"), Patient(temperature="moderate"), Patient(lymph_nodes_in_neck="yes"),
              Patient(dry_mouth="yes")))
    def mumps(self):
        print("\n\t\tYou have mumps.\n")

    # If the patient is a child and has signs of cold, brownish-pink rash,
    # high and fast temperature, bloodshot eyes, white spots inside cheek
    # then he/she has a measles.
    @Rule(AND(Patient(maturity="child"), Patient(signs="cold"), Patient(rash="yes"), Patient(fast_temp="yes"),
              Patient(temperature="high"), Patient(eyes_state="yes"), Patient(cheek_spots="yes")))
    def measles(self):
        print("\n\t\tYou have measles.\n")

    # If the patient is a child or an adult and has signs of cold, conjunctives,
    # strong body aches, weakness, vomiting, sore throat and sneezing
    # then he/she has a child-flu if the patient is a child or adult-flu if the patient is an adult.
    @Rule(AND(Patient(maturity=MATCH.maturity), Patient(signs="cold"), Patient(conjunctive="yes"),
              Patient(body_ache="strong"), Patient(weakness="yes"),
              Patient(sore_throat="yes"), Patient(vomiting="yes"), Patient(sneezing="yes")))
    def flu(self, maturity):
        print("\n\t\tYou have the " + maturity + "-flu.\n")


class Diagnoses(Fact):
    pass


class PlantDiagnosesES(KnowledgeEngine):
    # If the plant has high temperature, normal humidity,
    # tuber color is reddish-brown and tuber has spots
    # then the plant has black heart.
    @Rule(AND(Diagnoses(temperature="high"), Diagnoses(humidity="normal"),
              Diagnoses(color="reddish-brown"), Diagnoses(appearance="spots")))
    def diagnose1(self):
        print("The plant has black heart.")

    # If the plant has low temperature, high humidity,
    # normal tuber and tuber has spots
    # then the plant has late blight.
    @Rule(AND(Diagnoses(temperature="low"), Diagnoses(humidity="high"),
              Diagnoses(state="normal"), Diagnoses(appearance="spots")))
    def diagnose2(self):
        print("The plant has late blight.")

    # If the plant has high temperature, normal humidity,
    # tuber is dry and tuber has circles
    # then the plant has dry rot.
    @Rule(AND(Diagnoses(temperature="high"), Diagnoses(humidity="normal"),
              Diagnoses(state="dry"), Diagnoses(appearance="circles")))
    def diagnose3(self):
        print("The plant has dry rot.")

    # If the plant has normal temperature, normal humidity,
    # tuber color is brown and tuber has wrinkles
    # then the plant has early blight.
    @Rule(AND(Diagnoses(temperature="normal"), Diagnoses(humidity="normal"),
              Diagnoses(color="brown"), Diagnoses(appearance="wrinkles")))
    def diagnose4(self):
        print("The plant has early blight.")


def main():
    es_choice = int(input("What system would you like to start? (1: Medical, 2: Plant Diagnoses, 0: Exit)\n"))
    while es_choice != 0:
        if es_choice == 1:
            engine = MedicalES()
            engine.reset()
            in_age = int(input("What's your age? "))
            if in_age <= 5:
                engine.declare(Patient(maturity="child"))
                engine.declare(Patient(temperature=input("How is your temperature (high, low or moderate)? ")))

            else:
                engine.declare(Patient(maturity="adult"))

            print("----------------------------------------------------")
            user_answer = input("Do you wish to check for signs of cold, yes or no? ")
            if user_answer == "yes":
                sym_answer = input("Do you have runny nose, yes or no? ")
                if sym_answer == "yes":
                    engine.declare(Patient(symptom="runny nose"))
                sym_answer = input("Do you have harsh cough, yes or no? ")
                if sym_answer == "yes":
                    engine.declare(Patient(symptom="harsh cough"))

            print("----------------------------------------------------")
            user_answer = input("Do you wish to check if you have mumps, yes or no? ")
            if user_answer == "yes":
                engine.check_for_mumps()

            print("----------------------------------------------------")
            user_answer = input("Do you wish to check if you have low sugar level, yes or no? ")
            if user_answer == "yes":
                ls_count = 0
                print("Do you have any of the following low sugar symptoms, yes or no? ")
                for i in engine.low_sugar_symptoms:
                    answer = input(i+": ")
                    if answer == "yes":
                        ls_count += 1
                engine.declare(Patient(low_sugar_symptoms_count=ls_count))

            print("----------------------------------------------------")
            user_answer = input("Do you wish to check if you have high sugar level, yes or no? ")
            if user_answer == "yes":
                hs_count = 0
                print("Do you have any of the following high sugar symptoms, yes or no? ")
                for i in engine.high_sugar_symptoms:
                    answer = input(i+": ")
                    if answer == "yes":
                        hs_count += 1
                engine.declare(Patient(high_sugar_symptoms_count=hs_count))

            engine.run()
        else:
            engine = PlantDiagnosesES()
            engine.reset()
            # temperature
            engine.declare(Diagnoses(temperature=input("What's the plant temperature(high, low, or normal)? ")))
            # humidity
            engine.declare(Diagnoses(humidity=input("What's the plant humidity level(high or normal)? ")))
            # tuber color
            engine.declare(Diagnoses(color=input("What's the plant tuber color(reddish-brown or brown)? ")))
            # tuber state
            engine.declare(Diagnoses(state=input("What's the plant tuber state(normal or dry)? ")))
            # tuber appearance
            engine.declare(Diagnoses(appearance=input("What does the plant tuber appearance has(spots, wrinkles or circles)? ")))
            engine.run()
        es_choice = int(input("What system would you like to start? (1: Medical, 2: Plant Diagnoses, 0: Exit)\n"))


main()
