import sys
import random
from math import log

cache_size = 0
data_block_size = 0
associativity = 0
replacement_policy = 0
write_hit_policy = 0
write_miss_policy = 0
S = 0
m = 0
M = 0
b = 0
t = 0
s = 0
hitcounter = 0
misscounter = 0
cache_content = {}
RAM = []

#Step 1: Initalize physical memory
#recieve as command line argument
#make sure that the RAM has some content as given file before starting the simulator

def initialize(filename):
  """ This function initializes the RAM  """
  global RAM
  print("*** Welcome to the cache simulator ***")
  print("initialize the RAM: ")
  initram = input().split(' ')
  lowerbound = initram[1][2:]
  upperbound = initram[2][2:]
  filename = sys.argv[1]
  file = open(filename)
  ram = file.readlines()
  for i in range (int(lowerbound, 16),int(upperbound,16)+1):
    line = ram[i]
    line = line.strip()
    RAM.append(line)
  for i in range(int(upperbound,16)+1, 256):
    RAM.append('00')
  print("RAM successfully initialized!")
#Step 2: Configure the Cache
#allow the user to configure the cache (command line)
def configure():
  """ This function configures the cache. """  
  global cache_size
  global data_block_size
  global associativity
  global replacement_policy
  global write_hit_policy
  global write_miss_policy
  global S
  global m
  global M
  global b
  global t
  global s
  global valid
  global tag
  global dirty
  global cacheblock
  global cache_content

  #to access variables, use configure.var_name
  cache_size = int(input("cache size: "))
  while ((cache_size <8 or cache_size > 256)):
    print("That is not within the accepted range.")
    cache_size = int(input("Enter the cache size: "))

  data_block_size = int(input("data block size: "))

  associativity = int(input("associativity: "))
  while(associativity != 1 and associativity != 2 and associativity != 4):
    print("That is not an accepted value.")
    associativity = int(input("associativity: "))

  replacement_policy = int(input("replacement policy: "))
  while(replacement_policy != 1 and replacement_policy !=2):
    print("That is not an accepted value.")
    replacement_policy = int(input("replacement policy: "))

  write_hit_policy = int(input("write hit policy: "))
  while(write_hit_policy != 1 and write_hit_policy !=2):
    print("That is not an accepted value.")
    write_hit_policy = int(input("write hit policy: "))

  write_miss_policy = int(input("write miss policy: "))
  while(write_miss_policy != 1 and write_miss_policy != 2):
    print("That is not an accepted value.")
    write_miss_policy = int(input("write miss policy: "))

  S = cache_size/(data_block_size*associativity) #number of sets
  if S%1 > 0:
    S = int(S) + 1
  S = int(S)
  m = int(8) #physical memory address
  M = int(2^8) #maximum number of addresses
  b = int(log(data_block_size,(2))) #number of block offset bits
  print("number of block offset bits: ", b)
  s = int(log(S,(2))) #number of set index bits
  print("number of index bits: ", s)
  t = int(m - s - b) #number of tag bits
  print("number of tag bits: ", t)

  
  #for i in number of sets
  for i in range(0,S):
    #for j in number of lines per set
    cache_content[i]={}
    for j in range(0,associativity):
        #for k in number of bits per set 
        cache_content[i][j]={}
        blocks = ""
        for k in range(0,data_block_size):
          blocks += "00 "
        cache_content[i][j]['mem'] = blocks
        cache_content[i][j]['valid'] = 0
        cache_content[i][j]['dirty'] = 0
        cache_content[i][j]['tag'] = 0
        cache_content[i][j]['position'] = 0

  print("cache successfully configured!")
 
#Step 3: Simulate the Cache
#Show a menu of cache-read, cache-write, cache-flush, cache-view, memory-view, cache-dump, memory-dump, quit.
def simulate():
  """ This function simulates the menu and calls appropriate functions """ 
  menu = {}
  menu['1']="cache-read" 
  menu['2']="cache-write"
  menu['3']="cache-flush"
  menu['4']="cache-view"
  menu['5']="memory-view"
  menu['6']="cache-dump"
  menu['7']="memory-dump"
  menu['8']="quit"
  while True: 
      options=menu.keys()
      print("***Cache simulator menu***")
      for entry in options: 
          print (entry, menu[entry])
      selection=input("type one command:") 
      selection = selection.split(" ")
      if selection[0] =='cache-read': 
        address = selection[1]
        cacheread(address)
      elif selection[0] == 'cache-write': 
        address = selection[1]
        byte = selection[2]
        cachewrite(address,byte)
      elif selection[0] == 'cache-flush':
        cacheflush()
      elif selection[0] == 'cache-view':
        cacheview()
      elif selection[0] == 'memory-view':
        memoryview()
      elif selection[0] == 'cache-dump':
        cachedump()
      elif selection[0] == 'memory-dump':
        memorydump()
      elif selection[0] == 'quit': 
        break
      else: 
       print ("Unknown Option Selected!")
      print("****************************")
      
