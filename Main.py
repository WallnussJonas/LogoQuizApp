import time
import threading
import tkinter as tk
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import yaml
import os

with open("data/questions.yaml", 'rt', encoding='utf8') as yml:
    yaml_content = yaml.safe_load(yml)


question_counter = 0
score = 0
filename = "scoreboard"
file = filename +".yaml"

if os.path.exists("data/scoreboard.yaml"):
    with open("data/scoreboard.yaml", 'rt', encoding='utf8') as yml:
        scoreboard = yaml.safe_load(yml)
else:
    scoreboard = []

root = Tk()
root.resizable(False, False)

root.title("Quiz App")
root.geometry("600x400")
root.iconbitmap("./image.ico")

frame = Frame(root)
frame.pack(side="top", expand=True, fill="both")

frage = Label(frame, text="Welches Logo ist das?", width=20, height=5, font=("Ubuntu", 15))
frage.pack()

logo = ImageTk.PhotoImage(Image.open(f"data/images/{yaml_content['questions'][question_counter]['image']}"))
imglabel = Label(frame, image=logo, height=120, width=120)
imglabel.pack()

def refreshCnfg(question_counter):
    btnsConfig = {
        "ans1": {
            "y": "250",
            "x": "100",
            "text": yaml_content["questions"][question_counter]['answers'][0],
            "height": 1,
            "width": 12,
            "bg": "#EEEEEE"
        },
        "ans2": {
            "y": "310",
            "x": "100",
            "text": yaml_content["questions"][question_counter]['answers'][1],
            "height": 1,
            "width": 12,
            "bg": "#EEEEEE"
        },
        "ans3": {
            "y": "250",
            "x": "410",
            "text": yaml_content["questions"][question_counter]['answers'][2],
            "height": 1,
            "width": 12,
            "bg": "#EEEEEE"
        },
        "ans4": {
            "y": "310",
            "x": "410",
            "text": yaml_content["questions"][question_counter]['answers'][3],
            "height": 1,
            "width": 12,
            "bg": "#EEEEEE"
        }
    }
    return btnsConfig

def changeImg():
    img2 = ImageTk.PhotoImage(Image.open(f"data/images/{yaml_content['questions'][question_counter]['image']}"))
    imglabel.configure(image=img2)
    imglabel.image = img2

