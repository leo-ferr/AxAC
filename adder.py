import numpy as np

class Adder:
    def corrcoef(self, data0, data1):
        def norm_data(data):
            mean_data=np.mean(data)
            std_data=np.std(data, ddof=1)
            return (data-mean_data)/(std_data)

        return (1.0/(data0.size-1)) * np.sum(norm_data(data0)*norm_data(data1))

    def flatten(self, l):
        r = []
        for element in l:
            if isinstance(element, list):
                r.extend(self.flatten(element))
            else:
                r.append(element)
        return r

    def bin_to_bool(self, n):
        r = []

        for i in n:
            if i == '0':
                r.append(False)
            else:
                r.append(True)

        return r

    def bool_to_bin(self, n):
        r = []
        for i in n:
            if i == True:
                r.append('1')
            else:
                r.append('0')

        return "".join(r)

    def FA(self, a, b, cin):
        xor1 = a ^ b

        s = xor1 ^ cin
        carry = cin if xor1 == 1 else a 

        return s, carry

    def HA(self, a, b):
        s = a ^ b
        carry = a and b

        return s, carry

    def add_4_2(self, a, b, c, d, cin):
        xor1 = a ^ b
        xor2 = xor1 ^ (c ^ d)

        s = xor2 ^ cin
        carry = cin if xor2 == 1 else d 

        cout = c if xor1 == 1 else a 

        return s, carry, cout
