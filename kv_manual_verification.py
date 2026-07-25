size = 31

triple_array = [[[0 for _ in range(size)] for _ in range(size)] for _ in range(size)]
with open('results/cube_p31_fullmult.txt') as file:

        file.readline()
        file.readline()
        file.readline()
        file.readline()
        for i in range(size):
                for j in range(size):
                        for k in range(size):
                               l = file.readline().split(' ') 
                               triple_array[i][j][k] = int(l[3])
                               assert (triple_array[i][j][k] <= 3*(size -1))
                               assert (triple_array[i][j][k] >= 0)

        for i in range(size):
                for j in range(size):
                        k = (2*size-i-j)%size
                        s = set()
                        s.add(triple_array[i][j][k])
                        for v in range(1,size):
                            s.add(triple_array[(i+v)%size][j][k])
                            s.add(triple_array[i][(j+v)%size][k])
                            s.add(triple_array[i][j][(k+v)%size])
                        assert(len(s) == 3*size-2)
        print('all good')
                        
                                
