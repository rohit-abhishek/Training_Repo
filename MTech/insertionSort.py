numberArray = [31,41,59,26,41,58]
 
for j in range(1,len(numberArray)):
    key = numberArray[j]
    i = j - 1

    while i >= 0 and numberArray[i] < key:
        numberArray[i+1] = numberArray[i]
        i = i-1
    numberArray[i+1] = key 

print (numberArray)