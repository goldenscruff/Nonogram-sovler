
import os

def create_clues(lines, rowcolumn):
    #creates and stores the clues for either a row or column for x lines
    i = 0
    rowcolumnclue = []
    while i < lines:
        i += 1
        bufferclue = input(f"What are the clues for {rowcolumn} {i}: ")
        bufferclue = bufferclue.split(",")
        for x in bufferclue:
            bufferclue[bufferclue.index(x)] = int(x)
        rowcolumnclue.append(bufferclue)
    return rowcolumnclue

def create_board():
    #asks user for board information
    is_file_input = input("Inport board data form .nono file? y/n ").lower()
    if is_file_input in {"y", "yes"}:
        is_from_file[0] = True
        name = input("Give name of file to import data from: ")
        _ = read_board_from_file(name)
        return (len(_[1]), _[3], len(_[2]), _[4], _[1], _[2], _[0])
    else:
        name = input("Give a save name for the board: ")
        row_no = (int(input("How many rows are there? ")))
        print("Please enter the row clues in the form of \"x, y, z\"")
        rowclue = create_clues(row_no, "row")
        column_no = (int(input("How many columns are there? ")))
        print("Please enter the column clues in the form of \"x, y, z\"")
        columnclue = create_clues(column_no, "column")
        
        #creates empty board with correct dimensions
        mastercolumn = []
        masterrow = []
        i = 0
        while i < column_no:
            i += 1
            columnhold = []
            j = 0
            while j < row_no:
                j += 1
                columnhold.append(0)
            mastercolumn.append(columnhold)
        i = 0
        while i < row_no:
            i += 1
            rowhold = []
            j = 0
            while j < column_no:
                j += 1
                rowhold.append(0)
            masterrow.append(rowhold)

        return row_no, rowclue, column_no, columnclue, masterrow, mastercolumn, name

#generates the minimum length a set of clues can be
def min_row_length(list):
    min_length = sum(list) - 1
    min_length += len(list)
    return min_length

#returns if the board state is valid
def is_valid_board():
    #print("validateboard")
    row_c_sum = []
    column_c_sum = []
    for row in master_row_clue:
        row_c_sum.append(sum(row)) #appends the sum of each row to a list

    for column in master_column_clue:
        column_c_sum.append(sum(column))
    row_c_sum = sum(row_c_sum)
    column_c_sum = sum(column_c_sum)

    if row_c_sum != column_c_sum: #checks that the sum of the sum of the clues of rows/columns are equal
        return False, "Clue sum error" #each clue has a row(y) and (x) pos, so the sum of the x must equal y
    
    for row in master_row_clue:
        if min_row_length(row) > len(master_row[0]): #the minimum clue length for all rows cannot be longer than the length of the row 
            return False, "Row clue overflow error"
    for column in master_column_clue:
        if min_row_length(column) > len(master_column[0]):
            return False, "Column clue overflow error"
    return True

def update(row, column, cell) -> None:
    """function when called updates the cell in (row, column) for both master row and column, as well as adding the fact that the row and column need updating"""
    print("updating", row, column, "with", cell)
    if master_row[row][column] == 0 or master_row[row][column] == cell:
        change_update = False
        if master_row[row][column] == 0:
            change_update = True
        master_row[row][column] = cell
        master_column[column][row] = cell
        update_all_gaps_from_cell(row, "row", cell, column)
        update_all_gaps_from_cell(column, "column", cell, row)

        if update_row[row] != -1 and change_update:
            update_row[row] = update_row[row] + 1
        if update_column[column] != -1 and change_update:
            update_column[column] = update_column[column] + 1
    else:
        print(row, column)
        print("Cell overide error")    

#generates a list would be the clues for the current row/column
def clue_row(x, rowcolumn):
    i = 0
    if rowcolumn == "row":
        current_row_clue = []
        for a in master_row[x]: #every value in row x
            if a == 1: # if it is a one
                if master_row[x][i - 1] != 1 or (i-1) == -1: # if the value before it isn't 1 or it is the first value (else list wraps, and takes from the last value)
                    current_row_clue.append(1) #add a new 1 to the list
                elif master_row[x][i - 1] == 1: #in the case that the previous is one, the value needs to be incremented, so that you get clue length 2 instead of 1,1
                    current_row_clue[len(current_row_clue) -1] = current_row_clue[len(current_row_clue) - 1] + 1 #incrementing the last value
            i += 1
        if len(current_row_clue) == 0:
            current_row_clue.append(0)
        return current_row_clue
    elif rowcolumn == "column":# same code as above except using column variables
        current_column_clue = []
        for a in master_column[x]:
            if a == 1:
                if master_column[x][i - 1] != 1 or (i-1) == -1:
                    current_column_clue.append(1)
                elif master_column[x][i - 1] == 1:
                    current_column_clue[len(current_column_clue) - 1] = current_column_clue[len(current_column_clue) - 1] + 1
            i += 1
        if len(current_column_clue) == 0:
            current_column_clue.append(0)
        return current_column_clue

