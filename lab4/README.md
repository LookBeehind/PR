# Dicol Oliviu
### TI-211 FR
### Lab 4 - Aplicație de tip client HTTP
### --------------------------------------------------------------------------------------------------------------------
## Option arguments:
1. `-m` HTTP method to use (GET, POST, PUT, DELETE).
2. `-i` Category ID.
3. `-d` Data to send with POST or PUT request (as a JSON string).

## Available functions
1. GET all categories:<br>
`python http_handler.py -m GET`

2. Get the details of 1 Category:<br>
`python http_handler.py -m GET -i 1`

3. Create a mew category:<br>
`python http_handler.py -m POST -d title`

4. Delete an existing category:<br>
`python http_handler.py -m DELETE -i 13`

5. Edit the title of specific category:<br>
`python http_handler.py -m PUT -d "New Category" -i 1`

6. Create a new product within a specific category:<br>
`python http_handler.py -m POST -d "{\"id\":0,\"title\":\"product\",\"price\":0,\"categoryId\":0}" -i 1`

7. List the products within a category:<br>
`python http_handler.py -m GET -i 1 -d products`

