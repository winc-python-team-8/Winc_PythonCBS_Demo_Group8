import logging
import uu


class DecodeTransactionData:
    def __init__(self, infile, outfile, csvfile):
        self.infile = infile
        self.outfile = outfile
        self.csvfile = csvfile

    def decode_transaction_file(self):
        uu.decode('CBS_DecodeTransactionData/{0}'.format(self.infile), out_file=self.outfile, quiet=False)
        out_file = open(self.csvfile, 'w')
        with open(self.outfile, 'r') as infile:
            i = 0
            for line in infile:
                if i == 0:
                    line = "id" + (line.replace('\"', ''))
                    line = line.replace('|', ',')
                    i = 1
                else:
                    line = line.replace('\"', '').replace('|', ',')
                out_file.write(line)
            out_file.close()


