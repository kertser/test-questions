import asyncio
import aiohttp
from typing import List

async def fetch_text(url:str) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    if response.status >= 500:
                        print("Server Error")
                        exit(1)
                    else:
                        print("Successful Response")
                        return await response.text()
            except AssertionError as error:
                print('Assertion Error')
                exit(1)
    except aiohttp.ClientError as error:
        print("Network Error:", error)

def rotate_90deg(matrix: list) -> List[int]:
    # transpose and reverse each row to rotate by 90deg
    return [list(reversed(x)) for x in zip(*matrix)]

async def get_matrix(url: str) -> List[int]:
    # Reads the testcase from url

    text = await fetch_text(url)
    print('This is a test case:\n',text)

    # Prepare the integer matrix from textlines
    lines = text.strip().split("\n")
    matrix  = [line.split('|') for line in lines][1::2]
    for i, sublist in enumerate(matrix):
        matrix[i] = [int(element.strip()) for element in sublist if element != '']
    # In this stage, the matrix is a list of lists of integers.

    traversal = []
    while matrix:
        # strip, pop, rotate - until no more elements in matrix
        matrix = rotate_90deg(matrix)
        element = matrix.pop(0)
        traversal.append(element[::-1])

    # Return the flattened list of traversal elements
    return [element for sublist in traversal for element in sublist]

if __name__ == "__main__":
    url = "https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt"
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy()) #This is for windows
    print('TRAVERSAL = ',asyncio.run(get_matrix(url)))
