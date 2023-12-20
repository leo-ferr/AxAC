from adder import Adder
import numpy as np
import math
import random
import os


class FA(Adder):
    def __init__(self, a, b, save=False):
        
        self.save = save
        self.SUM = 0
        self.CODIFICATION = ['a', 'b', 'cin']

        self.sum = 0
        self.carry = 0

        self.inputs = 3
        self.outputs = 2
        self.poss = int(math.pow(self.inputs, self.outputs))

        self.set_values(a, b)

    def ax_add_FA(self, a, b, cin):
        #                 0  1  2
        possibilities = [a, b, cin]

        return possibilities[self.sum], possibilities[self.carry]

    def adder_FA(self, k=0):
        results = []
        BITS = 8
        LENGTH = BITS - 1

        for i in range(len(self.a)): ## aqui estou estimulando as estradas do 3-2
            a = self.a[i]
            b = self.b[i]


            carrys = []
            sums = []

            ##### compressors #####

            for i in range(k):
                if i == 0:
                    s, carry = self.ax_add_FA(a[LENGTH], b[LENGTH], False)
                else:
                    s, carry = self.ax_add_FA(a[LENGTH - i], b[LENGTH - i], carrys[i - 1])

                sums.append(s)
                carrys.append(carry)


            for i in range(k, BITS):
                if i == 0:
                    s, carry = self.FA(a[LENGTH], b[LENGTH], False)

                else: 
                    s, carry = self.FA(a[LENGTH - i], b[LENGTH - i], carrys[i - 1])
   
                sums.append(s)
                carrys.append(carry)

            sums.append(carrys.pop())

            sums.reverse()

            ######## converte para binario #######
            numero_bin = self.bool_to_bin(sums)

            ####### converte  o numero para decimal e adiciona na lista de resultados aproximados #######
            results.append(int(numero_bin, 2))
            
        return results

    def run_ax(self):
        for k in range(9):  # range from 0 to 8
            results = []
            print(f"---- K = {k} ----")
            for _ in range(self.poss):
                r = self.adder_FA(k)

                try:
                    pres = self.corrcoef(self.SUM, r)
                    # pres = round(pres * 100, 2)   # if enabled, some values will be rounded to 100 when they are not.

                    if math.isnan(pres): # corrcoef can return "nan"
                        pres = 0

                except:
                    pres = -1

                results.append({'sum': self.sum,
                            'carry': self.carry,
                            'pres': pres,
                            })

                print(f"{self.CODIFICATION[self.sum]:^3} {self.CODIFICATION[self.carry]:^3} = {pres}")

                self.next_combination()

            if self.save:
                with open(f"./result_FA_k_{k}.txt", "w") as f:
                    for i in results:
                        f.write(f"{self.CODIFICATION[i['sum']]:3} {self.CODIFICATION[i['carry']]:3} {i['pres']:5}\n")

    def next_combination(self):
        self.carry += 1

        if self.carry >= self.inputs:
            self.carry = 0
            self.sum += 1

        if self.sum >= self.inputs:
            self.sum = 0

    def set_values(self, a, b):
        if len(a) != len(b):
            raise ValueError("The number of values of 'a' and 'b' must be the same!")

        a = np.array(a)
        b = np.array(b)

        self.SUM = a + b

        self.a = [self.bin_to_bool(bin(i)[2:].zfill(8)) for i in a]
        self.b = [self.bin_to_bool(bin(i)[2:].zfill(8)) for i in b]


if __name__ == "__main__":
    n = 10_000 # number of values

    a = np.array([random.randint(0, 255) for _ in range(n)]) # n 8-bit values
    b = np.array([random.randint(0, 255) for _ in range(n)]) # n 8-bit values
    

    ad = FA(a, b, save=True)

    print("Testing the inputs...")
    ad.run_ax()
