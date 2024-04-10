import logging
def multiline_to_single_conv(text, debug_mode = 0):

    new_text  = text.replace('"', "'") #to remove double quotes
    new_text  = new_text.replace('\n',' ') #to remove new lines

    if(debug_mode):
        print(new_text)
        print("\n")
     
    return new_text
