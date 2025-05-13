import argparse
import json
import time
import requests
from prettytable import PrettyTable


class DehashedAPI:
    def __init__(self, api_key):
        self.headers = {
            'Content-Type': 'application/json',
            'Dehashed-Api-Key': api_key
        }
        self.base_url = 'https://api.dehashed.com/v2/search'

    def search(self, query_value, max_results=10000, wildcard=False, regex=False, de_dupe=False):
        results = []
        page = 1
        size = 100  

        while len(results) < max_results:
            payload = {
                'query': query_value,
                'page': page,
                'size': size,
                'wildcard': wildcard,
                'regex': regex,
                'de_dupe': de_dupe
            }

            try:
                response = requests.post(
                    self.base_url,
                    json=payload,
                    headers=self.headers
                )

                if response.status_code == 403:
                    print("! Error 403: Access Denied. Check your API key.")
                    return []
                elif response.status_code == 401:
                    print("! Error 401: Unauthorized access. Check your API key.")
                    return []
                
                response.raise_for_status()

                data = response.json()
                results.extend(data.get('entries', []))

                
                balance = data.get('balance', 0)
                print(f"Balance of requests: {balance}")

                if len(data.get('entries', [])) < size:
                    break

                page += 1
                time.sleep(0.5)

            except requests.exceptions.RequestException as e:
                print(f"! Request error: {e}")
                break

        return results


def main():
    parser = argparse.ArgumentParser(description='Dehashed API Search Tool v2')
    parser.add_argument('-k', '--key', required=True, help='Dehashed API key')
    parser.add_argument('-q', '--query', required=True, help='Search value (domain/username/phone/email)')
    parser.add_argument('-o', '--output', default='results.json', help='Output file (default: results.json)')
    parser.add_argument('-a', '--append', action='store_true', help='Append to output file')
    parser.add_argument('--wildcard', action='store_true', help='Enable wildcard search')
    parser.add_argument('--regex', action='store_true', help='Enable regex search')
    parser.add_argument('--dedupe', action='store_true', help='Remove duplicate results')
    args = parser.parse_args()

  
    if args.wildcard and args.regex:
        print("! Error: Cannot use wildcard and regex search at the same time")
        return

  
    dehashed = DehashedAPI(args.key)

    print(f" Searching for: {args.query}")
    results = dehashed.search(
        args.query,
        wildcard=args.wildcard,
        regex=args.regex,
        de_dupe=args.dedupe
    )

    if not results:
        print("! No results found.")
        return


    table = PrettyTable()
    table.field_names = ["Email", "Username", "Password", "Phone", "IP", "Source"]
    table.max_width = 30
    
    for entry in results[:50]:  
        table.add_row([
            ', '.join(entry.get('email', [])) or 'N/A',
            ', '.join(entry.get('username', [])) or 'N/A',
            entry.get('password', 'N/A'),
            ', '.join(entry.get('phone', [])) or 'N/A',
            ', '.join(entry.get('ip_address', [])) or 'N/A',
            entry.get('database_name', 'N/A')
        ])
    
    print(table)
    print(f"\nResults found: {len(results)} (shown first 50)")


    mode = 'a' if args.append else 'w'
    try:
        with open(args.output, 'r') as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    existing_data.extend(results)

    with open(args.output, 'w') as f:
        json.dump(existing_data, f, indent=2, ensure_ascii=False)

    print(f"\n(+) The results are saved in{args.output}")


if __name__ == "__main__":
    main()