def cacheread(address):
  """ This simulates the cacheread function """ 
  #reads data from an address. The user should type the read command followed by an 8-bit address in hexadecimal.
  cachehit = False
  addressbin = bin(int(address,16))[2:].zfill(8)
  tag = addressbin[0:t]
  set_ = addressbin[t: s+t]
  offset = addressbin[s+t :]
  if tag == '':
    tag = 0
  else:
    tag = int(tag,2)
  if set_ == '':
    set_ = 0
  else:
    set_ = int(set_,2)
  if offset == '':
    offset = 0
  else:
    offset = int(offset,2)
  r = int(address,16)//data_block_size
  for line in cache_content[int(set_)]:
      valid = cache_content[int(set_)][int(line)]["valid"]
      if valid == 1:
        if cache_content[int(set_)][int(line)]['tag']==tag:
          cachehit = True
          break
  if (cachehit == True):
    print("hit: yes")
    print("eviction_line: -1")
    print("RAM_address: -1")
  else:
    print("hit: no")
    if(replacement_policy == 1): #random replacement
      for line in cache_content[set_]:
        if cache_content[set_][line]['valid'] == 0:
          newline = line
          break
        else:
          newline = random.randint(0,associativity)
    else:  
      for line in cache_content[set_]:
        if cache_content[set_][line]['valid'] == 0:
          newline = line
          break
        else:
          maxline = -1;
          for line in range(0,associativity):
            position = cache_content[int(set_)][line]['position']
            if position > maxline:
              newline = position

    print("eviction_line: ", newline)  
    print("tag bits: ", tag)

    NewRAM = []
    line = ""
    #writing ram line into cache
    for k in range(0, len(RAM), data_block_size):
      chunk = RAM[k:k+data_block_size]
      NewRAM.append(chunk)
    
    if cache_content[set_][newline]['dirty'] == 1:
      index = set_ * data_block_size
      for l in range(0, data_block_size): 
        mem_byte = cache_content[set_][newline]['mem'][l*3:l*3+2]
        RAM[index + l] = mem_byte

    for block in NewRAM[r]:
      line = str(line) + str(block) + " "
    cache_content[set_][newline]['mem'] = line[0:]
    cache_content[set_][newline]['valid'] = 1
    cache_content[set_][newline]['tag'] = tag
  print("RAM_address: ", address)
  print ("data: 0x" + RAM[r+offset])
  

