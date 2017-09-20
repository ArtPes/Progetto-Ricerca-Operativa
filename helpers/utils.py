import os
import random

def output(lock, message):
    lock.acquire()
    print(message)
    lock.release()


def loop_menu(lock, header, options):
    action = None
    while action is None:
        output(lock, header)

        for idx, o in enumerate(options, start=1):
            output(lock, str(idx) + ": " + o + "")

        try:
            action = input()
        except SyntaxError:
            action = None

        if not action:
            output(lock, "Please select an option")
            action = None
        elif action == 'e':
            return None
        else:
            try:
                selected = int(action)
            except ValueError:
                output(lock, "A number is required")
                continue
            else:
                if selected > len(options):
                    output(lock, "Option " + str(selected) + " not available")
                    action = None
                    continue
                else:
                    return selected


def loop_input(lock, header):
    var = None
    while var is None:
        output(lock, header)

        try:
            var = input()
        except ValueError:
            var = None

        if not var:
            output(lock, "Type something!")
            var = None
        elif var == 'e':
            return None
        else:
            return var


def loop_int_input(lock, header):
    var = None
    while var is None:
        output(lock, header)

        try:
            var = input()
        except ValueError:
            var = None

        if not var:
            output(lock, "Type something!")
            var = None
        elif var == 'e':
            return None
        else:
            try:
                selected = int(var)
            except ValueError:
                output(lock, "A number is required")
                continue
            else:
                return selected

def inserimento_random(listp):
    saletta = [1, 2, 3]
    for i in range(0, len(listp)):
        listp[i].saletta = random.choice(saletta)
        # output(out_lck,"Paziente "+str(listp[i].id)+" nella saletta: "+str(listp[i].saletta))

    sala1 = []
    sala2 = []
    sala3 = []

    for s in saletta:
        for i in range(0, len(listp)):
            if s == 1:
                if listp[i].saletta == s:
                    sala1.append(listp[i].id)
            if s == 2:
                if listp[i].saletta == s:
                    sala2.append(listp[i].id)
            if s == 3:
                if listp[i].saletta == s:
                    sala3.append(listp[i].id)

    return sala1,sala2,sala3