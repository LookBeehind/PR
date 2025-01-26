import http.client
import json
import ssl
import argparse

class ShopAPIClient:
    def __init__(self, base_url: str="localhost", port: int=5001):
        self.base_url = base_url
        self.port = port
        context = ssl._create_unverified_context()
        self.conn = http.client.HTTPSConnection(self.base_url, self.port, context=context)

    def __del__(self):
        self.conn.close()

    def _send_request(self, method, endpoint, body=None, headers=None):
        if headers is None:
            headers = {'Content-Type': 'application/json'}

        self.conn.request(method, endpoint, body=body, headers=headers)

        try:
            response = self.conn.getresponse()
            if response.status == 200:
                data = response.read().decode("utf-8")
                if data:
                    return json.loads(data)
                return None
            else:
                raise Exception(f"Failed to {method} {endpoint}. Status Code: {response.status}."
                                f"\nResponseBody: {response.read().decode('utf-8')}")
        except Exception as e:
            raise Exception(f"Error with {method} request to {endpoint}: {e}")

    def get_categories(self):
        categories = self._send_request("GET", "/api/Category/categories")
        print("Categories:", categories)

    def get_category(self, category_id):
        endpoint = f"/api/Category/categories/{category_id}"
        catgory = self._send_request("GET", endpoint)
        print(f"Category {category_id}: ", catgory)

    def create_category(self, title):
        category_data = json.dumps({"title": title})
        endpoint = "/api/Category/categories"
        created_category = self._send_request("POST", endpoint, body=category_data)
        print(f"Created Category: {created_category}")

    def delete_category(self, category_id):
        endpoint = f"/api/Category/categories/{category_id}"
        self._send_request("DELETE", endpoint)
        print(f"Category {category_id} deleted successfully.")

    def update_category(self, category_id, new_title):
        category_data = json.dumps({"title": new_title})
        endpoint = f"/api/Category/{category_id}"
        updated_category = self._send_request("PUT", endpoint, body=category_data)
        print(f"Updated Category: {updated_category}")

    def create_product(self, category_id, product):
        product_data = json.dumps(product)
        endpoint = f"/api/Category/categories/{category_id}/products"
        updated_category = self._send_request("POST", endpoint, body=product_data)
        print(f"New product created: {updated_category}")

    def get_products(self, category_id):
        endpoint = f"/api/Category/categories/{category_id}/products"
        products = self._send_request("GET", endpoint)
        print(f"Products: {products}")


def main():
    parser = argparse.ArgumentParser(description="API client for interacting with the shop.")
    parser.add_argument('-m', '--method', choices=['GET', 'POST', 'DELETE', 'PUT'], required=True, help="HTTP method to use (GET, POST, DELETE, PUT).")
    parser.add_argument('-i', '--id', type=int, help="Category ID.")
    parser.add_argument('-d', '--data', type=str, help="Data to send with POST or PUT request (as a JSON string).")

    args = parser.parse_args()

    api_client = ShopAPIClient(base_url="localhost", port=5001)

    try:
        if args.method == "GET":
            if args.data:
                if not args.id:
                    raise Exception("Please Provide the category id -i for the GET request.")

                api_client.get_products(args.id)
            elif args.id:
                api_client.get_category(args.id)
            else:
                api_client.get_categories()
        elif args.method == "POST":
            if not args.data:
                raise Exception("Please Provide the data -d for the POST request.")

            category_id = args.id
            if category_id:
                product = json.loads(args.data)
                api_client.create_product(category_id, product)
                return

            api_client.create_category(args.data)
        elif args.method == "DELETE":
            if not args.id:
                raise Exception("Please Provide the category id -i for the DELETE request.")

            api_client.delete_category(args.id)
        elif args.method == "PUT":
            if not args.data:
                raise Exception("Please Provide the data -d for the PUT request.")
            if not args.id:
                raise Exception("Please Provide the category id -i for the PUT request.")

            api_client.update_category(args.id, args.data)

    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
