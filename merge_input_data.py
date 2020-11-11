import json

if __name__ == '__main__':
    output = {}

    for file_name in ['AAVE.json', 'CTXC.json', 'OXT.json']:
        with open(file_name, 'r') as file:
            for date, coins in json.loads(file.read()).items():
                if date not in output:
                    output[date] = coins
                else:
                    output[date].update(coins)

    with open('input_data.json', 'w') as file:
        file.write(json.dumps(output))
