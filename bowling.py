import doctest
import re

def bowling(spiel):
    """
    >>> bowling("--|--|--|--|--|--|--|--|--|--||")
    0
    >>> bowling("9-|--|--|--|--|--|--|--|--|--||")
    9
    >>> bowling("51|51|51|51|51|51|51|51|51|51||")
    60
    >>> bowling("9-|9-|9-|9-|9-|9-|9-|9-|9-|9-||")
    90
    >>> bowling("--|--|X|--|--|--|--|--|--|--||")
    10
    >>> bowling("--|--|--|--|--|--|--|X|6-|--||")
    22
    >>> bowling("--|--|--|--|--|--|--|X|62|--||")
    26
    >>> bowling("--|--|--|--|--|--|--|X|62|2-||")
    28
    >>> bowling("X|9-|9-|9-|X|9-|X|X|9-|9-||")
    140
    >>> bowling("--|--|--|--|--|--|--|--|--|X||81")
    19
    >>> bowling("--|--|--|--|--|--|--|--|--|X||X")
    20
    >>> bowling("--|--|--|--|--|--|--|--|X|X||81")
    47
    >>> bowling("9/|--|--|--|--|--|--|--|--|--||")
    10
    >>> bowling("9/|1-|--|--|--|--|--|--|--|--||")
    12
    >>> bowling("X|1/|--|--|--|--|--|--|--|--||")
    31
    >>> bowling("--|--|--|--|--|--|--|--|X|X||8/")
    48
    >>> bowling("--|--|--|--|--|--|--|--|X|1/||8")
    39

    >>> bowling("--|--|--|--|--|--|56|--|X|X||8/")
    Traceback (most recent call last):
        ...
    Exception: This combination of Throws is not possible: 56

    >>> bowling("--|--|--|--|--|--|51|--|X|11||8/")
    Traceback (most recent call last):
        ...
    Exception: No Bonus required: 11

    >>> bowling("--|--|--|--|--|--|51|--|X|11|4|")
    Traceback (most recent call last):
        ...
    Exception: Dont put stuff between the Endmarkers: 4

    >>> bowling("--|--|--|--|--|51|X|11|4|")
    Traceback (most recent call last):
        ...
    Exception: String is formatted wrongly

    >>> bowling("--|--|611|--|--|--|--|--|X|X||8/")
    Traceback (most recent call last):
        ...
    Exception: Unknown Error occured here: 611

    >>> bowling("--|--|61|--|--|--|--|--|X|1/||82")
    Traceback (most recent call last):
        ...
    Exception: Bonus too long: 82

    >>> bowling("--|--|--|--|--|--|--|--|X|X|8/")
    Traceback (most recent call last):
        ...
    Exception: String is formatted wrongly

    >>> bowling("--|--|--|--|5|--|--|X|62|--||")
    Traceback (most recent call last):
        ...
    Exception: Unknown Error occured here: 5
    """
    resultat=0
    return_tuple=(0,False,False,False)

    split=spiel.split("|")
    IsValid(split)
    for x in split:
        return_tuple=evaluire(x,return_tuple[1],return_tuple[2],return_tuple[3])
        resultat=resultat+return_tuple[0]
        #print(resultat)
    return(resultat)
    
def IsValid(Split):
    #Funktion gives Exception on invalid Input, else pass
    if len(Split)!=12:
        raise Exception('String is formatted wrongly')
    if Split[10]!="":
        raise Exception('Dont put stuff between the Endmarkers: '+Split[10])
    if Split[11]!="":
        if re.match("X$",Split[9]):
            pass
        elif re.match("[1-9-]\/$",Split[9]):
            if len(Split[11])!=1:
                raise Exception('Bonus too long: '+Split[11])
        else:
            raise Exception('No Bonus required: '+Split[9])
        


    for x in Split:
        if re.match("[1-9]{2}$",x):
            if int(x[0])+int(x[1])<10:
                pass
            else:
                print("Ungültig")
                raise Exception('This combination of Throws is not possible: '+x)

        elif re.match("[1-9-]{2}$",x):
            pass
        elif re.match("[1-9-]\/$",x):
            pass
        elif re.match("X$",x):
            pass
        elif x=="":
            pass
        elif len(x)==1 and re.match("[1-9-]",x) and Split[11]==x:
            pass
        else:
            raise Exception('Unknown Error occured here: '+x)
    #print (Split)

