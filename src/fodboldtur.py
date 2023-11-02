
# Import biblioteker.
import pickle
import time
import re

# Definer en variabel for savefilen.
filename: str = 'betalinger.pk'


# Funktion der styrer hovedmenuen.
def menu():
    # Så længe dette while loop kører, kører programmet i ring.
    while True:
        print("MENU")
        print("-----------------------------")
        print("1: Print liste")
        print("2: Lav indbetaling")
        print("3: Fjern en indbetaler")
        print("4: Nulstil et medlems indbetalte beløb")
        print("5: Se holdets fattigste medlemmer")
        print("9: Afslut programmet")
        print("-----------------------------")
        valg: str = input("Indtast dit valg: ")

        match valg:
            case '1':
                print_liste(fodboldtur)

            case '2':
                indbetal(fodboldtur)

            case '3':
                slet_indbetaler(fodboldtur)

            case '4':
                nulstil_beløb(fodboldtur)

            case '5':
                poor_people_leaderboard(fodboldtur)

            case '9':
                print("Programmet er afsluttet!")
                break

            case '_':
                print('Ahhh det var vidst ikke et helt gyldigt tal. Prøv igen.')
                time.sleep(1)

        gem()

        if tilbage_til_menu() != "ja":
            print('Programmet afsluttes!')
            time.sleep(1)
            break


# Funktion der kaldes hvert iteration af while loopet i main funktionen. Gemmer dictionariet fodboldtur i en fil.
def gem():
    outfile = open(filename, 'wb')
    pickle.dump(fodboldtur, outfile)
    outfile.close()


# Funktion der kaldes til slut i main funktionens while loop
# Fungerer som en variabel og indeholder valget om brugeren vil afslutte programmet eller ej.
def tilbage_til_menu() -> str:
    return input('\nVil du tilbage til menuen? - Skriv Ja \nEller afslutte programmet? - Skriv Nej \n').lower()


# Udregner beløbet, hver medlem skal betale for fodboldturen. Varierer afhængig af antallet af indbetalere.
def total_per_person(dic: dict):
    antalIndbetalere: int = len(dic.items())
    return 4500 / antalIndbetalere


def formater_string(tekst: str, mellemrum: bool = False) -> str:
    tekst = tekst.lower().title().replace(" ", "")
    if mellemrum:
        return re.sub(r"(?<=\w)([A-Z])", r" \1", tekst)
    return tekst


# Printer listen af indbetalere; hvor meget de har indbetalt og, hvor meget mere de skylder.
def print_liste(dictionary: dict):
    total: float = sum(dictionary.values())
    totalPerPerson: float = total_per_person(dictionary)

    for key, val in fodboldtur.items():
        print(f'{key} har betalt {val} kr. | MANGLER: {totalPerPerson - val} kr.')
    print(f'\nI alt er der betalt {total} kr. - der mangler at betales {4500 - total}')


# Funktion der styrer indbetalinger.
def indbetal(dictionary: dict):
    print('Her kan du lave håndtere indbetalingere. Du kan enten lave en indbetaling for en person på listen'
          'eller tilføje en ny indbetaler ved bare at skrive deres navn.\n')
    person: str = input('Hvem er du? ')
    udenMellemrumPerson: str = formater_string(person)
    medMellemrumPerson: str = formater_string(person, True)

    totalPerPerson: float = total_per_person(dictionary)

    lowerKeyDict: dict = {formater_string(k): v for k, v in dictionary.copy().items()}

    # Hvis personen allerede har en entry i dictionariet og de har betalt, hvad de skylder hoppes der ud af funktionen.
    if udenMellemrumPerson in lowerKeyDict.keys():
        if lowerKeyDict[udenMellemrumPerson] == totalPerPerson:
            print('Du har allerede indbetalt det fulde beløb.')
            return

    # Hvis personen ikke har en entry, oprettes de i dictionariet fodboldtur.
    else:
        print('Dette er din første indbetaling.')
        dictionary.update({f'{medMellemrumPerson}': 0})
        totalPerPerson = total_per_person(dictionary)

    beløb: float = float(input("Hvor meget vil du indbetale? "))

    # Hvis beløbet personen vil indbetale sammenlagt med, hvad de allerede har betalt overstier, hvad de skal betale
    # sættes beløbet de vil betale, til det resterende beløb de skylder.
    if dictionary[medMellemrumPerson] + beløb > totalPerPerson:
        beløb: float = totalPerPerson - dictionary[medMellemrumPerson]
        print(f'Din indbetaling er sat til det resterende beløb, {beløb}, '
              f'da du forsøgte at indbetale mere end, hvad du skyldte.')

    # Opdater værdien i dictionariet med det beløb personen lige har indbetalt.
    fodboldtur.update({f'{medMellemrumPerson}': dictionary[medMellemrumPerson] + beløb})
    print(f'Du har nu i alt indbetalt {dictionary[medMellemrumPerson]} kr.')


# Fjern indbetaler fra dictionariet.
def slet_indbetaler(dictionary: dict):
    indbetaler: str = formater_string(input('Hvilken indbetaler vil du slette? '), True)
    dictionary.__delitem__(indbetaler)
    print(f'{indbetaler} er nu blevet fjernet fra listen af indbetalere.')


def nulstil_beløb(dictionary: dict):
    medMellemrumPerson = formater_string(input('Hvis beløb vil du nulstille? '), True)
    dictionary.update({f'{medMellemrumPerson}': 0})
    print(f'{medMellemrumPerson}s indbetalte beløb er blevet sat til 0')


# Sorter dictionary efter størrelse af nøglerne respektive værdier og print de tre individer, der har indbetalt mindst.
def poor_people_leaderboard(dictionary: dict):
    sortedDict: list = sorted(dictionary.items(), key=lambda x: x[1])
    for i in range(3):
        print(sortedDict[i])


# Kør programmet hvis værdien dets navn er "__main__".
if __name__ == "__main__":
    infile = open(filename, 'rb')
    fodboldtur: dict = {}
    fodboldtur = pickle.load(infile)
    infile.close()
    menu()
