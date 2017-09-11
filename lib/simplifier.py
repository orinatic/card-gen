import re
import operator

class Simplifier:
    def simplify(s):
        split = (re.split(r"(\+|-)", s))
        nums = []
        prev = "+"
        text = []
        for token in split:
            if(token.strip().isdigit()):
                if(prev == "+"):
                    nums.append(int(token))
                elif(prev == "-"):
                    nums.append(-int(token))
                else:
                    raise Exception(f"Token is {token}, and previous token is {prev}. Expected previous token to be '+' or '-'")
                text = text[:-1]
            else:
                prev = token
                text.append(token)
        out = "".join(text)
                
        if(not nums == []):
            out += "{:+.0f}".format(sum(nums))
        if(out[0] == "+"):
            out = out[1:]
            
        return out
            
        