def evaluire(teil, doppler,einzler,Enderman):
    # Double für eine Pos nach X
    # Single für zwei Pos nach X oder eine Pos nach /
    # Ende zeigt die Bonuskugeln an die nur zum Auswerten des letzten frames benötigt werden und nicht selber zählen.
    teil_resultat = 0
    Ende=Enderman
    if teil=="":
        Ende=True
    Double=doppler
    Single=einzler
    for x in teil:
        modificator=0
        if Ende==True:
            modificator-=1

        if x=="-":
            
            if Double==True and Single==True:
                Double=False
            elif Double==True:
                Double=False
                Single=True
            elif Single==True:
                Single=False
        elif x=="X":
            
            if Double==True and Single==True:
                modificator+=3
            elif Double==True:
                modificator+=2
                Single=True
            elif Single==True:
                modificator+=2
                Double=True
                Single=False
            else:
                modificator+=1
                Double=True

           
            teil_resultat += modificator*10
        
        elif x =="/":
            #modificator is one lower so completion to 10 works
            y= 10-int(teil[0])
            if Single==True:
                modificator+=1
            else:
                modificator+=0
                Single=True
            teil_resultat += y+10*modificator
        #spare has a maximum of a single since double has been used already so only single and none :)
        else:
            
            if Double==True and Single==True:
                modificator+=3
                Double=False
            elif Double==True:
                modificator+=2
                Double=False
                Single=True
            elif Single==True:
                modificator+=2
                Single=False
            else:
                modificator+=1
            teil_resultat += modificator*int(x)
        #print (teil_resultat, Double, Single,modificator)
    
    return teil_resultat, Double, Single, Ende

"""
Rules
Jedes Bowlingspiel (oder "Line") umfasst zehn Runden (oder "Frames") für den Bowlingspieler.

In jedem Frame hat der Bowler bis zu zwei Versuche, alle zehn Pins umzuwerfen.

Wenn die erste Kugel in einem Frame alle zehn Pins umwirft, nennt man das einen "Strike". Der Frame ist beendet. Die Punktzahl für den Frame ist zehn plus die Summe der Pins, die mit den nächsten beiden Kugeln umgeworfen werden.

Wenn die zweite Kugel in einem Frame alle zehn Pins umwirft, nennt man dies einen "Spare". Der Frame ist beendet. Die Punktzahl für den Frame ist zehn plus die Anzahl der mit der nächsten Kugel umgeworfenen Pins.

Wenn nach beiden Bällen noch mindestens einer der zehn Pins steht, ist das Ergebnis für diesen Frame einfach die Gesamtzahl der in diesen beiden Bällen umgeworfenen Pins.

Wenn du im letzten (10.) Frame einen Spare erzielst, erhältst du eine weitere Bonuskugel. Wenn du im letzten (10.) Frame einen Strike erzielst, erhältst du zwei weitere Bonuskugeln. Diese Bonuskugeln werden in der gleichen Runde geworfen. Wenn ein Bonusball alle Pins umwirft, wird der Vorgang nicht wiederholt. 

Die Bonuskugeln werden nur zur Berechnung des Ergebnisses des letzten Frames verwendet.

Der Spielstand ist die Summe aller Frame-Punkte.

Symbol meanings
X zeigt einen Streik an
/ zeigt einen Spare an
- zeigt ein Miss an
| zeigt eine Frame begrenzung an
Die Zeichen nach dem || bezeichnen Bonuskugeln

9-|9-|9-|9-|9-|9-|9-|9-|9-|9-||
X|X|X|X|X|X|X|X|X|X||XX
5/|5/|5/|5/|5/|5/|5/|5/|5/|5/||5
X|7/|9-|X|-8|8/|-6|X|X|X||81
"""
doctest.testmod()
"""



"""
