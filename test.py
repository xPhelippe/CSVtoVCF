
outFileToTest = 0


f = open('./test/test.vcf','r')

testedCount = 0
totalCount = 0
testedNames = []
failedNames = []
successfulNames= []
for line in f.readlines():

    if line.startswith("FN:"):
        testedNames.append(line)
        totalCount = totalCount + 1
    

f.close



f = open('./out/out' + str(outFileToTest) + '.vcf')

for line in f.readlines():


    if line.startswith("FN:"):
        
        if line in testedNames:
            print("MATCH: " + line)
            successfulNames.append(line)
        else:
            print("NOT A MATCH: "  + line)
            failedNames.append(line)
        
        testedCount = testedCount + 1
        
f.close()
print(successfulNames)
print(failedNames)
print("Total Count: " + str(totalCount))
print("Tested Count: " + str(testedCount))