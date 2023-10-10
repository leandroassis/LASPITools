import argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ferramenta desenvolvida por Leandro A. (leandro@laspi.ufrj.br)', prog="python CertTool.py")

    parser.add_argument('-m', '--module', type=str, help='Module to be tested', required=True)
    parser.add_argument('--pin', nargs="?", default="1234", type=str, help='User\'s PIN')
    parser.add_argument('--puk', nargs="?", default="12345678", type=str, help='User PUK')
    parser.add_argument('-n', '--name', type=str, nargs="?", default="ensaios", help='Base name for the token(s) labels.')
    parser.add_argument('-s', '--slots', type=int, nargs='+', help='Slots to be tested', default=0)
    parser.add_argument('--version', action='version', version='%(prog)s Release 1.0')
    parser.add_argument('-r', '--requirements', action="extend", nargs="+", type=str, help='Requirements to be tested (e.g. -r II.7, II.9, II.10-II.15', required=True)

    arguments = parser.parse_args()
    print(arguments)
