import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if len(self.cells) == self.count:
        	return self.cells
        return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        #raise NotImplementedError
        if len(self.cells) == 0:
        	return self.cells
        return None

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        #raise NotImplementedError
        if cell in self.cells:
        	self.cells.remove(cell)
        	self.count = self.count-1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        #raise NotImplementedError
        if cell in self.cells:
        	self.cells.remove(cell)

class MinesweeperAI():
	"""
	Minesweeper game player
	"""

	def __init__(self, height=8, width=8):

	    # Set initial height and width
	    self.height = height
	    self.width = width

	    # Keep track of which cells have been clicked on
	    self.moves_made = set()

	    # Keep track of cells known to be safe or mines
	    self.mines = set()
	    self.safes = set()

	    # List of sentences about the game known to be true
	    self.knowledge = []

	def mark_mine(self, cell):
	    """
	    Marks a cell as a mine, and updates all knowledge
	    to mark that cell as a mine as well.
	    """
	    self.mines.add(cell)
	    mines = []
	    safe = []
	    l =[]
	    for sentence in self.knowledge:
	        sentence.mark_mine(cell)
	        if len(sentence.cells) == sentence.count:
	        	l.append(sentence)
	        	for cell1 in sentence.cells:
	        		mines.append(cell1)
	        elif sentence.count == 0:
	        	l.append(sentence)
	        	for cell1 in sentence.cells:
	        		safe.append(cell1)

	    for sent in l:
	    	self.knowledge.remove(sent)
	    for cells in safe:
	    	self.mark_safe(cells)
	    for cells in mines:
	    	self.mark_mine(cells)

	def mark_safe(self, cell):
	    """
	    Marks a cell as safe, and updates all knowledge
	    to mark that cell as safe as well.
	    """
	    mines=[]
	    safe=[]
	    l = []
	    self.safes.add(cell)
	    for sentence in self.knowledge:
	        sentence.mark_safe(cell)
	        if len(sentence.cells) == sentence.count:
	        	l.append(sentence)
	        	for cell1 in sentence.cells:
	        		mines.append(cell1)
	        elif sentence.count == 0:
	        	l.append(sentence)
	        	for cell1 in sentence.cells:
	        		safe.append(cell1)

	    for sent in l:
	    	self.knowledge.remove(sent)
	    for cells in safe:
	    	self.mark_safe(cells)
	    for cells in mines:
	    	self.mark_mine(cells)


	def add_knowledge(self, cell, count):
		"""
		Called when the Minesweeper board tells us, for a given
		safe cell, how many neighboring cells have mines in them.

		This function should:
		    1) mark the cell as a move that has been made
		    2) mark the cell as safe
		    3) add a new sentence to the AI's knowledge base
		       based on the value of `cell` and `count`
		    4) mark any additional cells as safe or as mines
		       if it can be concluded based on the AI's knowledge base
		    5) add any new sentences to the AI's knowledge base
		       if they can be inferred from existing knowledge
		"""
		#raise NotImplementedError
		self.mark_safe(cell)
		self.moves_made.add(cell)

		neigh = set()
		x,y = cell
		dx = [1,0,-1,0,-1,1,-1,1]
		dy = [0,1,0,-1,1,1,-1,-1]
		#print("here1")

		for l in range(8):
			i,j = x+dx[l],y+dy[l]
			if (0 <= i < self.height) & (0 <= j < self.width):
				if (i,j) in self.mines:
					count -= 1
				elif (i,j) not in self.safes:
					neigh.add((i,j))
				# if ((i,j) not in self.safes) & ((i,j) not in self.mines):

		added = False
		#print("here2")
		if count == 0:
			added = True
			for i in neigh:
				self.mark_safe(i)

		if count == len(neigh):
			added = True
			for i in neigh:
				self.mark_mine(i)
		#print("here3")
		l1=[]
		#print(len(self.knowledge))
		self.knowledge.append(Sentence(neigh,count))
		cnt = 0
		n = len(self.knowledge)
		if not added:

			for i in range(n):
				for j in range(i+1,n):
					s1 = self.knowledge[i]
					s2 = self.knowledge[j]
					if s1.cells.issubset(s2.cells):
						s = Sentence(s2.cells-s1.cells,s2.count-s1.count)
						if s not in self.knowledge:
							self.knowledge.append(s)
						l1.append(s2)
					elif s2.cells.issubset(s1.cells):
						s = Sentence(s1.cells-s2.cells,s1.count-s2.count)
						if s not in self.knowledge:
							self.knowledge.append(s)
						l1.append(s1)

			# for kno in self.knowledge[:length]:
			# 	#print(cnt)
			# 	if neigh.issubset(kno.cells):

			# 		rem_cells = kno.cells-neigh
			# 		rem_cnt = kno.count-count
			# 		self.my_add(rem_cells,rem_cnt)

			# 		if not added:
			# 			self.knowledge += [Sentence(neigh,count)]
			# 			added = True
			# 		l1 += [kno]

			# 	elif kno.cells.issubset(neigh):
			# 		rem_cells = neigh-kno.cells
			# 		rem_cnt = count - kno.count
			# 		if not added:
			# 			self.my_add(rem_cells,rem_cnt)
			# 	cnt += 1

		#print("here4")
		for kno in l1:
			self.knowledge.remove(kno)	

	def my_add(self,rem_cells,rem_cnt):
		if rem_cnt == 0:
			for i in rem_cells:
				self.safes.add(i)
		elif rem_cnt == len(rem_cells):
			for i in rem_cells:
				self.mines.add(i)
		else:
			self.knowledge += [Sentence(rem_cells,rem_cnt)]

	def make_safe_move(self):
	    """
	    Returns a safe cell to choose on the Minesweeper board.
	    The move must be known to be safe, and not already a move
	    that has been made.

	    This function may use the knowledge in self.mines, self.safes
	    and self.moves_made, but should not modify any of those values.
	    """
	    #raise NotImplementedError
	    #print(self.safes)
	    #print(self.mines)
	    #print(self.safes)
	    for cell in self.safes:
	    	if cell not in self.moves_made:
	    		#print(cell)
	    		return cell
	    return None

	def make_random_move(self):
	    """
	    Returns a move to make on the Minesweeper board.
	    Should choose randomly among cells that:
	        1) have not already been chosen, and
	        2) are not known to be mines
	    """
	    #raise NotImplementedError
	    l = []
	    for i in range(self.height):
	    	for j in range(self.width):
	    		if (i,j) not in self.mines:
	    			if (i,j) not in self.moves_made:
	    				l.append((i,j))
	    if len(l) != 0:
	    	return random.choice(l)
	    #random.choice(l)
	    return None
