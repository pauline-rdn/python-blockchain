import hashlib
import json

def stringify(data):
     return json.dumps(data)

def crypto_hash(*data):

    """
    Return a sha-256 hash of the given data
    """

    stringify_data = sorted(map(stringify, data))
    joined_data = ''.join(stringify_data)

    return hashlib.sha256(joined_data.encode('utf-8')).hexdigest()


def main():
    print(f"crypto_hash(data): {crypto_hash('one', 2, [3])}")
    print(f"crypto_hash(data2): {crypto_hash(2, 'one', [3])}")

if __name__ == '__main__':
    main()