def cachewrite(address,byte):
  """ This simulates the cachewrite function """
  global hitcounter
  global misscounter
  #writes data to an address in the cache. The user should type the write command followed by an 8-bit address and a byte of data in hexadecimal. In case of a tie following LRU or LFU replacement policies, evict one with the min line number.
  Blockline = 0
  addressbin = bin(int(address,16))[2:].zfill(8)
  tag = addressbin[0:t]
  set_ = addressbin[t: s+t]
  offset = addressbin[s+t :]
  if tag == '':
    tag = 0
  else:
    tag = int(tag,2)
  if set_ == '':
    set_ = 0
  else:
    set_ = int(set_,2)
  if offset == '':
    offset = 0
  else:
    offset = int(offset,2)
  cachehit = False
  print("set: ", set_)
  print("tag: ",tag)
  for Line in cache_content[int(set_)]:
    valid = cache_content[set_][Line]["valid"]
    if valid == 1:
      if cache_content[int(set_)][int(Line)]['tag']==tag:
        Blockline = Line
        cachehit = True
        break

        ################## CACHE HIT (Valid) == TRUE ###################################

  if (cachehit == True):
    hitcounter += 1
    print("hit: yes")
    print("eviction_line: -1")
    print("RAM_address: -1")
    if (write_hit_policy ==1):  ######## Write through: ############
      #write the data in both the block in the cache and the block in RAM.
      if cache_content[set_][Blockline]['dirty'] == 1:
        index = set_ * data_block_size
        for l in range(0, data_block_size): 
          mem_byte = cache_content[set_][Blockline]['mem'][l*3:l*3+2]
          RAM[index + l] = mem_byte
      cacheread(address)
      memory = cache_content[int(set_)][Blockline]['mem'].split(' ')
      memory[offset] = byte[2:]
      line = ""
      for block in memory:
        line = line + block + " "
      cache_content[int(set_)][Blockline]['mem'] = line[0:]
      index = set_ * data_block_size + offset
      RAM[index] = byte[2:]
      
    else:     ############# write back ##################
    #just cache and dirty bit
      cacheread(address)
      memory = cache_content[int(set_)][Blockline]['mem'].split(' ')
      memory[offset] = byte[2:]
      line = ""
      if cache_content[set_][Blockline]['dirty'] == 1:
        index = set_ * data_block_size
        for l in range(0, data_block_size): 
          mem_byte = cache_content[set_][Blockline]['mem'][l*3:l*3+2]
          RAM[index + l] = mem_byte
      for block in memory:
        line = line + block + " "
      cache_content[int(set_)][Blockline]['mem'] = line[0:]
      cache_content[int(set_)][Blockline]['dirty'] = 1
      
      ################ CACHE HIT == FALSE ####################################

  else:                 
    misscounter += 1
    print("hit: no")
    if(replacement_policy == 1): 
      if(replacement_policy == 1): ######random replacement#########
        for line in cache_content[set_]:
          if cache_content[set_][line]['valid'] == 0:
            newline = line
            break
          else:
            newline = random.randint(0,associativity)
      else:
        for line in cache_content[set_]:
          if cache_content[set_][line]['valid'] == 0:
            newline = line
            break
          else:
            maxline = -1;
            for line in range(0,associativity):
              position = cache_content[int(set_)][line]['position']
              if position > maxline:
                newline = position

      print("eviction_line: ", newline)  
    if (write_miss_policy ==1):          ############ write-allocate: ###########
      #load the block from RAM and write it in the cache.
    #write info in cache first, then write into memory(update it)
      #index = S * data_block_size + offset
      #value = RAM[index]
      #memory = cache_content[int(set_)][Blockline]['mem'].split(' ')
      #memory[offset] = byte[2:]
      #line = ""
      #for block in memory:
        #line = str(line) + block + " "
      #cache_content[int(set_)][Blockline]['mem'] = line[0:]
      cacheread(address)
      memory = cache_content[int(set_)][Blockline]['mem'].split(' ')
      memory[offset] = byte[2:]
      if cache_content[set_][Blockline]['dirty'] == 1:
        index = set_ * data_block_size
        for l in range(0, data_block_size): 
          mem_byte = cache_content[set_][Blockline]['mem'][l*3:l*3+2]
          RAM[index + l] = mem_byte      
      line = ""
      for block in memory:
        line = str(line) + block + " "
      cache_content[int(set_)][Blockline]['mem'] = line[0:]
      cache_content[int(set_)][Blockline]['valid'] = 1
      if (write_hit_policy ==1):  ######## Write through: ############
        index = set_ * data_block_size + offset
        print("S: ", S)
        print("data_block_size: ", data_block_size)
        print("offset: ", offset)
        print(index)
        RAM[index] = byte[2:]
      else:                      ######### write back ################
        cache_content[int(set_)][Blockline]['dirty'] = 1
      

    else:    ## no write-allocate: write the block in RAM and do not load it in the cache.
      index = set_ * data_block_size + offset
      RAM[index] = byte[2:]

    memory = cache_content[int(set_)][Blockline]['mem'].split(' ')
    #data = memory[offset]
    print("RAM_address: ", address)
    print ("data: ", byte)
    print ("dirty_bit: ", cache_content[int(set_)][Blockline]['dirty'])