def check_board():
    #makes board_clue_rows reflect current state of board and checks if they are the same as the master_clue_row
    #if the board_clue_row == clue_row then returns that the board is solved.
    board_row_clue = [clue_row(i, "row") for i in range(row_no)]
    board_column_clue = [clue_row(i, "column") for i in range(column_no)]
    if board_row_clue == master_row_clue and board_column_clue == master_column_clue:
        print("Board is solved")
        return True
    else:
        print("Board is not solved")
        return False

#takes a list of possible board states, and finds and updates cells that have only one possible state
def logic_update(logic_list, rowcolumn, rowcolumnno):
    i = 0
    possible_cell = [] + [0] * len(logic_list[0])
    #while i < len(logic_list[0]):
    #    i += 1
    #    possible_cell.append(0)
    for minilist in logic_list:
        i = 0
        for x in minilist:
            possible_cell[i] = possible_cell[i] + x
            i += 1
    i = 0
    logic_list_length = len(logic_list)
    #print(possible_cell)
    #print(len(possible_cell))
    if rowcolumn == "row":
        for a in possible_cell:
            if a == -1 * logic_list_length:
                update(rowcolumnno, i, -1)
            elif a == logic_list_length:
                update(rowcolumnno, i, 1)
            i += 1

    if rowcolumn == "column":
        for a in possible_cell:
            if a == -1 * logic_list_length:
                update(i, rowcolumnno, -1)
            elif a == logic_list_length:
                update(i, rowcolumnno, 1)
            i += 1
   
