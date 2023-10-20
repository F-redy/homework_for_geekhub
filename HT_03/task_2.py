# 2. Write a script to remove an empty elements from a list.
# Test list: [(), ('hey'), ('',), ('ma', 'ke', 'my'), [''], {}, ['d', 'a', 'y'], '', []]


test_list = [(), ('hey'), ('',), ('ma', 'ke', 'my'), [''], {}, ['d', 'a', 'y'], '', []]
print(f'Started list:\n{test_list}')

test_list = [value for value in test_list if value]
print(f'Changed list:\n{test_list}')
