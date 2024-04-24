import PySimpleGUI as sg
import random
import keyboard


def digit_set_up(mode):
    pass
    num_of_digits = random.randint(1, 8)
    operator_1 = random.randint(1, 10)
    operator_2 = random.randint(1, 10)
    if mode == "x":
        correct = operator_1 * operator_2
    if mode == "/":
        correct = round(operator_1/operator_2, 2)
    return [correct, operator_1, operator_2]


def run(mode):
    equation = (digit_set_up(mode))
    layout = [sg.Text(str(equation[1]) + mode + str(equation[2]))], [sg.Text("Answer"),
                                                                     sg.InputText(
        key="answer",  enable_events=True),
        [sg.Button("Continue"), sg.Button("End Session")]]
    final = str(equation[0])
    window = sg.Window('Mental Math', layout, return_keyboard_events=False)
    while True:
        event, values = window.Read()
        if event == sg.WIN_CLOSED:
            break
        window.bind("<Return>", "Continue")
        window.bind("Escape", "End Session")
        if event == 'answer' and len(values["answer"]) >= 1 and values['answer'][-1] not in ('0123456789.'):
            window.Element('answer').Update(values['answer'][:-1])
        if event == "Continue":
            if values["answer"] == final:
                equation = (digit_set_up(mode))
                layout = [sg.Text(str(equation[1]) + mode + str(equation[2]))], [sg.Text("Answer"),
                                                                                 sg.InputText(
                    key="answer",  enable_events=True)], [sg.Button("Continue"), sg.Button("End Session")]
                final = str(equation[0])
                window.close()
                window = sg.Window("Mental Math", layout,
                                   return_keyboard_events=True)
        if event == "End Session":
            layout = [[sg.Text("Correct answer of current question is " +
                               str(final))], [sg.Button("Return to title")]]
            window.close()
            window = sg.Window("Mental Math", layout)
        if event == "Return to title":
            window.close()
            title()
            break
    window.close()


def title():
    layout = [[sg.Text("Answer all questions to 3 decimal places")], [sg.Text("Choose a mode")], [sg.Button(
        "Multiplication"), sg.Button("Division")]]
    window = sg.Window("Mental Math", layout)
    mode = ""
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "Multiplication":
            mode = "x"
            window.close()
            run(mode)
            break
        if event == "Division":
            mode = "/"
            window.close()
            run(mode)
            break
    window.close()


title()
