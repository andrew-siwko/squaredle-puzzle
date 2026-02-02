import multiprocessing
import enchant
import itertools
import pprint
import time
import datetime
import os

start_time=time.time()

def etime(start_time):
    return(str(datetime.timedelta(seconds=time.time()-start_time)))


d=enchant.Dict('en_US')

def create_puzzle_and_connections(puzzle_string_array):
    puzzle=[]
    for row_string in puzzle_string_array:
        puzzle.append([x for x in row_string])
    connections={}
    rows=len(puzzle)
    cols=len(puzzle[0])
    for row in range(rows):
        for column in range(cols):
            if puzzle[row][column]!=' ':
                position=(row+1,column+1)
                connections[position]=[]
                for delta_row in [-1,0,1]:
                    for delta_column in [-1,0,1]:
                        if delta_row!=0 or delta_column!=0:
                            next_row=row+delta_row
                            next_column=column+delta_column
                            if next_row>=0 and next_row<rows and next_column>=0 and next_column<cols and puzzle[next_row][next_column]!=' ':
                                connections[position].append((next_row+1,next_column+1))
    return(puzzle,connections)

import json
with open('puzzle.json','rt') as file:
    puzzle_json=json.loads(file.read())
print(puzzle_json)
max_length=puzzle_json['puzzle_length']
(puzzle,connections)=create_puzzle_and_connections(puzzle_json['puzzle_text'])

def find_next_letter(current_position,current_word,current_path,max_length,words_found):
    # print(current_word,current_path)
    if len(current_word)>3 and d.check(current_word.lower()) and current_word not in words_found:
        print('***',current_word)
        words_found.append(current_word)
    if len(current_word)<max_length:
        if current_position not in connections:
            print('no connections for position:',current_position)
            print(current_word,current_path)
            pprint.pprint(connections)
        for next_position in connections[current_position]:
            if next_position not in current_path:
                next_letter=puzzle[next_position[0]-1][next_position[1]-1]
                next_word=current_word+next_letter
                next_path=current_path+[next_position]
                words_found=find_next_letter(next_position,next_word,next_path,max_length,words_found)
    return(words_found)

if __name__=='__main__':
    # multiprocessing.freeze_support()
    print(etime(start_time),'starting')
    pprint.pprint(connections)
    print('cpu count:',multiprocessing.cpu_count())
    with multiprocessing.Pool(min(1,multiprocessing.cpu_count())) as p:
        argument_list=[]
        for letter_position in connections.keys():
            starting_letter=puzzle[letter_position[0]-1][letter_position[1]-1]
            if starting_letter!=' ':
                arguments=(letter_position,starting_letter,[letter_position],max_length,[])
                # print('setting up arguments:',arguments)
                argument_list.append(arguments)
        print(etime(start_time),'invoking starmap()...')
        # pprint.pprint(argument_list)
        result=p.starmap(find_next_letter, argument_list,chunksize=1)
        print(etime(start_time),'starmap complete')
        # pprint.pprint(result)
    words_found=itertools.chain(*result)
    sorted_words=sorted(list(set(words_found)))
    print('=================================')
    print(sorted_words)
    print('=================================')
    word_length_dict={}
    for w in sorted_words:
        l=len(w)
        if l not in word_length_dict:
            word_length_dict[l]=[]
        word_length_dict[l].append(w)
    import pprint
    # pprint.pprint(word_length_dict,width=280)
    print('********************************')
    for length in sorted(list(word_length_dict.keys())):
        print(length)
        print(word_length_dict[length])
        print('********************************')

    print(etime(start_time),'ending')