def cacheflush():
  """ This function clears the cache """
  global cache_content
  #clears the cache.
  #don't clear miss and hit counters
  for i in range(0,S): #number of sets
    
    #cache_content[i]={}
    for j in range(0,associativity): #number of lines per set
         
        #cache_content[i][j]={}
        if cache_content[i][j]['dirty'] == 1:
          index = i * data_block_size
          for l in range(0, data_block_size): 
            mem_byte = cache_content[i][j]['mem'][l*3:l*3+2]
            RAM[index + l] = mem_byte
            print("cache_content mem: ", cache_content[i][j]['mem'])
            print("index: ", index)
            print("mem_byte: ",mem_byte)
        blocks = ""
        for k in range(0,data_block_size): #number of blocks per line
          #index = i * data_block_size
          #for l in range(0,3 * data_block_size): 
            #mem_byte = cache_content[i][j]['mem'][l*3:l*3+2]
            #RAM[index + l] = mem_byte
          blocks += "00 "
        cache_content[i][j]['mem'] = blocks
        cache_content[i][j]['valid'] = 0
        cache_content[i][j]['dirty'] = 0
        cache_content[i][j]['tag'] = 0
        cache_content[i][j]['position'] = 0
  print("cache_cleared")

  
def cacheview():
  """ This function shows the current cache """  
  global cache_content
  #displays the cache content and status.The view should print the cache configuration and the cache’s content.
  print("cache_size: ", cache_size)
  print("data_block_size: ", data_block_size)
  print("associativity: ", associativity)
  if (replacement_policy == 1):
    print("replacement_policy: random_replacement")
  else:
    print("replacement_policy: least_recently_used")
  if(write_hit_policy == 1):
    print("write_hit_policy: write_through")
  else:
    print("write_hit_policy: write_back")
  if(write_miss_policy == 1):
    print("write_miss_policy: write_allocate")
  else:
    print("write_miss_policy: no_write_allocate")  
  print("number of cache hits: ", hitcounter)
  print("number of cache misses: ", misscounter)
  print("cache_content: ")
  #for i in number of sets
  for i in range(0,S):
    #for j in number of lines per set
    for j in range(0,associativity):
      print(cache_content[i][j]['valid'], cache_content[i][j]['dirty'], cache_content[i][j]['tag'], cache_content[i][j]['mem'], "\n")
      

def memoryview():
  """ This displays the current memory """  
  print("memory_size: 256")
  print("memory_content:")
  print("address:data")
  if (len(RAM)%data_block_size >0):
    length = int(len(RAM)/data_block_size) +1
  else:
    length = int(len(RAM)/data_block_size)
  for i in range(0,length):
    #print((hex(i*data_block_size)),":")
    print("\n")
    sys.stdout.write((hex(i*data_block_size))+":")
    newlist = []
    for k in range(0, len(RAM), data_block_size):
      chunk = RAM[k:k+data_block_size]
      newlist.append(chunk)
    for j in newlist[i]:
      #print(j + " ")
      sys.stdout.write(j+" ")
      
  #the memory-view command displays the RAM content and status. 
  #Line 1: memory_size:<integer in bytes> 
  #Line 2: memory_content: 
  #address:data 
  #0x<address in hexadecimal>:<8 single-space-separated bytes of data in hexadecimal>
  

def cachedump():
  """ This dumps the cache into a text file """
  global S
  global associativity
  cachefile = open("cache.txt", 'w')
  for i in range(0,S):
    #for j in number of lines per set
    for j in range(0,associativity):
      line = str(str(cache_content[i][j]['mem']) + "\n")
      cachefile.write(line)
  #dumps the current state of cache in a file cache.txt.
  #The cache.txt file gets updated only when this command is called.
  #Output format in cache.txt
  #Line1:<hex data in set 0 line 0 with single-space-separated byte byte0 byte1 ...>
  #Line2:<hex data in set 0 line 1 with single-space-separated byte byte0 byte1 ...>
  #Line n:<hex data in the last set last line with single-space-separated byte byte0 byte1 ...>

def memorydump():
  """ This dumps the memory into a text file """ 
  ramfile = open("ram.txt", 'w')
  for i in RAM:
    ramfile.write(i)
    ramfile.write('\n')
  #dumps the RAM content in a file ram.txt.
  #The ram.txt file gets updated only when this command is called.
  #Output format in ram.txt
  #Line 1: hex data at address 0
  #Line 2: hex data at address 1
  #Line 3: hex data at address 2
  #Line 256: hex data at address 255
    

def main():
  """ This is the main funtion """ 
  filename = sys.argv[1]
  initialize(filename)
  configure()
  simulate()

if __name__ == '__main__':
  main()
