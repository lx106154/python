import hashlib as hs
from getpass import getpass

def encrypt(msg, N, E):
    return [(ord(s) ** E) % N for s in msg]


def lst2msg(lst):
    '''
    This function generates a string splitted by ',' from a list of encrypted
    integers.
    '''
    str_lst = [str(i) for i in lst]
    msg = ','.join(str_lst)
    return msg


def msg2lst(msg):
    '''
    This function generates a list of encrypted integers from a string
    splitted by ','.
    '''
    str_lst = msg.split(',')
    lst = [int(i) for i in str_lst]
    return lst


def password(enc_msg, usr, passwd, N, D):
    def decrypt(enc_msg, N, D):
        return ''.join([chr((s ** D) % N) for s in enc_msg])

    dict = {'hherbol1':'cc4f0932d664a47b6a5d74b7b9023ce10db48991c64bcd849ff98b6ddbc9b078d600fccd51978621b0f5611100883c929bb549a39c4449bdd0666f8a7ac7c8ed', 'zchen55':'896ebf4b00294d80bd83156069f2dba16441e32fee0b05a8c22a2f7b412ac702d140dd839103c0441d9c94ca32297f52ea85caf35487b0d57f26c4faedd8a45d'}

    if dict[usr] == hs.sha512((passwd + 'delta66').encode()).hexdigest():
        return decrypt(enc_msg, N, D)
    elif usr in dict.keys():
        raise Exception('The password is not correct')
    else:
        raise Exception('The username does not exist')


def start_messenger(msg_fptr, N=17947, E=7):
    '''
    This function starts the messenger. It reads in each line of input from the
    user , encrypts each line , and stores them in a list. Each line of
    encrypted text is written to a text file , the name of which is specified
    by "msg_ftpr".
    '''
    inf = 1
    while inf == 1:
        user_input = input("Please type your input, type STOP to finish:")
        if user_input == "STOP":
            break
        with open(msg_fptr, 'a') as f:
            f.write(lst2msg(encrypt(user_input, N, E)) + "#")


def read_messages(msg_fptr, N=17947, D=10103):
    '''
    Asks the user for their username and password. Reads the encrypted text
    from "msg_fptr" and decrypts it if the username/password combination is
    correct.
    '''
    usr, passwd = input('Please enter your username:'), getpass(
        'Please enter your password:')
    with open(msg_fptr, 'r') as f:
        encrypted_str0 = f.read()
    encrypted_str = encrypted_str0[0:-1]
    encrypted_lst = encrypted_str.split('#')
    msg = [password(msg2lst(enc_msg), usr, passwd, N, D)
           for enc_msg in encrypted_lst]
    return '\n'.join(msg)


if __name__ == "__main__":

    message = "This is a secret message"
    encrypted_message = encrypt(message, N=17947, E=7)
    decrypted_message = password(
        encrypted_message, "hherbol1", "Fifa", N=17947, D=10103)
    assert message == decrypted_message, "Error - Decryption failed!"

    start_messenger("messages.txt")
    messages = read_messages("messages.txt")
    print(messages)