def createOrRefreshFrame():
    global scorelbl
    global question_counter
    if question_counter == len(yaml_content['questions']):
        ask()
        return

    scorelbl = tk.Label(frame, text="Score: ", font=("Arial", 12))
    scorelbl.pack()
    scorelbl.place(x=10, y=10)

    print(f'counter before: {question_counter}')
    changeImg()
    refreshCnfg(question_counter)
    Ans = {"rigthAns": yaml_content['questions'][question_counter]['right_answer'],
           "ansOpt": yaml_content['questions'][question_counter]['answers']}

    btnsConfig = refreshCnfg(question_counter)
    global ans1, ans2, ans3, ans4
    ans1 = tk.Button(frame, text=btnsConfig["ans1"]["text"], height=btnsConfig["ans1"]["height"],
                     width=btnsConfig["ans1"]["width"], bg=btnsConfig["ans1"]["bg"],
                     command=lambda: onclick(Ans["ansOpt"][0], Ans["rigthAns"]))
    ans1.pack()
    ans1.place(x=btnsConfig["ans1"]["x"], y=btnsConfig["ans1"]["y"])

    ans2 = tk.Button(frame, text=btnsConfig["ans2"]["text"], height=btnsConfig["ans2"]["height"],
                     width=btnsConfig["ans2"]["width"], bg=btnsConfig["ans2"]["bg"],
                     command=lambda: onclick(Ans["ansOpt"][1], Ans["rigthAns"]))
    ans2.place(x=btnsConfig["ans2"]["x"], y=btnsConfig["ans2"]["y"])

    ans3 = tk.Button(frame, text=btnsConfig["ans3"]["text"], height=btnsConfig["ans3"]["height"],
                     width=btnsConfig["ans3"]["width"], bg=btnsConfig["ans3"]["bg"],
                     command=lambda: onclick(Ans["ansOpt"][2], Ans["rigthAns"]))
    ans3.pack()
    ans3.place(x=btnsConfig["ans3"]["x"], y=btnsConfig["ans3"]["y"])

    ans4 = tk.Button(frame, text=btnsConfig["ans4"]["text"], height=btnsConfig["ans4"]["height"],
                     width=btnsConfig["ans4"]["width"], bg=btnsConfig["ans4"]["bg"],
                     command=lambda: onclick(Ans["ansOpt"][3], Ans["rigthAns"]))
    ans4.pack()
    ans4.place(x=btnsConfig["ans4"]["x"], y=btnsConfig["ans4"]["y"])

    question_counter += 1
    scorelbl.configure(text="Score: " + str(score))
    print(f'counter after: {question_counter}')
    print(score)


    def revealWrong():
        next.configure(state="disabled")
        time.sleep(1)
        wrong()
        ans1.configure(state="disabled")
        ans2.configure(state="disabled")
        ans3.configure(state="disabled")
        ans4.configure(state="disabled")
        next.configure(state="normal")

    def revealRight():
        next.configure(state="disabled")
        global score
        time.sleep(1)
        right()
        score -= 1
        ans1.configure(state="disabled")
        ans2.configure(state="disabled")
        ans3.configure(state="disabled")
        ans4.configure(state="disabled")
        next.configure(state="normal")

    def right():
        global score
        if (Ans["rigthAns"] == Ans["ansOpt"][0]):
            ans1.configure(bg="green")
            score += 1
        if (Ans["rigthAns"] == Ans["ansOpt"][1]):
            ans2.configure(bg="green")
            score += 1
        if (Ans["rigthAns"] == Ans["ansOpt"][2]):
            ans3.configure(bg="green")
            score += 1
        if (Ans["rigthAns"] == Ans["ansOpt"][3]):
            ans4.configure(bg="green")
            score += 1

    def wrong():
        if (Ans["rigthAns"] != Ans["ansOpt"][0]):
            ans1.configure(bg="red")
        if (Ans["rigthAns"] != Ans["ansOpt"][1]):
            ans2.configure(bg="red")
        if (Ans["rigthAns"] != Ans["ansOpt"][2]):
            ans3.configure(bg="red")
        if (Ans["rigthAns"] != Ans["ansOpt"][3]):
            ans4.configure(bg="red")

    def onclick(args, right_answer):
        if args == right_answer:
            t1 = threading.Thread(target=right)
            t1.start()
            t2 = threading.Thread(target=revealWrong)
            t2.start()

        else:
            t1 = threading.Thread(target=wrong)
            t1.start()
            t2 = threading.Thread(target=revealRight)
            t2.start()


createOrRefreshFrame()

def ask():
    for widgets in frame.winfo_children():
        widgets.destroy()

    namelbl = tk.Label(root, text="Wie heißt du?")
    namelbl.pack()
    namelbl.place(x=250, y=10)

    nameentr = tk.Entry()
    nameentr.pack()
    nameentr.place(x=230, y=50)

    def getName():
        name = nameentr.get()
        print(name)
        scoreboard.append({"name": name, "score": score})
        with open("data/scoreboard.yaml", 'w', encoding='utf8') as file:
            yaml.dump(scoreboard, file)
        namelbl.destroy()
        nameentr.destroy()
        nextbtn.destroy()
        printScorebrd()

    nextbtn = tk.Button(root, text="weiter", command=getName)
    nextbtn.pack
    nextbtn.place(x=270, y=80)

next = tk.Button(frame, text="Nächste Frage", height=1, width=12, command=createOrRefreshFrame, state="normal") #create function that enables this button after one was clicked
next.pack()
next.place(x=250, y=350)

def printScorebrd():
    again = tk.Button(frame, text="Quiz wiederholen ↺")
    again.pack()
    again.place(x=40, y=10)

    exit = tk.Button(frame, text="Beenden ❌", command=lambda: root.quit())
    exit.pack()
    exit.place(x=450, y=10)

    headings =["User", "Score"]
    table = ttk.Treeview(frame, columns=headings, show="headings")
    table.pack(fill="both", expand=True,pady=50)

    for heading in headings:
        table.heading(heading, text=heading)

    for i, row in enumerate(scoreboard):
        table.insert("", i, values=[row["name"], row["score"]])


def board():
    frage.destroy()
    imglabel.destroy()
    ans1.destroy()
    ans2.destroy()
    ans3.destroy()
    ans4.destroy()
    next.destroy()
    scorelbl.destroy()
    scorebrd.destroy()
    printScorebrd()

scorebrd = tk.Button(frame, text="Scoreboard", command=board)
scorebrd.pack()
scorebrd.place(x=510, y=10)

frame.mainloop()
