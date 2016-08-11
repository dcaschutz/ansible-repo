class FilterModule(object):
    ''' Ansible math jinja2 filters '''

    def filters(self):
        return {
            'pyfilter' : pyfilter,
            'pymap' : pymap,
            'pyflatten' : pyflatten,
        }

# usage- filter a list
# "{{ [ { 'a': 1 }, { 'a': 2 }]|pyfilter('lambda x: x[\"a\"] == 1') }}" => { 'a': 1 }
def pyfilter(input, filter_lambda):
  return filter(eval(filter_lambda), input)

# usage- map an object- list or hash
# "{{ { 'a': 1 , 'b': 2 }|pymap('lambda x,y: x, y+1) }}" => { 'a': 2, 'b': 3 }
def pymap(input, filter_lambda):
  return map(eval(filter_lambda), input)

def pyflatten(input_list):
  return [item for sublist in input_list for item in sublist]
