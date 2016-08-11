class FilterModule(object):
    ''' Ansible math jinja2 filters '''

    def filters(self):
        return {
            'grab' : grab,

        }

# usage- do stuff to a and return it.
# {{ {'a': 1, 'b': 2}|grab('a.values') }} => [ 1, 2 ]
def grab(a, eval_string):
  return eval(eval_string)
