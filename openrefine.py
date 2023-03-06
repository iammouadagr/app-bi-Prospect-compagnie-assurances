def transform_value(value):

    split= value.split('-')
    if len(split) ==2:
      return (int(split[0]) + int(split[1])) / 2
    else:
       return int(split[0])

#return transform_value(value)

print(transform_value("4-3"))