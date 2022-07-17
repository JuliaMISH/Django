from django import template

register = template.Library()


BAD_WORDS = {
   'Urgent': 'U*****',
   'fun': 'f**',
}


@register.filter(name='censor')
def censor(text):
   a = list(text.split(" "))
   print(a)
   c = []
   for i in a:
      print(i)
      if i in BAD_WORDS:
         print('f')
         b = i.replace(i, BAD_WORDS[i])
         print(b)
         c.append(b)
      else:
         c.append(i)
   return f'{" ".join(c)}'