"""Function definitions that are used in LSB steganography."""
from matplotlib import pyplot as plt
import numpy as np
import binascii
import cv2 as cv
import math
plt.rcParams["figure.figsize"] = (18,10)


def encode_as_binary_array(msg):
    """Encode a message as a binary string."""
    msg = msg.encode("utf-8")
    msg = msg.hex()
    msg = [msg[i:i + 2] for i in range(0, len(msg), 2)]
    msg = [ "{:08b}".format(int(el, base=16)) for el in msg]
    return "".join(msg)


def decode_from_binary_array(array):
    """Decode a binary string to utf8."""
    array = [array[i:i+8] for i in range(0, len(array), 8)]
    if len(array[-1]) != 8:
        array[-1] = array[-1] + "0" * (8 - len(array[-1]))
    array = [ "{:02x}".format(int(el, 2)) for el in array]
    array = "".join(array)
    result = binascii.unhexlify(array)
    return result.decode("utf-8", errors="replace")


def load_image(path, pad=False):
    """Load an image.
    
    If pad is set then pad an image to multiple of 8 pixels.
    """
    image = cv.imread(path)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
    if pad:
        y_pad = 8 - (image.shape[0] % 8)
        x_pad = 8 - (image.shape[1] % 8)
        image = np.pad(
            image, ((0, y_pad), (0, x_pad) ,(0, 0)), mode='constant')
    return image


def save_image(path, image):
    """Save an image."""
    plt.imsave(path, image) 


def clamp(n, minn, maxn):
    """Clamp the n value to be in range (minn, maxn)."""
    return max(min(maxn, n), minn)


def hide_message(image, message, nbits=1):
    """Hide a message in an image (LSB).
    
    nbits: number of least significant bits
    """
    nbits = clamp(nbits, 1, 8)
    shape = image.shape
    image = np.copy(image).flatten()
    if len(message) > len(image) * nbits:
        raise ValueError("Message is to long :(")
    
    chunks = [message[i:i + nbits] for i in range(0, len(message), nbits)]
    for i, chunk in enumerate(chunks):
        byte = "{:08b}".format(image[i])
        new_byte = byte[:-nbits] + chunk
        image[i] = int(new_byte, 2)
        
    return image.reshape(shape)


def wyswietl_wiadomosc():
  image_path = input("Podaj ścieżkę do obrazka: ")
  image = load_image(image_path)

  # test dla obu wartosci nbitow
  output_1 = decode_from_binary_array(decode(image, nbits=1))
  output_2 = decode_from_binary_array(decode(image, nbits=2))

  # wybor ktora ilosc nbitow daje poprawny wynik
  i = 0
  while(output_1[i].isprintable() and output_2[i].isprintable()):
    i += 1

  if output_1[i].isprintable():
      output = output_1
  else:
      output = output_2

  # wypisywanie wiadomosci do czasu napotkania znaku nieprintowalnego gdzie nastapil blad w dekodowaniu - czyli koniec wiadomosci
  valid = []
  for s in output:
      if s.isprintable():
          valid.append(s)
      else: break;
      
  print()
  print("Wiadomosc: ")
  print("".join(valid))  # Odczytanie ukrytej wiadomości z PNG

def decode(image, nbits):
  """Reveal the hidden message. 
  
  nbits: number of least significant bits
  length: length of the message in bits.
  """
  
  img_len = len(image)
  image = np.copy(image).flatten()
  length_in_pixels = math.ceil(img_len/nbits)
  if img_len < length_in_pixels or length_in_pixels <= 0:
      length_in_pixels = img_len
  
  message = ""
  i = 0
  while i < length_in_pixels:
      byte = "{:08b}".format(image[i])
      message += byte[-nbits:]
      i += 1
      
  mod = img_len % -nbits
  if mod != 0:
      message = message[:mod]
  return message

def kodowanie():
  image_path = input("Podaj ścieżkę do obrazka: ") # "images/rembrandt.png"
  message = input("Podaj wiadomość: ")
  bits = clamp(int(input("Podaj ilość bitów [1/2]: ")), 1, 2) # ograniczenie do 1 lub 2
  
  original_image = load_image(image_path)  # Wczytanie obrazka

  message = encode_as_binary_array(message)  # Zakodowanie wiadomości jako ciąg 0 i 1
  image_with_message = hide_message(original_image, message, bits)  # Ukrycie wiadomości w obrazku

  save_image("zakodowane.png", image_with_message)  # Zapisanie obrazka w formacie PNG

def main():
  print("1. Kodowanie")
  print("2. Dekodowanie")
  print("3. Wyjście")
  choice = int(input("Wybierz opcję: "))
  if choice == 1:
    kodowanie()
  elif choice == 2:
    wyswietl_wiadomosc()
  elif choice == 3:
    exit()
  else:
    print("Nieprawidłowy wybór")
    main()

main()