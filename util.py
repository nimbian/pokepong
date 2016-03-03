from pygame.image import load
from pygame import display
images = 'images/'


def loadalphaimg(img):
    return loadimg(img).convert_alpha()

def loadimg(img):
    return load(images + img)

def alphabet():
    alpha_dict = dict()
    alph = [' ','!','#','&',"'",'(',')','+',',','_','.','/','0','1','2','3','4','5','6','7','8','9',':',';','?','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','[',']','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','#','$','-','=','+','>','^','%','~','','']
    c = 0
    for i in range(47,1168,140):
        for j in range(16,791,86):
            alpha_dict[alph[c]] = (j,i,54,60)
            c+=1
    return alpha_dict

