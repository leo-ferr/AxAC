from adder import Adder
import numpy as np
import math
import random
import os


class Adder_4_2(Adder):
    def __init__(self, a, b, c, d, save=False):
        self.save = save
        self.SUM = 0
        self.CODIFICATION = ['a', 'b', 'c', 'd', 'cin']

        self.sum = 0
        self.carry = 0
        self.cout = 0

        self.inputs = 5
        self.outputs = 3
        self.poss = int(math.pow(self.inputs, self.outputs))

        self.set_values(a, b, c, d)

    def ax_add4_2(self, a, b, c, d, cin):
        #                0  1  2  3    4
        possibilities = [a, b, c, d, cin]

        return possibilities[self.sum], possibilities[self.carry], possibilities[self.cout]

    def adder_4_2(self, k=0):
        results = []
        BITS = 8
        LENGTH = BITS - 1

        for i in range(len(self.a)): ## aqui estou estimulando as estradas do 8-2
            a = self.a[i]
            b = self.b[i]
            c = self.c[i]
            d = self.d[i]


            carrys_Lr = []
            carrys = []
            couts = []
            sums = []
            r = []

            ##### compressors #####

            for i in range(k):
                if i == 0:
                    s, carry, cout = self.ax_add4_2(a[LENGTH], b[LENGTH], c[LENGTH], d[LENGTH], False)
                else:
                    s, carry, cout = self.ax_add4_2(a[LENGTH - i], b[LENGTH - i], c[LENGTH - i], d[LENGTH - i], couts[i - 1])

                sums.append(s)
                carrys.append(carry)
                couts.append(cout)


            for i in range(k, BITS):
                if i == 0:
                    s, carry, cout = self.add_4_2(a[LENGTH], b[LENGTH], c[LENGTH], d[LENGTH], False)

                else: 
                    s, carry, cout = self.add_4_2(a[LENGTH - i], b[LENGTH - i], c[LENGTH - i], d[LENGTH - i], couts[i - 1])
   
                sums.append(s)
                carrys.append(carry)
                couts.append(cout)

            r.append(sums.pop(0))

            ####### recombination #######

            for i in range(BITS - 1):
                if i == 0:
                    s, carry = self.HA(sums[i], carrys[i])

                else:
                    s, carry = self.FA(sums[i], carrys[i], carrys_Lr[i - 1])

                r.append(s)
                carrys_Lr.append(carry)

            s, carry = self.FA(carrys[-1], couts[-1], carrys_Lr[-1])
            r.append(s)
            r.append(carry)

            r.reverse()

            numero_bin = self.bool_to_bin(r)

            results.append(int(numero_bin, 2))

        return results

    def run_ax(self):
        for k in range(9): # range from 0 to 8
            results = []
            print(f"---- K = {k} ----")
            for _ in range(self.poss):
                r = self.adder_4_2(k)

                try:
                    pres = self.corrcoef(self.SUM, r)
                    # pres = round(pres * 100, 2)   # if enabled, some values will be rounded to 100 when they are not.

                    if math.isnan(pres):
                        pres = 0

                except:
                    pres = -1

                results.append({'sum': self.sum,
                        'carry': self.carry,
                        'cout': self.cout,
                        'pres': pres,
                        })

                print(f"{self.CODIFICATION[self.sum]:3} {self.CODIFICATION[self.carry]:3} {self.CODIFICATION[self.cout]:3} {pres}")

                self.next_combination()

            with open(f"./result_4_2_k_{k}.txt", "w") as f:
                for i in results:
                    f.write(f"{self.CODIFICATION[i['sum']]:3} {self.CODIFICATION[i['carry']]:3} {self.CODIFICATION[i['cout']]:3} {i['pres']}\n")

    def next_combination(self):
        self.cout += 1

        if self.cout >= self.inputs:
            self.cout = 0
            self.carry += 1

        if self.carry >= self.inputs:
            self.carry = 0
            self.sum += 1

        if self.sum >= self.inputs:
            self.sum = 0

    def set_values(self, a, b, c, d):
        if len(a) != len(b) != len(c) != len(d):
            raise ValueError("The number of values of 'a', 'b', 'c' and 'd' must be the same!")

        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        d = np.array(d)

        self.SUM = a + b + c + d

        self.a = [self.bin_to_bool(bin(i)[2:].zfill(8)) for i in a]
        self.b = [self.bin_to_bool(bin(i)[2:].zfill(8)) for i in b]
        self.c = [self.bin_to_bool(bin(i)[2:].zfill(8)) for i in c]
        self.d = [self.bin_to_bool(bin(i)[2:].zfill(8)) for i in d]


if __name__ == "__main__":
    n = 10_000 # number of values

    a = np.array([random.randint(0, 255) for _ in range(n)]) # n 8-bit values 
    b = np.array([random.randint(0, 255) for _ in range(n)]) # n 8-bit values
    c = np.array([random.randint(0, 255) for _ in range(n)]) # n 8-bit values
    d = np.array([random.randint(0, 255) for _ in range(n)]) # n 8-bit values
    

    ad = Adder_4_2(a, b, c, d, save=True)

    print("Testing the inputs...")
    ad.run_ax()
