import logging
def multiline_to_single_conv(text, debug_mode = 0):

    new_text  = text.replace('"', "'") #to remove double quotes
    new_text  = ' '.join(new_text.split()) #to remove new lines

    if(debug_mode):
        print("The text is : \n")
        print(new_text)
        print("\n")
     
    return new_text