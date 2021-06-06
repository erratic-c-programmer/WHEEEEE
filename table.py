class table:
    def __init__(self):
        self.cols = {}
    
    def add_col(self, name):
        """
        Add column to table. Does nothing if column is already
        present.
        """
        if name in self.cols:
            return
        self.cols[name] = []

    def get_cview(self):
        ret = {}
        for k in self.cols:
            ret[k] = self.cols[k][-1]
