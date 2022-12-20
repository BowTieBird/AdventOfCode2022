file = open("input.txt")

key = 811589153
originalList = [int(line) for line in file.readlines()]
n = len(originalList)
outputList = [(x*key) for x in originalList]
encryptedList =  [(x*key) % (n-1) for x in originalList]

decryptedList = [x for x in encryptedList]
index_of_x_in_decrypted_list = [i for i in range(n)]
mixed_indices = [i for i in range(n)]

for _ in range(10):
    for i in range(n):
        j = index_of_x_in_decrypted_list[i]
        assert i == mixed_indices[j]
        x = encryptedList[i] 
        assert x == decryptedList[j]

        new_j = (j + x)
        while (new_j >= n): new_j -= n-1
        while (new_j <= 0): new_j += n-1

        del decryptedList[j]
        decryptedList.insert(new_j, x)
        del mixed_indices[j]
        mixed_indices.insert(new_j, i)

        index_of_x_in_decrypted_list[i] = new_j
        if j < new_j:
            for ind in mixed_indices[j:new_j]:
                index_of_x_in_decrypted_list[ind] -= 1
        else:
            for ind in mixed_indices[new_j+1:j+1]:
                index_of_x_in_decrypted_list[ind] += 1
        
        # for q in range(n):
        #     assert decryptedList[index_of_x_in_decrypted_list[q]] == encryptedList[q]
        #     assert mixed_indices[index_of_x_in_decrypted_list[q]] == q

        # print(decryptedList)
        # print(mixed_indices)
        # print(index_of_x_in_decrypted_list)
        # print()
zero = decryptedList.index(0)
grove = [outputList[mixed_indices[(zero + 1000) % n]] , outputList[mixed_indices[(zero + 2000) % n]] , outputList[mixed_indices[(zero + 3000)%n]]]
print(grove)
print(sum(grove))


