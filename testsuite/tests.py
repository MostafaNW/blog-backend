import requests
import json
posts_sol = ''
author_sol = ''

posts_prod = 'http://127.0.0.1:5000/api/posts'
author_prod = 'http://127.0.0.1:5000/api/authors'
test_num = 0
passes = 0

def test1():
    '''
    Basic test with a single tag
    '''
    prod_url = f'{posts_prod}?tags=tech'
    sol_url = f'{posts_sol}?tags=tech'
    global test_num
    test_num += 1
    test(prod_url,sol_url,test_num)

def test2():
    '''
    Basic test with more than one tag
    '''
    prod_url = f'{posts_prod}?tags=tech,science,startup'
    sol_url = f'{posts_sol}?tags=tech,science,startup'
    global test_num
    test_num += 1
    test(prod_url,sol_url,test_num)

def test3():
    '''
    Test Empty tag supplied
    '''
    prod_url = f'{posts_prod}?tags='
    sol_url = f'{posts_sol}?tags='
    global test_num
    test_num += 1
    test(prod_url,sol_url,test_num)

def test4():
    '''
    Test sortyBy id
    '''
    prod_url = f'{posts_prod}?tags=tech,science,startup&sortBy=id'
    sol_url = f'{posts_sol}?tags=tech,science,startup&sortBy=id'
    global test_num
    test_num += 1
    test(prod_url,sol_url,test_num)

def test5():
    '''
    Test sortBy reads
    '''
    prod_url = f'{posts_prod}?tags=tech,science,startup&sortBy=reads'
    sol_url = f'{posts_sol}?tags=tech,science,startup&sortBy=reads'
    global test_num
    test_num += 1
    test(prod_url,sol_url,test_num)

def test6():
    '''
    Test sortBy likes
    '''
    prod_url = f'{posts_prod}?tags=tech,science,startup&sortBy=likes'
    sol_url = f'{posts_sol}?tags=tech,science,startup&sortBy=likes'
    global test_num
    test_num += 1
    test(prod_url,sol_url,test_num)

def test7():
    '''
    Test sortBy popularity
    '''
    prod_url = f'{posts_prod}?tags=tech,science,startup&sortBy=popularity'
    sol_url = f'{posts_sol}?tags=tech,science,startup&sortBy=popularity'
    global test_num
    test_num += 1
    test(prod_url,sol_url,test_num)

def test8():
    '''
    Test invalid sortBy parameter
    '''
    prod_url = f'{posts_prod}?tags=tech,science,startup&sortBy=hello'
    sol_url = f'{posts_sol}?tags=tech,science,startup&sortBy=hello'
    global test_num
    test_num += 1
    test(prod_url,sol_url,test_num)

def test9():
    '''
    Test sort direction as descending
    '''
    prod_url = f'{posts_prod}?tags=tech,science,startup&sortBy=popularity&direction=desc'
    sol_url = f'{posts_sol}?tags=tech,science,startup&sortBy=popularity&direction=desc'
    global test_num
    test_num += 1
    test(prod_url,sol_url,test_num)
def test10():
    '''
    Test sort direction as ascending explicitely
    '''
    prod_url = f'{posts_prod}?tags=tech,science,startup&direction=asc'
    sol_url = f'{posts_sol}?tags=tech,science,startup&direction=asc'
    global test_num
    test_num += 1
    test(prod_url,sol_url,test_num)

def test11():
    '''
    Test invalid sort direction
    '''
    prod_url = f'{posts_prod}?tags=tech,science,startup&sortBy=id&direction=invalid'
    sol_url = f'{posts_sol}?tags=tech,science,startup&sortBy=id&direction=invalid'
    global test_num
    test_num += 1
    test(prod_url,sol_url,test_num)

def test12():
    '''
    Test Step4, accurate author data gathering
    '''
    global test_num
    test_num += 1
    test_final(author_prod,author_sol,test_num)

def test(prod_url, sol_url, test_num):
    global passes
    res_prod = requests.get(prod_url)
    res_sol = requests.get(sol_url)
    prod_code= res_prod.status_code
    sol_code = res_sol.status_code
    prod_data = json.loads(res_prod.content)
    sol_data = json.loads(res_sol.content)
    if (prod_data == sol_data) and (prod_code == sol_code):
        print(f'TEST{test_num}: PASS')
        passes += 1
    else:
        print(f'TEST{test_num}: FAIL')
        print(f'PRODUCTION CONTENT:{prod_data}\n\n\n\n\nSOLUTION CONTENT:{sol_data}')

def test_final(prod_url, sol_url, test_num):
    '''
    For Part 4
    Sorts the tags so we can check for equivalency, since I return them in a random order
    '''
    global passes
    res_prod = requests.get(prod_url)
    res_sol = requests.get(sol_url)
    prod_code= res_prod.status_code
    sol_code = res_sol.status_code
    prod_data = json.loads(res_prod.content)['authors']
    sol_data = json.loads(res_sol.content)['authors']
    for author in prod_data:
        author['tags'].sort()
    for author in sol_data:
        author['tags'].sort()
    if (prod_data == sol_data) and (prod_code == sol_code):
        print(f'TEST{test_num}: PASS')
        passes += 1
    else:
        print(f'TEST{test_num}: FAIL')
        print(f'PRODUCTION CONTENT:{prod_data}\n\n\n\n\nSOLUTION CONTENT:{sol_data}')
def run_tests():
    global passes
    global test_num
    print("Starting tests....")
    test1()
    test2()
    test3()
    test4()
    test5()
    test6()
    test7()
    test8()
    test9()
    test10()
    test11()
    test12()
    print(f"\nTests complete! {passes}/{test_num} PASSED")
if __name__ == '__main__':
    run_tests()
