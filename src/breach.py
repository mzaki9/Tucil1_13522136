import random,time

class Sequence:
    def __init__(self, sequenceData=None, bonus=0):
        self.sequenceData = sequenceData if sequenceData is not None else []
        self.bonus = bonus

    def __eq__(self, other):
        return self.sequenceData == other.sequenceData

def search(row, col, currentSequence, direction, allSequences):
    if row < 0 or row >= matrixSizerow or col < 0 or col >= matrixSizecol:
        return allSequences

    currentSequence.append((board[row][col], row, col))


    
    if len(currentSequence) == int(bufferSize):
        #print("Found sequence:", currentSequence)
        allSequences.append(list(currentSequence))
        currentSequence.pop()
        return allSequences

    if direction == "vertical":
        for new_row in range(row + 1, matrixSizerow):
            allSequences = search(new_row, col, currentSequence, "horizontal", allSequences)
        for new_row in range(row - 1, -1, -1):
            allSequences = search(new_row, col, currentSequence, "horizontal", allSequences)
    elif direction == "horizontal":
        for new_col in range(col + 1, matrixSizecol):
            allSequences = search(row, new_col, currentSequence, "vertical", allSequences)
        for new_col in range(col - 1, -1, -1):
            allSequences = search(row, new_col, currentSequence, "vertical", allSequences)

    currentSequence.pop()
    return allSequences

def printMatrix():
    for i in range(matrixSizerow):
        for j in range(matrixSizecol):
            print(board[i][j], end=" ")
        print()

def createSequence(totalSequence, maxSequence, token):
    sequences = []
    for _ in range(int(totalSequence)):
        sequenceLength = random.randint(2, int(maxSequence))
        sequenceData = [random.choice(token) for _ in range(sequenceLength)]
        bonus = random.randint(1, 10) * 5
        sequences.append(Sequence(sequenceData, bonus))
    return sequences

def printSequence(sequences):
    for i in range(int(totalSequence)):
        print("Sequence " + str(i + 1) + ": ", end="")
        for j in range(len(sequences[i].sequenceData)):
            print(sequences[i].sequenceData[j], end=" ")
        print("Bonus: " + str(sequences[i].bonus))

def traverseAndFindSequences():
    allSequences = []
    for col in range(matrixSizecol):
        search(0, col, [], "vertical", allSequences)
    return allSequences


def compareSequences(allSequences, sequences):
    bestSequence = None
    maxTotalBonus = 0

    for foundSeq in allSequences:
        totalBonus = 0
        foundSeqData = [item[0] for item in foundSeq]

        for sequence in sequences:
            if sequence.sequenceData == foundSeqData[:len(sequence.sequenceData)]:
                totalBonus += sequence.bonus

        if totalBonus > maxTotalBonus:
            maxTotalBonus = totalBonus
            bestSequence = foundSeq

    return bestSequence, maxTotalBonus


while True:
    #Cek input CLI or txt
    print("Masukkan jenis input :")
    print("1. CLI")
    print("2. TXT")
    inputType = input("Pilih jenis input : ")

    if int(inputType) == 1:
        totalUniqueToken = input("Masukkan jumlah token unik: ")
        token = []
        token = input("Masukkan token: ").split()
        
        if len(token) != int(totalUniqueToken):
            print("Jumlah token tidak sesuai")
            exit()

        while True:
            try:
                bufferSize = int(input("Masukkan ukuran buffer: "))
                if bufferSize > 0:
                    break  
                else:
                    print("Pilih angka lebih dari 0 !!!!.")
            except ValueError:
                print("INPUT HANYA INTEGER !.")

        matrixSize = input("Masukkan ukuran matriks : ").split()
        matrixSizerow = int(matrixSize[0])
        matrixSizecol = int(matrixSize[1])
        totalSequence = input("Masukkan jumlah sequence: ")
        maxSequence = input("Masukkan jumlah maksimum sequence: ")

        sequences = createSequence(totalSequence, maxSequence, token)
        
        print("Sequence: ")
        printSequence(sequences)
        print()

        board = [[0 for i in range(matrixSizecol)] for j in range(matrixSizerow)]

        for i in range(matrixSizerow):
            for j in range(matrixSizecol):
                board[i][j] = random.choice(token)

    elif int(inputType) == 2:
        fileName = input("Masukkan nama file : ")
        filePath = "../test/" + fileName + ".txt"
        with open(filePath, "r") as file:
            lines = file.readlines()
            bufferSize = int(lines[0].split()[0])

            if bufferSize <= 0:
                print("Buffer size harus lebih dari 0")
                exit()

            matrixSize = lines[1].split()
            matrixSizerow = int(matrixSize[0])
            matrixSizecol = int(matrixSize[1])

            board = [[0 for i in range(matrixSizecol)] for j in range(matrixSizerow)]

            for i in range(matrixSizerow):
                val = lines[i + 2].split()
                for j in range(matrixSizecol):
                    board[i][j] = (val[j])

            totalSequence = int(lines[matrixSizerow + 2])
            if totalSequence <= 0:
                print("Jumlah sequence harus lebih dari 0")
                exit()

            sequences = []
            for i in range(matrixSizerow + 3, matrixSizerow + 2 + (int(totalSequence) * 2), 2):
                sequenceData = lines[i].split()
                bonus = int(lines[i+1].strip())
                sequences.append(Sequence(sequenceData, bonus))
            printSequence(sequences)   
    else:
        print("Input tidak valid")

    print("Matriks: ")
    printMatrix()
    print()

    startTime = time.time()
    allSequences = traverseAndFindSequences()
    endTime = time.time()

    #DEBUG
    # print("All Sequences:")
    # print(allSequences)

    bestSequence, totalBonus = compareSequences(allSequences, sequences)
    elapsedTimeMs = (endTime - startTime) * 1000



    print(totalBonus)
    if (totalBonus > 0):
        for item in bestSequence:
            print(" ".join(map(str, item[0:1])), end=" ")
        print()

        for item in bestSequence:
            print(", ".join(map(str, item[1:3])))

        print("\n" + str(elapsedTimeMs) + " ms \n")

    choice = input("Apakah ingin menyimpan solusi? (y/n) \n")

    if choice == "y" or choice == "Y":
        outputFileName = input("Masukkan nama file : ")
        filePath = "../test/" + outputFileName + ".txt"
        with open(filePath, "w") as file:
            file.write(str(totalBonus) + "\n")
            if (totalBonus != 0):
                for item in bestSequence:
                    file.write(" ".join(map(str, item[0:1])) + " ")
                file.write("\n")
                for item in bestSequence:
                    file.write(", ".join(map(str, item[1:3])) + "\n")
            file.write("\n" + str(elapsedTimeMs) + " ms")
        print("Solusi berhasil disimpan di " + filePath)

    print("Continue Playing ? (y/n)")
    exitChoice = input()
    if exitChoice == "y" or exitChoice == "Y":
        continue
    else:
        break