import PySimpleGUI as sg
import random
import time


def digit_set_up(mode, selected_range):
    selected_range = selected_range.replace("to ", "")
    ends = selected_range.split(" ")
    operator_1 = random.randint(int(ends[0]), int(ends[1]))
    operator_2 = random.randint(int(ends[0]), int(ends[1]))
    if mode == "x":
        correct = operator_1 * operator_2
    if mode == "/":
        correct = round(operator_1/operator_2, 2)
    return [correct, operator_1, operator_2]


def point_calc(time, sig_figs_1, sig_figs_2):
    factor = round(time/10, 0) + 1
    raw = (10**sig_figs_1 + 10**sig_figs_2)/factor
    points = int(round(raw))
    return points


def run(mode, selected_range):
    pts = 0
    equation = (digit_set_up(mode, selected_range))
    layout = [[sg.Column([[sg.Text("Time elapsed: ", justification="right", key="timer"), sg.Text("Total points: " + str(pts), justification="left")]], expand_x=True, element_justification="right")], [sg.Column([[sg.Text(
        str(equation[1]) + mode + str(equation[2]))]], element_justification="left")], [sg.Text("Answer"),                                                             sg.InputText(
            key="answer",  enable_events=True)],
        [sg.Button("Continue", enable_events=True), sg.Button("End Session", enable_events=True)]]
    final = str(equation[0])
    window = sg.Window('Mental Math', layout)
    starttime = time.time()
    ongoing = True
    num_ans = 0
    num_attempted = 0
    total_times = []
    while True:
        stpwatch = int(2 + time.time() - starttime)
        event, values = window.Read(timeout=1000)
        window.bind("<Escape>", "End Session")
        window.bind("<Return>", "Continue")
        if event == sg.WIN_CLOSED:
            break
        else:
            if ongoing:
                window["timer"].update("Time elapsed: " + str(stpwatch))
        if event == 'answer' and len(values["answer"]) >= 1 and values['answer'][-1] not in ('0123456789.'):
            window.Element('answer').Update(values['answer'][:-1])
        if event == "Continue":
            if values["answer"] == final:
                num_ans += 1
                ongoing = False
                total_times.append(stpwatch)
                pts += point_calc(stpwatch,
                                  len(str(equation[1])), len(str(equation[2])))
            else:
                ongoing = False
                total_times.append(stpwatch)
            num_attempted += 1
            starttime = time.time()
            stpwatch = int(time.time() - starttime)
            equation = (digit_set_up(mode, selected_range))
            layout = [[sg.Column([[sg.Text("Time elapsed: ", justification="right", key="timer"), sg.Text("Total points: " + str(pts), justification="left")]], expand_x=True, element_justification="right")], [sg.Column([[sg.Text(
                str(equation[1]) + mode + str(equation[2]))]], element_justification="left")], [sg.Text("Answer"),                                                             sg.InputText(
                    key="answer",  enable_events=True)],
                [sg.Button("Continue", enable_events=True), sg.Button("End Session", enable_events=True)]]
            final = str(equation[0])
            window.close()
            window = sg.Window("Mental Math", layout,
                               return_keyboard_events=True)
            ongoing = True
        elif event == "End Session":
            if values["answer"] == final:
                num_ans += 1
                pts += point_calc(stpwatch,
                                  len(str(equation[1])), len(str(equation[2])))
            total_times.append(stpwatch)
            num_attempted += 1
            layout = [[sg.Text("The correct answer of the current question is " +
                               str(final))], [sg.Text("Total points: " + str(pts))], [sg.Text("Total time elapsed: " + str(sum(total_times)) + " seconds")], [sg.Text("Number of correct answers: " + str(num_ans))], [sg.Text("Number of questions attempted: " + str(num_attempted))], [sg.Button("Return to title")]]
            window.close()
            ongoing = False
            window = sg.Window("Mental Math", layout)
        elif event == "Return to title":
            window.close()
            title()
            break
    window.close()


def title():
    layout = [[sg.Text("Answer all questions to 3 decimal places")], [sg.Text("Choose a mode")], [sg.Button(
        "Multiplication"), sg.Button("Division")]]
    window = sg.Window("Mental Math", layout)
    mode = ""
    selected_range = ""
    while True:
        event, values = window.read()
        events = ["1 to 10", "1 to 100", "1 to 1000",
                  "10 to 100", "10 to 1000", "100 to 1000"]
        if event == sg.WIN_CLOSED:
            break
        if event == "Multiplication":
            mode = "x"
            layout = [[sg.Text("Within what range of figures should the factors of the equation fall?")], [sg.Button("1 to 10"), sg.Button(
                "1 to 100"), sg.Button("1 to 1000")], [sg.Button("10 to 100"), sg.Button("10 to 1000")], [sg.Button("100 to 1000")]]
            window.close()
            window = sg.Window("Mental Math", layout)
        if event == "Division":
            layout = [[sg.Text("Within what range of figures should the divedend and divisor of the equation fall?")], [sg.Button("1 to 10"), sg.Button(
                "1 to 100"), sg.Button("1 to 1000")], [sg.Button("10 to 100"), sg.Button("10 to 1000")], [sg.Button("100 to 1000")]]
            window.close()
            window = sg.Window("Mental Math", layout)
            mode = "/"
        for e in events:
            if event == e:
                selected_range = e
                window.close()
                run(mode, selected_range)
                break
    window.close()


title()