def print_board() -> None:
    scale = ["0", "__","--","__","--","5","__","--","__","--"]
    _ = "  "
    for i in range(column_no):
        if i%5 ==0:
            _ += (str((i//10)%10) + scale[i%10])
        else:
            _ += scale[i%10]
    print(_)
    scale = ["0", "--","--","--","--","5","--","--","--","--"]
    for i, row in enumerate(master_row):
        print_row = (str((i//10)%10) + scale[i%10]) if i % 5 == 0 else scale[i%10]
        for value in row:
            if value == 0:
                print_row += "▒▒"
            elif value == 1:
                print_row += "██"
            else:
                print_row += "  "
        print(print_row)

def do_basic_logic() -> list:
    weight_row = []
    for w in range(row_no):
        #master_possible_row.append(allclues("row",w))
        weight_row.append(min_row_length(master_row_clue[w]))

    weight_column = []
    for w in range(column_no):
        #master_possible_column.append(allclues("column",w))
        weight_column.append(min_row_length(master_column_clue[w]))
    all_weight = weight_row + weight_column
    update_indicies = []
    for i in range(len(all_weight)):
        if i >= row_no:
            _max = max(master_column_clue[i-row_no])
            if _max > row_no - all_weight[i] or _max == 0:
                update_indicies.append(i)
        else:
            _max = max(master_row_clue[i])
            if _max > (column_no) - all_weight[i] or _max == 0:
                update_indicies.append(i)

    for update_index in update_indicies:
        #print_board()
        print("doing intial logic for index", update_index)
        if update_index >= row_no:
            #logic_update_sum(all_clues_sum("column",(update_index-row_no)),"column", (update_index-row_no))
            fixed_cells = get_fixed_cells(master_possible_column_gaps[update_index-row_no], "column", (update_index-row_no))
            print("fixed_cells", fixed_cells)
            for row in fixed_cells[0]:
                update(row, update_index-row_no, -1)
            for row in fixed_cells[1]:
                update(row, update_index-row_no, 1)
            #update_column[update_index - row_no] = 0
        else:
            #logic_update_sum(all_clues_sum("row",(update_index)),"row", (update_index))
            fixed_cells = get_fixed_cells(master_possible_row_gaps[update_index], "row", update_index)
            print("fixed_cells", fixed_cells)
            for column in fixed_cells[0]:
                update(update_index, column, -1)
            for column in fixed_cells[1]:
                update(update_index, column, 1)
            #update_row[update_index] = 0
        
    print("intial logic done")
    return all_weight

def generate_all_possible_gaps(rowno, rowcolumn) -> list:
    """Generates a list of lists that represent the possible numbers of empty spaces in front of each clue
    The first item in each nested list is the left side offset, and is initially zero
    The row collapses to one possibility when each nested list has only a len() == 2 (including the offset)"""

    if rowcolumn == "row":
        row_clue = master_row_clue[rowno]
        row_len = len(master_row[0])
    elif rowcolumn == "column":
        row_clue = master_column_clue[rowno]
        row_len = len(master_column[0])

    #if row_clue == [0]:
    #    return [[0]]

    row_possible_gaps = []
    min_length = min_row_length(row_clue)

    start = 0
    for clue in row_clue:
        row_possible_gaps.append([0] + list(range(start, row_len - min_length + start+1)))
        start += clue + 1

    return row_possible_gaps

def yield_possible_row_from_possible_gaps(rowno, rowcolumn) -> list:
    """Creates a generator that recursively goes through a possible_gaps and sequentially yields a list of a possible gaps for each clue in the row.
    The yielded list is not a copy and shouldn't be mutated.
    Yields:
        A list looking like: (for 5 clues)
            [0, 3, 8, 12, 15]"""
    if rowcolumn == "row":
        possible_gaps = master_possible_row_gaps[rowno]
        current_row = master_row[rowno]
        current_clues = master_row_clue[rowno]
    elif rowcolumn == "column":
        possible_gaps = master_possible_column_gaps[rowno]
        current_row = master_column[rowno]
        current_clues = master_column_clue[rowno]
    
    num_clues = len(possible_gaps)
    gap_offset = [possible_gaps[i][0] for i in range(num_clues)] 
    gaps_list = [0 for _ in range(num_clues)]
    def get_gaps_sequentially(index, clue):
        """Should always be called with (1,0) as initial values"""
        #print("called with index:", index, "clue:", clue)
        index = max(index - gap_offset[clue], 1)
        enumerate_clues = possible_gaps[clue][index:]
        for i, gap in enumerate(enumerate_clues):
            if gap == None:
                continue
            gaps_list[clue] = gap
            #print(gap, index, clue, possible_gaps[clue][max((index), 1):], i)
            if clue + 1 == num_clues:
                yield gaps_list
            else:
                yield from get_gaps_sequentially(index+i, clue+1)
        
    Gaps_generator = get_gaps_sequentially(1,0)
    
    #Doing checking to ensure the gaps generated (naively) are actually valid

    #Getting the 1 values that need checking, if there aren't any, no checking required
    row_1_indicies = [i for i, j in enumerate(current_row) if j == 1]
    
    row_len = len(current_row)
    #Trimming the row_1_indicies to avoid checking -1 are implied over cells that are guaranteed to be a 1
    for i, clue in enumerate(current_clues):
        forced_1s = set(range(possible_gaps[i][1], possible_gaps[i][1] + clue))
        for j in range(possible_gaps[i][-1], possible_gaps[i][-1] + clue):
            if j in forced_1s and j in row_1_indicies:
                row_1_indicies.remove(j)

    if row_1_indicies == []:
        yield from Gaps_generator

    for gaps in Gaps_generator:
        valid = True
        #Checking first and last gaps are valid
        if row_1_indicies[0] < gaps[0] or row_1_indicies[-1] >= gaps[-1] + current_clues[-1]:
            continue #move to next set of gaps as this is invalid
        
        #Checking that there are no stretches of -1 over a 1 on the current board
        for index in row_1_indicies:
            if valid:
                index_fraction = (index * (num_clues - 1))//row_len - 1
                for i in range(num_clues-1):
                    i = (i + index_fraction) % (num_clues - 1) #better first guess for which invalidates/validates the 1 
                    if index in range(gaps[i], gaps[i] + current_clues[i]):
                        break #valid = True
                    elif index >= gaps[i] + current_clues[i] and index < gaps[i+1]:
                        valid = False
                        break
            else:
                break
        
        if valid:
            yield gaps

def compress_possible_gaps(gaps:list, raw_input = False) -> list:
    """Recieves a matrix of gaps, and returns a matrix with the final Nones removed, and the initial Nones (with coresponding offset) removed
    If raw_input is True then it will assume a rectangular matrix otherwise it will decompress the input to a matrix with the leading Nones
    eg input (raw): [
        [None, 1, 2, 3, 4, None],
        [None, 5, 6, 7, None, None],
        [8, 9, 10, 11, None, 12],
        [None, None, 15, 16, 17, 18]]
    output: [
        [0, 1, 2, 3],
        [0, 5, 6, 7],
        [0, 9, 10, 11, None, 12],
        [1, 15, 16, 17, 18]]
    (output[0][0] is 0 by default)"""
    _gaps = gaps
    if not raw_input:
        _gaps = []
        total_None = 0
        for i, gap in enumerate(gaps):
            total_None = total_None + gap[0]
            _gaps.append([None] * total_None + gap[1:]) 
    
    initial_None = []
    final_None = []
    num_gaps = len(_gaps)
    i = 0
    total_None = 0
    while i < num_gaps:
        #print(_gaps[i])
        if _gaps[i][total_None] == None:
            total_None += 1
        else:
            initial_None.append(total_None)
            i += 1
            

    total_None = len(_gaps[-1])-1
    i += -1
    while i >= 0:
        try:
            if _gaps[i][total_None] == None:
                total_None += -1
            else:
                final_None.append(total_None+1 if total_None+1 != 0 else None)
                i += -1
        except IndexError:
            total_None = len(_gaps[i]) -1
    
    final_None.reverse()
    return_list = []
    return_list.append([0]+_gaps[0][initial_None[0]:final_None[0]])
    for i in range(1, num_gaps):
        offset = initial_None[i] - initial_None[i-1]
        return_list.append([offset] + _gaps[i][initial_None[i]:final_None[i]])
    return return_list

def get_available_clue_gaps(gaps) -> list:
    """Returns a list of sets containing all of the possible gaps for each clue, as determined by the generator gaps (the Argument)"""
    first = next(gaps)
    num_clues = len(first)
    available_clues = []
    for _ in range(num_clues):
        available_clues.append(set())
    add_clues = lambda list: [available_clues[i].add(list[i]) for i in range(num_clues)]
    add_clues(first)
    #[add_clues(clues) for clues in gaps]
    for clues in gaps:
        #print(available_clues)
        add_clues(clues)
    return available_clues

def get_fixed_cells(gaps, rowcolumn, rowno) -> list:
    """Calculates which indexes are forced -1 or 1 cells from a list of sets of gaps for clues"""
    if rowcolumn == "row":
        current_clues = master_row_clue[rowno]
        current_row = master_row[rowno]
    elif rowcolumn == "column":
        current_clues = master_column_clue[rowno]
        current_row = master_row[rowno]
    current_0_cells = set([i for i, value in enumerate(current_row) if value == 0])
    current_possible = set()
    current_forced = set()
    
    def min_max(x):
        _min = None
        _max = None
        iterable = iter(x)
        current = next(iterable)
        try:
            while current == None:
                current = next(iterable)
            _min = current
            _max = current
            while True:
                current = next(iterable)
                if current == None:
                    continue
                elif current < _min:
                    _min = current
                    continue
                elif current > _max:
                    _max = current
        except StopIteration:
            return (_min, _max)
    
    for clue_gaps, clue in zip(gaps, current_clues):
        if type(clue_gaps) == list:
            _ = min_max(clue_gaps[1:])
        elif type(clue_gaps) == set:
            _ = min_max(clue_gaps)
        _min = _[0]
        _max = _[1]
        clue_possible_1s = set(range(_min, _max + clue))
        current_possible.update(clue_possible_1s)
        #print(_max, _min+ clue)
        clue_forced_1s = set(range(_max, _min + clue))
        current_forced.update(clue_forced_1s)
    
    #print("poss", current_possible, "\nforced", current_forced)
    forced_empty = set((i for i in current_0_cells if i not in current_possible))
    forced_1_cells = set((i for i in current_0_cells if i in current_forced))
    return [forced_empty, forced_1_cells]

def update_gaps_from_available(original:list, new:list) -> None:
    """Takes in a list of old gaps, and keeps the elements that are in the new list, with the same positions in the old list
    All other values are replaced with None"""
    for clue_gaps, new_clues in zip(original, new):
        for i, clue in enumerate(clue_gaps[1:]):
            if clue not in new_clues:
                clue_gaps[i + 1] = None

def get_fixed_clues_and_cells(Gaps_gen, rowno, rowcolumn):
    #clue gaps
    first = next(Gaps_gen)
    num_clues = len(first)
    available_clues = []
    for _ in range(num_clues):
        available_clues.append(set())
    
    #cells
    if rowcolumn == "row":
        current_clues = master_row_clue[rowno]
        current_row = master_row[rowno]
    elif rowcolumn == "column":
        current_clues = master_column_clue[rowno]
        current_row = master_column[rowno]
    forced_1_cells = set(i for i in range(len(current_row)) if current_row[i] == 0)
    forced_empty = forced_1_cells.copy()
    
    #print(forced_1_cells, forced_empty)
    def process_gaps(gaps):
        filled_cells = set()
        for i, gap in enumerate(gaps):
            available_clues[i].add(gap)
            filled_cells.update(set(range(gap, gap+current_clues[i])))
        _ = [i for i in forced_1_cells if i not in filled_cells]
        [forced_1_cells.discard(i) for i in _]
        _ = [i for i in forced_empty if i in filled_cells]
        [forced_empty.discard(i) for i in _]
    process_gaps(first)
    #[add_clues(clues) for clues in gaps]
    for clues in Gaps_gen:
        #print(available_clues)
        process_gaps(clues)
    #print(forced_1_cells, forced_empty)
    return (available_clues, forced_1_cells, forced_empty)

def update_all_gaps_from_cell(rowno, rowcolumn, cell_value, position:int) -> None:
    """Updates the nested lists created by generate_all_possible_gaps() using the cell_value (-1 or 1) and position (equivalent to master_row[x][position])
    """
    #print("update all gaps from cell", rowno, rowcolumn, cell_value, position)
    if rowcolumn == "row":
        row_gaps = master_possible_row_gaps[rowno]
        row_clue = master_row_clue[rowno]
        if rowno == 50:
            pass
    elif rowcolumn == "column":
        row_gaps = master_possible_column_gaps[rowno]
        row_clue = master_column_clue[rowno]

    if cell_value == 1:
        """Does naive check, only checking the -1 imediately before and after the cell"""
        for i, clue_gaps in enumerate(row_gaps):
            clue = row_clue[i]
            #print(clue_gaps, rowno, rowcolumn)
            if clue_gaps[1] != None:
                if clue_gaps[1] > position + 1:
                    continue
                if clue_gaps[-1] + clue < position:
                    continue
            
            try:
                t = clue_gaps[1:].index(position+1)
                clue_gaps[t + 1] = None
                while clue_gaps[-1] == None:
                    clue_gaps.pop(-1)
            except ValueError:
                pass
            try:
                t = clue_gaps[1:].index(position-clue)
                clue_gaps[t + 1] = None
                while clue_gaps[-1] == None:
                    clue_gaps.pop(-1)     
            except ValueError:
                pass
            
    elif cell_value == -1:
        """Need to remove the invalid gaps numbers that would put a 1 cell into position
        The number depends the length of the clue (for clue length of 4 and pos 6, [3, 4, 5, 6] all put a 1 in the seventh (pos 6) cell, where as clue length 1 only [6] would be invalid)		
        """
        for i, clue_gaps in enumerate(row_gaps):
            if clue_gaps[1] != None:
                if clue_gaps == [0]: #the case only if the clue is 0, all other rows have len >= 2
                    break
                if clue_gaps[1] > position:
                    #the furthest left value is the lowest value for the clue_gaps, if this gap (the furthest left this clue can go) is greater than the position, then it and all others are gaps.
                    continue
            clue = row_clue[i]
            if clue_gaps[-1] + clue -1 < position:
                #similar logic as above
                continue
            
            #checking for invalid gap numbers in the possible gaps for each clue, and replaces it with None if found. 
            for gap in range(position - clue + 1, position + 1):
                try:
                    update_index = clue_gaps[1:].index(gap)
                    clue_gaps[update_index+1] = None
                except ValueError:
                    pass
            while clue_gaps[-1] == None:
                clue_gaps.pop(-1)

def only_clues_for_row(rowno, rowcolumn) -> None:
    """Creates a set of clues that can reach each block of 1 cells in the board
    It then uses these to thin the gaps, and pertentially update some 1 cells"""
    if rowcolumn == "row":
        current_row = master_row[rowno]
        current_gaps = master_possible_row_gaps[rowno]
        current_clues = master_row_clue[rowno]
        update_recursion[rowno] = update_recursion[rowno] + update_row[rowno]
        update_row[rowno] = 0
    elif rowcolumn == "column":
        current_row = master_column[rowno]
        current_gaps = master_possible_column_gaps[rowno]
        current_clues = master_column_clue[rowno]
        update_recursion[rowno + row_no] = update_recursion[rowno + row_no] + update_column[rowno]
        update_column[rowno] = 0

    found_block = False #used to keep track of if the previous cells were a one cell (forming a block)
    clues_for_block = []

    for i, cell in enumerate(current_row + [-1]):
        if cell != 1 and not found_block:
            continue
        elif cell == 1 and not found_block:
            found_block = True
            block_len = 1
            continue
        #found_block == True
        elif cell == 1:
            block_len +=1
            continue
        else: #terminating a block
            found_block = False
            # i is currently the index of the cell after the block ends, and block_len is length of the block
            #for each clue gap need to check range(i-clue, i - block_len + 1) as all of those (or only one of them) can be valid for the block
            #update_gaps_from_avaliable takes a list of sets
            clues_can_reach = [i-block_len, i]
            for clue_index, clue_gaps in enumerate(current_gaps):
                if clue_gaps[1] > i - block_len:
                    break #if the current clue is too far to the right to be able to place a 1 at the start of the block, then so would all the following clues
                current_clue = current_clues[clue_index]
                if current_clue < block_len:
                    continue
                elif clue_gaps[-1] + current_clue < i:
                    continue
                else:
                    for j in range(i - current_clue, i - block_len + 1):
                        if j in clue_gaps:
                            clues_can_reach.append(clue_index)
                            break
            clues_for_block.append(clues_can_reach)
            
    for block in clues_for_block:
        if len(block) == 3:
            #if only one clue can reach that block (as block[0,1] are the positions of the block), then remove all of the gaps that don't hit the block 
            clue = current_clues[block[2]]
            gaps = current_gaps[block[2]]
            for i, gap in enumerate(gaps[1:]):
                if gap == None:
                    continue
                elif gap <= block[0] and gap >= block[1] - clue:
                    pass
                else:
                    gaps[i+1] = None
                    while gaps[-1] == None:
                        gaps.pop(-1)

        #doing logic to see if the smallest clue is restricted, giving free 1s ie: [-1, 0, 1, 1, 0, 0] and smallest clue is 4, can deduce [-1, 0, 1, 1, 1, 0]
        smallest_clue = min([current_clues[i] for i in block[2:]])
        check_distance = smallest_clue + block[0] - block[1]
        right_bound = len(current_row)
        #Check left sequentially until hit left edge or -1, then call update(x,block[1] + i,1) for i in range (check_distance - checked_distance)
        #The weird i +- 1 is because of the asymetry in the block co-ords. block[0] is the first 1 of the block, block[1] is the first 0/-1 **after** the block [0,0,0,**1**,1,1,**-1**]
        #Checking left side for restrictions
        for i in range(check_distance):
            if block[0] - i - 1 == -1 or current_row[block[0] - i - 1] == -1:
                if rowcolumn == "row":
                    for j in range(check_distance - i):
                        update(rowno, block[1] + j, 1)
                elif rowcolumn == "column":
                    for j in range(check_distance - i):
                        update(block[1] + j, rowno, 1)
                break #checking a further check distance would only update fewer things, so can break early
        #Checking right
        for i in range(check_distance):
            if block[1] + i == right_bound or current_row[block[1] + i] == -1:
                if rowcolumn == "row":
                    for j in range(check_distance - i):
                        update(rowno, block[0] - j - 1, 1)
                elif rowcolumn == "column":
                    for j in range(check_distance - i):
                        update(block[0] - j - 1, rowno, 1)
                break


def logic_row(rowno, rowcolumn) -> None:
    """logic to run to update a row
    1. compress row_gaps
    2. create generator for the row
    3. get gaps for each clue
    4a. update gaps to include only the actual gap positions
    5a. compress row_gaps
    4b. get the fixed 1 and -1 positions
    5b. update the board with the fixed -1 and 1 positions
    6b. reset the update row"""
    print(rowno, rowcolumn)
    if rowcolumn == "row":
        gaps = compress_possible_gaps(master_possible_row_gaps[rowno])
        master_possible_row_gaps[rowno] = gaps
        only_clues_for_row(rowno, "row")
        master_possible_row_gaps[rowno] = compress_possible_gaps(master_possible_row_gaps[rowno])
    elif rowcolumn == "column":
        gaps = compress_possible_gaps(master_possible_column_gaps[rowno])
        master_possible_column_gaps[rowno] = gaps
        only_clues_for_row(rowno, "column")
        master_possible_column_gaps[rowno] = compress_possible_gaps(master_possible_column_gaps[rowno])

    generator = yield_possible_row_from_possible_gaps(rowno, rowcolumn)
    #available_clues = get_available_clue_gaps(generator)
    #update_gaps_from_available(gaps, available_clues)
    #fixed_cells = get_fixed_cells(available_clues, rowcolumn, rowno)
    processed = get_fixed_clues_and_cells(generator, rowno, rowcolumn)
    update_gaps_from_available(gaps, processed[0])
    #print(processed, rowno, rowcolumn)

    if rowcolumn == "row":
        master_possible_row_gaps[rowno] = compress_possible_gaps(master_possible_row_gaps[rowno])
        for column in processed[2]:
        #for column in fixed_cells[0]:
            update(rowno, column, -1)
        for column in processed[1]:
        #for column in fixed_cells[1]:
            update(rowno, column, 1)
        update_recursion[rowno] = 0
    elif rowcolumn == "column":
        master_possible_column_gaps[rowno] = compress_possible_gaps(master_possible_column_gaps[rowno])
        for row in processed[2]:
        #for row in fixed_cells[0]:
            update(row, rowno, -1)
        for row in processed[1]:
        #for row in fixed_cells[1]:
            update(row, rowno, 1)
        update_recursion[rowno+row_no] = 0
        
def get_index_highest_weight() -> tuple:
    highest_weight = 0.0
    highest_index = -1
    for i, update in enumerate(update_row):
        if update == 0:
            continue
        calc = update/(len(master_row_clue[i])**2)
        if calc > highest_weight:
            highest_weight = calc
            highest_index = i
    row = True
    for i, update in enumerate(update_column):
        if update == 0:
            continue
        calc = update/(len(master_column_clue[i])**2)
        if calc > highest_weight:
            highest_weight = calc
            highest_index = i
            row = False
    
    if row == True:
        #print("weight", master_row_clue[highest_index], update_row[highest_index])
        return ("row", highest_index)
    else:
        #print("weight", master_column_clue,[highest_index], update_column[highest_index])
        return ("column", highest_index)

def save_board_to_file():
    dirname = os.path.dirname(__file__)
    with open(dirname + "/Boards/" + name + ".nono", "w") as file:
        file.write(f"name,row_no,column_no\n{name},{row_no},{column_no}\n")
        file.write("row_board\n")
        board_state = {1:"1", 0: "0", -1: "-"}
        string_of_row = lambda row: "".join([board_state[i] for i in row])
        file.write("".join([string_of_row(row) + "\n" for row in master_row]))
        file.write("clues\nrow\n")
        file.write("".join([",".join([str(i) for i in clues]) + "\n" for clues in master_row_clue]))
        file.write("clues\ncolumn\n")
        file.write("".join([",".join([str(i) for i in clues]) + "\n" for clues in master_column_clue]))

def read_board_from_file(file_name):
    dirname = os.path.dirname(__file__)
    with open(dirname + "/Boards/" + file_name + ".nono", "r") as file:
        file_iter = iter(file)
        header = next(file_iter).strip().split(",")
        meta_data = next(file_iter).strip().split(",")
        name = meta_data[header.index("name")]
        row_no = int(meta_data[header.index("row_no")])
        column_no = int(meta_data[header.index("column_no")])
        master_possible_row_gaps = [[] for i in range(row_no)]
        master_possible_column_gaps = [[] for i in range(column_no)]
        return_list = [name, None, None, None, None, master_possible_row_gaps, master_possible_column_gaps]
        index_dict = {"name":0, "master_row":1, "master_column":2, "row_clues":3, "column_clues":4, "row_gaps":5, "column_gaps":6}
        #[master_row, master_column, row_clues, column_clues, row_gaps, column_gaps]
        
        def read_board():
            master_row = [[] for i in range(row_no)]
            master_column = [[] for i in range(column_no)]
            str_to_int = {"1":1, "0":0, "-":-1}
            for i in range(row_no):
                row = next(file_iter)
                for j, character in enumerate(row.strip()):
                    master_row[i].append(str_to_int[character])
                    master_column[j].append(str_to_int[character])
            return_list[index_dict["master_row"]] = master_row
            return_list[index_dict["master_column"]] = master_column
        
        def read_clues():
            arguments = next(file_iter).strip()
            if arguments == "row":
                num = row_no
                index_string = "row_clues"
            elif arguments == "column":
                num = column_no
                index_string = "column_clues"
            master_clue = [[int(x) for x in next(file_iter).split(",")] for i in range(num)]
            return_list[index_dict[index_string]] = master_clue

        def read_gaps():
            arguments = next(file_iter).strip().split(",")
            

        file_parse_func_map = {"row_board":read_board, "clues": read_clues, "gaps":read_gaps}
        try:
            while True:
                file_parse_func_map[next(file_iter).strip()]()
        except StopIteration:
            return return_list      

def is_solved_board() -> bool:
    """yields a bool of whether the board is solved"""
    test_index = 0
    total_indicies = row_no * column_no
    while True:
        if master_row[test_index//column_no][test_index%column_no] == 0:
            yield False
        elif test_index == total_indicies - 1:
            yield True
        else:
            test_index += 1
def main():
    pass



if __name__ == "__main__":
    #assing the values of create_board to single variables
    is_from_file = [False]
    board = create_board()
    row_no = board[0] #number of rows
    master_row_clue = board[1] #master clues are what the user inputs
    column_no = board[2]
    master_column_clue = board[3]
    master_row = board[4] #a list of the board state (a list) for each row, initially column_no + 1 0s
    master_column = board[5]
    name = board[6]
    update_row = [0] * (row_no) if not is_from_file[0] else [sum((abs(i) for i in row)) for row in master_row] #A list that stores which rows and columns have been updated (and need to have their logic checked again)
    update_column = [0] * (column_no) if not is_from_file[0] else [sum((abs(i) for i in column)) for column in master_column]
    update_recursion = [0] * (row_no + column_no)
    master_possible_row = [] #initiallising the lists that contain the lists of all possible board states looks like:
    for _ in range(row_no):
        master_possible_row.append([])
    master_possible_column = [] #[[[1,-1], [-1, 1]], [[1, 1]]] where possible[0] contains a list of all the possible rows (lists) for row 0
    for _ in range(column_no):
        master_possible_column.append([])
    master_possible_row_gaps = []
    master_possible_column_gaps = []
    for i, clues in enumerate(master_row_clue):
        master_possible_row_gaps.append(generate_all_possible_gaps(i, "row"))
    for i, clues in enumerate(master_column_clue):
        master_possible_column_gaps.append(generate_all_possible_gaps(i, "column"))
    
    if is_from_file[0]:
        for i in range(row_no):
            for clue_index in range(column_no):
                if master_row[i][clue_index] !=0:
                    update(i, clue_index, master_row[i][clue_index])


    print(is_valid_board())
    all_weight = do_basic_logic()
    row_weight = all_weight[:row_no]
    column_weight = all_weight[row_no:] 
    print_board()

    anti_loop = 0
    prev_index = -1
    rec_weight = lambda i: update_recursion[i] ** 2 // len((master_row_clue + master_column_clue)[i])
    while not next(is_solved_board()):
        to_update = get_index_highest_weight()
        while to_update[1] != -1: #this will be a positive index as long as there is basic logic to do.
            if to_update[0] == "row":
                master_possible_row_gaps[to_update[1]] = compress_possible_gaps(master_possible_row_gaps[to_update[1]])
                only_clues_for_row(to_update[1], to_update[0])
                _ = get_fixed_cells(master_possible_row_gaps[to_update[1]], to_update[0], to_update[1])
                for column in _[0]:
                    update(to_update[1], column, -1)
                for column in _[1]:
                    update(to_update[1], column, 1)
            else:
                master_possible_column_gaps[to_update[1]] = compress_possible_gaps(master_possible_column_gaps[to_update[1]])
                only_clues_for_row(to_update[1], to_update[0])
                _ = get_fixed_cells(master_possible_column_gaps[to_update[1]], "column", (to_update[1]))
                for row in _[0]:
                    update(row, to_update[1], -1)
                for row in _[1]:
                    update(row, to_update[1], 1)

            to_update = get_index_highest_weight()
            print(to_update)
            #print_board()
        
        print_board()
        index = 0
        weight = 0
        for i in range(row_no + column_no):
            if rec_weight(i) > weight:
                weight = rec_weight(i)
                index = i
        #index = update_recursion.index(max(update_recursion))

        if index == prev_index:
            anti_loop += 1
            if anti_loop == 10:
                print("Breaking logic as trying to do recursion logic on the same row 10 times in a row.\nBoard may be looping, in logic (likely caused by ambiguous clues eg: 1:1|1:1, in a 2x2 board)")
                break #while not next(is_solved_board())
        else:
            anti_loop = 0
        prev_index = index

        if index < row_no:
            _ = "row"
        else:
            index = index - row_no
            _ = "column"
        logic_row(index, _)
        #print_board()
        save_board_to_file()

    print("Final board is:")
    print_board()
