import hashlib
import json
import os


blockchain_dir = os.curdir + '/blockchain/'  # Dir where will be blocks


def generate_hash(filename):
    file = open(blockchain_dir + filename, 'rb').read()
    return hashlib.sha256(file).hexdigest()


def get_files():
    files = os.listdir(blockchain_dir)
    return sorted([int(i) for i in files])


def check_integrity():
    files = get_files()
    result = []
    for file in files[1:]:
        f = open(blockchain_dir + str(file))
        h = json.load(f)['hash']

        last_file = str(file - 1)
        actual_hash = generate_hash(last_file)

        res = "Ok" if h == actual_hash else "Corrupted"

        result.append({f"Block: {last_file} is {res}"})

    return result


def write_block(sender, amount, recipient, hash=''):
    files = get_files()
    last_file = files[-1]

    filename = str(last_file + 1)
    prev_hash = generate_hash(str(last_file))

    data = {
        "sender": sender,
        "amount": amount,
        "recipient": recipient,
        "hash": prev_hash
    }

    with open(blockchain_dir + filename, 'w') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def main():
    print(check_integrity())
    # write_block("Vanya", 512, "Vitalik")  # Add a new transaction


if __name__ == '__main__':
    main()
