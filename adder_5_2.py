import multiprocessing
from adder import Adder
import numpy as np
import math
import random
import os


class Ax_adder_5_2(Adder):
    def __init__(self, save=False):
        self.save = save
        self.RESULT_SUM = 0
        self.CODIFICATION = ['a', 'b', 'c', 'd', 'e', 'cin1', 'cin2']

        self.sum = 0
        self.carry = 0
        self.cout1 = 0
        self.cout2 = 0

        pass

    def ax_add5_2(self, a, b, c, d, e, cin1, cin2):
        #                 0  1  2  3  4    5     6
        possibilidades = [a, b, c, d, e, cin1, cin2]

        s = possibilidades[self.sum]

        cout1 = possibilidades[self.cout1]

        cout2 = possibilidades[self.cout2]

        carry = possibilidades[self.carry]

        return s, carry, cout1, cout2
    
    def ax_adder_5_2(self, k):
        results = []
        BITS = 8
        LENGTH = BITS - 1

        for i in range(len(self.a)):
            a = self.a[i]
            b = self.b[i]
            c = self.c[i]
            d = self.d[i]
            e = self.e[i]


            carrys_Lr = []
            carrys = []
            couts1 = []
            couts2 = []
            sums = []
            r = []

            ##### compressors #####

            for i in range(k):
                if i == 0:
                    s, carry, cout1, cout2 = self.ax_add5_2(a[LENGTH], b[LENGTH], c[LENGTH], d[LENGTH], e[LENGTH], False, False)
                else:
                    s, carry, cout1, cout2 = self.ax_add5_2(a[LENGTH - i], b[LENGTH - i], c[LENGTH - i], d[LENGTH - i], e[LENGTH - i], couts1[i - 1], couts2[i - 1])

                sums.append(s)
                carrys.append(carry)
                couts1.append(cout1)
                couts2.append(cout2)


            for i in range(k, BITS):
                if i == 0:
                    s, carry, cout1, cout2 = self.add5_2(a[LENGTH], b[LENGTH], c[LENGTH], d[LENGTH], e[LENGTH], False, False)

                else: 
                    s, carry, cout1, cout2 = self.add5_2(a[LENGTH - i], b[LENGTH - i], c[LENGTH - i], d[LENGTH - i], e[LENGTH - i], couts1[i - 1], couts2[i - 1])
   
                sums.append(s)
                carrys.append(carry)
                couts1.append(cout1)
                couts2.append(cout2)

            r.append(sums.pop(0))

            ####### recombination line #######

            for i in range(BITS - 1):
                if i == 0:
                    s, carry = self.HA(sums[i], carrys[i])

                else:
                    s, carry = self.FA(sums[i], carrys[i], carrys_Lr[i - 1])

                r.append(s)
                carrys_Lr.append(carry)

            s4_2, carry4_2, out4_2 = self.add4_2(carrys[-1], couts1[-1], couts2[-1], carrys_Lr[-1], False)
            r.append(s4_2)
            s, carry = self.HA(carry4_2, out4_2)
            r.append(s)
            r.append(carry)


            r.reverse()

            numero_bin = self.bool_to_bin(r)

            results.append(int(numero_bin, 2))

        return results
    
    def __adder_5_2(self, A, B, C, D, E):
        results = []
        amount = len(A)

        for i in range(amount):
            a = A[i]
            b = B[i]
            c = C[i]
            d = D[i]
            e = E[i]


            ##### compressors #####
            s1, carry1, c1_1, c1_2 = self.add5_2(a[7], b[7], c[7], d[7], e[7], False, False)
            s2, carry2, c2_1, c2_2 = self.add5_2(a[6], b[6], c[6], d[6], e[6], c1_1, c1_2)
            s3, carry3, c3_1, c3_2 = self.add5_2(a[5], b[5], c[5], d[5], e[5], c2_1, c2_2)
            s4, carry4, c4_1, c4_2 = self.add5_2(a[4], b[4], c[4], d[4], e[4], c3_1, c3_2)
            s5, carry5, c5_1, c5_2 = self.add5_2(a[3], b[3], c[3], d[3], e[3], c4_1, c4_2)
            s6, carry6, c6_1, c6_2 = self.add5_2(a[2], b[2], c[2], d[2], e[2], c5_1, c5_2)
            s7, carry7, c7_1, c7_2 = self.add5_2(a[1], b[1], c[1], d[1], e[1], c6_1, c6_2)
            s8, carry8, c8_1, c8_2 = self.add5_2(a[0], b[0], c[0], d[0], e[0], c7_1, c7_2)

            ##### recombination #####

            sf1, carryf1 = self.FA(s2, carry1, False)
            sf2, carryf2 = self.FA(s3, carry2, carryf1)
            sf3, carryf3 = self.FA(s4, carry3, carryf2)
            sf4, carryf4 = self.FA(s5, carry4, carryf3)
            sf5, carryf5 = self.FA(s6, carry5, carryf4)
            sf6, carryf6 = self.FA(s7, carry6, carryf5)
            sf7, carryf7 = self.FA(s8, carry7, carryf6)
            s4_2, carry4_2, c4_2_1 = self.add4_2(c8_1, c8_2, carryf7, carry8, False)
            sf8, carryf8 = self.HA(carry4_2, c4_2_1)

            numero_bool = [carryf8, sf8, s4_2, sf7, sf6, sf5, sf4, sf3, sf2, sf1, s1]

            numero_bin = self.bool_to_bin(numero_bool)

            results.append(int(numero_bin, 2))

        return results

    def run_ax(self):
        results = []

        inputs = 7
        outputs = 4

        pos = int(math.pow(inputs, outputs))

        for _ in range(pos):
            r = self.ax_adder_5_2_complete(8)

            try:
                pres = self.corrcoef(self.RESULT_SUM, r)
                pres = round(pres * 100, 2)

                if math.isnan(pres):
                    pres = 0

            except:
                pres = -1

            results.append({"sum" : self.sum,
                "carry" : self.carry,
                "cout1" : self.cout1,
                "cout2" : self.cout2,
                "pres" : pres
            })

            print(f"{self.sum:^2}  {self.carry:^2} {self.cout1:^2} {self.cout2:^2} = {pres:^5}%")

            self.next()

        if self.save:
            with open("./r_5_2.txt", "w") as f:
                for i in results:
                    f.write(f"{i['sum']:^2}  {i['carry']:^2} {i['cout1']:^2} {i['cout2']:^2} {i['pres']:^5}\n")
        
        else:
            return results

    def run_ax_ks(self):

        inputs = 7
        outputs = 4

        poss = int(math.pow(inputs, outputs))

        for k in range(1, 9):
            results = []
            for _ in range(poss):
                r = self.ax_adder_5_2_complete(k)

                try:
                    pres = self.corrcoef(self.RESULT_SUM, r)

                    if math.isnan(pres):
                        pres = 0

                except:
                    pres = -1

                results.append({'sum': self.sum,
                        'carry': self.carry,
                        'cout1': self.cout1,
                        'cout2': self.cout2,
                        'pres': pres,
                        })

                print(f"{self.sum:^2} {self.carry:^2} {self.cout1:^2} {self.cout2:^2} k_{k} = {pres}")

                self.next()

            if self.save:
                with open(f"./resultados_5_2_k_{k}.txt", "w") as f:
                    for i in results:
                        f.write(f"{i['sum']:^2} {i['carry']:^2} {i['cout1']:^2} {i['cout2']:^2} {i['pres']:^5}\n")

    def run(self):
        r = self.__adder_5_2(self.a, self.b, self.c, self.d, self.e)


        return np.array(r)

    def next(self):
        self.cout2 += 1
            
        if self.cout2 >= 7:
            self.cout2 = 0
            self.cout1 += 1

        if self.cout1 >= 7:
            self.cout1 = 0
            self.carry += 1

        if self.carry >= 7:
            self.carry = 0
            self.sum += 1

        if self.sum >= 7:
            self.sum = 0

    def set_values(self, a, b, c, d, e):
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        d = np.array(d)
        e = np.array(e)

        self.RESULT_SUM = a + b + c + d + e

        self.a = [self.bin_to_bool(bin(i)[2:].zfill(8)) for i in a]
        self.b = [self.bin_to_bool(bin(i)[2:].zfill(8)) for i in b]
        self.c = [self.bin_to_bool(bin(i)[2:].zfill(8)) for i in c]
        self.d = [self.bin_to_bool(bin(i)[2:].zfill(8)) for i in d]
        self.e = [self.bin_to_bool(bin(i)[2:].zfill(8)) for i in e]


if __name__ == "__main__":
    n = 100_000

    a = np.array([random.randint(0, 255) for _ in range(n)])
    b = np.array([random.randint(0, 255) for _ in range(n)])
    c = np.array([random.randint(0, 255) for _ in range(n)])
    d = np.array([random.randint(0, 255) for _ in range(n)])
    e = np.array([random.randint(0, 255) for _ in range(n)])
    

    ad = Ax_adder_5_2(save=True)
    print("Configurando os valores...")

    ad.set_values(a, b, c, d, e)

    print("Valores configurados.")
    print("Testando as entradas...")

    ad.run_ax_ks()
